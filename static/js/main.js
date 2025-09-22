// Main JavaScript file for the Mental Health Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize bokeh background effect
    initBokehEffect();
    
    // Initialize pill navigation
    initPillNavigation();
    
    // Initialize spotlight cards
    initSpotlightCards();
    
    // Initialize hamburger menu
    initHamburgerMenu();
    
    // Initialize tooltips and popovers
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Fade in animations
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-permanent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
});

// Chat functionality
class ChatInterface {
    constructor(chatContainer, inputField, sendButton) {
        this.chatContainer = chatContainer;
        this.inputField = inputField;
        this.sendButton = sendButton;
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }
        if (this.inputField) {
            this.inputField.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    }
    
    sendMessage() {
        const message = this.inputField.value.trim();
        if (message && !this.isTyping) {
            this.addMessage(message, 'user');
            this.inputField.value = '';
            this.simulateTyping();
            
            // Send to backend (replace with actual API call)
            this.sendToBackend(message);
        }
    }
    
    addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = message;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    simulateTyping() {
        this.isTyping = true;
        this.sendButton.disabled = true;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing';
        typingDiv.innerHTML = 'AI is typing<span class="typing-dots">...</span>';
        typingDiv.id = 'typing-indicator';
        
        this.chatContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    stopTyping() {
        this.isTyping = false;
        this.sendButton.disabled = false;
        
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    sendToBackend(message) {
        // Simulate API call - replace with actual backend integration
        setTimeout(() => {
            this.stopTyping();
            this.addMessage(this.generateResponse(message), 'bot');
        }, 1500);
    }
    
    generateResponse(message) {
        // Simple response simulation - replace with actual AI integration
        const responses = [
            "I understand you're going through a difficult time. Can you tell me more about what's bothering you?",
            "Thank you for sharing that with me. Have you considered speaking with a counselor about this?",
            "It's completely normal to feel overwhelmed sometimes. Here are some coping strategies that might help...",
            "I'm here to support you. Would you like me to help you schedule an appointment with a professional?",
            "That sounds challenging. Remember that seeking help is a sign of strength, not weakness."
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
}

// Appointment booking functionality
class AppointmentBooking {
    constructor() {
        this.selectedSlot = null;
        this.init();
    }
    
    init() {
        const slots = document.querySelectorAll('.appointment-slot');
        slots.forEach(slot => {
            slot.addEventListener('click', () => this.selectSlot(slot));
        });
        
        // Initialize calendar if present
        this.initCalendar();
    }
    
    selectSlot(slot) {
        // Remove previous selection
        if (this.selectedSlot) {
            this.selectedSlot.classList.remove('selected');
        }
        
        // Select new slot
        this.selectedSlot = slot;
        slot.classList.add('selected');
        
        // Enable booking button
        const bookButton = document.getElementById('book-appointment-btn');
        if (bookButton) {
            bookButton.disabled = false;
        }
    }
    
    initCalendar() {
        // Calendar initialization would go here
        // This could integrate with a library like FullCalendar.js
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Loading state management
function showLoading(element) {
    element.innerHTML = '<div class="spinner"></div>';
    element.disabled = true;
}

function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
}

// Emergency contact modal
function showEmergencyModal() {
    const modal = new bootstrap.Modal(document.getElementById('emergencyModal'));
    modal.show();
}

// Utility functions
function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(time) {
    return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Pill Navigation functionality
function initPillNavigation() {
    const pillLinks = document.querySelectorAll('.pill-link');
    const currentPath = window.location.pathname;
    
    // Set active state based on current URL
    pillLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        
        // Check if current path matches or contains the link path
        if (currentPath === linkPath || 
            (linkPath !== '/' && currentPath.includes(linkPath.split('/')[1]))) {
            link.classList.add('current-page');
        }
        
        // Add click event for smooth navigation
        link.addEventListener('click', function(e) {
            // Add loading state
            pillLinks.forEach(l => l.classList.remove('current-page'));
            this.classList.add('current-page');
            
            // Add navigation animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
        
        // Add hover effects
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('current-page')) {
                this.style.transform = '';
            }
        });
    });
    
    // Special handling for home page
    if (currentPath === '/' || currentPath === '/en/' || currentPath === '/hi/' || 
        currentPath.match(/^\/(en|hi|ta|bn|mr|gu|kn|ml|pa|te)\/?$/)) {
        const homeLink = document.querySelector('.pill-link[data-page="home"]');
        if (homeLink) {
            pillLinks.forEach(l => l.classList.remove('current-page'));
            homeLink.classList.add('current-page');
        }
    }
}

// Spotlight Card functionality
class SpotlightCards {
    constructor() {
        this.cards = document.querySelectorAll('.spotlight-card');
        this.init();
    }
    
    init() {
        this.cards.forEach((card, index) => {
            this.setupCardEvents(card, index);
        });
        
        // Initialize intersection observer for animation on scroll
        this.setupScrollAnimations();
    }
    
    setupCardEvents(card, index) {
        // Mouse move spotlight effect
        card.addEventListener('mousemove', (e) => {
            this.updateSpotlight(card, e);
        });
        
        // Reset spotlight on mouse leave
        card.addEventListener('mouseleave', () => {
            this.resetSpotlight(card);
        });
        
        // Click animation
        card.addEventListener('click', (e) => {
            if (!e.target.matches('a, button, .spotlight-btn')) {
                this.animateClick(card);
            }
        });
        
        // Add entry animation delay
        card.style.animationDelay = `${index * 0.1}s`;
    }
    
    updateSpotlight(card, event) {
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const deltaX = (x - centerX) / centerX;
        const deltaY = (y - centerY) / centerY;
        
        // Update spotlight position
        const spotlight = card.querySelector('::before') || card;
        card.style.setProperty('--spotlight-x', `${x}px`);
        card.style.setProperty('--spotlight-y', `${y}px`);
        
        // Subtle tilt effect
        const tiltX = deltaY * 5;
        const tiltY = deltaX * -5;
        
        card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-8px) scale(1.02)`;
    }
    
    resetSpotlight(card) {
        card.style.transform = '';
    }
    
    animateClick(card) {
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    }
    
    setupScrollAnimations() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('fade-in');
                            observer.unobserve(entry.target);
                        }
                    });
                },
                {
                    threshold: 0.1,
                    rootMargin: '50px'
                }
            );
            
            this.cards.forEach((card) => {
                observer.observe(card);
            });
        }
    }
    
    // Public method to add spotlight effect to new cards
    addCard(cardElement) {
        this.setupCardEvents(cardElement, this.cards.length);
        this.cards.push(cardElement);
    }
}

// Bokeh Background Effect
function initBokehEffect() {
    const bokehContainer = document.querySelector('.bokeh-container');
    if (!bokehContainer) return;
    
    // Add random horizontal drift to bokeh lights
    const lights = document.querySelectorAll('.bokeh-light');
    lights.forEach((light, index) => {
        // Random horizontal position variation
        const randomLeft = Math.random() * 100;
        light.style.left = randomLeft + '%';
        
        // Add subtle horizontal drift animation
        const drift = (Math.random() - 0.5) * 30; // -15 to 15px drift
        light.style.setProperty('--drift', drift + 'px');
        
        // Vary the opacity slightly for more natural effect
        const baseOpacity = 0.4 + (Math.random() * 0.6); // 0.4 to 1.0
        light.style.setProperty('--base-opacity', baseOpacity);
    });
    
    // Create additional floating lights periodically
    let lightCounter = 10;
    setInterval(() => {
        if (document.querySelectorAll('.bokeh-light').length < 20) {
            createFloatingLight(lightCounter++);
        }
    }, 5000); // Create a new light every 5 seconds
}

function createFloatingLight(id) {
    const bokehContainer = document.querySelector('.bokeh-container');
    if (!bokehContainer) return;
    
    const light = document.createElement('div');
    light.className = 'bokeh-light';
    light.id = `dynamic-light-${id}`;
    
    // Random properties
    const size = 4 + Math.random() * 12; // 4-16px
    const left = Math.random() * 100;
    const duration = 15 + Math.random() * 10; // 15-25s
    const delay = Math.random() * 5; // 0-5s delay
    
    // Random color - soft warm or cool tones
    const colors = [
        'rgba(255, 248, 220, 0.8)', // warm white
        'rgba(173, 216, 230, 0.6)', // light blue
        'rgba(255, 255, 255, 0.9)', // pure white
        'rgba(255, 223, 186, 0.7)', // peach
        'rgba(176, 196, 222, 0.5)', // light steel blue
        'rgba(255, 250, 205, 0.8)', // lemon chiffon
    ];
    const color = colors[Math.floor(Math.random() * colors.length)];
    
    light.style.cssText = `
        width: ${size}px;
        height: ${size}px;
        left: ${left}%;
        background: radial-gradient(circle, ${color} 0%, ${color.replace('0.', '0.1')} 70%, transparent 100%);
        animation: floatAndFade ${duration}s infinite linear;
        animation-delay: -${delay}s;
        filter: blur(${2 + Math.random() * 2}px);
    `;
    
    bokehContainer.appendChild(light);
    
    // Remove the light after animation completes
    setTimeout(() => {
        if (light.parentNode) {
            light.parentNode.removeChild(light);
        }
    }, duration * 1000);
}

// Initialize spotlight cards
function initSpotlightCards() {
    if (document.querySelector('.spotlight-card')) {
        return new SpotlightCards();
    }
    return null;
}

// Hamburger Menu functionality
class HamburgerMenu {
    constructor() {
        this.hamburgerButton = document.getElementById('hamburgerMenu');
        this.desktopMenuButton = document.getElementById('desktopMenuButton');
        this.drawer = document.getElementById('slidingDrawer');
        this.overlay = document.getElementById('drawerOverlay');
        this.menuItems = document.querySelectorAll('.drawer-menu-item');
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        if (!this.drawer || !this.overlay) {
            return; // Essential elements not found, skip initialization
        }
        
        // Hamburger button click (mobile)
        if (this.hamburgerButton) {
            this.hamburgerButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggle();
            });
        }
        
        // Desktop menu button click
        if (this.desktopMenuButton) {
            this.desktopMenuButton.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggle();
            });
        }
        
        // Overlay click - close drawer
        this.overlay.addEventListener('click', () => {
            this.close();
        });
        
        // Close drawer when clicking outside
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.drawer.contains(e.target) && 
                !(this.hamburgerButton && this.hamburgerButton.contains(e.target)) &&
                !(this.desktopMenuButton && this.desktopMenuButton.contains(e.target))) {
                this.close();
            }
        });
        
        // Close drawer on menu item click
        this.menuItems.forEach(item => {
            item.addEventListener('click', () => {
                // Add a slight delay to allow the click navigation to process
                setTimeout(() => {
                    this.close();
                }, 150);
            });
        });
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });
        
        // Prevent scroll when drawer is open
        this.setupScrollLock();
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    open() {
        this.isOpen = true;
        if (this.hamburgerButton) {
            this.hamburgerButton.classList.add('active');
        }
        if (this.desktopMenuButton) {
            this.desktopMenuButton.classList.add('active');
        }
        this.drawer.classList.add('active');
        this.overlay.classList.add('active');
        
        // Lock body scroll
        document.body.style.overflow = 'hidden';
        
        // Animate menu items
        this.animateMenuItems('in');
        
        // Focus management for accessibility
        setTimeout(() => {
            const firstMenuItem = this.drawer.querySelector('.drawer-menu-item');
            if (firstMenuItem) {
                firstMenuItem.focus();
            }
        }, 400);
    }
    
    close() {
        this.isOpen = false;
        if (this.hamburgerButton) {
            this.hamburgerButton.classList.remove('active');
        }
        if (this.desktopMenuButton) {
            this.desktopMenuButton.classList.remove('active');
        }
        this.drawer.classList.remove('active');
        this.overlay.classList.remove('active');
        
        // Unlock body scroll
        document.body.style.overflow = '';
        
        // Animate menu items
        this.animateMenuItems('out');
    }
    
    animateMenuItems(direction) {
        this.menuItems.forEach((item, index) => {
            if (direction === 'in') {
                item.style.transform = 'translateX(-30px)';
                item.style.opacity = '0';
                
                setTimeout(() => {
                    item.style.transition = 'all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1)';
                    item.style.transform = 'translateX(0)';
                    item.style.opacity = '1';
                }, index * 50 + 200); // Stagger animation
                
                // Reset transition after animation
                setTimeout(() => {
                    item.style.transition = '';
                }, index * 50 + 500);
            } else {
                item.style.transform = 'translateX(-30px)';
                item.style.opacity = '0';
                
                // Reset after close animation
                setTimeout(() => {
                    item.style.transform = '';
                    item.style.opacity = '';
                }, 400);
            }
        });
    }
    
    setupScrollLock() {
        // Store original body overflow style
        this.originalOverflow = document.body.style.overflow;
        
        // Handle iOS Safari scroll lock
        let startY = 0;
        
        const preventScroll = (e) => {
            if (this.isOpen) {
                const currentY = e.touches[0].clientY;
                
                if (e.type === 'touchstart') {
                    startY = currentY;
                } else if (e.type === 'touchmove') {
                    // Prevent scrolling unless within the drawer
                    if (!this.drawer.contains(e.target)) {
                        e.preventDefault();
                    }
                }
            }
        };
        
        document.addEventListener('touchstart', preventScroll, { passive: false });
        document.addEventListener('touchmove', preventScroll, { passive: false });
    }
}

// Initialize hamburger menu
function initHamburgerMenu() {
    return new HamburgerMenu();
}

// Export classes and functions for use in other files
window.ChatInterface = ChatInterface;
window.AppointmentBooking = AppointmentBooking;
window.SpotlightCards = SpotlightCards;
window.HamburgerMenu = HamburgerMenu;
window.validateForm = validateForm;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showEmergencyModal = showEmergencyModal;
window.formatDate = formatDate;
window.formatTime = formatTime;
window.initPillNavigation = initPillNavigation;
window.initSpotlightCards = initSpotlightCards;
window.initBokehEffect = initBokehEffect;
window.initHamburgerMenu = initHamburgerMenu;
