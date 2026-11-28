/**
 * KK Aurora - Micro-Interactions
 * 
 * Subtle, inevitable-feeling interactions.
 * Taste is knowing when NOT to animate.
 */

(function() {
  'use strict';

  // Respect user preferences
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  // ============================================
  // CARD SPOTLIGHT EFFECT
  // Light follows cursor on cards
  // ============================================
  
  function initCardSpotlight() {
    if (prefersReducedMotion) return;
    if (!window.matchMedia('(pointer: fine)').matches) return;
    
    const cards = document.querySelectorAll('.aurora-card, .aurora-card-premium');
    
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        
        card.style.setProperty('--mouse-x', x + '%');
        card.style.setProperty('--mouse-y', y + '%');
      }, { passive: true });
    });
  }

  // Scroll reveal and lazy-image loading are owned by theme.js so non-journal
  // pages do not run competing IntersectionObservers, 1.2s fades, or 10px blurs.

  // ============================================
  // TEXT SPLIT FOR ANIMATION
  // Split text into words/chars for animation
  // ============================================
  
  function initTextSplit() {
    if (prefersReducedMotion) return;
    
    document.querySelectorAll('[data-split-text]').forEach(el => {
      const text = el.textContent;
      const words = text.split(' ');
      
      el.innerHTML = words.map((word, i) => 
        `<span class="word" style="--word-index: ${i}">${word}</span>`
      ).join(' ');
    });
    
    const style = document.createElement('style');
    style.textContent = `
      [data-split-text] .word {
        display: inline-block;
        opacity: 0;
        transform: translateY(0.5em);
      }
      
      [data-split-text].is-revealed .word {
        opacity: 1;
        transform: translateY(0);
        transition: 
          opacity 0.5s ease,
          transform 0.5s cubic-bezier(0.25, 0.1, 0.25, 1);
        transition-delay: calc(var(--word-index) * 0.05s);
      }
    `;
    document.head.appendChild(style);
  }

  // ============================================
  // SMOOTH NUMBER COUNTER
  // No library needed
  // ============================================
  
  function initCounters() {
    if (prefersReducedMotion) return;
    
    const counters = document.querySelectorAll('[data-aurora-counter]');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
      observer.observe(counter);
    });
    
    function animateCounter(el) {
      const target = parseFloat(el.dataset.auroraCounter);
      const suffix = el.dataset.auroraSuffix || '';
      const prefix = el.dataset.auroraPrefix || '';
      const duration = 2000;
      const start = performance.now();
      
      function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease out quint
        const eased = 1 - Math.pow(1 - progress, 5);
        const current = target * eased;
        
        // Format with commas
        const formatted = Math.round(current).toLocaleString();
        el.textContent = prefix + formatted + suffix;
        
        if (progress < 1) {
          requestAnimationFrame(update);
        }
      }
      
      requestAnimationFrame(update);
    }
  }

  // ============================================
  // HEADER SHRINK ON SCROLL
  // Subtle, not jarring
  // ============================================
  
  function initHeaderTransform() {
    const header = document.querySelector('.aurora-header');
    if (!header) return;
    
    let lastScroll = 0;
    let ticking = false;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
      .aurora-header {
        transition: 
          background-color 0.3s ease,
          backdrop-filter 0.3s ease,
          box-shadow 0.3s ease;
      }
      
      .aurora-header.is-scrolled {
        background-color: rgba(239, 230, 210, 0.92);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 1px 0 rgba(23, 19, 16, 0.08);
      }
      
      .aurora-header.is-hidden {
        transform: translateY(-100%);
      }
    `;
    document.head.appendChild(style);
    
    function updateHeader() {
      const scroll = window.pageYOffset;
      
      // Add scrolled state
      if (scroll > 50) {
        header.classList.add('is-scrolled');
      } else {
        header.classList.remove('is-scrolled');
      }
      
      // Hide on scroll down, show on scroll up (optional - disabled for now)
      // if (scroll > lastScroll && scroll > 200) {
      //   header.classList.add('is-hidden');
      // } else {
      //   header.classList.remove('is-hidden');
      // }
      
      lastScroll = scroll;
      ticking = false;
    }
    
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(updateHeader);
        ticking = true;
      }
    }, { passive: true });
  }

  // ============================================
  // LINK HOVER PREVIEW
  // Show a subtle preview on link hover
  // ============================================
  
  function initLinkPreview() {
    if (prefersReducedMotion) return;
    if (!window.matchMedia('(pointer: fine)').matches) return;
    
    // This is intentionally minimal - just a URL preview
    // Full page previews would be overkill
    
    const style = document.createElement('style');
    style.textContent = `
      a[href^="http"]:not(.no-preview):hover::after {
        content: attr(href);
        position: absolute;
        bottom: 100%;
        left: 0;
        padding: 0.25em 0.5em;
        font-size: 0.75rem;
        background: var(--wp--preset--color--surface);
        border: 1px solid var(--wp--preset--color--elevated);
        border-radius: 4px;
        white-space: nowrap;
        max-width: 300px;
        overflow: hidden;
        text-overflow: ellipsis;
        opacity: 0;
        animation: aurora-preview-in 0.2s 0.5s ease forwards;
        pointer-events: none;
        z-index: 1000;
      }
      
      @keyframes aurora-preview-in {
        to {
          opacity: 1;
        }
      }
    `;
    document.head.appendChild(style);
    
    // Add relative positioning to links
    document.querySelectorAll('a[href^="http"]').forEach(link => {
      link.style.position = 'relative';
    });
  }

  // ============================================
  // INITIALIZE
  // ============================================
  
  function init() {
    initCounters();
    initHeaderTransform();
    const motionProfile = document.body?.dataset?.auroraMotionProfile;
    if (motionProfile === 'enhanced') {
      initCardSpotlight();
      initTextSplit();
    }
    // initLinkPreview(); // Disabled - too distracting
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
