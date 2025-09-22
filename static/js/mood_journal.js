// Mood Journal JavaScript - Interactive functionality

class MoodJournal {
    constructor() {
        this.form = document.getElementById('moodForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.noteTextarea = document.getElementById('note');
        this.charCount = document.getElementById('charCount');
        this.selectedMood = null;
        this.isSubmitting = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupAnimations();
        this.setupCharacterCounter();
        this.setupJournalView();
    }

    setupEventListeners() {
        // Mood selection
        const moodOptions = document.querySelectorAll('.mood-option input[type="radio"]');
        moodOptions.forEach(option => {
            option.addEventListener('change', (e) => {
                this.handleMoodSelection(e.target.value, e.target.closest('.mood-option'));
            });
        });

        // Form submission
        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });
        }

        // Note textarea events
        if (this.noteTextarea) {
            this.noteTextarea.addEventListener('input', (e) => {
                this.updateCharacterCount(e.target.value.length);
            });

            this.noteTextarea.addEventListener('focus', () => {
                this.noteTextarea.parentElement.classList.add('focused');
            });

            this.noteTextarea.addEventListener('blur', () => {
                this.noteTextarea.parentElement.classList.remove('focused');
            });
        }

        // Load more entries button
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => {
                this.loadMoreEntries();
            });
        }
    }

    setupFormValidation() {
        // Real-time validation
        this.updateSubmitButton();
    }

    setupAnimations() {
        // Fade in cards on page load
        const cards = document.querySelectorAll('.mood-entry-card, .ai-insights-card, .recent-entries-card, .tips-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 150);
        });

        // Animate timeline items
        const timelineItems = document.querySelectorAll('.timeline-item');
        timelineItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('fade-in');
            }, (index * 100) + 500);
        });

        // Animate insight items
        const insightItems = document.querySelectorAll('.insight-item');
        insightItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('scale-in');
            }, (index * 150) + 300);
        });
    }

    setupCharacterCounter() {
        if (this.noteTextarea) {
            this.updateCharacterCount(this.noteTextarea.value.length);
        }
    }

    handleMoodSelection(mood, optionElement) {
        this.selectedMood = mood;
        
        // Remove previous selections
        document.querySelectorAll('.mood-option').forEach(option => {
            option.classList.remove('selected', 'error');
        });
        
        // Mark current selection
        optionElement.classList.add('selected');
        
        // Add selection animation
        const emoji = optionElement.querySelector('.mood-emoji');
        if (emoji) {
            emoji.style.animation = 'none';
            setTimeout(() => {
                emoji.style.animation = 'bounce 0.6s ease-in-out';
            }, 10);
        }
        
        // Update submit button state
        this.updateSubmitButton();
        
        // Show selection feedback
        this.showMoodSelectionFeedback(mood);
    }

    showMoodSelectionFeedback(mood) {
        const feedbackMessages = {
            'happy': '😊 Great to hear you\'re feeling happy!',
            'sad': '😢 It\'s okay to feel sad sometimes. You\'re not alone.',
            'angry': '😡 Anger is a valid emotion. Let\'s work through it together.',
            'tired': '😴 Rest is important. Take care of yourself.',
            'anxious': '😨 Anxiety can be tough. You\'re brave for acknowledging it.'
        };
        
        const message = feedbackMessages[mood];
        if (message) {
            this.showTooltip(message);
        }
    }

    showTooltip(message) {
        // Create temporary tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'mood-feedback-tooltip';
        tooltip.textContent = message;
        tooltip.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--primary-color);
            color: white;
            padding: 1rem 2rem;
            border-radius: 25px;
            z-index: 9999;
            animation: fadeIn 0.3s ease-in;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            font-weight: 500;
        `;
        
        document.body.appendChild(tooltip);
        
        setTimeout(() => {
            tooltip.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => {
                if (document.body.contains(tooltip)) {
                    document.body.removeChild(tooltip);
                }
            }, 300);
        }, 2000);
    }

    updateCharacterCount(count) {
        if (this.charCount) {
            this.charCount.textContent = count;
            
            // Color coding for character count
            if (count > 400) {
                this.charCount.style.color = '#dc3545';
            } else if (count > 300) {
                this.charCount.style.color = '#fd7e14';
            } else {
                this.charCount.style.color = '#6c757d';
            }
        }
    }

    updateSubmitButton() {
        if (!this.submitBtn) return;
        
        const isValid = this.selectedMood !== null;
        
        if (isValid) {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = '<i class="bi bi-heart-fill"></i> Save My Mood';
            this.submitBtn.classList.remove('btn-secondary');
            this.submitBtn.classList.add('btn-primary');
        } else {
            this.submitBtn.disabled = true;
            this.submitBtn.innerHTML = '<i class="bi bi-arrow-right"></i> Select a mood first';
            this.submitBtn.classList.remove('btn-primary');
            this.submitBtn.classList.add('btn-secondary');
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();
        
        if (this.isSubmitting) return;
        
        // Validate mood selection
        if (!this.selectedMood) {
            this.showMoodValidationError();
            return;
        }
        
        // Show loading state
        this.setSubmittingState(true);
        
        // Submit form
        this.submitForm();
    }

    showMoodValidationError() {
        // Highlight mood options with error
        const moodOptions = document.querySelectorAll('.mood-option');
        moodOptions.forEach(option => {
            option.classList.add('error');
        });
        
        // Remove error class after animation
        setTimeout(() => {
            moodOptions.forEach(option => {
                option.classList.remove('error');
            });
        }, 500);
        
        // Show error message
        this.showErrorMessage('Please select your current mood before submitting.');
        
        // Scroll to mood selector
        document.querySelector('.mood-selector').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }

    showErrorMessage(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at top of form
        this.form.insertBefore(alertDiv, this.form.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (document.body.contains(alertDiv)) {
                alertDiv.remove();
            }
        }, 5000);
    }

    setSubmittingState(isSubmitting) {
        this.isSubmitting = isSubmitting;
        
        if (isSubmitting) {
            this.submitBtn.disabled = true;
            this.submitBtn.innerHTML = '<span class="loading-spinner"></span> Saving...';
            this.form.classList.add('loading');
        } else {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = '<i class="bi bi-heart-fill"></i> Save My Mood';
            this.form.classList.remove('loading');
        }
    }

    async submitForm() {
        try {
            // Get form data
            const formData = new FormData(this.form);
            
            // Submit via fetch API
            const response = await fetch(this.form.action || window.location.pathname, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                // Success - reload page to show new entry and updated insights
                this.showSuccessMessage();
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                throw new Error('Failed to save mood entry');
            }
            
        } catch (error) {
            console.error('Error submitting mood entry:', error);
            this.showErrorMessage('Failed to save your mood entry. Please try again.');
            this.setSubmittingState(false);
        }
    }

    showSuccessMessage() {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <i class="bi bi-check-circle"></i>
            <strong>Mood saved successfully!</strong> Your entry has been recorded and AI insights have been updated.
        `;
        
        // Insert at top of form
        this.form.insertBefore(successDiv, this.form.firstChild);
        
        // Add animation
        successDiv.classList.add('scale-in');
    }

    loadMoreEntries() {
        const loadMoreBtn = document.getElementById('loadMoreBtn');
        if (!loadMoreBtn) return;
        
        // Show loading state
        loadMoreBtn.innerHTML = '<span class="loading-spinner"></span> Loading...';
        loadMoreBtn.disabled = true;
        
        // Simulate loading (in real app, this would be an AJAX call)
        setTimeout(() => {
            // For demo, just hide the button
            loadMoreBtn.style.display = 'none';
            
            // In a real implementation, you would:
            // 1. Make AJAX call to get more entries
            // 2. Append new entries to timeline
            // 3. Update button state based on whether more entries exist
        }, 1000);
    }

    // Utility method to show mood statistics
    showMoodStatistics() {
        // This could be called to show a modal with mood statistics
        const stats = this.calculateMoodStats();
        console.log('Mood Statistics:', stats);
    }

    calculateMoodStats() {
        // Calculate statistics from recent entries
        // This would be more sophisticated in a real implementation
        return {
            totalEntries: document.querySelectorAll('.timeline-item').length,
            mostCommonMood: 'happy', // This would be calculated
            longestStreak: 7, // Days of consecutive entries
            averageMoodScore: 4.2 // Calculated average
        };
    }

    setupJournalView() {
        // Initialize calendar
        this.currentDate = new Date();
        this.currentYear = this.currentDate.getFullYear();
        this.currentMonth = this.currentDate.getMonth();
        this.entries = new Map(); // Store entries by date
        
        // Setup View Journal button functionality
        const viewJournalBtn = document.getElementById('viewJournalBtn');
        if (viewJournalBtn) {
            viewJournalBtn.addEventListener('click', () => {
                this.loadJournalEntries();
            });
        }

        // Setup modal event listeners
        const journalModal = document.getElementById('journalModal');
        if (journalModal) {
            journalModal.addEventListener('shown.bs.modal', () => {
                this.loadJournalEntries();
            });
        }

        // Setup navigation buttons
        const prevMonthBtn = document.getElementById('prevMonthBtn');
        const nextMonthBtn = document.getElementById('nextMonthBtn');

        if (prevMonthBtn) {
            prevMonthBtn.addEventListener('click', () => {
                this.navigateMonth(-1);
            });
        }

        if (nextMonthBtn) {
            nextMonthBtn.addEventListener('click', () => {
                this.navigateMonth(1);
            });
        }
    }

    navigateMonth(direction) {
        this.currentMonth += direction;
        if (this.currentMonth > 11) {
            this.currentMonth = 0;
            this.currentYear++;
        } else if (this.currentMonth < 0) {
            this.currentMonth = 11;
            this.currentYear--;
        }
        this.renderCalendar();
    }

    async loadJournalEntries() {
        const loadingDiv = document.getElementById('journalLoading');
        const calendarDiv = document.getElementById('journalCalendar');
        const noEntriesDiv = document.getElementById('noJournalEntries');

        // Show loading state
        loadingDiv.style.display = 'block';
        calendarDiv.style.display = 'none';
        noEntriesDiv.style.display = 'none';

        try {
            const response = await fetch('/api/mood-journal-entries/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load journal entries');
            }

            const data = await response.json();
            
            // Hide loading
            loadingDiv.style.display = 'none';

            if (data.entries && data.entries.length > 0) {
                console.log('Mood journal entries:', data.entries);
                this.processEntries(data.entries);
                
                // Navigate to the month with the most recent entry
                if (data.entries.length > 0) {
                    const mostRecentDate = data.entries[0].entry_date; // Entries are ordered by newest first
                    const dateParts = mostRecentDate.split('-');
                    this.currentYear = parseInt(dateParts[0]);
                    this.currentMonth = parseInt(dateParts[1]) - 1; // JavaScript months are 0-based
                    console.log('Navigating to month with entries:', this.currentMonth, this.currentYear);
                }
                
                this.renderCalendar();
                calendarDiv.style.display = 'block';
            } else {
                console.log('No mood journal entries found');
                noEntriesDiv.style.display = 'block';
            }

        } catch (error) {
            console.error('Error loading journal entries:', error);
            loadingDiv.style.display = 'none';
            
            // Show error state
            calendarDiv.innerHTML = `
                <div class="text-center py-4" style="padding: 3rem;">
                    <div class="mb-3">
                        <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: #dc3545;"></i>
                    </div>
                    <h5 class="text-danger">Error loading mood calendar</h5>
                    <p class="text-muted">Please try again later.</p>
                    <button class="btn btn-outline-primary" onclick="moodJournal.loadJournalEntries()">
                        <i class="bi bi-arrow-clockwise"></i> Retry
                    </button>
                </div>
            `;
            calendarDiv.style.display = 'block';
        }
    }

    processEntries(entries) {
        this.entries.clear();
        entries.forEach(entry => {
            const date = entry.entry_date; // Use entry_date which has YYYY-MM-DD format
            console.log('Processing entry for date:', date, 'mood:', entry.mood);
            this.entries.set(date, entry);
        });
        console.log('Total entries processed:', this.entries.size);
    }

    renderCalendar() {
        console.log('Rendering calendar for:', this.currentMonth, this.currentYear);
        console.log('Available entries:', this.entries);
        
        const monthYearElement = document.getElementById('currentMonthYear');
        const calendarGrid = document.getElementById('calendarGrid');

        // Update month/year display
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        monthYearElement.textContent = `${monthNames[this.currentMonth]} ${this.currentYear}`;

        // Clear calendar grid
        calendarGrid.innerHTML = '';

        // Add day headers
        const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        dayHeaders.forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.className = 'calendar-day-header';
            dayHeader.textContent = day;
            calendarGrid.appendChild(dayHeader);
        });

        // Get first day of month and number of days
        const firstDay = new Date(this.currentYear, this.currentMonth, 1).getDay();
        const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
        const daysInPrevMonth = new Date(this.currentYear, this.currentMonth, 0).getDate();
        
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];

        // Add previous month's trailing days
        for (let i = firstDay - 1; i >= 0; i--) {
            const dayNum = daysInPrevMonth - i;
            const dateCell = this.createDateCell(dayNum, true, false);
            calendarGrid.appendChild(dateCell);
        }

        // Add current month's days
        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const isToday = dateStr === todayStr;
            const hasEntry = this.entries.has(dateStr);
            const entry = hasEntry ? this.entries.get(dateStr) : null;
            
            if (hasEntry) {
                console.log(`Date ${dateStr} has entry:`, entry);
            }
            
            const dateCell = this.createDateCell(day, false, isToday, hasEntry, entry);
            calendarGrid.appendChild(dateCell);
        }

        // Add next month's leading days to fill the grid
        const totalCells = calendarGrid.children.length - 7; // Minus day headers
        const remainingCells = 42 - totalCells; // 6 weeks * 7 days
        for (let day = 1; day <= remainingCells; day++) {
            const dateCell = this.createDateCell(day, true, false);
            calendarGrid.appendChild(dateCell);
        }
    }

    createDateCell(day, isOtherMonth, isToday, hasEntry = false, entry = null) {
        const dateCell = document.createElement('div');
        dateCell.className = 'calendar-date';
        
        if (isOtherMonth) {
            dateCell.className += ' other-month';
        }
        if (isToday) {
            dateCell.className += ' today';
        }
        if (hasEntry) {
            dateCell.className += ' has-entry';
            // Add mood-specific color class
            const moodClass = this.getMoodColorClass(entry.mood);
            dateCell.className += ` ${moodClass}`;
        }

        const dateNumber = document.createElement('span');
        dateNumber.className = 'calendar-date-number';
        dateNumber.textContent = day;
        dateCell.appendChild(dateNumber);

        // Add click handler for dates with entries
        if (hasEntry) {
            dateCell.style.cursor = 'pointer';
            dateCell.addEventListener('click', () => {
                this.showEntryDetail(entry);
            });
        }

        return dateCell;
    }

    getMoodColorClass(mood) {
        const moodColors = {
            'happy': 'mood-happy',
            'sad': 'mood-sad', 
            'angry': 'mood-angry',
            'tired': 'mood-tired',
            'anxious': 'mood-anxious',
            'neutral': 'mood-neutral'
        };
        return moodColors[mood] || 'mood-neutral';
    }

    showEntryDetail(entry) {
        console.log('Showing entry detail for:', entry);
        try {
            // Create backdrop that goes over the modal
            const backdrop = document.createElement('div');
            backdrop.className = 'popup-backdrop';
            backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
            document.body.appendChild(backdrop);

            // Create popup
            const popup = document.createElement('div');
            popup.className = 'entry-detail-popup';
        
        popup.innerHTML = `
            <div class="entry-detail-header">
                <button class="entry-detail-close" onclick="this.closest('.entry-detail-popup').remove(); document.querySelectorAll('.popup-backdrop').forEach(el => el.remove());">
                    <i class="bi bi-x-lg"></i>
                </button>
                <div class="entry-detail-date">${entry.created_date}</div>
                <div class="entry-detail-time">${entry.created_time} • ${entry.relative_time}</div>
            </div>
            <div class="entry-detail-body">
                <div class="entry-detail-mood">
                    <span class="entry-detail-mood-emoji">${entry.mood_emoji}</span>
                    <div class="entry-detail-mood-label">${entry.mood_label}</div>
                </div>
                
                ${entry.note ? `
                    <div class="entry-detail-note">
                        ${this.escapeHtml(entry.note)}
                    </div>
                ` : ''}
                
                ${entry.emotions && entry.emotions.length > 0 ? `
                    <div class="entry-detail-emotions">
                        <h6>Emotions</h6>
                        <div class="diary-emotions">
                            ${entry.emotions.map(emotion => `<span class="emotion-tag ${emotion.type}">${emotion.name}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
                
                ${entry.sleep_data ? `
                    <div class="entry-detail-sleep-data">
                        <h6><i class="bi bi-moon-stars"></i> Sleep Data</h6>
                        <div class="sleep-detail-stats">
                            <div class="sleep-detail-stat">
                                <span class="sleep-detail-stat-value">${entry.sleep_data.duration}</span>
                                <div class="sleep-detail-stat-label">Duration</div>
                            </div>
                            <div class="sleep-detail-stat">
                                <span class="sleep-detail-stat-value">${entry.sleep_data.quality}/5</span>
                                <div class="sleep-detail-stat-label">Quality</div>
                            </div>
                            ${entry.sleep_data.efficiency ? `
                                <div class="sleep-detail-stat">
                                    <span class="sleep-detail-stat-value">${entry.sleep_data.efficiency}%</span>
                                    <div class="sleep-detail-stat-label">Efficiency</div>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;

        document.body.appendChild(popup);

        // Close on backdrop click
        backdrop.addEventListener('click', () => {
            popup.remove();
            backdrop.remove();
        });

        // Close on escape key
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                popup.remove();
                backdrop.remove();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
        } catch (error) {
            console.error('Error showing entry detail:', error);
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        // Fallback to meta tag
        const metaToken = document.querySelector('meta[name="csrf-token"]');
        return metaToken ? metaToken.getAttribute('content') : '';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.moodJournal = new MoodJournal();
    
    // Add some CSS animations via JavaScript
    const style = document.createElement('style');
    style.textContent = `
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; transform: translate(-50%, -50%); }
            to { opacity: 0; transform: translate(-50%, -60%); }
        }
        
        .mood-feedback-tooltip {
            pointer-events: none;
            white-space: nowrap;
        }
        
        .focused {
            transform: scale(1.02);
            transition: transform 0.3s ease;
        }
    `;
    document.head.appendChild(style);
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MoodJournal;
}