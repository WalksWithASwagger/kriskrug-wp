/**
 * KK Aurora - Animation Controller
 * 
 * GSAP-powered scroll animations and interactions.
 * Respects prefers-reduced-motion automatically.
 */

(function() {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  // Don't initialize animations if reduced motion is preferred
  if (prefersReducedMotion) {
    // Just make everything visible
    document.querySelectorAll('[data-aurora-animate]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  // Wait for GSAP to be available
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    console.warn('KK Aurora: GSAP or ScrollTrigger not loaded');
    return;
  }

  // Register ScrollTrigger plugin
  gsap.registerPlugin(ScrollTrigger);

  // ============================================
  // CONFIGURATION
  // ============================================

  const config = {
    // Default animation settings
    fadeUp: {
      y: 30,
      opacity: 0,
      duration: 0.6,
      ease: 'power2.out',
    },
    fadeIn: {
      opacity: 0,
      duration: 0.5,
      ease: 'power2.out',
    },
    scaleIn: {
      scale: 0.95,
      opacity: 0,
      duration: 0.5,
      ease: 'power2.out',
    },
    stagger: {
      each: 0.1,
      from: 'start',
    },
    // ScrollTrigger defaults
    scrollTrigger: {
      start: 'top 85%',
      end: 'bottom 20%',
      toggleActions: 'play none none reverse',
    },
  };

  // ============================================
  // SCROLL ANIMATIONS
  // ============================================

  /**
   * Initialize fade up animations
   */
  function initFadeUp() {
    const elements = document.querySelectorAll('[data-aurora-animate="fade-up"]');
    
    elements.forEach(el => {
      gsap.from(el, {
        ...config.fadeUp,
        scrollTrigger: {
          trigger: el,
          ...config.scrollTrigger,
        },
      });
    });
  }

  /**
   * Initialize fade in animations
   */
  function initFadeIn() {
    const elements = document.querySelectorAll('[data-aurora-animate="fade-in"]');
    
    elements.forEach(el => {
      gsap.from(el, {
        ...config.fadeIn,
        scrollTrigger: {
          trigger: el,
          ...config.scrollTrigger,
        },
      });
    });
  }

  /**
   * Initialize scale in animations
   */
  function initScaleIn() {
    const elements = document.querySelectorAll('[data-aurora-animate="scale-in"]');
    
    elements.forEach(el => {
      gsap.from(el, {
        ...config.scaleIn,
        scrollTrigger: {
          trigger: el,
          ...config.scrollTrigger,
        },
      });
    });
  }

  /**
   * Initialize staggered animations for groups
   */
  function initStagger() {
    const groups = document.querySelectorAll('[data-aurora-stagger]');
    
    groups.forEach(group => {
      const children = group.children;
      const type = group.dataset.auroraStagger || 'fade-up';
      
      let animationConfig;
      switch (type) {
        case 'fade-in':
          animationConfig = config.fadeIn;
          break;
        case 'scale-in':
          animationConfig = config.scaleIn;
          break;
        case 'fade-up':
        default:
          animationConfig = config.fadeUp;
      }
      
      gsap.from(children, {
        ...animationConfig,
        stagger: config.stagger,
        scrollTrigger: {
          trigger: group,
          ...config.scrollTrigger,
        },
      });
    });
  }

  // ============================================
  // NUMBER COUNTERS
  // ============================================

  /**
   * Animate number counters when they enter viewport
   */
  function initCounters() {
    const counters = document.querySelectorAll('[data-aurora-counter]');
    
    counters.forEach(counter => {
      const target = parseFloat(counter.dataset.auroraCounter);
      const suffix = counter.dataset.auroraSuffix || '';
      const prefix = counter.dataset.auroraPrefix || '';
      const decimals = parseInt(counter.dataset.auroraDecimals, 10) || 0;
      
      // Set initial value
      counter.textContent = prefix + '0' + suffix;
      
      ScrollTrigger.create({
        trigger: counter,
        start: 'top 80%',
        onEnter: () => {
          gsap.to(counter, {
            duration: 2,
            ease: 'power2.out',
            onUpdate: function() {
              const progress = this.progress();
              const currentValue = target * progress;
              counter.textContent = prefix + currentValue.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
            },
          });
        },
        once: true,
      });
    });
  }

  // ============================================
  // HEADER SCROLL EFFECTS
  // ============================================

  /**
   * Add glass effect to header on scroll
   */
  function initHeaderScroll() {
    const header = document.querySelector('.aurora-header');
    if (!header) return;
    
    ScrollTrigger.create({
      start: 'top -50',
      onUpdate: (self) => {
        if (self.scroll() > 50) {
          header.classList.add('is-scrolled');
        } else {
          header.classList.remove('is-scrolled');
        }
      },
    });
  }

  // ============================================
  // PARALLAX EFFECTS
  // ============================================

  /**
   * Initialize subtle parallax on images
   */
  function initParallax() {
    const elements = document.querySelectorAll('[data-aurora-parallax]');
    
    elements.forEach(el => {
      const speed = parseFloat(el.dataset.auroraParallax) || 0.1;
      
      gsap.to(el, {
        yPercent: speed * 100,
        ease: 'none',
        scrollTrigger: {
          trigger: el,
          start: 'top bottom',
          end: 'bottom top',
          scrub: true,
        },
      });
    });
  }

  // ============================================
  // HERO ANIMATIONS
  // ============================================

  /**
   * Initialize hero entrance animation
   */
  function initHeroAnimation() {
    const hero = document.querySelector('.aurora-hero');
    if (!hero) return;
    
    const timeline = gsap.timeline({
      defaults: { ease: 'power2.out' },
    });
    
    // Animate hero elements in sequence
    timeline
      .from('.aurora-hero .aurora-hero-headline', {
        y: 40,
        opacity: 0,
        duration: 0.8,
      })
      .from('.aurora-hero .aurora-hero-description', {
        y: 30,
        opacity: 0,
        duration: 0.6,
      }, '-=0.4')
      .from('.aurora-hero .aurora-badge', {
        y: 20,
        opacity: 0,
        duration: 0.4,
        stagger: 0.1,
      }, '-=0.3')
      .from('.aurora-hero .wp-block-button', {
        y: 20,
        opacity: 0,
        duration: 0.4,
        stagger: 0.1,
      }, '-=0.2')
      .from('.aurora-hero .aurora-scroll-indicator', {
        opacity: 0,
        duration: 0.6,
      }, '-=0.1');
  }

  // ============================================
  // CARD HOVER EFFECTS (enhanced)
  // ============================================

  /**
   * Add tilt effect on card hover
   */
  function initCardTilt() {
    const cards = document.querySelectorAll('[data-aurora-tilt]');
    
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        
        gsap.to(card, {
          rotateX: rotateX,
          rotateY: rotateY,
          duration: 0.3,
          ease: 'power2.out',
          transformPerspective: 1000,
        });
      });
      
      card.addEventListener('mouseleave', () => {
        gsap.to(card, {
          rotateX: 0,
          rotateY: 0,
          duration: 0.5,
          ease: 'power2.out',
        });
      });
    });
  }

  // ============================================
  // MAGNETIC BUTTONS
  // ============================================

  /**
   * Add magnetic effect to buttons
   */
  function initMagneticButtons() {
    const buttons = document.querySelectorAll('[data-aurora-magnetic]');
    
    buttons.forEach(button => {
      button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        gsap.to(button, {
          x: x * 0.2,
          y: y * 0.2,
          duration: 0.3,
          ease: 'power2.out',
        });
      });
      
      button.addEventListener('mouseleave', () => {
        gsap.to(button, {
          x: 0,
          y: 0,
          duration: 0.5,
          ease: 'elastic.out(1, 0.5)',
        });
      });
    });
  }

  // ============================================
  // PROGRESS BAR
  // ============================================

  /**
   * Initialize scroll progress bar
   */
  function initProgressBar() {
    const progressBar = document.querySelector('.aurora-progress-bar');
    if (!progressBar) return;
    
    gsap.to(progressBar, {
      scaleX: 1,
      ease: 'none',
      scrollTrigger: {
        trigger: document.body,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 0.3,
      },
    });
  }

  // ============================================
  // INITIALIZE
  // ============================================

  function init() {
    // Scroll animations
    initFadeUp();
    initFadeIn();
    initScaleIn();
    initStagger();
    
    // Special effects
    initCounters();
    initHeaderScroll();
    initParallax();
    initHeroAnimation();
    initProgressBar();
    
    // Interactive effects
    initCardTilt();
    initMagneticButtons();
    
    // Refresh ScrollTrigger after images load
    window.addEventListener('load', () => {
      ScrollTrigger.refresh();
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
