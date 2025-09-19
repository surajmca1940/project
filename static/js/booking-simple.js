// Simplified Working Booking System
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Simple Booking System Loading...');
    
    // Simple booking state
    const booking = {
        step: 1,
        counselor: null,
        date: null,
        time: null,
        duration: '50min',
        type: 'video'
    };
    
    // Show/hide steps
    function showStep(stepNum) {
        console.log('Showing step:', stepNum);
        
        // Hide all steps
        for (let i = 1; i <= 4; i++) {
            const step = document.getElementById(`step-${i}`);
            if (step) {
                step.style.display = 'none';
            }
        }
        
        // Show current step
        const currentStep = document.getElementById(`step-${stepNum}`);
        if (currentStep) {
            currentStep.style.display = 'block';
            booking.step = stepNum;
        }
        
        updateButtons();
        updateProgress();
    }
    
    // Update navigation buttons
    function updateButtons() {
        const nextBtn = document.querySelector('.btn-next');
        const prevBtn = document.querySelector('.btn-prev');
        const confirmBtn = document.querySelector('.btn-confirm');
        
        console.log('Updating buttons for step:', booking.step);
        
        if (prevBtn) {
            prevBtn.style.display = booking.step === 1 ? 'none' : 'inline-flex';
        }
        
        if (nextBtn) {
            if (booking.step === 4) {
                nextBtn.style.display = 'none';
            } else {
                nextBtn.style.display = 'inline-flex';
                nextBtn.disabled = !isStepComplete(booking.step);
            }
        }
        
        if (confirmBtn) {
            confirmBtn.style.display = booking.step === 4 ? 'inline-flex' : 'none';
        }
    }
    
    // Update progress bar
    function updateProgress() {
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach((step, index) => {
            const stepNum = index + 1;
            const circle = step.querySelector('.progress-circle');
            
            step.classList.remove('active', 'completed');
            
            if (stepNum < booking.step) {
                step.classList.add('completed');
                if (circle) circle.innerHTML = '✓';
            } else if (stepNum === booking.step) {
                step.classList.add('active');
                if (circle) circle.innerHTML = stepNum;
            } else {
                if (circle) circle.innerHTML = stepNum;
            }
        });
    }
    
    // Check if step is complete
    function isStepComplete(stepNum) {
        switch (stepNum) {
            case 1: return booking.counselor !== null;
            case 2: return booking.date && booking.time;
            case 3: return true; // Optional step
            case 4: return true;
            default: return false;
        }
    }
    
    // Next step
    function nextStep() {
        if (booking.step < 4 && isStepComplete(booking.step)) {
            showStep(booking.step + 1);
            showMessage('Step completed!', 'success');
        } else {
            showMessage('Please complete this step first.', 'error');
        }
    }
    
    // Previous step
    function prevStep() {
        if (booking.step > 1) {
            showStep(booking.step - 1);
        }
    }
    
    // Show message
    function showMessage(text, type) {
        // Remove existing messages
        document.querySelectorAll('.temp-message').forEach(msg => msg.remove());
        
        const message = document.createElement('div');
        message.className = `temp-message alert alert-${type === 'success' ? 'success' : 'danger'}`;
        message.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            padding: 10px 15px;
            border-radius: 5px;
            max-width: 300px;
        `;
        message.textContent = text;
        
        document.body.appendChild(message);
        
        setTimeout(() => message.remove(), 3000);
    }
    
    // Initialize counselor selection
    function initCounselors() {
        const cards = document.querySelectorAll('.counselor-card');
        console.log('Found counselor cards:', cards.length);
        
        cards.forEach(card => {
            card.addEventListener('click', function() {
                // Remove previous selection
                cards.forEach(c => c.classList.remove('selected'));
                
                // Select current
                this.classList.add('selected');
                
                // Store data
                const name = this.querySelector('h6')?.textContent || 'Unknown';
                booking.counselor = {
                    name: name,
                    id: this.dataset.counselorId
                };
                
                console.log('Counselor selected:', booking.counselor);
                showMessage(`${name} selected!`, 'success');
                
                updateButtons();
                
                // Auto advance
                setTimeout(() => {
                    if (booking.step === 1) nextStep();
                }, 1000);
            });
        });
    }
    
    // Initialize time slots
    function initTimeSlots() {
        const slots = document.querySelectorAll('.time-slot:not(.booked)');
        console.log('Found time slots:', slots.length);
        
        slots.forEach(slot => {
            slot.addEventListener('click', function() {
                // Remove previous selection
                slots.forEach(s => s.classList.remove('selected'));
                
                // Select current
                this.classList.add('selected');
                
                // Store data
                const time = this.querySelector('.time')?.textContent || 'Unknown';
                booking.time = time;
                booking.date = 'Today'; // Simplified for now
                
                console.log('Time selected:', booking.time);
                showMessage(`${time} selected!`, 'success');
                
                updateButtons();
            });
        });
    }
    
    // Initialize calendar (simplified)
    function initCalendar() {
        // Generate simple calendar
        const grid = document.getElementById('calendar-grid');
        if (grid) {
            const today = new Date();
            let html = '<div class="simple-calendar">';
            
            for (let i = 1; i <= 30; i++) {
                const date = new Date(today);
                date.setDate(today.getDate() + i - 1);
                const isPast = i === 1;
                
                html += `<div class="cal-day ${isPast ? 'past' : ''}" data-date="${date.toISOString().split('T')[0]}">${i}</div>`;
            }
            
            html += '</div>';
            grid.innerHTML = html;
            
            // Add click handlers
            grid.querySelectorAll('.cal-day:not(.past)').forEach(day => {
                day.addEventListener('click', function() {
                    grid.querySelectorAll('.cal-day').forEach(d => d.classList.remove('selected'));
                    this.classList.add('selected');
                    booking.date = this.dataset.date;
                    showMessage('Date selected!', 'success');
                    updateButtons();
                });
            });
        }
    }
    
    // Initialize navigation
    function initNavigation() {
        const nextBtn = document.querySelector('.btn-next');
        const prevBtn = document.querySelector('.btn-prev');
        const confirmBtn = document.querySelector('.btn-confirm');
        
        console.log('Navigation buttons:', {
            next: !!nextBtn,
            prev: !!prevBtn,
            confirm: !!confirmBtn
        });
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Next clicked');
                nextStep();
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Previous clicked');
                prevStep();
            });
        }
        
        if (confirmBtn) {
            confirmBtn.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Confirm clicked');
                confirmBooking();
            });
        }
    }
    
    // Confirm booking
    function confirmBooking() {
        const btn = document.querySelector('.btn-confirm');
        if (btn) {
            btn.textContent = 'Processing...';
            btn.disabled = true;
        }
        
        showMessage('Processing your booking...', 'success');
        
        setTimeout(() => {
            showSuccessPage();
        }, 2000);
    }
    
    // Show success page
    function showSuccessPage() {
        const mainCard = document.querySelector('.booking-main-card');
        if (mainCard) {
            mainCard.innerHTML = `
                <div style="text-align: center; padding: 3rem;">
                    <div style="font-size: 4rem; color: #10b981; margin-bottom: 1rem;">✓</div>
                    <h2 style="color: #10b981; margin-bottom: 1rem;">Booking Confirmed!</h2>
                    <p style="color: #666; margin-bottom: 2rem;">Your appointment has been successfully booked.</p>
                    
                    <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 8px; margin: 2rem 0;">
                        <h5>Appointment Details:</h5>
                        <p><strong>Counselor:</strong> ${booking.counselor?.name || 'Selected Counselor'}</p>
                        <p><strong>Date:</strong> ${booking.date || 'Selected Date'}</p>
                        <p><strong>Time:</strong> ${booking.time || 'Selected Time'}</p>
                        <p><strong>Duration:</strong> ${booking.duration}</p>
                        <p><strong>Type:</strong> ${booking.type}</p>
                    </div>
                    
                    <button class="btn btn-primary" onclick="location.reload()">Book Another Appointment</button>
                </div>
            `;
        }
        
        showMessage('Appointment confirmed successfully!', 'success');
    }
    
    // Initialize everything
    function init() {
        console.log('Initializing simple booking system...');
        
        // Add simple calendar styles
        const style = document.createElement('style');
        style.textContent = `
            .simple-calendar { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
            .cal-day { 
                padding: 10px; text-align: center; border: 1px solid #ddd; 
                cursor: pointer; border-radius: 4px; 
            }
            .cal-day:hover:not(.past) { background: #e3f2fd; }
            .cal-day.selected { background: #2196f3; color: white; }
            .cal-day.past { opacity: 0.3; cursor: not-allowed; }
        `;
        document.head.appendChild(style);
        
        showStep(1);
        initCounselors();
        initTimeSlots();
        initCalendar();
        initNavigation();
        
        console.log('✅ Simple booking system initialized!');
        showMessage('Booking system ready!', 'success');
    }
    
    // Start initialization
    init();
    
    // Debug helper
    window.bookingDebug = {
        showStep: showStep,
        booking: booking,
        jumpToStep4: () => {
            booking.counselor = { name: 'Test Counselor' };
            booking.date = 'Test Date';
            booking.time = 'Test Time';
            showStep(4);
        }
    };
});