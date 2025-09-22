// Enhanced Booking System with All Features
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Enhanced Booking System Loading...');
    
    // Booking System State
    const BookingSystem = {
        currentStep: 1,
        totalSteps: 4,
        selectedCounselor: null,
        selectedDate: null,
        selectedTime: null,
        selectedDuration: '50',
        selectedType: 'video',
        selectedConcerns: [],
        additionalNotes: '',
        privacyPreference: 'named',
        timeFilter: 'all'
    };
    
    // Initialize all components
    function initializeBookingSystem() {
        console.log('Initializing Enhanced Booking System...');
        
        // Initialize in proper order
        initializeAnimations();
        initializeCounselorSelection();
        initializeCalendar();
        initializeTimeSlots();
        initializeFormHandling();
        initializeMobileNavigation();
        
        // Initialize navigation last to ensure all elements exist
        initializeStepNavigation();
        
        // Show initial step and update UI
        showStep(1);
        updateStepperUI();
        
        // Debug: Check if buttons exist
        console.log('🔍 Debug - Navigation buttons:', {
            nextBtn: !!document.querySelector('.btn-next'),
            prevBtn: !!document.querySelector('.btn-previous'),
            confirmBtn: !!document.querySelector('.btn-confirm-desktop')
        });
        
        console.log('✅ Enhanced Booking System Initialized');
    }
    
    // Step Navigation Functions
    function showStep(stepNumber) {
        console.log(`Transitioning to step ${stepNumber}`);
        
        // Hide all steps with fade out
        document.querySelectorAll('.booking-step').forEach(step => {
            step.classList.remove('active');
            step.style.opacity = '0';
            step.style.transform = 'translateX(-20px)';
        });
        
        // Show target step with fade in
        setTimeout(() => {
            const targetStep = document.getElementById(`step-${stepNumber}`);
            if (targetStep) {
                targetStep.classList.add('active');
                targetStep.style.opacity = '1';
                targetStep.style.transform = 'translateX(0)';
                
                // Scroll to top smoothly
                targetStep.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
            
            BookingSystem.currentStep = stepNumber;
            updateStepperUI();
            updateNavigationButtons();
            updateMobileNavigation();
            
            // Special handling for confirmation step
            if (stepNumber === 4) {
                populateConfirmationDetails();
            }
        }, 300);
    }
    
    function nextStep() {
        console.log(`🔍 nextStep called - Current step: ${BookingSystem.currentStep}`);
        
        // Check if we're already at the last step
        if (BookingSystem.currentStep >= BookingSystem.totalSteps) {
            console.log('⚠️ Already at the last step');
            return;
        }
        
        // Validate current step
        const isValid = validateCurrentStep();
        console.log(`✅ Step ${BookingSystem.currentStep} validation:`, isValid);
        
        if (isValid) {
            const nextStepNum = BookingSystem.currentStep + 1;
            console.log(`➡️ Moving to step ${nextStepNum}`);
            showStep(nextStepNum);
            playStepTransitionSound();
        } else {
            console.log('❌ Validation failed, showing validation message');
            showValidationMessage();
        }
    }
    
    function prevStep() {
        if (BookingSystem.currentStep > 1) {
            showStep(BookingSystem.currentStep - 1);
        }
    }
    
    function validateCurrentStep() {
        console.log(`🔍 Validating step ${BookingSystem.currentStep}`);
        
        switch (BookingSystem.currentStep) {
            case 1:
                const counselorValid = BookingSystem.selectedCounselor !== null;
                console.log(`💼 Counselor selected:`, counselorValid, BookingSystem.selectedCounselor);
                return counselorValid;
            case 2:
                const dateTimeValid = BookingSystem.selectedDate && BookingSystem.selectedTime;
                console.log(`📅 Date/Time selected:`, dateTimeValid, {
                    date: BookingSystem.selectedDate,
                    time: BookingSystem.selectedTime
                });
                return dateTimeValid;
            case 3:
                console.log(`📝 Step 3 (preferences) - always valid`);
                return true; // Optional step
            case 4:
                console.log(`✅ Step 4 (confirmation) - always valid`);
                return true;
            default:
                console.log(`❌ Unknown step: ${BookingSystem.currentStep}`);
                return false;
        }
    }
    
    // Stepper UI Updates
    function updateStepperUI() {
        const stepperItems = document.querySelectorAll('.stepper-item');
        
        stepperItems.forEach((item, index) => {
            const stepNum = index + 1;
            item.classList.remove('active', 'completed');
            
            if (stepNum < BookingSystem.currentStep) {
                item.classList.add('completed');
                // Add checkmark animation
                const counter = item.querySelector('.stepper-counter');
                if (counter) {
                    counter.innerHTML = '<i class="bi bi-check"></i>';
                    counter.classList.add('completed-animation');
                }
            } else if (stepNum === BookingSystem.currentStep) {
                item.classList.add('active');
                const counter = item.querySelector('.stepper-counter');
                if (counter) {
                    const icon = counter.querySelector('i');
                    if (icon) {
                        counter.classList.add('active-pulse');
                    }
                }
            }
        });
    }
    
    // Counselor Selection
    function initializeCounselorSelection() {
        const counselorCards = document.querySelectorAll('.counselor-card');
        
        counselorCards.forEach(card => {
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove previous selections
                counselorCards.forEach(c => c.classList.remove('selected'));
                
                // Select current card
                this.classList.add('selected');
                
                // Extract counselor data
                const counselorData = {
                    id: this.dataset.counselorId,
                    name: this.querySelector('.counselor-name').textContent.trim(),
                    title: this.querySelector('.counselor-title').textContent.trim(),
                    avatar: this.querySelector('.counselor-avatar').src,
                    rating: this.querySelector('.rating-value')?.textContent || '4.8',
                    experience: this.querySelector('.stat-item:nth-child(2) span')?.textContent || '8+ years'
                };
                
                BookingSystem.selectedCounselor = counselorData;
                
                // Animation feedback
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = 'scale(1.02)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 200);
                }, 100);
                
                // Show success message
                showNotification(`${counselorData.name} selected!`, 'success');
                
                // Update summary
                updateAppointmentSummary();
                
                // Auto-advance after delay
                setTimeout(() => {
                    if (BookingSystem.currentStep === 1) {
                        nextStep();
                    }
                }, 1500);
            });
        });
        
        // Select counselor buttons
        document.querySelectorAll('.select-counselor-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                this.closest('.counselor-card').click();
            });
        });
    }
    
    // Enhanced Calendar with Color Coding
    function initializeCalendar() {
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();
        
        generateCalendar(currentYear, currentMonth);
        
        // Navigation buttons
        document.querySelector('.prev-month')?.addEventListener('click', () => {
            const newDate = new Date(currentYear, currentMonth - 1, 1);
            generateCalendar(newDate.getFullYear(), newDate.getMonth());
        });
        
        document.querySelector('.next-month')?.addEventListener('click', () => {
            const newDate = new Date(currentYear, currentMonth + 1, 1);
            generateCalendar(newDate.getFullYear(), newDate.getMonth());
        });
    }
    
    function generateCalendar(year, month) {
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        // Update header
        const monthHeader = document.querySelector('.current-month-year');
        if (monthHeader) {
            monthHeader.textContent = `${monthNames[month]} ${year}`;
        }
        
        // Generate calendar grid
        const calendarGrid = document.getElementById('calendar-grid');
        if (calendarGrid) {
            const firstDay = new Date(year, month, 1);
            const lastDay = new Date(year, month + 1, 0);
            const today = new Date();
            
            let calendarHTML = '<div class="calendar-weekdays">';
            const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            weekdays.forEach(day => {
                calendarHTML += `<div class="weekday">${day}</div>`;
            });
            calendarHTML += '</div><div class="calendar-days">';
            
            // Empty cells for days before month start
            for (let i = 0; i < firstDay.getDay(); i++) {
                calendarHTML += '<div class="calendar-day empty"></div>';
            }
            
            // Days of the month with color coding
            for (let day = 1; day <= lastDay.getDate(); day++) {
                const currentDate = new Date(year, month, day);
                const isPast = currentDate < today.setHours(0,0,0,0);
                const isToday = currentDate.toDateString() === new Date().toDateString();
                
                let classes = 'calendar-day';
                let status = 'available'; // Default status
                
                if (isPast) {
                    classes += ' past';
                    status = 'past';
                } else if (isToday) {
                    classes += ' today';
                } else {
                    // Mock availability status
                    const availability = getDateAvailability(currentDate);
                    classes += ` ${availability}`;
                    status = availability;
                }
                
                const dateStr = `${year}-${(month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
                
                calendarHTML += `
                    <div class="${classes}" 
                         data-date="${dateStr}" 
                         data-status="${status}"
                         title="${getDateTooltip(status)}">
                        <span class="day-number">${day}</span>
                        <div class="availability-indicator"></div>
                    </div>
                `;
            }
            
            calendarHTML += '</div>';
            calendarGrid.innerHTML = calendarHTML;
            
            // Add click handlers
            calendarGrid.querySelectorAll('.calendar-day:not(.past)').forEach(day => {
                day.addEventListener('click', function() {
                    if (this.classList.contains('booked')) return;
                    
                    // Remove previous selection
                    calendarGrid.querySelectorAll('.calendar-day.selected').forEach(d => 
                        d.classList.remove('selected'));
                    
                    // Select current day
                    this.classList.add('selected');
                    
                    // Store selection
                    BookingSystem.selectedDate = this.dataset.date;
                    
                    // Load time slots for this date
                    loadTimeSlotsForDate(this.dataset.date);
                    
                    // Update summary
                    updateAppointmentSummary();
                    
                    // Show success
                    const dateObj = new Date(this.dataset.date);
                    const formattedDate = dateObj.toLocaleDateString('en-US', {
                        weekday: 'long',
                        month: 'long',
                        day: 'numeric'
                    });
                    showNotification(`${formattedDate} selected!`, 'success');
                });
            });
        }
    }
    
    function getDateAvailability(date) {
        // Mock logic for demo - in real app, fetch from server
        const dayOfWeek = date.getDay();
        const dayOfMonth = date.getDate();
        
        if (dayOfWeek === 0 || dayOfWeek === 6) return 'limited'; // Weekends limited
        if (dayOfMonth % 5 === 0) return 'booked'; // Every 5th day booked
        if (dayOfMonth % 3 === 0) return 'limited'; // Every 3rd day limited
        return 'available';
    }
    
    function getDateTooltip(status) {
        switch (status) {
            case 'available': return 'Multiple slots available';
            case 'limited': return 'Limited slots available';
            case 'booked': return 'No slots available';
            case 'past': return 'Past date';
            default: return '';
        }
    }
    
    // Smart Time Filtering
    function initializeTimeSlots() {
        // Time filter buttons
        document.querySelectorAll('.time-filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active from all buttons
                document.querySelectorAll('.time-filter-btn').forEach(b => 
                    b.classList.remove('active'));
                
                // Activate current button
                this.classList.add('active');
                
                // Store filter
                BookingSystem.timeFilter = this.dataset.period;
                
                // Reload time slots with filter
                if (BookingSystem.selectedDate) {
                    loadTimeSlotsForDate(BookingSystem.selectedDate);
                }
            });
        });
        
        // Session preferences
        document.querySelectorAll('input[name="session-duration"]').forEach(input => {
            input.addEventListener('change', function() {
                BookingSystem.selectedDuration = this.value;
                updateAppointmentSummary();
            });
        });
        
        document.querySelectorAll('input[name="session-type"]').forEach(input => {
            input.addEventListener('change', function() {
                BookingSystem.selectedType = this.value;
                updateAppointmentSummary();
            });
        });
    }
    
    function loadTimeSlotsForDate(date) {
        const container = document.getElementById('time-slots-container');
        if (!container) return;
        
        // Show loading
        container.innerHTML = '<div class="loading-spinner">Loading available times...</div>';
        
        // Simulate API call
        setTimeout(() => {
            const slots = generateTimeSlotsForDate(date, BookingSystem.timeFilter);
            renderTimeSlots(slots);
        }, 500);
    }
    
    function generateTimeSlotsForDate(date, filter) {
        const allSlots = {
            morning: [
                { time: '09:00', status: 'available', label: '9:00 AM' },
                { time: '10:00', status: 'available', label: '10:00 AM' },
                { time: '11:00', status: 'limited', label: '11:00 AM' }
            ],
            afternoon: [
                { time: '14:00', status: 'available', label: '2:00 PM' },
                { time: '15:00', status: 'booked', label: '3:00 PM' },
                { time: '16:00', status: 'available', label: '4:00 PM' }
            ],
            evening: [
                { time: '18:00', status: 'available', label: '6:00 PM' },
                { time: '19:00', status: 'available', label: '7:00 PM' }
            ]
        };
        
        if (filter === 'all') {
            return allSlots;
        } else {
            return { [filter]: allSlots[filter] || [] };
        }
    }
    
    function renderTimeSlots(slots) {
        const container = document.getElementById('time-slots-container');
        if (!container) return;
        
        let html = '';
        
        Object.entries(slots).forEach(([period, periodSlots]) => {
            if (periodSlots.length > 0) {
                const periodIcons = {
                    morning: 'bi-sunrise',
                    afternoon: 'bi-sun',
                    evening: 'bi-moon'
                };
                
                html += `
                    <div class="time-period">
                        <h6 class="period-title">
                            <i class="bi ${periodIcons[period]}"></i>
                            ${period.charAt(0).toUpperCase() + period.slice(1)}
                        </h6>
                        <div class="time-slots">
                `;
                
                periodSlots.forEach(slot => {
                    const isDisabled = slot.status === 'booked';
                    const limitedClass = slot.status === 'limited' ? 'limited' : '';
                    
                    html += `
                        <div class="time-slot ${slot.status} ${limitedClass}" 
                             data-time="${slot.time}" 
                             data-status="${slot.status}"
                             ${isDisabled ? 'title="Not available"' : ''}>
                            <span class="time">${slot.label}</span>
                            <span class="status-indicator">
                                ${slot.status === 'available' ? '<i class="bi bi-check-circle"></i>' : 
                                  slot.status === 'limited' ? '<i class="bi bi-exclamation-triangle"></i>' : 
                                  '<i class="bi bi-x-circle"></i>'}
                            </span>
                        </div>
                    `;
                });
                
                html += '</div></div>';
            }
        });
        
        if (html === '') {
            html = '<div class="no-slots">No available slots for this time period</div>';
        }
        
        container.innerHTML = html;
        
        // Add click handlers
        container.querySelectorAll('.time-slot:not(.booked)').forEach(slot => {
            slot.addEventListener('click', function() {
                // Remove previous selection
                container.querySelectorAll('.time-slot.selected').forEach(s => 
                    s.classList.remove('selected'));
                
                // Select current
                this.classList.add('selected');
                
                // Store selection
                BookingSystem.selectedTime = this.dataset.time;
                
                // Update summary
                updateAppointmentSummary();
                
                // Show notification
                const timeLabel = this.querySelector('.time').textContent;
                showNotification(`${timeLabel} selected!`, 'success');
                
                // Add selection animation
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1.05)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 200);
                }, 100);
            });
        });
    }
    
    // Form Handling
    function initializeFormHandling() {
        // Concern tags
        document.querySelectorAll('.concern-tag input').forEach(input => {
            input.addEventListener('change', function() {
                const tag = this.closest('.concern-tag');
                if (this.checked) {
                    tag.classList.add('selected');
                    BookingSystem.selectedConcerns.push(this.value);
                } else {
                    tag.classList.remove('selected');
                    const index = BookingSystem.selectedConcerns.indexOf(this.value);
                    if (index > -1) {
                        BookingSystem.selectedConcerns.splice(index, 1);
                    }
                }
            });
        });
        
        // Additional notes
        const notesTextarea = document.getElementById('additional-notes');
        if (notesTextarea) {
            notesTextarea.addEventListener('input', function() {
                BookingSystem.additionalNotes = this.value;
            });
        }
        
        // Privacy preferences
        document.querySelectorAll('input[name="privacy"]').forEach(input => {
            input.addEventListener('change', function() {
                BookingSystem.privacyPreference = this.value;
            });
        });
    }
    
    // Mobile Navigation
    function initializeMobileNavigation() {
        console.log('📱 Initializing mobile navigation...');
        
        const nextBtn = document.querySelector('.mobile-nav-btn.next-btn');
        const prevBtn = document.querySelector('.mobile-nav-btn.prev-btn');
        const confirmBtn = document.querySelector('.mobile-nav-btn.confirm-btn');
        
        console.log('📱 Mobile buttons found:', {
            nextBtn: !!nextBtn,
            prevBtn: !!prevBtn,
            confirmBtn: !!confirmBtn
        });
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('📱 Mobile Next button clicked!');
                nextStep();
            });
            console.log('✅ Mobile Next button listener attached');
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('📱 Mobile Previous button clicked!');
                prevStep();
            });
            console.log('✅ Mobile Previous button listener attached');
        }
        
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('📱 Mobile Confirm button clicked!');
                confirmAppointment();
            });
            console.log('✅ Mobile Confirm button listener attached');
        }
        
        console.log('📱 Mobile navigation initialization complete');
    }
    
    function updateMobileNavigation() {
        const currentStepEl = document.querySelector('.mobile-step-indicator .current-step');
        const prevBtn = document.querySelector('.mobile-nav-btn.prev-btn');
        const nextBtn = document.querySelector('.mobile-nav-btn.next-btn');
        const confirmBtn = document.querySelector('.mobile-nav-btn.confirm-btn');
        
        if (currentStepEl) {
            currentStepEl.textContent = BookingSystem.currentStep;
        }
        
        if (prevBtn) {
            prevBtn.style.display = BookingSystem.currentStep === 1 ? 'none' : 'flex';
        }
        
        if (nextBtn && confirmBtn) {
            if (BookingSystem.currentStep === 4) {
                nextBtn.style.display = 'none';
                confirmBtn.style.display = 'flex';
            } else {
                nextBtn.style.display = 'flex';
                confirmBtn.style.display = 'none';
                
                // Enable/disable based on validation
                const isValid = validateCurrentStep();
                nextBtn.disabled = !isValid;
                nextBtn.style.opacity = isValid ? '1' : '0.5';
            }
        }
    }
    
    // Navigation Button Handlers
    function initializeStepNavigation() {
        console.log('🔧 Initializing step navigation...');
        
        // Desktop navigation buttons with enhanced error handling
        const nextBtn = document.querySelector('.btn-next');
        const prevBtn = document.querySelector('.btn-previous');
        const confirmBtn = document.querySelector('.btn-confirm-desktop');
        
        console.log('📍 Found buttons:', { nextBtn: !!nextBtn, prevBtn: !!prevBtn, confirmBtn: !!confirmBtn });
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🎯 Next button clicked!');
                nextStep();
            });
            console.log('✅ Next button listener attached');
        } else {
            console.error('❌ Next button not found!');
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('🔙 Previous button clicked!');
                prevStep();
            });
            console.log('✅ Previous button listener attached');
        }
        
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('✅ Confirm button clicked!');
                confirmAppointment();
            });
            console.log('✅ Confirm button listener attached');
        }
        
        // Legacy button support (if exists)
        document.querySelector('.btn-prev')?.addEventListener('click', prevStep);
        document.querySelector('.btn-confirm')?.addEventListener('click', confirmAppointment);
        
        // Edit booking button
        document.querySelector('.edit-booking')?.addEventListener('click', () => {
            showStep(1);
            showNotification('You can now edit your booking details', 'info');
        });
        
        // Confirmation button in step 4
        document.querySelector('.confirm-appointment')?.addEventListener('click', confirmAppointment);
        
        console.log('🔧 Step navigation initialization complete');
    }
    
    function updateNavigationButtons() {
        // Update desktop navigation buttons
        updateDesktopNavigation();
        
        // Update mobile navigation (already handled separately)
        updateMobileNavigation();
    }
    
    function updateDesktopNavigation() {
        const currentStepEl = document.querySelector('.current-step-number');
        const prevBtn = document.querySelector('.btn-previous');
        const nextBtn = document.querySelector('.btn-next');
        const confirmBtn = document.querySelector('.btn-confirm-desktop');
        
        // Update step counter
        if (currentStepEl) {
            currentStepEl.textContent = BookingSystem.currentStep;
        }
        
        // Handle Previous button
        if (prevBtn) {
            if (BookingSystem.currentStep === 1) {
                prevBtn.style.display = 'none';
            } else {
                prevBtn.style.display = 'flex';
                prevBtn.disabled = false;
            }
        }
        
        // Handle Next/Confirm buttons
        if (nextBtn && confirmBtn) {
            if (BookingSystem.currentStep === 4) {
                nextBtn.style.display = 'none';
                confirmBtn.style.display = 'flex';
                confirmBtn.disabled = false;
            } else {
                nextBtn.style.display = 'flex';
                confirmBtn.style.display = 'none';
                
                // Enable/disable based on validation
                const isValid = validateCurrentStep();
                nextBtn.disabled = !isValid;
                
                // Add visual feedback
                if (isValid) {
                    nextBtn.style.opacity = '1';
                    nextBtn.style.cursor = 'pointer';
                    nextBtn.title = '';
                    nextBtn.classList.remove('disabled');
                    
                    // Update button text based on step
                    const buttonText = nextBtn.querySelector('span');
                    if (buttonText) {
                        switch (BookingSystem.currentStep) {
                            case 1:
                                buttonText.textContent = 'Continue';
                                break;
                            case 2:
                                buttonText.textContent = 'Add Details';
                                break;
                            case 3:
                                buttonText.textContent = 'Review Booking';
                                break;
                            default:
                                buttonText.textContent = 'Next';
                        }
                    }
                } else {
                    nextBtn.style.opacity = '0.6';
                    nextBtn.style.cursor = 'not-allowed';
                    nextBtn.title = getValidationMessage();
                    nextBtn.classList.add('disabled');
                    
                    // Keep generic text when disabled
                    const buttonText = nextBtn.querySelector('span');
                    if (buttonText) {
                        buttonText.textContent = 'Next';
                    }
                }
            }
        }
    }
    
    function getValidationMessage() {
        switch (BookingSystem.currentStep) {
            case 1: return 'Please select a counselor';
            case 2: return 'Please select date and time';
            case 3: return 'Optional step - you can proceed';
            case 4: return 'Ready to confirm';
            default: return 'Please complete this step';
        }
    }
    
    // Appointment Summary Updates
    function updateAppointmentSummary() {
        const summaryContainer = document.querySelector('.appointment-summary .summary-content');
        if (!summaryContainer) return;
        
        let hasContent = false;
        
        // Update counselor summary
        const counselorSummary = summaryContainer.querySelector('.counselor-summary');
        if (BookingSystem.selectedCounselor && counselorSummary) {
            const avatar = counselorSummary.querySelector('.summary-avatar');
            const name = counselorSummary.querySelector('.counselor-name-summary');
            const title = counselorSummary.querySelector('.counselor-title-summary');
            
            if (avatar) avatar.src = BookingSystem.selectedCounselor.avatar;
            if (name) name.textContent = BookingSystem.selectedCounselor.name;
            if (title) title.textContent = BookingSystem.selectedCounselor.title;
            
            counselorSummary.style.display = 'flex';
            hasContent = true;
        }
        
        // Update date/time summary
        const dateSummary = summaryContainer.querySelector('.date-summary');
        if (BookingSystem.selectedDate && BookingSystem.selectedTime && dateSummary) {
            const dateEl = dateSummary.querySelector('.selected-date');
            const timeEl = dateSummary.querySelector('.selected-time');
            
            if (dateEl && timeEl) {
                const dateObj = new Date(BookingSystem.selectedDate);
                const formattedDate = dateObj.toLocaleDateString('en-US', {
                    weekday: 'long',
                    month: 'long',
                    day: 'numeric'
                });
                
                const timeObj = new Date(`2000-01-01T${BookingSystem.selectedTime}:00`);
                const formattedTime = timeObj.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit'
                });
                
                dateEl.textContent = formattedDate;
                timeEl.textContent = `${formattedTime} (${BookingSystem.selectedDuration} min, ${BookingSystem.selectedType})`;
                
                dateSummary.style.display = 'flex';
                hasContent = true;
            }
        }
        
        // Show/hide placeholder
        const placeholder = summaryContainer.querySelector('.summary-placeholder');
        if (placeholder) {
            placeholder.style.display = hasContent ? 'none' : 'block';
        }
    }
    
    // Confirmation Details
    function populateConfirmationDetails() {
        const detailsContainer = document.querySelector('.appointment-details');
        if (!detailsContainer) return;
        
        const counselor = BookingSystem.selectedCounselor;
        const date = BookingSystem.selectedDate;
        const time = BookingSystem.selectedTime;
        
        if (!counselor || !date || !time) return;
        
        // Format date and time
        const dateObj = new Date(date);
        const formattedDate = dateObj.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const timeObj = new Date(`2000-01-01T${time}:00`);
        const formattedTime = timeObj.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit'
        });
        
        const html = `
            <div class="confirmation-header">
                <div class="counselor-info">
                    <img src="${counselor.avatar}" alt="${counselor.name}" class="counselor-avatar-large">
                    <div class="counselor-details">
                        <h3>${counselor.name}</h3>
                        <p>${counselor.title}</p>
                        <div class="rating">
                            <i class="bi bi-star-fill"></i>
                            <span>${counselor.rating} rating</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="appointment-info">
                <div class="info-row">
                    <div class="info-icon">
                        <i class="bi bi-calendar-event"></i>
                    </div>
                    <div class="info-details">
                        <h5>Date & Time</h5>
                        <p>${formattedDate}</p>
                        <p>${formattedTime}</p>
                    </div>
                </div>
                
                <div class="info-row">
                    <div class="info-icon">
                        <i class="bi bi-clock"></i>
                    </div>
                    <div class="info-details">
                        <h5>Session Details</h5>
                        <p>${BookingSystem.selectedDuration} minute session</p>
                        <p>${BookingSystem.selectedType} call</p>
                    </div>
                </div>
                
                ${BookingSystem.selectedConcerns.length > 0 ? `
                <div class="info-row">
                    <div class="info-icon">
                        <i class="bi bi-heart-pulse"></i>
                    </div>
                    <div class="info-details">
                        <h5>Focus Areas</h5>
                        <p>${BookingSystem.selectedConcerns.join(', ')}</p>
                    </div>
                </div>
                ` : ''}
                
                <div class="info-row">
                    <div class="info-icon">
                        <i class="bi bi-shield-lock"></i>
                    </div>
                    <div class="info-details">
                        <h5>Privacy</h5>
                        <p>${BookingSystem.privacyPreference === 'named' ? 'Use my name' : 'Stay anonymous'}</p>
                    </div>
                </div>
            </div>
        `;
        
        detailsContainer.innerHTML = html;
    }
    
    // Booking Confirmation
    async function confirmAppointment() {
        const confirmBtn = document.querySelector('.confirm-appointment') || 
                          document.querySelector('.mobile-nav-btn.confirm-btn');
        
        if (!confirmBtn) return;
        
        // Show loading state
        const originalHTML = confirmBtn.innerHTML;
        confirmBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Confirming...';
        confirmBtn.disabled = true;
        
        try {
            // Prepare booking data
            const bookingData = {
                counselor_id: BookingSystem.selectedCounselor.id,
                date: BookingSystem.selectedDate,
                time: BookingSystem.selectedTime,
                duration: BookingSystem.selectedDuration,
                type: BookingSystem.selectedType,
                concerns: BookingSystem.selectedConcerns,
                notes: BookingSystem.additionalNotes,
                privacy: BookingSystem.privacyPreference
            };
            
            // Simulate API call
            await simulateAPICall(bookingData);
            
            // Show success with confetti
            showSuccessModal();
            
        } catch (error) {
            console.error('Booking error:', error);
            showNotification('Failed to confirm booking. Please try again.', 'error');
            
            // Restore button
            confirmBtn.innerHTML = originalHTML;
            confirmBtn.disabled = false;
        }
    }
    
    async function simulateAPICall(data) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulate successful booking (95% success rate for demo)
                if (Math.random() > 0.05) {
                    resolve({ success: true, id: Date.now() });
                } else {
                    reject(new Error('Network error'));
                }
            }, 2000);
        });
    }
    
    // Success Modal with Confetti
    function showSuccessModal() {
        const modal = document.getElementById('success-modal');
        if (!modal) return;
        
        // Show modal
        modal.style.display = 'flex';
        modal.style.opacity = '0';
        
        // Animate in
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 100);
        
        // Start confetti animation
        createConfettiAnimation();
        
        // Populate success details
        populateSuccessDetails();
        
        // Play success sound (if available)
        playSuccessSound();
    }
    
    function createConfettiAnimation() {
        const container = document.getElementById('confetti-container');
        if (!container) return;
        
        // Create confetti pieces
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7', '#fd79a8'];
        const shapes = ['circle', 'square', 'triangle'];
        
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti-piece';
            
            const color = colors[Math.floor(Math.random() * colors.length)];
            const shape = shapes[Math.floor(Math.random() * shapes.length)];
            const size = Math.random() * 8 + 4;
            const delay = Math.random() * 3000;
            const duration = Math.random() * 2000 + 3000;
            
            confetti.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: ${color};
                left: ${Math.random() * 100}%;
                top: -10px;
                animation: confetti-fall ${duration}ms linear ${delay}ms forwards;
                border-radius: ${shape === 'circle' ? '50%' : '0'};
                transform: ${shape === 'triangle' ? 'rotate(45deg)' : 'none'};
            `;
            
            container.appendChild(confetti);
        }
        
        // Clean up after animation
        setTimeout(() => {
            container.innerHTML = '';
        }, 8000);
    }
    
    function populateSuccessDetails() {
        const detailsContainer = document.querySelector('.success-details');
        if (!detailsContainer || !BookingSystem.selectedCounselor) return;
        
        const counselor = BookingSystem.selectedCounselor;
        const dateObj = new Date(BookingSystem.selectedDate);
        const timeObj = new Date(`2000-01-01T${BookingSystem.selectedTime}:00`);
        
        const formattedDate = dateObj.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        const formattedTime = timeObj.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit'
        });
        
        detailsContainer.innerHTML = `
            <div class="success-appointment-card">
                <div class="counselor-preview">
                    <img src="${counselor.avatar}" alt="${counselor.name}">
                    <div>
                        <h4>${counselor.name}</h4>
                        <p>${counselor.title}</p>
                    </div>
                </div>
                
                <div class="appointment-details-grid">
                    <div class="detail-item">
                        <i class="bi bi-calendar-check"></i>
                        <span>${formattedDate}</span>
                    </div>
                    <div class="detail-item">
                        <i class="bi bi-clock"></i>
                        <span>${formattedTime}</span>
                    </div>
                    <div class="detail-item">
                        <i class="bi bi-camera-video"></i>
                        <span>${BookingSystem.selectedDuration} min ${BookingSystem.selectedType}</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Animation and Sound Effects
    function initializeAnimations() {
        // Add CSS for smooth transitions
        const style = document.createElement('style');
        style.textContent = `
            .booking-step {
                transition: opacity 0.3s ease, transform 0.3s ease;
            }
            
            .stepper-counter.active-pulse {
                animation: pulse 2s infinite;
            }
            
            .stepper-counter.completed-animation {
                animation: bounce 0.6s ease;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            @keyframes bounce {
                0%, 20%, 60%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                80% { transform: translateY(-5px); }
            }
            
            @keyframes confetti-fall {
                0% {
                    transform: translateY(-10px) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(100vh) rotate(720deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    function playStepTransitionSound() {
        // Create a subtle sound effect for step transitions
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            try {
                const AudioContextClass = AudioContext || webkitAudioContext;
                const audioContext = new AudioContextClass();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                oscillator.frequency.value = 800;
                gainNode.gain.value = 0.1;
                
                oscillator.start();
                oscillator.stop(audioContext.currentTime + 0.1);
            } catch (e) {
                // Ignore audio errors
            }
        }
    }
    
    function playSuccessSound() {
        // Create a success sound effect
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            try {
                const AudioContextClass = AudioContext || webkitAudioContext;
                const audioContext = new AudioContextClass();
                
                // Create a pleasant success chord
                const frequencies = [523.25, 659.25, 783.99]; // C, E, G
                
                frequencies.forEach((freq, index) => {
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();
                    
                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);
                    
                    oscillator.frequency.value = freq;
                    gainNode.gain.value = 0.05;
                    
                    oscillator.start(audioContext.currentTime + index * 0.1);
                    oscillator.stop(audioContext.currentTime + 0.5 + index * 0.1);
                });
            } catch (e) {
                // Ignore audio errors
            }
        }
    }
    
    // Notification System
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        document.querySelectorAll('.notification').forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            padding: 12px 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateX(100%);
            transition: transform 0.3s ease;
            max-width: 300px;
            font-weight: 500;
        `;
        
        const icon = type === 'success' ? 'bi-check-circle' : 
                    type === 'error' ? 'bi-exclamation-triangle' : 'bi-info-circle';
        
        notification.innerHTML = `
            <i class="bi ${icon}" style="margin-right: 8px;"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    function showValidationMessage() {
        const messages = {
            1: 'Please select a counselor to continue',
            2: 'Please select both a date and time',
            3: 'Please complete the form details',
            4: 'Please review and confirm your appointment'
        };
        
        showNotification(messages[BookingSystem.currentStep] || 'Please complete this step', 'error');
    }
    
    // Initialize everything when DOM is ready
    initializeBookingSystem();
    
    // Global access for debugging
    window.BookingSystem = BookingSystem;
    window.showStep = showStep;
});

// CSS Animations (added dynamically)
document.addEventListener('DOMContentLoaded', function() {
    const css = `
        .notification {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .loading-spinner {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
            color: #6b7280;
            font-style: italic;
        }
        
        .loading-spinner::before {
            content: '';
            width: 20px;
            height: 20px;
            border: 2px solid #e5e7eb;
            border-top: 2px solid #3b82f6;
            border-radius: 50%;
            margin-right: 12px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    
    // Enhanced Keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Ignore keyboard events when user is typing in input fields
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') {
            return;
        }
        
        // Arrow key navigation
        if (e.key === 'ArrowLeft' && BookingSystem.currentStep > 1) {
            e.preventDefault();
            prevStep();
            showNotification('← Previous step', 'info');
        } else if (e.key === 'ArrowRight' && BookingSystem.currentStep < BookingSystem.totalSteps && validateCurrentStep()) {
            e.preventDefault();
            nextStep();
            showNotification('Next step →', 'success');
        }
        
        // Enter key to proceed
        if (e.key === 'Enter' && validateCurrentStep()) {
            e.preventDefault();
            if (BookingSystem.currentStep === 4) {
                confirmAppointment();
            } else {
                nextStep();
            }
        }
        
        // Escape key to go back
        if (e.key === 'Escape' && BookingSystem.currentStep > 1) {
            e.preventDefault();
            prevStep();
        }
    });
    
    // Add pulse animation to next button when step becomes valid
    function addButtonPulse() {
        const nextBtn = document.querySelector('.btn-next');
        if (nextBtn && !nextBtn.disabled) {
            nextBtn.classList.add('pulse');
            setTimeout(() => nextBtn.classList.remove('pulse'), 600);
        }
    }
    
    // Global reference for pulse animation
    window.addButtonPulse = addButtonPulse;
});
