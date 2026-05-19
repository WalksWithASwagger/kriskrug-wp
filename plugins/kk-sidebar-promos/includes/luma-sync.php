<?php
/**
 * Luma calendar sync.
 *
 * Pulls the next upcoming event from a configured Luma iCal feed and
 * upserts a Featured promo for it. The promo's end date is set to the
 * event date, so it auto-expires when the cron runs the next morning.
 *
 * Configure the iCal URL in Settings → Sidebar Promos. Find your calendar's
 * iCal URL on lu.ma → calendar settings → "Subscribe via iCal".
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KK_SP_OPT_LUMA_URL    = 'kk_sp_luma_ical_url';
const KK_SP_OPT_LUMA_LABEL  = 'kk_sp_luma_label';
const KK_SP_OPT_LUMA_LINK   = 'kk_sp_luma_link';

function kk_sp_run_luma_sync() {
	$ical_url = trim( (string) get_option( KK_SP_OPT_LUMA_URL, '' ) );
	if ( $ical_url === '' ) {
		return new WP_Error( 'kk_sp_no_url', 'No Luma iCal URL configured.' );
	}

	$response = wp_remote_get( $ical_url, [ 'timeout' => 15 ] );
	if ( is_wp_error( $response ) ) {
		return $response;
	}
	$code = (int) wp_remote_retrieve_response_code( $response );
	if ( $code < 200 || $code >= 300 ) {
		return new WP_Error( 'kk_sp_http', sprintf( 'Luma fetch returned HTTP %d.', $code ) );
	}

	$body   = (string) wp_remote_retrieve_body( $response );
	$events = kk_sp_parse_ical( $body );
	if ( empty( $events ) ) {
		return new WP_Error( 'kk_sp_no_events', 'No events parsed from Luma feed.' );
	}

	$now  = current_time( 'timestamp' );
	$next = null;
	foreach ( $events as $ev ) {
		if ( $ev['start_ts'] >= $now && ( $next === null || $ev['start_ts'] < $next['start_ts'] ) ) {
			$next = $ev;
		}
	}
	if ( ! $next ) {
		return new WP_Error( 'kk_sp_no_upcoming', 'No upcoming events.' );
	}

	$label    = get_option( KK_SP_OPT_LUMA_LABEL, __( 'Vancouver AI Community', 'kk-sidebar-promos' ) );
	$fallback = get_option( KK_SP_OPT_LUMA_LINK, 'https://lu.ma/vancouver-ai' );

	$title = sprintf(
		'%s — %s',
		$label,
		wp_date( get_option( 'date_format' ), $next['start_ts'] )
	);
	$end_date = wp_date( 'Y-m-d', $next['start_ts'] );
	$link     = $next['url'] ?: $fallback;

	$existing = get_posts( [
		'post_type'      => KK_SP_POST_TYPE,
		'post_status'    => [ 'publish', 'draft' ],
		'posts_per_page' => 1,
		'meta_query'     => [
			[
				'key'   => KK_SP_META_SOURCE,
				'value' => 'luma',
			],
			[
				'key'   => KK_SP_META_SOURCE_ID,
				'value' => $next['uid'],
			],
		],
		'no_found_rows'  => true,
	] );

	$post_data = [
		'post_type'    => KK_SP_POST_TYPE,
		'post_status'  => 'publish',
		'post_title'   => $title,
		'post_excerpt' => $next['summary_short'],
	];

	if ( $existing ) {
		$post_data['ID'] = $existing[0]->ID;
		$post_id         = wp_update_post( $post_data, true );
	} else {
		$post_id = wp_insert_post( $post_data, true );
	}

	if ( is_wp_error( $post_id ) ) {
		return $post_id;
	}

	update_post_meta( $post_id, KK_SP_META_TYPE, 'featured' );
	update_post_meta( $post_id, KK_SP_META_TONE, 'event' );
	update_post_meta( $post_id, KK_SP_META_LINK, esc_url_raw( $link ) );
	update_post_meta( $post_id, KK_SP_META_CTA, __( 'RSVP', 'kk-sidebar-promos' ) );
	update_post_meta( $post_id, KK_SP_META_END, $end_date );
	update_post_meta( $post_id, KK_SP_META_SOURCE, 'luma' );
	update_post_meta( $post_id, KK_SP_META_SOURCE_ID, $next['uid'] );

	return $post_id;
}

/**
 * Lightweight iCal parser. Handles the common subset Luma emits:
 * VEVENT blocks with UID, DTSTART (date or datetime), SUMMARY, URL,
 * DESCRIPTION. Folded lines (RFC 5545) are unfolded first.
 */
function kk_sp_parse_ical( $raw ) {
	if ( $raw === '' ) {
		return [];
	}

	// Unfold continuation lines: a line beginning with space or tab
	// is a continuation of the previous line.
	$normalized = preg_replace( "/\r\n[ \t]/", '', $raw );
	$lines      = preg_split( "/\r\n|\n|\r/", $normalized );

	$events  = [];
	$current = null;

	foreach ( $lines as $line ) {
		if ( $line === 'BEGIN:VEVENT' ) {
			$current = [
				'uid'           => '',
				'start_ts'      => 0,
				'summary'       => '',
				'summary_short' => '',
				'url'           => '',
			];
			continue;
		}
		if ( $line === 'END:VEVENT' ) {
			if ( $current && $current['start_ts'] ) {
				if ( $current['uid'] === '' ) {
					$current['uid'] = md5( $current['summary'] . $current['start_ts'] );
				}
				$events[] = $current;
			}
			$current = null;
			continue;
		}
		if ( $current === null ) {
			continue;
		}

		// Split "KEY[;PARAMS]:VALUE" on the first colon.
		$colon = strpos( $line, ':' );
		if ( $colon === false ) {
			continue;
		}
		$head  = substr( $line, 0, $colon );
		$value = substr( $line, $colon + 1 );
		$key   = strtoupper( strtok( $head, ';' ) );

		switch ( $key ) {
			case 'UID':
				$current['uid'] = trim( $value );
				break;
			case 'SUMMARY':
				$current['summary']       = kk_sp_ical_unescape( $value );
				$current['summary_short'] = wp_trim_words( $current['summary'], 18, '…' );
				break;
			case 'URL':
				$current['url'] = trim( $value );
				break;
			case 'DTSTART':
				$current['start_ts'] = kk_sp_parse_ical_date( $value, $head );
				break;
		}
	}

	return $events;
}

function kk_sp_ical_unescape( $value ) {
	return str_replace(
		[ '\\,', '\\;', '\\n', '\\N', '\\\\' ],
		[ ',', ';', "\n", "\n", '\\' ],
		$value
	);
}

function kk_sp_parse_ical_date( $value, $head ) {
	$value = trim( $value );
	if ( preg_match( '/^(\d{8})T(\d{6})Z$/', $value, $m ) ) {
		// UTC datetime.
		return strtotime( $m[1] . 'T' . $m[2] . 'Z' );
	}
	if ( preg_match( '/TZID=([^;:]+)/', $head, $tz ) && preg_match( '/^(\d{8})T(\d{6})$/', $value ) ) {
		// Floating datetime in a named TZ.
		try {
			$dt = new DateTime(
				substr( $value, 0, 4 ) . '-' . substr( $value, 4, 2 ) . '-' . substr( $value, 6, 2 ) . 'T' .
				substr( $value, 9, 2 ) . ':' . substr( $value, 11, 2 ) . ':' . substr( $value, 13, 2 ),
				new DateTimeZone( $tz[1] )
			);
			return $dt->getTimestamp();
		} catch ( Exception $e ) {
			return strtotime( $value );
		}
	}
	if ( preg_match( '/^\d{8}$/', $value ) ) {
		// All-day date.
		return strtotime( substr( $value, 0, 4 ) . '-' . substr( $value, 4, 2 ) . '-' . substr( $value, 6, 2 ) );
	}
	return strtotime( $value ) ?: 0;
}
