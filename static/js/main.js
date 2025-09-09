// Main JavaScript file for the Mental Health Platform

document.addEventListener('DOMContentLoaded', function() {
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

// Export classes and functions for use in other files
window.ChatInterface = ChatInterface;
window.AppointmentBooking = AppointmentBooking;
window.validateForm = validateForm;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showEmergencyModal = showEmergencyModal;
window.formatDate = formatDate;
window.formatTime = formatTime;
