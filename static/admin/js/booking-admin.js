/* Mental Health Platform - Enhanced Admin JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Booking Admin Enhanced - Loading...');
    
    // Initialize enhanced admin features
    initializeQuickActions();
    initializeStatusUpdates();
    initializeNotifications();
    initializeTooltips();
    initializeDashboardStats();
    initializeResponsiveFeatures();
    
    console.log('✅ Booking Admin Enhanced - Loaded successfully!');
});

/**
 * Initialize quick action buttons and hover effects
 */
function initializeQuickActions() {
    // Add hover effects to quick action buttons
    const quickActionButtons = document.querySelectorAll('.admin-quick-action');
    
    quickActionButtons.forEach(button => {
        // Add loading state on click
        button.addEventListener('click', function(e) {
            if (this.tagName.toLowerCase() === 'button') {
                showLoadingState(this);
            }
        });
        
        // Add tooltip on hover
        button.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        button.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
    
    // Add smooth transitions to table rows
    const tableRows = document.querySelectorAll('.results tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            this.style.zIndex = '10';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
            this.style.zIndex = '1';
        });
    });
}

/**
 * Handle status updates for appointments and slots
 */
function initializeStatusUpdates() {
    // Make updateStatus function globally available
    window.updateStatus = function(appointmentId, newStatus) {
        const button = event.target;
        showLoadingState(button);
        
        // Simulate API call (replace with actual AJAX call)
        setTimeout(() => {
            // Update the status badge
            const row = button.closest('tr');
            const statusCell = row.querySelector('.field-get_status_badge');
            
            if (statusCell) {
                updateStatusBadge(statusCell, newStatus);
            }
            
            // Update quick actions
            updateQuickActionsForStatus(row, newStatus);
            
            // Show success notification
            showNotification(`Appointment ${newStatus} successfully!`, 'success');
            
            hideLoadingState(button);
        }, 1000);
    };
    
    // Make updateSlotStatus function globally available
    window.updateSlotStatus = function(slotId, isBooked) {
        const button = event.target;
        showLoadingState(button);
        
        setTimeout(() => {
            const row = button.closest('tr');
            const statusCell = row.querySelector('.field-get_booking_status');
            
            if (statusCell) {
                updateSlotStatusBadge(statusCell, isBooked);
            }
            
            updateSlotQuickActions(row, isBooked);
            
            const statusText = isBooked ? 'booked' : 'available';
            showNotification(`Slot marked as ${statusText} successfully!`, 'success');
            
            hideLoadingState(button);
        }, 800);
    };
}

/**
 * Update status badge appearance
 */
function updateStatusBadge(statusCell, newStatus) {
    const statusConfig = {
        'confirmed': {color: '#5cb85c', icon: '✅', label: 'CONFIRMED'},
        'pending': {color: '#f0ad4e', icon: '⏳', label: 'PENDING'},
        'cancelled': {color: '#d9534f', icon: '❌', label: 'CANCELLED'},
        'completed': {color: '#5bc0de', icon: '✨', label: 'COMPLETED'}
    };
    
    const config = statusConfig[newStatus];
    if (config) {
        statusCell.innerHTML = `
            <span data-status="${newStatus}" style="background: ${config.color}; color: white; padding: 4px 8px; border-radius: 12px; 
            font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);">${config.icon} ${config.label}</span>
        `;
        
        // Add animation effect
        const badge = statusCell.querySelector('span');
        badge.style.transform = 'scale(1.2)';
        setTimeout(() => {
            badge.style.transform = 'scale(1)';
        }, 200);
    }
}

/**
 * Update slot status badge
 */
function updateSlotStatusBadge(statusCell, isBooked) {
    const html = isBooked 
        ? '<span style="background: #d9534f; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">🔴 BOOKED</span>'
        : '<span style="background: #5cb85c; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">🟢 AVAILABLE</span>';
    
    statusCell.innerHTML = html;
    
    // Add animation effect
    const badge = statusCell.querySelector('span');
    badge.style.transform = 'scale(1.2)';
    setTimeout(() => {
        badge.style.transform = 'scale(1)';
    }, 200);
}

/**
 * Update quick actions based on status
 */
function updateQuickActionsForStatus(row, newStatus) {
    const actionsCell = row.querySelector('.field-get_quick_actions');
    if (!actionsCell) return;
    
    // This would need to be implemented based on the specific appointment ID
    // For now, just add a visual indicator that actions have been updated
    const actionsContainer = actionsCell.querySelector('div');
    if (actionsContainer) {
        actionsContainer.style.opacity = '0.5';
        setTimeout(() => {
            actionsContainer.style.opacity = '1';
        }, 500);
    }
}

/**
 * Update slot quick actions
 */
function updateSlotQuickActions(row, isBooked) {
    const actionsCell = row.querySelector('.field-get_quick_actions');
    if (!actionsCell) return;
    
    const actionsContainer = actionsCell.querySelector('div');
    if (actionsContainer) {
        actionsContainer.style.opacity = '0.5';
        setTimeout(() => {
            actionsContainer.style.opacity = '1';
        }, 500);
    }
}

/**
 * Show loading state on buttons
 */
function showLoadingState(button) {
    button.disabled = true;
    button.originalText = button.textContent;
    button.innerHTML = '<span class="loading-spinner" style="width: 12px; height: 12px; border: 1px solid #fff; border-top: 1px solid transparent; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block;"></span>';
}

/**
 * Hide loading state on buttons
 */
function hideLoadingState(button) {
    button.disabled = false;
    button.innerHTML = button.originalText;
}

/**
 * Initialize notification system
 */
function initializeNotifications() {
    // Create notifications container if it doesn't exist
    if (!document.querySelector('.admin-notifications')) {
        const notificationsContainer = document.createElement('div');
        notificationsContainer.className = 'admin-notifications';
        document.body.appendChild(notificationsContainer);
    }
    
    // Check for upcoming appointments and show alerts
    checkUpcomingAppointments();
    
    // Set interval to check for new notifications every 5 minutes
    setInterval(checkUpcomingAppointments, 5 * 60 * 1000);
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const container = document.querySelector('.admin-notifications');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `admin-notification ${type}`;
    notification.innerHTML = `
        <div style="display: flex; justify-content: between; align-items: center;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: #666; cursor: pointer; margin-left: 10px;">×</button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Check for upcoming appointments
 */
function checkUpcomingAppointments() {
    // This would typically make an AJAX call to check for upcoming appointments
    // For now, we'll simulate with a random check
    if (Math.random() > 0.8) {
        const count = Math.floor(Math.random() * 5) + 1;
        showNotification(
            `📅 You have ${count} appointment${count > 1 ? 's' : ''} in the next 24 hours`, 
            'warning'
        );
    }
}

/**
 * Initialize tooltip system
 */
function initializeTooltips() {
    window.showTooltip = function(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'admin-tooltip';
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 11px;
            z-index: 1000;
            white-space: nowrap;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            pointer-events: none;
        `;
        
        // Set tooltip content based on button type
        let content = '';
        if (element.textContent.includes('Edit')) {
            content = 'Edit this record';
        } else if (element.textContent.includes('Confirm')) {
            content = 'Confirm this appointment';
        } else if (element.textContent.includes('Cancel')) {
            content = 'Cancel this appointment';
        } else if (element.textContent.includes('Complete')) {
            content = 'Mark as completed';
        } else if (element.textContent.includes('Appointments')) {
            content = 'View all appointments';
        } else if (element.textContent.includes('Slots')) {
            content = 'Manage time slots';
        }
        
        tooltip.textContent = content;
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        
        setTimeout(() => tooltip.remove(), 2000);
    };
    
    window.hideTooltip = function() {
        const existingTooltip = document.querySelector('.admin-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }
    };
}

/**
 * Initialize dashboard statistics
 */
function initializeDashboardStats() {
    // Add dashboard stats to the main admin page
    if (document.body.classList.contains('dashboard')) {
        addDashboardStats();
    }
    
    // Update counters with animations
    animateCounters();
}

/**
 * Add dashboard statistics cards
 */
function addDashboardStats() {
    const dashboardContent = document.querySelector('#content-main');
    if (!dashboardContent) return;
    
    const statsHTML = `
        <div class="dashboard-stats">
            <div class="stat-card appointments-today">
                <h3 id="today-count">0</h3>
                <p>Appointments Today</p>
            </div>
            <div class="stat-card pending-appointments">
                <h3 id="pending-count">0</h3>
                <p>Pending Appointments</p>
            </div>
            <div class="stat-card total-counselors">
                <h3 id="counselor-count">0</h3>
                <p>Active Counselors</p>
            </div>
            <div class="stat-card cancelled-appointments">
                <h3 id="cancelled-count">0</h3>
                <p>Cancelled This Week</p>
            </div>
        </div>
    `;
    
    dashboardContent.insertAdjacentHTML('afterbegin', statsHTML);
    
    // Simulate loading stats data
    setTimeout(() => {
        document.getElementById('today-count').textContent = Math.floor(Math.random() * 15) + 5;
        document.getElementById('pending-count').textContent = Math.floor(Math.random() * 8) + 2;
        document.getElementById('counselor-count').textContent = Math.floor(Math.random() * 12) + 6;
        document.getElementById('cancelled-count').textContent = Math.floor(Math.random() * 5) + 1;
        
        animateCounters();
    }, 500);
}

/**
 * Animate counter numbers
 */
function animateCounters() {
    const counters = document.querySelectorAll('.stat-card h3');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        let current = 0;
        const increment = target / 50;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}

/**
 * Initialize responsive features for mobile
 */
function initializeResponsiveFeatures() {
    // Handle mobile table scrolling
    const results = document.querySelector('.results');
    if (results) {
        let isScrolling = false;
        
        results.addEventListener('scroll', () => {
            if (!isScrolling) {
                results.style.boxShadow = 'inset 5px 0 10px -5px rgba(0,0,0,0.2)';
                isScrolling = true;
            }
        });
        
        results.addEventListener('scrollend', () => {
            results.style.boxShadow = 'none';
            isScrolling = false;
        });
    }
    
    // Add touch feedback for mobile devices
    if ('ontouchstart' in window) {
        const touchElements = document.querySelectorAll('.admin-quick-action, .results tbody tr');
        
        touchElements.forEach(element => {
            element.addEventListener('touchstart', function() {
                this.style.backgroundColor = 'rgba(44, 90, 160, 0.1)';
            });
            
            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.backgroundColor = '';
                }, 150);
            });
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', debounce(() => {
        adjustMobileLayout();
    }, 250));
    
    adjustMobileLayout();
}

/**
 * Adjust layout for mobile screens
 */
function adjustMobileLayout() {
    const isMobile = window.innerWidth <= 768;
    
    if (isMobile) {
        // Make tables horizontally scrollable
        const results = document.querySelectorAll('.results');
        results.forEach(result => {
            result.style.overflowX = 'auto';
            result.style.webkitOverflowScrolling = 'touch';
        });
        
        // Adjust button sizes
        const buttons = document.querySelectorAll('.admin-quick-action');
        buttons.forEach(button => {
            button.style.padding = '8px 12px';
            button.style.fontSize = '11px';
        });
    }
}

/**
 * Debounce function for performance
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Accessibility enhancements
 */
function initializeAccessibility() {
    // Add keyboard navigation for quick actions
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'a':
                    // Ctrl/Cmd + A for Add Appointment
                    if (document.querySelector('.addlink')) {
                        e.preventDefault();
                        document.querySelector('.addlink').click();
                    }
                    break;
                case 'f':
                    // Ctrl/Cmd + F for Filter
                    if (document.querySelector('#searchbar')) {
                        e.preventDefault();
                        document.querySelector('#searchbar').focus();
                    }
                    break;
            }
        }
    });
    
    // Add ARIA labels to buttons
    const quickActionButtons = document.querySelectorAll('.admin-quick-action');
    quickActionButtons.forEach(button => {
        if (!button.getAttribute('aria-label')) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
    });
}

// Initialize accessibility features
document.addEventListener('DOMContentLoaded', initializeAccessibility);

/**
 * Export functions for testing
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        updateStatus,
        updateSlotStatus,
        showNotification,
        showTooltip,
        hideTooltip
    };
}