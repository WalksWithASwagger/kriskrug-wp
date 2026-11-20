# Gorgeous Ghost refresh (#1340)

In-place editorial and media update to [Gorgeous Ghost](https://kriskrug.co/2026/11/19/gorgeous-ghost/), WordPress post 13003. Preserve the title, publication date, canonical, author, categories and tags. No theme changes. The HTML is a Gutenberg template, not upload-ready until every `media/…` path is mapped to approved media URLs.

The source is Kris's 1920×1080 preserved director master v3 (69.42s). Extract these exact frame times: 0:22 (1600×900 featured), 0:06, 0:24.5 and 0:58.6 (1200px wide inline). Use FFmpeg frame extraction, for example `ffmpeg -ss 22 -i "$MASTER" -frames:v 1 -vf scale=1600:-2 -q:v 3 gorgeous-ghost-chorus-hero.jpg`. Inline alt text, captions and filenames are in the template. No photos from the linked Film Club recap are reused.

Cut excerpts 19.53–26.80 and 57.55–63.00 from the same master (H.264/AAC, 960×540, MP4 fast-start). Example: `ffmpeg -ss 19.53 -i "$MASTER" -t 7.27 -vf scale=960:-2 -c:v libx264 -crf 22 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart gorgeous-ghost-colour-bloom.mp4`. Use the included excerpt-relative English VTT files. Both stop before the baked credits. No auto-play. Keep the inline flash warning and timestamped watch links. Do not change global mime permissions to upload captions.

Before writing to WordPress, confirm post ID and slug across statuses, snapshot the current body and fields, and check any intervening edits. Verify the new crop, audio, CC, all links, full embed or watch fallback, and metadata on the public permalink after the update. Leave #1340 open until production readback passes.
