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
        let target;
        try {
          target = href && href.length > 1 ? document.getElementById(decodeURIComponent(href.slice(1))) : null;
        } catch {
          return;
        }
        
        if (target) {
          e.preventDefault();
          
          const headerOffset = 100;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: prefersReducedMotion || document.body.classList.contains('aurora-journal-page') ? 'auto' : 'smooth'
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

  function initHeaderScrollProgress() {
    const bar = document.querySelector('.aurora-scroll-progress');
    if (!bar) return;

    function update() {
      const doc = document.documentElement;
      const max = Math.max(doc.scrollHeight - window.innerHeight, 1);
      const progress = Math.min(Math.max(window.scrollY / max, 0), 1);
      bar.style.setProperty('--scroll-progress', String(progress));
    }

    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
  }

  function initRevealOnScroll() {
    const nodes = document.querySelectorAll('[data-reveal]');
    if (!nodes.length) return;

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
      nodes.forEach((node) => node.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    // #701: mark in-viewport nodes visible synchronously so above-the-fold
    // content never depends on an async observer callback to stay painted.
    nodes.forEach((node) => {
      const r = node.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) {
        node.classList.add('is-visible');
      } else {
        observer.observe(node);
      }
    });
  }

  function initLiveMastheadDate() {
    const el = document.querySelector('[data-live-date]');
    if (!el) return;
    try {
      el.textContent = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      });
    } catch (e) {
      // keep server-rendered fallback
    }
  }

  // ============================================
  // ARTICLE READING HELPERS
  // ============================================

  function initArticleReadingHelpers() {
    const article = document.querySelector('.aurora-journal-article');
    const content = article?.querySelector('.aurora-journal-prose');

    if (!article || !content) return;

    const readTime = article.querySelector('[data-aurora-read-time]');
    const words = content.innerText.trim().split(/\s+/).filter(Boolean).length;

    if (readTime && words > 120) {
      const minutes = Math.max(1, Math.ceil(words / 225));
      readTime.textContent = `${minutes} min read`;
      readTime.hidden = false;
    }

    const map = article.querySelector('[data-aurora-article-map]');
    const nav = map?.querySelector('nav');
    const headings = Array.from(content.querySelectorAll('h2, h3'))
      .filter((heading) => heading.textContent.trim().length > 0);

    if (!map || !nav || headings.length < 3) return;

    const list = document.createElement('ol');

    headings.forEach((heading, index) => {
      if (!heading.id) {
        let id = `article-section-${index + 1}`;
        while (document.getElementById(id)) id += '-section';
        heading.id = id;
      }

      const item = document.createElement('li');
      const link = document.createElement('a');

      link.href = `#${encodeURIComponent(heading.id)}`;
      link.textContent = heading.textContent.trim();
      link.className = heading.tagName === 'H3' ? 'is-subsection' : '';
      item.appendChild(link);
      list.appendChild(item);
    });

    nav.appendChild(list);
    map.hidden = false;
    const desktop = window.matchMedia('(min-width: 1100px)');
    const updateContents = () => { map.open = desktop.matches; };
    updateContents();
    desktop.addEventListener('change', updateContents);
  }

  function initArticleContentsTracking() {
    const article = document.querySelector('.aurora-journal-article');
    const map = article?.querySelector('[data-aurora-article-map]');
    const mapLinks = Array.from(map?.querySelectorAll('a[href^="#"]') || []);
    if (!article || !map || mapLinks.length === 0) return;

    const headingsById = new Map(
      Array.from(article.querySelectorAll('.aurora-journal-prose h2[id], .aurora-journal-prose h3[id]'))
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

  function initLogoSoup() {
    const root = document.getElementById('clients');
    if (!root) return;

    const readout = document.getElementById('aurora-logo-soup-readout');
    const items = root.querySelectorAll('.aurora-logo-soup__item');
    const empty = 'Hover or focus a logo.';

    function setActive(btn) {
      items.forEach((el) => {
        el.classList.toggle('is-active', el === btn);
      });
      if (!readout) return;
      readout.textContent = btn
        ? `${btn.getAttribute('aria-label')}: ${btn.getAttribute('data-note') || ''}`
        : empty;
    }

    items.forEach((btn) => {
      btn.addEventListener('mouseenter', () => setActive(btn));
      btn.addEventListener('focus', () => setActive(btn));
      btn.addEventListener('click', () => {
        const stickyTap = window.matchMedia('(hover: none)').matches;
        setActive(stickyTap && btn.classList.contains('is-active') ? null : btn);
      });
    });

    root.addEventListener('mouseleave', () => {
      if (!root.querySelector('.aurora-logo-soup__item:focus')) {
        setActive(null);
      }
    });
  }

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
    document.querySelector('.aurora-journal-mobile-nav')?.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      event.currentTarget.open = false;
      event.currentTarget.querySelector('summary').focus();
    });
    initPrimaryNavKeyboard();
    initExternalLinks();
    initCodeCopy();
    initHeaderScrollProgress();
    if (!document.body.classList.contains('aurora-journal-page')) initRevealOnScroll();
    initLiveMastheadDate();
    initArticleReadingHelpers();
    initSmoothScroll();
    initArticleContentsTracking();
    if (!document.body.classList.contains('aurora-journal-page')) initLazyImages();
    initLogoSoup();
    initForms();
    initColorScheme();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
