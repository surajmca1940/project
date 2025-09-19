// Enhanced Booking System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize booking system
    const bookingSystem = {
        currentStep: 1,
        totalSteps: 4,
        selectedCounselor: null,
        selectedDate: null,
        selectedTime: null,
        sessionDuration: '50min',
        sessionType: 'video',
        formData: {}
    };
    
    // Success/Error message functions
    function showSuccessMessage(message) {
        showMessage(message, 'success');
    }
    
    function showErrorMessage(message) {
        showMessage(message, 'error');
    }
    
    function showMessage(message, type) {
        // Remove existing messages
        document.querySelectorAll('.booking-message').forEach(msg => msg.remove());
        
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.className = `booking-message alert alert-${type === 'success' ? 'success' : 'danger'}`;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideInRight 0.3s ease-out;
            max-width: 300px;
        `;
        messageEl.innerHTML = `
            <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(messageEl);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            messageEl.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => messageEl.remove(), 300);
        }, 3000);
    }

    // Step navigation
    function updateProgressBar() {
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach((step, index) => {
            const stepNumber = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNumber < bookingSystem.currentStep) {
                step.classList.add('completed');
                step.querySelector('.progress-circle').innerHTML = '✓';
            } else if (stepNumber === bookingSystem.currentStep) {
                step.classList.add('active');
                step.querySelector('.progress-circle').innerHTML = stepNumber;
            } else {
                step.querySelector('.progress-circle').innerHTML = stepNumber;
            }
        });
    }

    function showStep(stepNumber) {
        console.log('Showing step:', stepNumber);
        
        // Hide all steps
        document.querySelectorAll('.booking-step').forEach(step => {
            step.style.display = 'none';
            step.style.opacity = '0';
        });
        
        // Show current step
        const currentStepElement = document.querySelector(`#step-${stepNumber}`);
        if (currentStepElement) {
            currentStepElement.style.display = 'block';
            // Add smooth transition
            setTimeout(() => {
                currentStepElement.style.opacity = '1';
            }, 50);
        } else {
            console.error(`Step element #step-${stepNumber} not found`);
        }
        
        bookingSystem.currentStep = stepNumber;
        updateProgressBar();
        updateNavigationButtons();
        
        // If step 4, populate confirmation details
        if (stepNumber === 4) {
            populateConfirmationDetails();
        }
    }
    
    // Populate confirmation details in step 4
    function populateConfirmationDetails() {
        console.log('Populating confirmation details');
        
        try {
            // Update counselor information
            if (bookingSystem.selectedCounselor) {
                const counselorImg = document.getElementById('confirm-counselor-img');
                const counselorName = document.getElementById('confirm-counselor-name');
                const counselorTitle = document.getElementById('confirm-counselor-title');
                
                if (counselorImg) counselorImg.src = bookingSystem.selectedCounselor.avatar;
                if (counselorName) counselorName.textContent = bookingSystem.selectedCounselor.name;
                if (counselorTitle) counselorTitle.textContent = bookingSystem.selectedCounselor.title;
            }
            
            // Update date and time
            const confirmDate = document.getElementById('confirm-full-date');
            const confirmTime = document.getElementById('confirm-full-time');
            const confirmSessionType = document.getElementById('confirm-session-type');
            
            if (confirmDate && bookingSystem.selectedDate) {
                const dateObj = new Date(bookingSystem.selectedDate);
                confirmDate.textContent = dateObj.toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
            
            if (confirmTime && bookingSystem.selectedTime) {
                confirmTime.textContent = `${bookingSystem.selectedTime} (${bookingSystem.sessionDuration})`;
            }
            
            if (confirmSessionType) {
                const sessionTypes = {
                    'video': 'Video Session',
                    'phone': 'Phone Call',
                    'in-person': 'In-Person Meeting'
                };
                confirmSessionType.textContent = sessionTypes[bookingSystem.sessionType] || 'Video Session';
            }
            
            console.log('Confirmation details populated successfully');
            
        } catch (error) {
            console.error('Error populating confirmation details:', error);
        }

    function updateNavigationButtons() {
        const prevBtn = document.querySelector('.btn-prev');
        const nextBtn = document.querySelector('.btn-next');
        const confirmBtn = document.querySelector('.btn-confirm');
        
        console.log('Updating navigation buttons for step:', bookingSystem.currentStep);
        
        if (prevBtn) {
            if (bookingSystem.currentStep === 1) {
                prevBtn.style.display = 'none';
            } else {
                prevBtn.style.display = 'inline-flex';
                prevBtn.disabled = false;
            }
        } else {
            console.warn('Previous button not found');
        }
        
        if (nextBtn) {
            if (bookingSystem.currentStep === 4) {
                nextBtn.style.display = 'none';
            } else {
                nextBtn.style.display = 'inline-flex';
                const isValid = isStepValid(bookingSystem.currentStep);
                nextBtn.disabled = !isValid;
                nextBtn.style.opacity = isValid ? '1' : '0.5';
                nextBtn.style.cursor = isValid ? 'pointer' : 'not-allowed';
            }
        } else {
            console.warn('Next button not found');
        }
        
        if (confirmBtn) {
            if (bookingSystem.currentStep === 4) {
                confirmBtn.style.display = 'inline-flex';
                confirmBtn.disabled = false;
                confirmBtn.style.opacity = '1';
                confirmBtn.style.cursor = 'pointer';
                console.log('Confirm button is now visible and enabled');
            } else {
                confirmBtn.style.display = 'none';
            }
        } else {
            console.error('❌ CRITICAL: Confirm button (.btn-confirm) not found in DOM!');
            // Try to find any button with confirm text
            const allButtons = document.querySelectorAll('button');
            console.log('All buttons found:', Array.from(allButtons).map(btn => btn.textContent.trim()));
        }
    }

    function isStepValid(stepNumber) {
        switch (stepNumber) {
            case 1:
                const counselorValid = bookingSystem.selectedCounselor !== null;
                updateStepIndicator(1, counselorValid, counselorValid ? '✓ Counselor selected' : 'Please select a counselor');
                return counselorValid;
            case 2:
                const dateValid = bookingSystem.selectedDate !== null;
                const timeValid = bookingSystem.selectedTime !== null;
                const step2Valid = dateValid && timeValid;
                let message = '';
                if (!dateValid && !timeValid) message = 'Please select date and time';
                else if (!dateValid) message = 'Please select a date';
                else if (!timeValid) message = 'Please select a time';
                else message = '✓ Date and time selected';
                updateStepIndicator(2, step2Valid, message);
                return step2Valid;
            case 3:
                updateStepIndicator(3, true, '✓ Ready to confirm');
                return true; // Always valid as fields are optional
            case 4:
                const allValid = bookingSystem.selectedCounselor && bookingSystem.selectedDate && bookingSystem.selectedTime;
                updateStepIndicator(4, allValid, allValid ? '✓ Ready to book' : 'Missing required information');
                return allValid;
            default:
                return false;
        }
    }
    
    function updateStepIndicator(stepNumber, isValid, message) {
        const stepElement = document.querySelector(`[data-step="${stepNumber}"]`);
        if (stepElement) {
            const existingIndicator = stepElement.querySelector('.step-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            if (bookingSystem.currentStep === stepNumber) {
                const indicator = document.createElement('div');
                indicator.className = `step-indicator ${isValid ? 'valid' : 'invalid'}`;
                indicator.style.cssText = `
                    position: absolute;
                    top: -8px;
                    right: -8px;
                    background: ${isValid ? '#10b981' : '#ef4444'};
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    font-size: 11px;
                    font-weight: 500;
                    white-space: nowrap;
                    z-index: 10;
                    animation: fadeIn 0.3s ease;
                `;
                indicator.textContent = message;
                stepElement.style.position = 'relative';
                stepElement.appendChild(indicator);
            }
        }
    }

    // Counselor selection
    function initializeCounselorSelection() {
        const counselorCards = document.querySelectorAll('.counselor-card');
        console.log('Found counselor cards:', counselorCards.length);
        counselorCards.forEach(card => {
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                try {
                    // Remove previous selection
                    counselorCards.forEach(c => c.classList.remove('selected'));
                    
                    // Select current card
                    this.classList.add('selected');
                    
                    // Add visual feedback
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                    
                    // Store selection with better error handling
                    const nameElement = this.querySelector('.counselor-info h6');
                    const titleElement = this.querySelector('.counselor-title');
                    const avatarElement = this.querySelector('.avatar-img');
                    
                    if (nameElement && titleElement && avatarElement) {
                        bookingSystem.selectedCounselor = {
                            id: this.dataset.counselorId || 'unknown',
                            name: nameElement.textContent.trim(),
                            title: titleElement.textContent.trim(),
                            avatar: avatarElement.src
                        };
                        
                        console.log('Counselor selected:', bookingSystem.selectedCounselor);
                        
                        updateNavigationButtons();
                        updateSummary();
                        
                        // Show success feedback
                        showSuccessMessage(`${bookingSystem.selectedCounselor.name} selected!`);
                        
                        // Auto-advance after selection (with shorter delay)
                        setTimeout(() => {
                            if (bookingSystem.currentStep === 1) {
                                nextStep();
                            }
                        }, 1200);
                    } else {
                        console.error('Could not find counselor information elements');
                        showErrorMessage('Error selecting counselor. Please try again.');
                    }
                } catch (error) {
                    console.error('Error in counselor selection:', error);
                    showErrorMessage('Error selecting counselor. Please try again.');
                }
            });
        });
    }

    // Calendar functionality
    function initializeCalendar() {
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();
        
        generateCalendar(currentYear, currentMonth);
        
        // Calendar navigation
        const prevMonthBtn = document.querySelector('.prev-month');
        const nextMonthBtn = document.querySelector('.next-month');
        
        if (prevMonthBtn) {
            prevMonthBtn.addEventListener('click', () => {
                const newDate = new Date(currentYear, currentMonth - 1, 1);
                generateCalendar(newDate.getFullYear(), newDate.getMonth());
            });
        }
        
        if (nextMonthBtn) {
            nextMonthBtn.addEventListener('click', () => {
                const newDate = new Date(currentYear, currentMonth + 1, 1);
                generateCalendar(newDate.getFullYear(), newDate.getMonth());
            });
        }
    }

    function generateCalendar(year, month) {
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        const monthHeader = document.querySelector('.current-month');
        if (monthHeader) {
            monthHeader.textContent = `${monthNames[month]} ${year}`;
        }
        
        // Generate calendar days
        const calendarGrid = document.getElementById('calendar-grid');
        if (calendarGrid) {
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const today = new Date();
            
            let calendarHTML = '<div class="calendar-days">';
            calendarHTML += '<div class="day-header">Sun</div><div class="day-header">Mon</div><div class="day-header">Tue</div><div class="day-header">Wed</div><div class="day-header">Thu</div><div class="day-header">Fri</div><div class="day-header">Sat</div>';
            
            // Add empty cells for days before the first day of the month
            for (let i = 0; i < firstDay.getDay(); i++) {
                calendarHTML += '<div class="calendar-day empty"></div>';
            }
            
            // Add days of the month
            for (let day = 1; day <= lastDay.getDate(); day++) {
                const currentDate = new Date(year, month, day);
                const isPast = currentDate < today.setHours(0,0,0,0);
                const isToday = currentDate.toDateString() === new Date().toDateString();
                
                let classes = 'calendar-day';
                if (isPast) classes += ' past';
                if (isToday) classes += ' today';
                
                calendarHTML += `<div class="${classes}" data-date="${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}">${day}</div>`;
            }
            
            calendarHTML += '</div>';
            calendarGrid.innerHTML = calendarHTML;
            
            // Add click handlers to calendar days
            calendarGrid.querySelectorAll('.calendar-day:not(.past):not(.empty)').forEach(day => {
                day.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    try {
                        // Remove previous selection
                        calendarGrid.querySelectorAll('.calendar-day.selected').forEach(d => d.classList.remove('selected'));
                        
                        // Select current day
                        this.classList.add('selected');
                        
                        // Add visual feedback
                        this.style.transform = 'scale(0.9)';
                        setTimeout(() => {
                            this.style.transform = '';
                        }, 150);
                        
                        // Store selection
                        if (this.dataset.date) {
                            bookingSystem.selectedDate = this.dataset.date;
                            const dateObj = new Date(this.dataset.date);
                            const formattedDate = dateObj.toLocaleDateString('en-US', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            });
                            
                            console.log('Date selected:', bookingSystem.selectedDate);
                            
                            updateNavigationButtons();
                            updateSummary();
                            
                            showSuccessMessage(`${formattedDate} selected!`);
                        } else {
                            console.error('No date data found on calendar day');
                            showErrorMessage('Error selecting date. Please try again.');
                        }
                    } catch (error) {
                        console.error('Error in date selection:', error);
                        showErrorMessage('Error selecting date. Please try again.');
                    }
                });
            });
        }
    }

    // Time slot selection
    function initializeTimeSlots() {
        const timeSlots = document.querySelectorAll('.time-slot');
        console.log('Found time slots:', timeSlots.length);
        timeSlots.forEach(slot => {
            if (!slot.classList.contains('booked')) {
                slot.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    try {
                        // Remove previous selection
                        timeSlots.forEach(s => s.classList.remove('selected'));
                        
                        // Select current slot
                        this.classList.add('selected');
                        
                        // Add visual feedback
                        this.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            this.style.transform = '';
                        }, 150);
                        
                        // Store selection
                        const timeElement = this.querySelector('.time');
                        if (timeElement) {
                            bookingSystem.selectedTime = timeElement.textContent.trim();
                            console.log('Time slot selected:', bookingSystem.selectedTime);
                            
                            updateNavigationButtons();
                            updateSummary();
                            
                            showSuccessMessage(`${bookingSystem.selectedTime} selected!`);
                        } else {
                            console.error('Could not find time element');
                            showErrorMessage('Error selecting time. Please try again.');
                        }
                    } catch (error) {
                        console.error('Error in time slot selection:', error);
                        showErrorMessage('Error selecting time. Please try again.');
                    }
                });
            } else {
                // Make booked slots clearly non-interactive
                slot.style.cursor = 'not-allowed';
                slot.title = 'This time slot is not available';
            }
        });
        
        // Session duration selection
        const durationInputs = document.querySelectorAll('input[name="duration"]');
        durationInputs.forEach(input => {
            input.addEventListener('change', function() {
                bookingSystem.sessionDuration = this.value;
                updateSummary();
            });
        });
        
        // Session type selection
        const typeInputs = document.querySelectorAll('input[name="session-type"]');
        typeInputs.forEach(input => {
            input.addEventListener('change', function() {
                bookingSystem.sessionType = this.value;
                updateSummary();
            });
        });
    }

    // Form handling
    function initializeFormHandling() {
        // Concern tags
        const concernTags = document.querySelectorAll('.concern-tag input');
        concernTags.forEach(input => {
            input.addEventListener('change', function() {
                const tag = this.parentElement;
                if (this.checked) {
                    tag.classList.add('selected');
                } else {
                    tag.classList.remove('selected');
                }
            });
        });
        
        // Privacy options
        const privacyOptions = document.querySelectorAll('.privacy-option input');
        privacyOptions.forEach(input => {
            input.addEventListener('change', function() {
                bookingSystem.formData.privacy = this.value;
            });
        });
        
        // Additional notes
        const notesTextarea = document.querySelector('#additional-notes');
        if (notesTextarea) {
            notesTextarea.addEventListener('input', function() {
                bookingSystem.formData.notes = this.value;
            });
        }
    }

    // Summary updates
    function updateSummary() {
        const summary = document.querySelector('.appointment-summary');
        if (!summary) return;
        
        let summaryHTML = '<h6 class="mb-3">Appointment Summary</h6>';
        
        if (bookingSystem.selectedCounselor) {
            summaryHTML += `
                <div class="summary-item">
                    <span class="label">Counselor</span>
                    <span class="value">${bookingSystem.selectedCounselor.name}</span>
                </div>
            `;
        }
        
        if (bookingSystem.selectedDate) {
            summaryHTML += `
                <div class="summary-item">
                    <span class="label">Date</span>
                    <span class="value">${bookingSystem.selectedDate}</span>
                </div>
            `;
        }
        
        if (bookingSystem.selectedTime) {
            summaryHTML += `
                <div class="summary-item">
                    <span class="label">Time</span>
                    <span class="value">${bookingSystem.selectedTime}</span>
                </div>
            `;
        }
        
        summaryHTML += `
            <div class="summary-item">
                <span class="label">Duration</span>
                <span class="value">${bookingSystem.sessionDuration}</span>
            </div>
            <div class="summary-item">
                <span class="label">Type</span>
                <span class="value">${bookingSystem.sessionType}</span>
            </div>
        `;
        
        summary.innerHTML = summaryHTML;
    }

    // Navigation functions
    function nextStep() {
        if (bookingSystem.currentStep < bookingSystem.totalSteps && isStepValid(bookingSystem.currentStep)) {
            showStep(bookingSystem.currentStep + 1);
        }
    }

    function prevStep() {
        if (bookingSystem.currentStep > 1) {
            showStep(bookingSystem.currentStep - 1);
        }
    }

    // Event listeners for navigation buttons
    function initializeNavigation() {
        const nextBtn = document.querySelector('.btn-next');
        const prevBtn = document.querySelector('.btn-prev');
        const confirmBtn = document.querySelector('.btn-confirm');
        
        console.log('Initializing navigation buttons:', {
            next: !!nextBtn,
            prev: !!prevBtn,
            confirm: !!confirmBtn
        });
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Next button clicked');
                
                if (!nextBtn.disabled) {
                    nextStep();
                } else {
                    // Show validation message
                    const stepName = [
                        '', 'select a counselor', 'choose a date and time', 'fill in details', 'confirm'
                    ][bookingSystem.currentStep];
                    showErrorMessage(`Please ${stepName} to continue.`);
                }
            });
        } else {
            console.error('Next button not found in DOM');
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Previous button clicked');
                prevStep();
            });
        } else {
            console.error('Previous button not found in DOM');
        }
        
        if (confirmBtn) {
            // Remove any existing event listeners
            confirmBtn.replaceWith(confirmBtn.cloneNode(true));
            const newConfirmBtn = document.querySelector('.btn-confirm');
            
            newConfirmBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('✅ Confirm button clicked successfully!');
                
                if (!newConfirmBtn.disabled && !newConfirmBtn.classList.contains('loading')) {
                    console.log('Starting booking confirmation process...');
                    confirmBooking();
                } else {
                    console.log('Confirm button is disabled or loading');
                    showErrorMessage('Please wait while we process your request.');
                }
            });
            
            // Also add the edit booking button handler
            const editBtn = document.getElementById('edit-booking');
            if (editBtn) {
                editBtn.addEventListener('click', function(e) {
                    e.preventDefault();
                    console.log('Edit booking clicked - returning to step 1');
                    showStep(1);
                    showSuccessMessage('You can now edit your booking details.');
                });
            }
            
            console.log('Confirm button event listener attached successfully');
        } else {
            console.error('❌ CRITICAL: Confirm button not found when setting up navigation!');
        }
    }

    // Booking confirmation
    function confirmBooking() {
        try {
            // Show loading state
            const confirmBtn = document.querySelector('.btn-confirm');
            if (confirmBtn) {
                confirmBtn.classList.add('loading');
                confirmBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Confirming...';
                confirmBtn.disabled = true;
            }
            
            // Disable all form elements during confirmation
            document.querySelectorAll('input, button, textarea').forEach(el => {
                if (!el.classList.contains('btn-confirm')) {
                    el.disabled = true;
                }
            });
            
            console.log('Starting booking confirmation...');
            console.log('Booking details:', bookingSystem);
            
            // Show progress message
            showSuccessMessage('Processing your appointment...');
            
            // Simulate API call with realistic delay
            setTimeout(() => {
                console.log('Booking confirmed successfully');
                showConfirmationPage();
            }, 2500);
            
        } catch (error) {
            console.error('Error confirming booking:', error);
            showErrorMessage('Failed to confirm booking. Please try again.');
            
            // Re-enable form elements
            document.querySelectorAll('input, button, textarea').forEach(el => {
                el.disabled = false;
            });
            
            const confirmBtn = document.querySelector('.btn-confirm');
            if (confirmBtn) {
                confirmBtn.classList.remove('loading');
                confirmBtn.innerHTML = '<i class="bi bi-check-circle"></i> Confirm Booking';
                confirmBtn.disabled = false;
            }
        }
    }

    function showConfirmationPage() {
        console.log('✅ Showing confirmation page');
        
        try {
            // Hide progress bar
            const progressBar = document.querySelector('.booking-progress');
            if (progressBar) {
                progressBar.style.display = 'none';
            }
            
            // Get the main booking card
            const mainCard = document.querySelector('.booking-main-card');
            if (!mainCard) {
                console.error('Main booking card not found');
                return;
            }
            
            // Format the selected date
            let formattedDate = 'Today';
            if (bookingSystem.selectedDate) {
                const dateObj = new Date(bookingSystem.selectedDate);
                formattedDate = dateObj.toLocaleDateString('en-US', {
                    weekday: 'long',
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
            
            // Create confirmation HTML with Bootstrap icons
            const confirmationHTML = `
                <div class="confirmation-card text-center">
                    <div class="confirmation-header">
                        <div class="mb-4">
                            <i class="bi bi-check-circle-fill" style="font-size: 4rem; color: var(--success-color);"></i>
                        </div>
                        <h2 class="mb-3" style="color: var(--success-color);">Appointment Confirmed!</h2>
                        <p class="text-muted mb-4">Your appointment has been successfully booked. You will receive a confirmation email shortly.</p>
                    </div>
                    
                    <div class="confirmation-details" style="text-align: left; max-width: 500px; margin: 0 auto;">
                        ${bookingSystem.selectedCounselor ? `
                            <div class="detail-row">
                                <i class="bi bi-person-check text-primary"></i>
                                <div class="counselor-preview">
                                    <img src="${bookingSystem.selectedCounselor.avatar}" alt="${bookingSystem.selectedCounselor.name}" class="counselor-thumb">
                                    <div>
                                        <strong>${bookingSystem.selectedCounselor.name}</strong><br>
                                        <small class="text-muted">${bookingSystem.selectedCounselor.title}</small>
                                    </div>
                                </div>
                            </div>
                        ` : ''}
                        
                        <div class="detail-row">
                            <i class="bi bi-calendar3 text-primary"></i>
                            <div>
                                <strong>${formattedDate}</strong><br>
                                <small class="text-muted">${bookingSystem.selectedTime || '10:00 AM'}</small>
                            </div>
                        </div>
                        
                        <div class="detail-row">
                            <i class="bi bi-clock text-primary"></i>
                            <div>
                                <strong>${bookingSystem.sessionDuration} session</strong><br>
                                <small class="text-muted">${bookingSystem.sessionType} session</small>
                            </div>
                        </div>
                        
                        <div class="detail-row">
                            <i class="bi bi-envelope text-primary"></i>
                            <div>
                                <strong>Confirmation sent</strong><br>
                                <small class="text-muted">Check your email for appointment details</small>
                            </div>
                        </div>
                    </div>
                    
                    <div class="confirmation-actions mt-4">
                        <button class="btn btn-outline-primary me-2" onclick="window.print()">
                            <i class="bi bi-printer me-2"></i>Print Confirmation
                        </button>
                        <button class="btn btn-primary" onclick="window.location.href='/'">
                            <i class="bi bi-house me-2"></i>Back to Home
                        </button>
                    </div>
                    
                    <div class="mt-4 p-3" style="background: rgba(16, 185, 129, 0.1); border-radius: 12px; border-left: 4px solid var(--success-color);">
                        <small class="text-success">
                            <i class="bi bi-info-circle me-1"></i>
                            <strong>What's next?</strong> You'll receive a confirmation email with a calendar invite and session details.
                        </small>
                    </div>
                </div>
            `;
            
            // Update the main card content
            mainCard.innerHTML = confirmationHTML;
            mainCard.style.display = 'block';
            
            // Show success message
            showSuccessMessage('✓ Appointment successfully confirmed!');
            
            // Clear the stored booking data
            localStorage.removeItem('bookingFormData');
            
            console.log('Confirmation page displayed successfully');
            
        } catch (error) {
            console.error('Error showing confirmation page:', error);
            showErrorMessage('Error displaying confirmation. Please refresh the page.');
        }
    }

    // Animations and interactions
    function initializeAnimations() {
        // Smooth transitions between steps
        const steps = document.querySelectorAll('.booking-step');
        steps.forEach(step => {
            step.style.transition = 'opacity 0.3s ease-in-out';
        });
        
        // Hover effects for interactive elements
        const interactiveElements = document.querySelectorAll('.counselor-card, .time-slot, .concern-tag');
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            element.addEventListener('mouseleave', function() {
                if (!this.classList.contains('selected')) {
                    this.style.transform = 'translateY(0)';
                }
            });
        });
    }

    // Initialize all components
    function initialize() {
        console.log('🚀 Initializing Enhanced Booking System...');
        
        // Debug: Check DOM elements
        console.log('DOM Check:', {
            step1: !!document.querySelector('#step-1'),
            step2: !!document.querySelector('#step-2'),
            step3: !!document.querySelector('#step-3'),
            step4: !!document.querySelector('#step-4'),
            nextBtn: !!document.querySelector('.btn-next'),
            prevBtn: !!document.querySelector('.btn-prev'),
            confirmBtn: !!document.querySelector('.btn-confirm'),
            counselorCards: document.querySelectorAll('.counselor-card').length,
            timeSlots: document.querySelectorAll('.time-slot').length
        });
        
        updateProgressBar();
        showStep(1);
        initializeCounselorSelection();
        initializeCalendar();
        initializeTimeSlots();
        initializeFormHandling();
        initializeNavigation();
        initializeAnimations();
        updateSummary();
        
        // Add keyboard shortcut for debugging
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'd') {
                e.preventDefault();
                console.log('Debug Info:', {
                    currentStep: bookingSystem.currentStep,
                    selectedCounselor: bookingSystem.selectedCounselor,
                    selectedDate: bookingSystem.selectedDate,
                    selectedTime: bookingSystem.selectedTime,
                    sessionDuration: bookingSystem.sessionDuration,
                    sessionType: bookingSystem.sessionType,
                    stepValid: isStepValid(bookingSystem.currentStep)
                });
            }
            
            // Quick jump to step 4 for testing (Ctrl+4)
            if (e.ctrlKey && e.key === '4') {
                e.preventDefault();
                console.log('Quick jump to step 4 for testing');
                // Set dummy data for testing
                bookingSystem.selectedCounselor = {
                    id: 'test',
                    name: 'Test Counselor',
                    title: 'Test Therapist',
                    avatar: 'https://via.placeholder.com/60'
                };
                bookingSystem.selectedDate = '2023-12-01';
                bookingSystem.selectedTime = '2:00 PM';
                showStep(4);
                showSuccessMessage('Jumped to Step 4 for testing (Ctrl+4)');
            }
        });
        
        console.log('✅ Booking System Initialization Complete!');
    }

    // Start the booking system
    initialize();
    
    // Log successful initialization
    console.log('Enhanced booking system initialized successfully!');
    console.log('Current step:', bookingSystem.currentStep);
    console.log('Total steps:', bookingSystem.totalSteps);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' && bookingSystem.currentStep > 1) {
            prevStep();
        } else if (e.key === 'ArrowRight' && bookingSystem.currentStep < bookingSystem.totalSteps && isStepValid(bookingSystem.currentStep)) {
            nextStep();
        }
    });

    // Auto-save form data
    setInterval(() => {
        localStorage.setItem('bookingFormData', JSON.stringify(bookingSystem));
    }, 30000); // Save every 30 seconds

    // Load saved data on page load
    const savedData = localStorage.getItem('bookingFormData');
    if (savedData) {
        try {
            const parsed = JSON.parse(savedData);
            Object.assign(bookingSystem, parsed);
        } catch (e) {
            console.log('Could not load saved booking data');
        }
    }
});