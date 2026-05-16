/**
 * KK Aurora - Theme JavaScript
 * 
 * General theme functionality and utilities.
 */

(function() {
  'use strict';

  // ============================================
  // MOBILE MENU
  // ============================================

  function initMobileMenu() {
    const toggle = document.querySelector('.aurora-menu-toggle');
    const menu = document.querySelector('.aurora-mobile-menu');
    
    if (!toggle || !menu) return;
    
    toggle.addEventListener('click', () => {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      
      toggle.setAttribute('aria-expanded', !isOpen);
      menu.classList.toggle('is-open');
      document.body.classList.toggle('menu-open');
      
      // Trap focus within menu when open
      if (!isOpen) {
        menu.querySelector('a, button')?.focus();
      }
    });
    
    // Close on escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) {
        toggle.click();
        toggle.focus();
      }
    });
  }

  // ============================================
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ============================================

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
          e.preventDefault();
          
          const headerOffset = 100;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
          
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
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
    const article = document.querySelector('article, .entry-content');
    
    if (!progressBar || !article) return;
    
    function updateProgress() {
      const articleRect = article.getBoundingClientRect();
      const articleTop = articleRect.top + window.pageYOffset;
      const articleHeight = articleRect.height;
      const windowHeight = window.innerHeight;
      const scrollTop = window.pageYOffset;
      
      const progress = Math.min(
        Math.max((scrollTop - articleTop + windowHeight) / articleHeight, 0),
        1
      );
      
      progressBar.style.transform = `scaleX(${progress})`;
    }
    
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
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
    initMobileMenu();
    initSmoothScroll();
    initExternalLinks();
    initCodeCopy();
    initReadingProgress();
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
