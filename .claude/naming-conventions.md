# BC+AI Naming Conventions

Consistent naming across all code (human-written and agent-generated).

## PHP Naming (WordPress Standards)

### Function Names
```php
// Format: bc_ai_{context}_{action}
bc_ai_cache_get()
bc_ai_api_fetch_data()
bc_ai_admin_render_settings()
bc_ai_event_register_attendee()
```

### Class Names
```php
// Format: BC_AI_{Name}
class BC_AI_API_Client {}
class BC_AI_Cache_Manager {}
class BC_AI_Admin_Settings {}
class BC_AI_Event_Handler {}
```

### Constants
```php
// Format: BC_AI_{NAME}
define( 'BC_AI_VERSION', '1.0.0' );
define( 'BC_AI_PLUGIN_DIR', __DIR__ );
define( 'BC_AI_CACHE_DURATION', HOUR_IN_SECONDS );
```

### Variables
```php
// Format: $descriptive_name (snake_case)
$api_response = ...;
$cache_key = ...;
$user_data = ...;
```

### WordPress Hooks
```php
// Actions: bc_ai_{context}_{action}
do_action( 'bc_ai_cache_cleared' );
do_action( 'bc_ai_api_request_complete', $response );
do_action( 'bc_ai_settings_updated', $settings );

// Filters: bc_ai_{context}_{filter}
apply_filters( 'bc_ai_cache_duration', HOUR_IN_SECONDS );
apply_filters( 'bc_ai_api_url', $url );
apply_filters( 'bc_ai_admin_capabilities', 'manage_options' );
```

### Database

```php
// Table names: {$wpdb->prefix}bc_ai_{table}
global $wpdb;
$table_name = $wpdb->prefix . 'bc_ai_events';
$table_name = $wpdb->prefix . 'bc_ai_members';

// Options: bc_ai_{option_name}
get_option( 'bc_ai_api_key' );
update_option( 'bc_ai_cache_enabled', true );

// Transients: bc_ai_{key}
set_transient( 'bc_ai_api_response_' . md5( $url ), $data );
get_transient( 'bc_ai_events_list' );

// User meta: bc_ai_{meta_key}
get_user_meta( $user_id, 'bc_ai_preferences', true );
update_user_meta( $user_id, 'bc_ai_event_rsvp', $event_id );
```

---

## File Naming

### PHP Files

```
// Classes
class-api-client.php
class-cache-manager.php
class-admin-settings.php

// Functions (if not in class)
functions-helpers.php
functions-api.php

// Templates
template-event-list.php
template-member-profile.php

// Tests
test-api-client.php
test-cache-manager.php
```

### JavaScript Files

```
// Main files
navigation.js
form-handler.js
event-calendar.js

// Modules (if using)
api-client.js
cache-helper.js

// Min files (built)
navigation.min.js
```

### CSS Files

```
// Main stylesheet
style.css

// Component styles
navigation.css
events.css
forms.css

// Min files (built)
style.min.css
```

---

## Directory Structure

### WordPress Plugins

```
wp-content/plugins/bc-ai-core/
├── bc-ai-core.php          # Main plugin file
├── README.md               # Plugin documentation
├── includes/               # Core functionality
│   ├── class-api-client.php
│   ├── class-cache-manager.php
│   └── functions-helpers.php
├── admin/                  # Admin interface
│   ├── class-admin-settings.php
│   └── views/
│       └── settings-page.php
├── public/                 # Public-facing
│   ├── class-public.php
│   └── views/
│       └── event-list.php
├── integrations/           # Third-party integrations
│   ├── class-notion-sync.php
│   └── class-luma-events.php
├── assets/                 # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
└── tests/                  # PHPUnit tests
    ├── bootstrap.php
    ├── test-api-client.php
    └── test-cache-manager.php
```

### WordPress Themes

```
wp-content/themes/bc-ai-theme/
├── style.css               # Required WordPress theme file
├── functions.php           # Theme functions
├── README.md               # Theme documentation
├── header.php
├── footer.php
├── index.php
├── single.php
├── page.php
├── template-parts/         # Reusable components
│   ├── content-event.php
│   └── navigation-main.php
├── inc/                    # Theme includes
│   ├── customizer.php
│   └── template-functions.php
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── docs/                   # Design system docs
│   ├── colors.md
│   ├── typography.md
│   └── components.md
└── tests/
    └── test-theme-functions.php
```

---

## Consistency Rules

### Casing

- **PHP functions/variables:** snake_case
- **PHP classes:** PascalCase with BC_AI_ prefix
- **PHP constants:** SCREAMING_SNAKE_CASE
- **JavaScript:** camelCase (variables/functions), PascalCase (classes)
- **CSS:** kebab-case
- **Files:** kebab-case (except when WordPress convention differs)

### Prefixes

**Always use `bc_ai_` or `BC_AI_`** to avoid conflicts:

```php
// Good
function bc_ai_get_events() {}
class BC_AI_Event_Manager {}
define( 'BC_AI_VERSION', '1.0.0' );

// Bad (no prefix)
function get_events() {}  // Could conflict with another plugin
class Event_Manager {}    // Common name, likely conflict
```

### Acronyms

**In code:**
- API (all caps when standalone)
- URL (all caps when standalone)
- SEO, UX, UI (all caps)

**In prose/comments:**
- API, URL, SEO, UX, UI (all caps)
- HTML, CSS, JavaScript, PHP (proper casing)
- WordPress (one word, capital W and P)
- PHPUnit (capital PHP, capital U)

---

## Version Control

### Branch Names

```
// Features
feature/issue-123-add-event-calendar
feature/notion-integration

// Bugs
fix/issue-456-contact-form-mobile
fix/navigation-keyboard-access

// Enhancements
enhancement/issue-789-performance-optimization
enhancement/accessibility-improvements

// Documentation
docs/issue-101-update-api-guide
docs/add-development-guide

// Agent-generated (automated)
feature/issue-123-auto-fix
```

### Commit Messages

```
// Format: [Type]: Brief description (50 chars max)

// Types
[Fix]: Resolve contact form mobile submission issue
[Add]: Implement event calendar with filtering
[Update]: Improve navigation accessibility
[Refactor]: Simplify API client error handling
[Docs]: Add WordPress setup guide
[Test]: Add coverage for cache manager
[Chore]: Update dependencies to latest versions

// Multi-line format
[Fix]: Resolve contact form mobile submission

Why: Mobile Safari wasn't triggering form submit event
What: Added touchstart event listener with fallback
Impact: Mobile users can now submit contact form
WordPress: Tested on WP 6.4+, PHP 8.2
```

---

## Documentation

### README Files

**Every major directory should have a README:**

```markdown
# {Component Name}

Brief description of what this component does.

## Purpose

Why this exists and what problem it solves for BC+AI community.

## Files

- `file1.php` - Description
- `file2.php` - Description

## Usage

How to use this component.

## Dependencies

What this depends on.

## Tests

How to test this component.
```

### Inline Comments

```php
// Good comment: Explains WHY, provides context
// Cache API responses to reduce load on external services
// and improve performance for users on slower connections
$cached = get_transient( $cache_key );

// Bad comment: Just repeats the code
// Get transient
$cached = get_transient( $cache_key );

// Great comment: AI-friendly with future context
/**
 * AI Note: This caching pattern is used throughout BC+AI
 * because many community members access the site from areas
 * with slower internet. Always consider cache invalidation
 * when modifying API endpoints.
 */
```

---

## Testing Conventions

### Test File Names

```
// Mirror the file being tested
class-api-client.php → test-api-client.php
class-cache-manager.php → test-cache-manager.php
functions-helpers.php → test-functions-helpers.php
```

### Test Class Names

```php
// Format: Test_{Class_Name}
class Test_BC_AI_API_Client extends WP_UnitTestCase {}
class Test_BC_AI_Cache_Manager extends WP_UnitTestCase {}

// For function files
class Test_BC_AI_Helper_Functions extends WP_UnitTestCase {}
```

### Test Method Names

```php
// Format: test_{what_is_being_tested}
public function test_api_response_is_cached() {}
public function test_cache_expires_after_duration() {}
public function test_invalid_input_returns_error() {}
public function test_nonce_verification_fails_on_invalid() {}
```

---

## Asset Naming

### Images

```
// Format: descriptive-name.ext
bc-ai-logo.png
event-placeholder.jpg
member-avatar-default.svg
icon-calendar.svg

// Optimized versions
bc-ai-logo@2x.png
event-placeholder-mobile.jpg
```

### CSS Classes

```css
/* BEM-style for components */
.bc-ai-event {}
.bc-ai-event__title {}
.bc-ai-event__date {}
.bc-ai-event--featured {}

/* Utility classes */
.bc-ai-container {}
.bc-ai-button {}
.bc-ai-card {}
```

### JavaScript

```javascript
// Variables: camelCase
const apiClient = ...;
const cacheManager = ...;

// Constants: SCREAMING_SNAKE_CASE
const API_BASE_URL = ...;
const CACHE_DURATION = ...;

// Classes: PascalCase
class EventCalendar {}
class ApiClient {}

// Functions: camelCase
function fetchEvents() {}
function clearCache() {}
```

---

## When in Doubt

### WordPress Way First

If WordPress has a pattern, use it:
- Settings API for options
- Transients for caching
- wp_remote_get for HTTP
- wp_enqueue for assets
- Shortcodes for embed content

### Check WordPress Core

How does WordPress core do it? Follow that pattern.

### Community Standards

WordPress has a huge community. If something is a common pattern, there's probably a reason.

---

## Exceptions

### When to Break Rules

Sometimes you need to deviate. That's okay IF:

1. **Documented** - Explain why in comments
2. **Justified** - Clear technical or business reason
3. **Isolated** - Doesn't spread throughout codebase
4. **Reviewed** - Gets extra scrutiny in code review

**Example:**
```php
// Note: Using custom caching here instead of transients because
// transients are cleared on object cache flush, but we need this
// data to persist through cache clears for analytics accuracy.
// See ADR-005 in docs/decisions.md for full context.
```

---

**Consistency serves the community. Follow these conventions and BC+AI's codebase will be a joy to work with—for humans and AI alike.**
