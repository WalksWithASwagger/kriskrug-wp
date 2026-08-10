# [THEME] #681 purge left dangling form-message selectors glued to the footer rule — Aurora 1.6.1

**Labels:** bug, priority:low, track-b

## Problem

The 1.6.0 dead-CSS purge (#681 / dd6de31) deleted the rule bodies for form error/success colors but left their companion selectors behind. `theme/kk-aurora/style.css:2659-2664` now reads:

```css
.aurora-form-error,
.aurora-form-error,
.aurora-form-success,
.aurora-footer-bottom {
  border-top: 1px solid var(--aurora-line);
  color: var(--aurora-ink-muted);
```

So form error/success messages inherit footer styling (muted ink + top border) instead of the intended `var(--aurora-error-text)` / teal. Note also the duplicated `.aurora-form-error,` line.

The deleted rules previously carried an explicit a11y rationale: "#ffb4b4 was a dark-palette pink: 1.36:1 on cream, so validation errors were invisible on the surface they render against."

## Impact

**Zero live surface today** — verified 2026-08-10: no `<form>` renders on any of the 10 public routes (contact page included), and `.gform_validation_errors` / `.jetpack-field-error` / `.contact-form-submission` appear nowhere in live HTML. This is latent: the moment a contact/newsletter form returns server-rendered feedback, its messages will render muted-gray instead of red/teal.

## Fix

Detach `.aurora-form-error` / `.aurora-form-success` from the footer rule and restore their color rules (error → `var(--aurora-error-text)`, success → `var(--wp--preset--color--teal)`), dedupe the doubled selector line. One-selector-block change, Aurora 1.6.1 candidate, deploy rides the next window.
