/**
 * Advanced Pill Navigation with GSAP Animations
 * Converted from React to Vanilla JavaScript for Django
 */

class PillNavigation {
  constructor(options = {}) {
    this.config = {
      ease: options.ease || 'power3.easeOut',
      baseColor: options.baseColor || '#fff',
      pillColor: options.pillColor || '#0d6efd',
      hoveredPillTextColor: options.hoveredPillTextColor || '#fff',
      pillTextColor: options.pillTextColor || '#fff',
      initialLoadAnimation: options.initialLoadAnimation !== false
    };
    
    this.state = {
      isMobileMenuOpen: false
    };
    
    this.refs = {
      circles: [],
      timelines: [],
      activeTweens: [],
      logoImg: null,
      logoTween: null,
      hamburger: null,
      mobileMenu: null,
      navItems: null,
      logo: null
    };
    
    this.init();
  }
  
  init() {
    // Wait for DOM and GSAP to be ready
    if (typeof gsap === 'undefined') {
      console.warn('GSAP is not loaded. Please include GSAP before pill-nav.js');
      return;
    }
    
    this.setupElements();
    this.setupEventListeners();
    this.layout();
    
    if (this.config.initialLoadAnimation) {
      this.performInitialAnimation();
    }
    
    this.setActiveState();
  }
  
  setupElements() {
    // Cache DOM elements
    this.refs.circles = Array.from(document.querySelectorAll('.hover-circle'));
    this.refs.logoImg = document.querySelector('.pill-logo img');
    this.refs.hamburger = document.querySelector('.mobile-menu-button');
    this.refs.mobileMenu = document.querySelector('.mobile-menu-popover');
    this.refs.navItems = document.querySelector('.pill-nav-items');
    this.refs.logo = document.querySelector('.pill-logo');
    
    // Initialize mobile menu state
    if (this.refs.mobileMenu) {
      gsap.set(this.refs.mobileMenu, { 
        visibility: 'hidden', 
        opacity: 0, 
        scaleY: 1 
      });
    }
  }
  
  setupEventListeners() {
    // Pill hover events
    const pills = document.querySelectorAll('.pill');
    pills.forEach((pill, index) => {
      pill.addEventListener('mouseenter', () => this.handleEnter(index));
      pill.addEventListener('mouseleave', () => this.handleLeave(index));
      
      // Add click animation
      pill.addEventListener('click', (e) => {
        this.handlePillClick(pill, e);
      });
    });
    
    // Logo hover events
    if (this.refs.logo) {
      this.refs.logo.addEventListener('mouseenter', () => this.handleLogoEnter());
    }
    
    // Mobile menu toggle
    if (this.refs.hamburger) {
      this.refs.hamburger.addEventListener('click', () => this.toggleMobileMenu());
    }
    
    // Mobile menu links
    const mobileLinks = document.querySelectorAll('.mobile-menu-link');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        this.state.isMobileMenuOpen = false;
        this.updateMobileMenuState(false);
      });
    });
    
    // Window resize
    window.addEventListener('resize', () => this.layout());
    
    // Font loading
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => this.layout()).catch(() => {});
    }
  }
  
  layout() {
    this.refs.circles.forEach((circle, index) => {
      if (!circle || !circle.parentElement) return;
      
      const pill = circle.parentElement;
      const rect = pill.getBoundingClientRect();
      const { width: w, height: h } = rect;
      
      // Calculate circle properties
      const R = ((w * w) / 4 + h * h) / (2 * h);
      const D = Math.ceil(2 * R) + 2;
      const delta = Math.ceil(R - Math.sqrt(Math.max(0, R * R - (w * w) / 4))) + 1;
      const originY = D - delta;
      
      // Set circle dimensions and position
      circle.style.width = `${D}px`;
      circle.style.height = `${D}px`;
      circle.style.bottom = `-${delta}px`;
      
      // Initial GSAP setup
      gsap.set(circle, {
        xPercent: -50,
        scale: 0,
        transformOrigin: `50% ${originY}px`
      });
      
      const label = pill.querySelector('.pill-label');
      const hoverLabel = pill.querySelector('.pill-label-hover');
      
      if (label) gsap.set(label, { y: 0 });
      if (hoverLabel) gsap.set(hoverLabel, { y: h + 12, opacity: 0 });
      
      // Create timeline for this pill
      this.refs.timelines[index]?.kill();
      const tl = gsap.timeline({ paused: true });
      
      tl.to(circle, { 
        scale: 1.2, 
        xPercent: -50, 
        duration: 2, 
        ease: this.config.ease, 
        overwrite: 'auto' 
      }, 0);
      
      if (label) {
        tl.to(label, { 
          y: -(h + 8), 
          duration: 2, 
          ease: this.config.ease, 
          overwrite: 'auto' 
        }, 0);
      }
      
      if (hoverLabel) {
        gsap.set(hoverLabel, { y: Math.ceil(h + 100), opacity: 0 });
        tl.to(hoverLabel, { 
          y: 0, 
          opacity: 1, 
          duration: 2, 
          ease: this.config.ease, 
          overwrite: 'auto' 
        }, 0);
      }
      
      this.refs.timelines[index] = tl;
    });
  }
  
  handleEnter(index) {
    const tl = this.refs.timelines[index];
    if (!tl) return;
    
    this.refs.activeTweens[index]?.kill();
    this.refs.activeTweens[index] = tl.tweenTo(tl.duration(), {
      duration: 0.3,
      ease: this.config.ease,
      overwrite: 'auto'
    });
  }
  
  handleLeave(index) {
    const tl = this.refs.timelines[index];
    if (!tl) return;
    
    this.refs.activeTweens[index]?.kill();
    this.refs.activeTweens[index] = tl.tweenTo(0, {
      duration: 0.2,
      ease: this.config.ease,
      overwrite: 'auto'
    });
  }
  
  handlePillClick(pill, event) {
    // Add click animation
    gsap.to(pill, {
      scale: 0.95,
      duration: 0.1,
      ease: this.config.ease,
      yoyo: true,
      repeat: 1
    });
    
    // Update active state
    document.querySelectorAll('.pill').forEach(p => p.classList.remove('is-active'));
    pill.classList.add('is-active');
  }
  
  handleLogoEnter() {
    const img = this.refs.logoImg;
    if (!img) return;
    
    this.refs.logoTween?.kill();
    gsap.set(img, { rotate: 0 });
    this.refs.logoTween = gsap.to(img, {
      rotate: 360,
      duration: 0.6,
      ease: this.config.ease,
      overwrite: 'auto'
    });
  }
  
  toggleMobileMenu() {
    this.state.isMobileMenuOpen = !this.state.isMobileMenuOpen;
    this.updateMobileMenuState(this.state.isMobileMenuOpen);
  }
  
  updateMobileMenuState(isOpen) {
    const hamburger = this.refs.hamburger;
    const menu = this.refs.mobileMenu;
    
    if (hamburger) {
      const lines = hamburger.querySelectorAll('.hamburger-line');
      if (isOpen) {
        gsap.to(lines[0], { rotation: 45, y: 3, duration: 0.3, ease: this.config.ease });
        gsap.to(lines[1], { rotation: -45, y: -3, duration: 0.3, ease: this.config.ease });
      } else {
        gsap.to(lines[0], { rotation: 0, y: 0, duration: 0.3, ease: this.config.ease });
        gsap.to(lines[1], { rotation: 0, y: 0, duration: 0.3, ease: this.config.ease });
      }
    }
    
    if (menu) {
      if (isOpen) {
        gsap.set(menu, { visibility: 'visible' });
        gsap.fromTo(
          menu,
          { opacity: 0, y: 10, scaleY: 1 },
          {
            opacity: 1,
            y: 0,
            scaleY: 1,
            duration: 0.3,
            ease: this.config.ease,
            transformOrigin: 'top center'
          }
        );
      } else {
        gsap.to(menu, {
          opacity: 0,
          y: 10,
          scaleY: 1,
          duration: 0.2,
          ease: this.config.ease,
          transformOrigin: 'top center',
          onComplete: () => {
            gsap.set(menu, { visibility: 'hidden' });
          }
        });
      }
    }
  }
  
  performInitialAnimation() {
    const logo = this.refs.logo;
    const navItems = this.refs.navItems;
    
    if (logo) {
      gsap.set(logo, { scale: 0, opacity: 0 });
      gsap.to(logo, {
        scale: 1,
        opacity: 1,
        duration: 0.6,
        ease: this.config.ease
      });
    }
    
    if (navItems) {
      gsap.set(navItems, { width: 0, overflow: 'hidden', opacity: 0 });
      gsap.to(navItems, {
        width: 'auto',
        opacity: 1,
        duration: 0.8,
        delay: 0.2,
        ease: this.config.ease
      });
    }
  }
  
  setActiveState() {
    const currentPath = window.location.pathname;
    const pills = document.querySelectorAll('.pill');
    const mobileLinks = document.querySelectorAll('.mobile-menu-link');
    
    // Function to check if current path matches link
    const isActivePage = (linkPath) => {
      if (currentPath === linkPath) return true;
      
      // Handle language prefixes
      const langPrefixes = ['/en/', '/hi/', '/ta/', '/bn/', '/mr/', '/gu/', '/kn/', '/ml/', '/pa/', '/te/'];
      let normalizedCurrentPath = currentPath;
      
      for (let prefix of langPrefixes) {
        if (normalizedCurrentPath.startsWith(prefix)) {
          normalizedCurrentPath = normalizedCurrentPath.substring(prefix.length - 1);
          break;
        }
      }
      
      // Check if it's home page
      if ((normalizedCurrentPath === '/' || normalizedCurrentPath === '') && linkPath.includes('home')) {
        return true;
      }
      
      // Check for partial matches
      const linkSegments = linkPath.split('/').filter(s => s);
      const pathSegments = normalizedCurrentPath.split('/').filter(s => s);
      
      return linkSegments.some(segment => pathSegments.includes(segment));
    };
    
    // Set active state for desktop pills
    pills.forEach(pill => {
      const href = pill.getAttribute('href');
      if (href && isActivePage(href)) {
        pill.classList.add('is-active');
      }
    });
    
    // Set active state for mobile links
    mobileLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && isActivePage(href)) {
        link.classList.add('is-active');
      }
    });
  }
  
  // Public API methods
  updateActiveState(href) {
    document.querySelectorAll('.pill, .mobile-menu-link').forEach(el => {
      el.classList.remove('is-active');
    });
    
    document.querySelectorAll(`[href="${href}"]`).forEach(el => {
      el.classList.add('is-active');
    });
  }
  
  destroy() {
    // Clean up timelines and tweens
    this.refs.timelines.forEach(tl => tl?.kill());
    this.refs.activeTweens.forEach(tween => tween?.kill());
    this.refs.logoTween?.kill();
    
    // Remove event listeners
    window.removeEventListener('resize', this.layout.bind(this));
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  // Check if we have pill navigation elements
  if (document.querySelector('.pill-nav-container')) {
    window.pillNav = new PillNavigation({
      ease: 'power3.easeOut',
      initialLoadAnimation: true
    });
  }
});

// Export for global access
window.PillNavigation = PillNavigation;