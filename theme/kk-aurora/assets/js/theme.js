/**
 * KK Aurora - Theme JavaScript
 * 
 * General theme functionality and utilities.
 */

(function() {
  'use strict';

  // ============================================
  // PRIMARY NAV KEYBOARD
  // ============================================

  function initPrimaryNavKeyboard() {
    const nav = document.querySelector('.aurora-primary-nav');
    if (!nav) return;

    const links = Array.from(nav.querySelectorAll('a[href]'));
    if (links.length < 2) return;

    links.forEach((link, index) => {
      link.addEventListener('keydown', (event) => {
        let targetIndex = index;

        if (event.key === 'ArrowRight') {
          targetIndex = index + 1 >= links.length ? 0 : index + 1;
        } else if (event.key === 'ArrowLeft') {
          targetIndex = index - 1 < 0 ? links.length - 1 : index - 1;
        } else if (event.key === 'Home') {
          targetIndex = 0;
        } else if (event.key === 'End') {
          targetIndex = links.length - 1;
        } else {
          return;
        }

        event.preventDefault();
        const target = links[targetIndex];
        target.focus();
        target.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      });
    });
  }

  // ============================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================

  function initSmoothScroll() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        const target = href && href.length > 1 ? document.querySelector(href) : null;
        
        if (target) {
          e.preventDefault();
          
          const headerOffset = 100;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: prefersReducedMotion ? 'auto' : 'smooth'
          });
          
          // Update focus for accessibility
          target.focus({ preventScroll: true });
          if (document.activeElement !== target) {
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
          }
        }
      });
    });
  }

  // ============================================
  // EXTERNAL LINK HANDLING
  // ============================================

  function initExternalLinks() {
    document.querySelectorAll('a[href^="http"]').forEach(link => {
      // Check if external
      if (link.hostname !== window.location.hostname) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        
        // Add screen reader text
        if (!link.querySelector('.sr-only')) {
          const srText = document.createElement('span');
          srText.className = 'sr-only';
          srText.textContent = ' (opens in new tab)';
          link.appendChild(srText);
        }
      }
    });
  }

  // ============================================
  // COPY CODE BLOCKS
  // ============================================

  function initCodeCopy() {
    document.querySelectorAll('pre').forEach(pre => {
      // Create copy button
      const button = document.createElement('button');
      button.className = 'aurora-copy-code';
      button.setAttribute('type', 'button');
      button.setAttribute('aria-label', 'Copy code');
      button.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      `;
      
      button.addEventListener('click', async () => {
        const code = pre.querySelector('code')?.textContent || pre.textContent;
        
        try {
          await navigator.clipboard.writeText(code);
          button.classList.add('copied');
          button.setAttribute('aria-label', 'Copied!');
          
          setTimeout(() => {
            button.classList.remove('copied');
            button.setAttribute('aria-label', 'Copy code');
          }, 2000);
        } catch (err) {
          console.error('Failed to copy:', err);
        }
      });
      
      pre.style.position = 'relative';
      pre.appendChild(button);
    });
  }

  // ============================================
  // READING PROGRESS
  // ============================================

  function initReadingProgress() {
    const progressBar = document.querySelector('.aurora-reading-progress');
    const progressFill = progressBar?.querySelector('span') || progressBar;
    const article = document.querySelector('.aurora-article');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!progressBar || !progressFill || !article || prefersReducedMotion) return;
    
    function updateProgress() {
      const articleRect = article.getBoundingClientRect();
      const articleTop = articleRect.top + window.pageYOffset;
      const articleHeight = Math.max(articleRect.height - window.innerHeight, 1);
      const windowHeight = window.innerHeight;
      const scrollTop = window.pageYOffset;
      
      const progress = Math.min(
        Math.max((scrollTop - articleTop + windowHeight * 0.35) / articleHeight, 0),
        1
      );
      
      progressFill.style.transform = `scaleX(${progress})`;
    }
    
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // ============================================
  // OPAL READING PANE SHEEN
  // ============================================

  function initOpalReadingPane() {
    const pane = document.querySelector('.aurora-reader-pane');
    if (!pane) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const hasFinePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    if (prefersReducedMotion || !hasFinePointer) return;

    let frame = null;
    let pendingEvent = null;

    function updateSheen(event) {
      const rect = pane.getBoundingClientRect();
      const x = (event.clientX - rect.left - rect.width / 2) * 0.035;
      const y = (event.clientY - rect.top - rect.height / 2) * 0.025;

      pane.style.setProperty('--aurora-sheen-x', `${x.toFixed(1)}px`);
      pane.style.setProperty('--aurora-sheen-y', `${y.toFixed(1)}px`);
      pane.style.setProperty('--aurora-sheen-opacity', '0.24');
    }

    pane.addEventListener('pointermove', (event) => {
      pendingEvent = event;
      if (frame) return;

      frame = window.requestAnimationFrame(() => {
        frame = null;
        if (pendingEvent) {
          updateSheen(pendingEvent);
          pendingEvent = null;
        }
      });
    });

    pane.addEventListener('pointerleave', () => {
      pendingEvent = null;
      pane.style.setProperty('--aurora-sheen-x', '0px');
      pane.style.setProperty('--aurora-sheen-y', '0px');
      pane.style.setProperty('--aurora-sheen-opacity', '0.13');
    });
  }

  // ============================================
  // ARTICLE READING HELPERS
  // ============================================

  function initArticleReadingHelpers() {
    const article = document.querySelector('.aurora-article');
    const content = article?.querySelector('.aurora-prose');

    if (!article || !content) return;

    const readTime = article.querySelector('[data-aurora-read-time]');
    const words = content.textContent.trim().split(/\s+/).filter(Boolean).length;

    if (readTime && words > 120) {
      const minutes = Math.max(1, Math.ceil(words / 225));
      readTime.textContent = `${minutes} min read`;
      readTime.hidden = false;
      article.querySelector('.aurora-read-time-divider')?.removeAttribute('hidden');
    }

    const map = article.querySelector('[data-aurora-article-map]');
    const nav = map?.querySelector('nav');
    const headings = Array.from(content.querySelectorAll('h2, h3'))
      .filter((heading) => heading.textContent.trim().length > 0)
      .slice(0, 12);

    if (!map || !nav || headings.length < 3) return;

    const list = document.createElement('ol');

    headings.forEach((heading, index) => {
      if (!heading.id) {
        heading.id = `article-section-${index + 1}`;
      }

      const item = document.createElement('li');
      const link = document.createElement('a');

      link.href = `#${heading.id}`;
      link.textContent = heading.textContent.trim();
      link.className = heading.tagName === 'H3' ? 'is-subsection' : '';
      item.appendChild(link);
      list.appendChild(item);
    });

    nav.appendChild(list);
    map.hidden = false;
  }

  // ============================================
  // ARTICLE + BLOG LUX MOTION
  // ============================================

  function initArticleBlogLuxMotion() {
    const scope = document.querySelector('.aurora-single-2026, .aurora-writing-archive');
    if (!scope) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isCompactViewport = window.matchMedia('(max-width: 700px)').matches;
    const revealStep = isCompactViewport ? 22 : 32;
    const revealDelayCap = isCompactViewport ? 120 : 220;
    const revealSelectors = [
      '.aurora-writing-archive-header',
      '.aurora-writing-card',
      '.aurora-article-header',
      '.aurora-featured-media',
      '.aurora-article-map',
      '.aurora-prose > p',
      '.aurora-prose > h2',
      '.aurora-prose > h3',
      '.aurora-prose > figure',
      '.aurora-prose > blockquote',
      '.aurora-prose > .wp-block-quote',
      '.aurora-prose > .wp-block-pullquote',
      '.aurora-prose > .wp-block-group',
      '.aurora-prose > .wp-block-table',
      '.aurora-prose > pre',
      '.aurora-prose > .wp-block-code',
      '.aurora-author-panel',
      '.aurora-tag-panel',
      '.aurora-related h2',
      '.aurora-related-row',
    ];

    const revealTargets = Array.from(document.querySelectorAll(revealSelectors.join(',')))
      .filter((target) => !target.hidden);

    revealTargets.forEach((target, index) => {
      target.classList.add('is-aurora-lux-reveal');
      target.style.setProperty('--aurora-lux-index', String(index));
      target.style.setProperty('--aurora-lux-delay', `${Math.min(index * revealStep, revealDelayCap)}ms`);
    });

    if (prefersReducedMotion) {
      revealTargets.forEach((target) => target.classList.add('is-revealed'));
    } else if ('IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          entry.target.classList.add('is-revealed');
          revealObserver.unobserve(entry.target);
        });
      }, {
        rootMargin: '0px 0px -8% 0px',
        threshold: 0.08,
      });

      revealTargets.forEach((target) => revealObserver.observe(target));

      requestAnimationFrame(() => {
        revealTargets.forEach((target) => {
          const rect = target.getBoundingClientRect();
          if (rect.top < window.innerHeight && rect.bottom > 0) {
            target.classList.add('is-revealed');
            revealObserver.unobserve(target);
          }
        });
      });
    } else {
      revealTargets.forEach((target) => target.classList.add('is-revealed'));
    }

    const article = document.querySelector('.aurora-article');
    const map = article?.querySelector('[data-aurora-article-map]');
    const mapLinks = Array.from(map?.querySelectorAll('a[href^="#"]') || []);
    if (!article || !map || mapLinks.length === 0) return;

    const headingsById = new Map(
      Array.from(article.querySelectorAll('.aurora-prose h2[id], .aurora-prose h3[id]'))
        .map((heading) => [heading.id, heading])
    );

    function getLinkHashId(link) {
      const rawId = link.hash.slice(1);

      try {
        return decodeURIComponent(rawId);
      } catch (error) {
        return rawId;
      }
    }

    const mapHeadings = mapLinks
      .map((link) => headingsById.get(getLinkHashId(link)))
      .filter(Boolean);

    if (mapHeadings.length === 0) return;

    function setActiveMapLink(id) {
      mapLinks.forEach((link) => {
        const isActive = getLinkHashId(link) === id;
        link.classList.toggle('is-active', isActive);

        if (isActive) {
          link.setAttribute('aria-current', 'true');
        } else {
          link.removeAttribute('aria-current');
        }
      });
    }

    const firstHeading = mapHeadings[0];
    if (firstHeading) {
      setActiveMapLink(firstHeading.id);
    }

    let pendingMapTargetId = '';
    let pendingMapTargetUntil = 0;

    mapLinks.forEach((link) => {
      link.addEventListener('click', () => {
        const id = getLinkHashId(link);
        if (id) {
          pendingMapTargetId = id;
          pendingMapTargetUntil = Date.now() + 3000;
          setActiveMapLink(id);
        }
      });
    });

    const getActiveHeadingId = () => {
      const anchor = Math.min(window.innerHeight * 0.35, 280);

      if (pendingMapTargetId && Date.now() < pendingMapTargetUntil) {
        const pendingHeading = headingsById.get(pendingMapTargetId);

        if (pendingHeading && pendingHeading.getBoundingClientRect().top > anchor) {
          return pendingMapTargetId;
        }

        pendingMapTargetId = '';
      }

      let activeHeading = mapHeadings[0];

      mapHeadings.forEach((heading) => {
        if (heading.getBoundingClientRect().top <= anchor) {
          activeHeading = heading;
        }
      });

      return activeHeading.id;
    };

    let activeMapFrame = null;
    const updateActiveMapLink = () => {
      activeMapFrame = null;
      setActiveMapLink(getActiveHeadingId());
    };
    const scheduleActiveMapUpdate = () => {
      if (activeMapFrame) return;
      activeMapFrame = window.requestAnimationFrame(updateActiveMapLink);
    };

    window.addEventListener('scroll', scheduleActiveMapUpdate, { passive: true });
    window.addEventListener('resize', scheduleActiveMapUpdate);
    window.addEventListener('load', scheduleActiveMapUpdate, { once: true });
    scheduleActiveMapUpdate();
  }

  // ============================================
  // LAZY LOAD IMAGES WITH FADE
  // ============================================

  function initLazyImages() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    images.forEach(img => {
      img.classList.add('aurora-lazy');
      
      img.addEventListener('load', () => {
        img.classList.add('is-loaded');
      });
      
      // If already loaded
      if (img.complete) {
        img.classList.add('is-loaded');
      }
    });
  }

  // ============================================
  // FORM ENHANCEMENTS
  // ============================================

  function initForms() {
    // Add active class to form groups with focus
    document.querySelectorAll('.aurora-form-group input, .aurora-form-group textarea').forEach(input => {
      input.addEventListener('focus', () => {
        input.closest('.aurora-form-group')?.classList.add('is-focused');
      });
      
      input.addEventListener('blur', () => {
        input.closest('.aurora-form-group')?.classList.remove('is-focused');
        
        // Add filled class if has value
        if (input.value.trim()) {
          input.closest('.aurora-form-group')?.classList.add('is-filled');
        } else {
          input.closest('.aurora-form-group')?.classList.remove('is-filled');
        }
      });
    });
  }

  // ============================================
  // DARK/LIGHT MODE (if needed in future)
  // ============================================

  function initColorScheme() {
    // Aurora is dark-mode only, but we could add this later
    // document.documentElement.classList.add('dark');
  }

  // ============================================
  // INITIALIZE
  // ============================================

  function init() {
    initPrimaryNavKeyboard();
    initSmoothScroll();
    initExternalLinks();
    initCodeCopy();
    initReadingProgress();
    initOpalReadingPane();
    initArticleReadingHelpers();
    initArticleBlogLuxMotion();
    initLazyImages();
    initForms();
    initColorScheme();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
