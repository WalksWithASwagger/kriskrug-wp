# Common Failure Patterns & Solutions

Documented patterns to help agents learn from common mistakes and avoid repeating them.

---

## WordPress Coding Standards Failures

### Pattern: WordPress.DB.PreparedSQL.NotPrepared

**Error Message:**
```
Use of unprepared SQL statement detected
```

**Cause:**
Direct SQL queries without using `$wpdb->prepare()`

**Bad Example:**
```php
$results = $wpdb->get_results( "SELECT * FROM {$wpdb->prefix}bc_ai_events WHERE id = {$id}" );
```

**Good Example:**
```php
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}bc_ai_events WHERE id = %d",
        $id
    )
);
```

**Prevention:**
- ALWAYS use `$wpdb->prepare()` for queries with variables
- Use placeholders: `%d` (integer), `%s` (string), `%f` (float)
- See: `implementer.agent.md` security section

---

### Pattern: WordPress.Security.EscapeOutput.OutputNotEscaped

**Error Message:**
```
All output should be run through an escaping function
```

**Cause:**
Outputting data without escaping for HTML context

**Bad Example:**
```php
echo $user_input;
echo '<a href="' . $url . '">Link</a>';
```

**Good Example:**
```php
echo esc_html( $user_input );
echo '<a href="' . esc_url( $url ) . '">Link</a>';
```

**Escaping Functions:**
- `esc_html()` - For HTML content
- `esc_attr()` - For HTML attributes
- `esc_url()` - For URLs
- `esc_js()` - For JavaScript
- `wp_kses_post()` - For post content (allows some HTML)

**Prevention:**
- ALWAYS escape output
- Choose appropriate escaping function for context
- See: `implementer.agent.md` security checklist

---

### Pattern: WordPress.Security.ValidatedSanitizedInput.InputNotSanitized

**Error Message:**
```
Input variable not sanitized before use
```

**Cause:**
Using $_GET, $_POST, $_REQUEST without sanitization

**Bad Example:**
```php
$email = $_POST['email'];
$name = $_GET['name'];
```

**Good Example:**
```php
$email = sanitize_email( $_POST['email'] );
$name = sanitize_text_field( $_GET['name'] );
```

**Sanitization Functions:**
- `sanitize_text_field()` - General text
- `sanitize_email()` - Email addresses
- `sanitize_url()` - URLs
- `sanitize_key()` - Keys/slugs
- `sanitize_textarea_field()` - Textarea content
- `absint()` - Absolute integer

**Prevention:**
- NEVER trust user input
- Sanitize immediately after receiving
- Use appropriate sanitization for data type

---

## PHPUnit Test Failures

### Pattern: Headers Already Sent

**Error Message:**
```
Cannot modify header information - headers already sent
```

**Cause:**
Output (echo, print, whitespace) before PHPUnit starts

**Common Culprits:**
- Whitespace before `<?php` tag
- `echo` statements left in code
- Syntax errors causing output

**Solution:**
```php
// Check files for leading/trailing whitespace
// Ensure no output before tests run
// Use output buffering if needed

// In test bootstrap
ob_start();
```

**Prevention:**
- Remove all debugging `echo` statements
- Check for whitespace before `<?php`
- Use error_log() instead of echo for debugging

---

### Pattern: Call to Undefined Function

**Error Message:**
```
Call to undefined function wp_remote_get()
```

**Cause:**
WordPress functions not loaded in test environment

**Solution:**
```php
// In tests/bootstrap.php
require_once '/path/to/wordpress/wp-load.php';

// Or mock the function
if ( ! function_exists( 'wp_remote_get' ) ) {
    function wp_remote_get( $url ) {
        // Mock implementation
    }
}
```

**Prevention:**
- Ensure WordPress test suite is properly configured
- Check WP_TESTS_DIR environment variable
- See: `test-writer.agent.md` for WordPress test setup

---

### Pattern: Test Dependencies

**Error Message:**
```
Test depends on another test's state
```

**Cause:**
Tests not properly isolated, relying on order of execution

**Bad Example:**
```php
// Test 1 creates data
public function test_create_event() {
    $this->event_id = create_event();
}

// Test 2 assumes data exists
public function test_get_event() {
    $event = get_event( $this->event_id ); // May be null!
}
```

**Good Example:**
```php
public function test_get_event() {
    // Create data within this test
    $event_id = $this->factory()->post->create( ['post_type' => 'event'] );
    $event = get_event( $event_id );
    $this->assertNotEmpty( $event );
}
```

**Prevention:**
- Each test should be completely independent
- Use setUp() and tearDown() properly
- Use WordPress factory methods
- See: `test-writer.agent.md` for patterns

---

## Git & GitHub Failures

### Pattern: Push Rejected (Protected Branch)

**Error Message:**
```
protected branch hook declined
```

**Cause:**
Trying to push directly to protected branch (main/develop)

**Solution:**
- Always create feature branch
- Never commit directly to main
- Create PR instead

**Prevention:**
```bash
# Create feature branch first
git checkout -b feature/issue-123-description

# Make changes, commit
git add .
git commit -m "Description"

# Push feature branch
git push -u origin feature/issue-123-description

# Create PR
gh pr create
```

---

### Pattern: Merge Conflict

**Error Message:**
```
CONFLICT (content): Merge conflict in file.php
```

**Cause:**
Base branch has changed since branch was created

**Solution:**
```bash
# Update local main
git checkout main
git pull origin main

# Return to feature branch
git checkout feature/issue-123

# Rebase on latest main
git rebase main

# Resolve conflicts
# Edit files, then:
git add resolved-file.php
git rebase --continue

# Force push (branch was rebased)
git push --force-with-lease
```

**Prevention:**
- Rebase frequently on long-running branches
- Keep PRs small and merge quickly
- Pull latest main before starting work

---

## Agent Orchestration Failures

### Pattern: Stage Timeout

**Symptom:**
Agent task runs longer than configured timeout

**Common Causes:**
- Analysis stuck searching large codebase
- Implementation more complex than expected
- Tests running very slowly

**Solution:**
1. Check agent-state for current stage
2. Review agent task logs
3. Increase timeout if legitimate
4. Or kill and restart with better context

**Prevention:**
- Set realistic timeouts per stage
- Monitor long-running tasks
- See: `.github/agent-config/error-handling.yml`

---

### Pattern: State File Corruption

**Symptom:**
Invalid JSON in state.json file

**Cause:**
- Concurrent writes from multiple processes
- Manual editing errors
- Git merge conflicts

**Solution:**
```bash
# Check JSON validity
jq '.' .github/agent-state/123/state.json

# If invalid, restore from git
git checkout HEAD .github/agent-state/123/state.json

# Or manually fix JSON syntax
```

**Prevention:**
- Never manually edit state files unless debugging
- Use jq for all state updates
- Commit state changes immediately

---

### Pattern: Missing Agent Output

**Symptom:**
Expected output file doesn't exist after agent completes

**Causes:**
- Agent failed silently
- Output written to wrong location
- Permissions issue

**Solution:**
```bash
# Check agent task logs
gh agent-task view {task-id}

# Check for file in alternate locations
find .github/agent-state -name "analysis.json"

# Manually run agent if needed
```

**Prevention:**
- Validate output file exists after each stage
- Check agent task exit code
- Log all agent outputs

---

## WordPress-Specific Failures

### Pattern: Plugin Conflict

**Symptom:**
Code works in isolation but fails with other plugins active

**Common Causes:**
- JavaScript namespace collisions
- Filter/action priority conflicts
- Global variable pollution

**Solution:**
```php
// Namespace JavaScript
(function($) {
    'use strict';
    // Your code here
})(jQuery);

// Check if function exists
if ( ! function_exists( 'bc_ai_function' ) ) {
    function bc_ai_function() {
        // Implementation
    }
}

// Use specific hook priority
add_action( 'init', 'bc_ai_init', 5 );  // Run early
```

**Prevention:**
- Always prefix functions and variables
- Test with common plugins active
- Use specific hook priorities

---

### Pattern: Transient Cache Not Working

**Symptom:**
Transients disappear immediately or don't persist

**Causes:**
- Object cache plugin active (overrides transients)
- WordPress multisite configuration
- Cache being aggressively cleared

**Solutions:**
```php
// Check if using object cache
if ( wp_using_ext_object_cache() ) {
    // Use wp_cache instead
    wp_cache_set( 'key', $data, 'bc_ai', $duration );
} else {
    // Use transients
    set_transient( 'key', $data, $duration );
}

// Or use options for persistent storage
update_option( 'bc_ai_data', $data, false );  // false = don't autoload
```

**Prevention:**
- Document caching strategy
- Test in production-like environment
- Have fallback for cache failures

---

## Performance Failures

### Pattern: N+1 Query Problem

**Symptom:**
Page loads slowly due to repeated database queries

**Cause:**
Loop making individual queries instead of batch

**Bad Example:**
```php
foreach ( $events as $event ) {
    $author = get_user_by( 'id', $event->author_id );  // N queries!
}
```

**Good Example:**
```php
// Get all author IDs first
$author_ids = wp_list_pluck( $events, 'author_id' );

// Single query for all authors
$authors = get_users( ['include' => $author_ids] );
```

**Prevention:**
- Use WP_Query with proper arguments
- Cache query results
- Use WordPress object cache

---

### Pattern: Large Image Files

**Symptom:**
Slow page loads, large page weight

**Cause:**
Unoptimized or incorrectly sized images

**Solution:**
- Use WordPress image sizes
- Implement responsive images (srcset)
- Lazy-load images below fold
- Compress images (TinyPNG, ImageOptim)
- Use WebP with fallbacks

**Prevention:**
- Always optimize images before upload
- Use appropriate image size for context
- Implement lazy loading
- See: Issue #4 (Performance optimization)

---

## Security Failures

### Pattern: SQL Injection

**Symptom:**
User input executed as SQL

**Bad Example:**
```php
$id = $_GET['id'];
$query = "SELECT * FROM table WHERE id = $id";
```

**Good Example:**
```php
$id = absint( $_GET['id'] );
$query = $wpdb->prepare( "SELECT * FROM table WHERE id = %d", $id );
```

**Prevention:**
- NEVER put variables directly in SQL
- ALWAYS use $wpdb->prepare()
- Sanitize even when using prepare

---

### Pattern: XSS (Cross-Site Scripting)

**Symptom:**
JavaScript executed from user input

**Bad Example:**
```php
echo '<div>' . $_POST['comment'] . '</div>';
```

**Good Example:**
```php
echo '<div>' . esc_html( $_POST['comment'] ) . '</div>';
// Or for allowed HTML
echo '<div>' . wp_kses_post( $_POST['comment'] ) . '</div>';
```

**Prevention:**
- Escape ALL output
- Sanitize ALL input
- Use appropriate escaping for context

---

### Pattern: CSRF (Missing Nonce)

**Symptom:**
Unauthorized actions executed

**Bad Example:**
```php
if ( $_POST['action'] == 'delete' ) {
    delete_post( $_POST['id'] );  // No verification!
}
```

**Good Example:**
```php
if ( $_POST['action'] == 'delete' ) {
    // Verify nonce
    if ( ! wp_verify_nonce( $_POST['nonce'], 'bc_ai_delete' ) ) {
        wp_die( 'Security check failed' );
    }

    // Check capabilities
    if ( ! current_user_can( 'delete_posts' ) ) {
        wp_die( 'Unauthorized' );
    }

    delete_post( absint( $_POST['id'] ) );
}
```

**Prevention:**
- ALL forms need nonces
- ALL AJAX requests need nonces
- ALWAYS verify nonces
- ALWAYS check capabilities

---

## Quick Reference

### Before Committing

```bash
# Run these checks
make validate      # PHPCS check
make test         # Run tests
git diff          # Review changes
```

### Before Creating PR

```bash
make health       # System check
make validate     # Coding standards
make test         # All tests
```

### When Agent Fails

```bash
# Check state
cat .github/agent-state/{issue}/state.json

# Check logs
gh run list --limit 5
gh run view {run-id}

# Check retry count
jq '.retry_counts' .github/agent-state/{issue}/state.json
```

---

## Learning from Failures

### Document Patterns

When you encounter a new failure pattern:

1. Document it here
2. Add to relevant agent instructions
3. Update error-handling.yml if needed
4. Share in .github/agent-learnings.md

### Continuous Improvement

**This file should grow as we learn.**

Each failure is an opportunity to make the system more robust and prevent future occurrences.

---

**Remember:** Failures are not bad—they're learning opportunities. Document them, learn from them, prevent them next time.
