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

  // ============================================
  // SMOOTH REVEAL ON SCROLL
  // Intersection Observer based, no GSAP needed
  // ============================================
  
  function initScrollReveal() {
    if (prefersReducedMotion) {
      // Just show everything
      document.querySelectorAll('[data-reveal]').forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
      return;
    }
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -10% 0px'
    });
    
    document.querySelectorAll('[data-reveal]').forEach(el => {
      observer.observe(el);
    });
    
    // Add base styles
    const style = document.createElement('style');
    style.textContent = `
      [data-reveal] {
        opacity: 0;
        transform: translateY(24px);
        transition:
          opacity 1.2s cubic-bezier(0.25, 0.1, 0.25, 1),
          transform 1.2s cubic-bezier(0.25, 0.1, 0.25, 1);
      }
      
      [data-reveal].is-revealed {
        opacity: 1;
        transform: translateY(0);
      }
      
      /* Stagger children */
      [data-reveal-stagger] > * {
        opacity: 0;
        transform: translateY(18px);
        transition:
          opacity 1.1s cubic-bezier(0.25, 0.1, 0.25, 1),
          transform 1.1s cubic-bezier(0.25, 0.1, 0.25, 1);
      }
      
      [data-reveal-stagger].is-revealed > *:nth-child(1) { transition-delay: 0s; opacity: 1; transform: translateY(0); }
      [data-reveal-stagger].is-revealed > *:nth-child(2) { transition-delay: 0.1s; opacity: 1; transform: translateY(0); }
      [data-reveal-stagger].is-revealed > *:nth-child(3) { transition-delay: 0.2s; opacity: 1; transform: translateY(0); }
      [data-reveal-stagger].is-revealed > *:nth-child(4) { transition-delay: 0.3s; opacity: 1; transform: translateY(0); }
      [data-reveal-stagger].is-revealed > *:nth-child(5) { transition-delay: 0.4s; opacity: 1; transform: translateY(0); }
      [data-reveal-stagger].is-revealed > *:nth-child(6) { transition-delay: 0.5s; opacity: 1; transform: translateY(0); }
    `;
    document.head.appendChild(style);

    // #116: reveal anything already in the initial viewport on the next frame, so the
    // hero/above-the-fold never waits on the async observer — no cold-load flash, and a
    // hard guarantee against a blank first paint even if the observer is slow to fire.
    requestAnimationFrame(() => {
      document.querySelectorAll('[data-reveal]:not(.is-revealed)').forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) {
          el.classList.add('is-revealed');
        }
      });
    });
  }

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
        background-color: rgba(13, 13, 18, 0.9);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 1px 0 rgba(255, 255, 255, 0.05);
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
  // IMAGE LAZY LOAD WITH BLUR
  // Graceful reveal
  // ============================================
  
  function initImageReveal() {
    const style = document.createElement('style');
    style.textContent = `
      img[loading="lazy"] {
        opacity: 0;
        filter: blur(10px);
        transition: 
          opacity 0.5s ease,
          filter 0.5s ease;
      }
      
      img[loading="lazy"].is-loaded {
        opacity: 1;
        filter: blur(0);
      }
    `;
    document.head.appendChild(style);
    
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      if (img.complete) {
        img.classList.add('is-loaded');
      } else {
        img.addEventListener('load', () => {
          img.classList.add('is-loaded');
        }, { once: true });
      }
    });
  }

  // ============================================
  // INITIALIZE
  // ============================================
  
  function init() {
    initScrollReveal();
    initCounters();
    initHeaderTransform();
    initImageReveal();
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
