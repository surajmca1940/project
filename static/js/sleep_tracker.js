// Sleep Tracker JavaScript - Comprehensive sleep tracking functionality

class SleepTracker {
    constructor() {
        this.form = document.getElementById('sleepForm');
        this.submitBtn = document.getElementById('submitSleepBtn');
        this.notesTextarea = document.getElementById('notes');
        this.charCount = document.getElementById('noteCharCount');
        this.sleepChart = null;
        this.currentAudio = null;
        this.sleepTimer = null;
        this.timerDuration = 0;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFormDefaults();
        this.setupCharacterCounter();
        this.setupAnimations();
        this.initializeSleepChart();
        this.initializeAudioControls();
        this.setupSleepJournalView();
    }

    setupEventListeners() {
        // Form submission
        if (this.form) {
            this.form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });
        }

        // Character counter for notes
        if (this.notesTextarea) {
            this.notesTextarea.addEventListener('input', (e) => {
                this.updateCharacterCount(e.target.value.length);
            });
        }

        // Sleep date default to today
        const sleepDateInput = document.getElementById('sleep_date');
        if (sleepDateInput && !sleepDateInput.value) {
            sleepDateInput.value = new Date().toISOString().split('T')[0];
        }

        // Calculate duration when times change
        const bedtimeInput = document.getElementById('bedtime');
        const waketimeInput = document.getElementById('wake_time');
        
        if (bedtimeInput && waketimeInput) {
            bedtimeInput.addEventListener('change', () => this.calculateDuration());
            waketimeInput.addEventListener('change', () => this.calculateDuration());
        }

        // Quality selector interactions
        const qualityOptions = document.querySelectorAll('.quality-option input[type="radio"]');
        qualityOptions.forEach(option => {
            option.addEventListener('change', (e) => {
                this.handleQualitySelection(e.target.value);
            });
        });
    }

    setupFormDefaults() {
        // Set default sleep date to yesterday (since people usually log sleep in the morning)
        const sleepDateInput = document.getElementById('sleep_date');
        if (sleepDateInput && !sleepDateInput.value) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            sleepDateInput.value = yesterday.toISOString().split('T')[0];
        }
    }

    setupCharacterCounter() {
        if (this.notesTextarea && this.charCount) {
            this.updateCharacterCount(this.notesTextarea.value.length);
        }
    }

    setupAnimations() {
        // Fade in cards on page load
        const cards = document.querySelectorAll('.sleep-entry-card, .sleep-chart-card, .ai-insights-card, .sleep-sounds-card, .recent-entries-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 150);
        });

        // Animate insight items
        const insightItems = document.querySelectorAll('.insight-item');
        insightItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('scale-in');
            }, (index * 100) + 500);
        });
    }

    calculateDuration() {
        const bedtime = document.getElementById('bedtime').value;
        const waketime = document.getElementById('wake_time').value;
        
        if (bedtime && waketime) {
            const bedtimeDate = new Date(`2000-01-01 ${bedtime}`);
            let waketimeDate = new Date(`2000-01-01 ${waketime}`);
            
            // Handle sleep across midnight
            if (waketimeDate < bedtimeDate) {
                waketimeDate.setDate(waketimeDate.getDate() + 1);
            }
            
            const durationMs = waketimeDate - bedtimeDate;
            const durationHours = durationMs / (1000 * 60 * 60);
            
            // Show duration feedback
            this.showDurationFeedback(durationHours);
        }
    }

    showDurationFeedback(hours) {
        // Remove any existing duration feedback
        const existingFeedback = document.querySelector('.duration-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Create duration feedback element
        const feedback = document.createElement('div');
        feedback.className = 'duration-feedback alert alert-info mt-2';
        feedback.innerHTML = `
            <i class="bi bi-clock"></i>
            <strong>Sleep Duration:</strong> ${hours.toFixed(1)} hours
            ${this.getDurationAdvice(hours)}
        `;

        // Insert after wake time input
        const waketimeGroup = document.getElementById('wake_time').closest('.col-md-6');
        waketimeGroup.appendChild(feedback);

        // Add fade in animation
        feedback.classList.add('fade-in');
    }

    getDurationAdvice(hours) {
        if (hours < 6) {
            return '<br><small class="text-warning">⚠️ This seems quite short. Most adults need 7-9 hours.</small>';
        } else if (hours >= 6 && hours < 7) {
            return '<br><small class="text-info">💤 A bit short, but some people do well with 6-7 hours.</small>';
        } else if (hours >= 7 && hours <= 9) {
            return '<br><small class="text-success">✅ Great! This is in the recommended range for most adults.</small>';
        } else if (hours > 9 && hours <= 10) {
            return '<br><small class="text-info">💤 A bit long, but fine if you feel rested.</small>';
        } else {
            return '<br><small class="text-warning">⚠️ This seems quite long. Consider sleep quality factors.</small>';
        }
    }

    handleQualitySelection(quality) {
        // Add visual feedback for quality selection
        const qualityInt = parseInt(quality);
        const feedbackMessages = {
            1: '😔 Sorry to hear you had such poor sleep. Let\'s work on improving it.',
            2: '😟 Poor sleep can be frustrating. Consider our recommendations below.',
            3: '😐 Fair sleep - there\'s definitely room for improvement.',
            4: '😊 Good sleep! Keep up the healthy habits.',
            5: '🌟 Excellent sleep! You\'re doing great!'
        };

        this.showQualityFeedback(feedbackMessages[qualityInt]);
    }

    showQualityFeedback(message) {
        // Remove existing feedback
        const existingFeedback = document.querySelector('.quality-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Create feedback tooltip
        const feedback = document.createElement('div');
        feedback.className = 'quality-feedback alert alert-light mt-2';
        feedback.innerHTML = message;

        // Insert after quality selector
        const qualitySelector = document.querySelector('.quality-selector');
        qualitySelector.parentNode.insertBefore(feedback, qualitySelector.nextSibling);

        // Add fade in animation and auto-remove
        feedback.classList.add('fade-in');
        setTimeout(() => {
            if (feedback.parentNode) {
                feedback.remove();
            }
        }, 4000);
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

    handleFormSubmit(e) {
        e.preventDefault();
        
        if (this.isSubmitting) return;
        
        // Validate required fields
        const requiredFields = ['sleep_date', 'bedtime', 'wake_time', 'quality'];
        let isValid = true;
        
        for (const fieldName of requiredFields) {
            const field = document.querySelector(`[name="${fieldName}"]`);
            if (fieldName === 'quality') {
                const qualitySelected = document.querySelector('[name="quality"]:checked');
                if (!qualitySelected) {
                    this.showValidationError('Please select your sleep quality.');
                    isValid = false;
                    break;
                }
            } else if (!field || !field.value.trim()) {
                this.showValidationError(`Please fill in the ${fieldName.replace('_', ' ')}.`);
                field?.focus();
                isValid = false;
                break;
            }
        }
        
        if (!isValid) return;
        
        // Show loading state
        this.setSubmittingState(true);
        
        // Submit form
        this.form.submit();
    }

    showValidationError(message) {
        // Remove existing error
        const existingError = document.querySelector('.validation-error');
        if (existingError) {
            existingError.remove();
        }

        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'validation-error alert alert-danger';
        errorDiv.innerHTML = `<i class="bi bi-exclamation-triangle"></i> ${message}`;
        
        // Insert at top of form
        this.form.insertBefore(errorDiv, this.form.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
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
            this.submitBtn.innerHTML = '<i class="bi bi-moon-stars-fill"></i> Log Sleep';
            this.form.classList.remove('loading');
        }
    }

    initializeSleepChart() {
        const chartCanvas = document.getElementById('sleepChart');
        if (!chartCanvas || typeof chartData === 'undefined' || !chartData.labels.length) {
            return;
        }

        const ctx = chartCanvas.getContext('2d');
        
        this.sleepChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [
                    {
                        label: 'Sleep Duration (hours)',
                        data: chartData.duration_data,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        yAxisID: 'y',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Sleep Quality (1-5)',
                        data: chartData.quality_data,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        yAxisID: 'y1',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Sleep Duration (hours)'
                        },
                        min: 0,
                        max: 12,
                        ticks: {
                            stepSize: 1
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Sleep Quality (1-5)'
                        },
                        min: 0,
                        max: 5,
                        ticks: {
                            stepSize: 1
                        },
                        grid: {
                            drawOnChartArea: false,
                        },
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Sleep Patterns Over Time'
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            afterBody: function(context) {
                                const dataIndex = context[0].dataIndex;
                                const bedtime = chartData.bedtime_data[dataIndex];
                                const efficiency = chartData.efficiency_data[dataIndex];
                                
                                let tooltip = '';
                                if (bedtime) {
                                    const hours = Math.floor(bedtime);
                                    const minutes = Math.floor((bedtime - hours) * 60);
                                    tooltip += `Bedtime: ${hours}:${minutes.toString().padStart(2, '0')}\n`;
                                }
                                if (efficiency) {
                                    tooltip += `Sleep Efficiency: ${efficiency.toFixed(1)}%`;
                                }
                                return tooltip;
                            }
                        }
                    }
                }
            }
        });
    }

    initializeAudioControls() {
        // Sleep sounds functionality
        const playButtons = document.querySelectorAll('.play-btn');
        const stopButton = document.getElementById('stopBtn');
        const volumeSlider = document.getElementById('volumeSlider');
        const sleepTimerSelect = document.getElementById('sleepTimer');
        const audioControls = document.getElementById('audioControls');
        const nowPlayingTitle = document.getElementById('nowPlayingTitle');

        playButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const soundType = button.getAttribute('data-sound');
                this.playSound(soundType);
            });
        });

        if (stopButton) {
            stopButton.addEventListener('click', () => {
                this.stopSound();
            });
        }

        if (volumeSlider) {
            volumeSlider.addEventListener('input', (e) => {
                this.setVolume(e.target.value / 100);
            });
        }

        if (sleepTimerSelect) {
            sleepTimerSelect.addEventListener('change', (e) => {
                this.setSleepTimer(parseInt(e.target.value));
            });
        }
    }

    playSound(soundType) {
        // Stop current sound if playing
        this.stopSound();

        // Get audio element (in production, these would be actual audio files)
        const audioElement = document.getElementById(`${soundType}Audio`);
        if (!audioElement) {
            console.warn(`Audio element for ${soundType} not found`);
            return;
        }

        // Since we're using placeholder audio, let's simulate the sound playing
        this.simulateSoundPlayback(soundType);
    }

    simulateSoundPlayback(soundType) {
        // In production, this would actually play the audio
        // For demo purposes, we'll simulate it with visual feedback
        
        const soundTitles = {
            rain: 'Gentle Rain',
            ocean: 'Ocean Waves',
            whitenoise: 'White Noise',
            forest: 'Forest Night'
        };

        // Update UI to show playing state
        const soundCards = document.querySelectorAll('.sound-card');
        soundCards.forEach(card => {
            card.classList.remove('active');
            const button = card.querySelector('.play-btn');
            button.innerHTML = '<i class="bi bi-play-fill"></i> Play';
        });

        // Mark current sound as active
        const currentSoundCard = document.querySelector(`[data-sound="${soundType}"]`);
        if (currentSoundCard) {
            currentSoundCard.classList.add('active');
            const button = currentSoundCard.querySelector('.play-btn');
            button.innerHTML = '<i class="bi bi-pause-fill"></i> Playing';
        }

        // Show audio controls
        const audioControls = document.getElementById('audioControls');
        const nowPlayingTitle = document.getElementById('nowPlayingTitle');
        
        if (audioControls) {
            audioControls.style.display = 'block';
            audioControls.classList.add('fade-in');
        }
        
        if (nowPlayingTitle) {
            nowPlayingTitle.textContent = soundTitles[soundType];
        }

        // Store current sound reference
        this.currentSound = soundType;
    }

    stopSound() {
        if (this.currentSound) {
            // Reset all sound cards
            const soundCards = document.querySelectorAll('.sound-card');
            soundCards.forEach(card => {
                card.classList.remove('active');
                const button = card.querySelector('.play-btn');
                button.innerHTML = '<i class="bi bi-play-fill"></i> Play';
            });

            // Hide audio controls
            const audioControls = document.getElementById('audioControls');
            if (audioControls) {
                audioControls.style.display = 'none';
            }

            // Clear sleep timer
            if (this.sleepTimer) {
                clearTimeout(this.sleepTimer);
                this.sleepTimer = null;
            }

            this.currentSound = null;
        }
    }

    setVolume(volume) {
        // In production, this would set the actual audio volume
        console.log(`Setting volume to ${Math.round(volume * 100)}%`);
        
        // Visual feedback
        const volumeSlider = document.getElementById('volumeSlider');
        if (volumeSlider) {
            const percentage = Math.round(volume * 100);
            volumeSlider.title = `Volume: ${percentage}%`;
        }
    }

    setSleepTimer(minutes) {
        // Clear existing timer
        if (this.sleepTimer) {
            clearTimeout(this.sleepTimer);
            this.sleepTimer = null;
        }

        if (minutes > 0 && this.currentSound) {
            this.timerDuration = minutes;
            this.sleepTimer = setTimeout(() => {
                this.stopSound();
                this.showTimerNotification();
            }, minutes * 60 * 1000);

            console.log(`Sleep timer set for ${minutes} minutes`);
        }
    }

    showTimerNotification() {
        const notification = document.createElement('div');
        notification.className = 'alert alert-info sleep-timer-notification';
        notification.innerHTML = `
            <i class="bi bi-clock"></i>
            <strong>Sleep Timer:</strong> Sound stopped automatically after ${this.timerDuration} minutes.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);
        notification.classList.add('fade-in');

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    setupSleepJournalView() {
        // Initialize calendar
        this.currentDate = new Date();
        this.currentYear = this.currentDate.getFullYear();
        this.currentMonth = this.currentDate.getMonth();
        this.sleepEntries = new Map(); // Store entries by date
        
        // Setup View Sleep Journal button functionality
        const viewSleepJournalBtn = document.getElementById('viewSleepJournalBtn');
        if (viewSleepJournalBtn) {
            viewSleepJournalBtn.addEventListener('click', () => {
                this.loadSleepJournalEntries();
            });
        }

        // Setup modal event listeners
        const sleepJournalModal = document.getElementById('sleepJournalModal');
        if (sleepJournalModal) {
            sleepJournalModal.addEventListener('shown.bs.modal', () => {
                this.loadSleepJournalEntries();
            });
        }

        // Setup navigation buttons
        const sleepPrevMonthBtn = document.getElementById('sleepPrevMonthBtn');
        const sleepNextMonthBtn = document.getElementById('sleepNextMonthBtn');

        if (sleepPrevMonthBtn) {
            sleepPrevMonthBtn.addEventListener('click', () => {
                this.navigateSleepMonth(-1);
            });
        }

        if (sleepNextMonthBtn) {
            sleepNextMonthBtn.addEventListener('click', () => {
                this.navigateSleepMonth(1);
            });
        }
    }

    navigateSleepMonth(direction) {
        this.currentMonth += direction;
        if (this.currentMonth > 11) {
            this.currentMonth = 0;
            this.currentYear++;
        } else if (this.currentMonth < 0) {
            this.currentMonth = 11;
            this.currentYear--;
        }
        this.renderSleepCalendar();
    }

    async loadSleepJournalEntries() {
        const loadingDiv = document.getElementById('sleepJournalLoading');
        const calendarDiv = document.getElementById('sleepJournalCalendar');
        const noEntriesDiv = document.getElementById('noSleepJournalEntries');

        // Show loading state
        loadingDiv.style.display = 'block';
        calendarDiv.style.display = 'none';
        noEntriesDiv.style.display = 'none';

        try {
            const response = await fetch('/api/sleep-journal-entries/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load sleep journal entries');
            }

            const data = await response.json();
            
            // Hide loading
            loadingDiv.style.display = 'none';

            if (data.entries && data.entries.length > 0) {
                console.log('Sleep journal entries:', data.entries);
                this.processSleepEntries(data.entries);
                
                // Navigate to the month with the most recent entry
                if (data.entries.length > 0) {
                    const mostRecentDate = data.entries[0].sleep_date; // Entries are ordered by newest first
                    const dateParts = mostRecentDate.split('-');
                    this.currentYear = parseInt(dateParts[0]);
                    this.currentMonth = parseInt(dateParts[1]) - 1; // JavaScript months are 0-based
                    console.log('Navigating to month with sleep entries:', this.currentMonth, this.currentYear);
                }
                
                this.renderSleepCalendar();
                calendarDiv.style.display = 'block';
            } else {
                console.log('No sleep journal entries found');
                noEntriesDiv.style.display = 'block';
            }

        } catch (error) {
            console.error('Error loading sleep journal entries:', error);
            loadingDiv.style.display = 'none';
            
            // Show error state
            calendarDiv.innerHTML = `
                <div class="text-center py-4" style="padding: 3rem;">
                    <div class="mb-3">
                        <i class="bi bi-exclamation-triangle" style="font-size: 3rem; color: #dc3545;"></i>
                    </div>
                    <h5 class="text-danger">Error loading sleep calendar</h5>
                    <p class="text-muted">Please try again later.</p>
                    <button class="btn btn-outline-primary" onclick="sleepTracker.loadSleepJournalEntries()">
                        <i class="bi bi-arrow-clockwise"></i> Retry
                    </button>
                </div>
            `;
            calendarDiv.style.display = 'block';
        }
    }

    processSleepEntries(entries) {
        this.sleepEntries.clear();
        entries.forEach(entry => {
            const date = entry.sleep_date; // Use sleep_date which has YYYY-MM-DD format
            this.sleepEntries.set(date, entry);
        });
    }

    renderSleepCalendar() {
        const monthYearElement = document.getElementById('sleepCurrentMonthYear');
        const calendarGrid = document.getElementById('sleepCalendarGrid');

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
            const dateCell = this.createSleepDateCell(dayNum, true, false);
            calendarGrid.appendChild(dateCell);
        }

        // Add current month's days
        for (let day = 1; day <= daysInMonth; day++) {
            const dateStr = `${this.currentYear}-${String(this.currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const isToday = dateStr === todayStr;
            const hasEntry = this.sleepEntries.has(dateStr);
            const entry = hasEntry ? this.sleepEntries.get(dateStr) : null;
            
            const dateCell = this.createSleepDateCell(day, false, isToday, hasEntry, entry);
            calendarGrid.appendChild(dateCell);
        }

        // Add next month's leading days to fill the grid
        const totalCells = calendarGrid.children.length - 7; // Minus day headers
        const remainingCells = 42 - totalCells; // 6 weeks * 7 days
        for (let day = 1; day <= remainingCells; day++) {
            const dateCell = this.createSleepDateCell(day, true, false);
            calendarGrid.appendChild(dateCell);
        }
    }

    createSleepDateCell(day, isOtherMonth, isToday, hasEntry = false, entry = null) {
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
            // Add sleep quality-specific color class
            const sleepClass = this.getSleepQualityColorClass(entry.quality);
            dateCell.className += ` ${sleepClass}`;
        }

        const dateNumber = document.createElement('span');
        dateNumber.className = 'calendar-date-number';
        dateNumber.textContent = day;
        dateCell.appendChild(dateNumber);

        // Add click handler for dates with entries
        if (hasEntry) {
            dateCell.style.cursor = 'pointer';
            dateCell.addEventListener('click', () => {
                this.showSleepEntryDetail(entry);
            });
        }

        return dateCell;
    }

    getSleepQualityColorClass(quality) {
        const qualityColors = {
            5: 'sleep-excellent',
            4: 'sleep-good',
            3: 'sleep-fair',
            2: 'sleep-poor',
            1: 'sleep-very-poor'
        };
        return qualityColors[quality] || 'sleep-fair';
    }

    showSleepEntryDetail(entry) {
        // Create backdrop that goes over the modal
        const backdrop = document.createElement('div');
        backdrop.className = 'popup-backdrop';
        backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
        document.body.appendChild(backdrop);

        // Create popup
        const popup = document.createElement('div');
        popup.className = 'entry-detail-popup';
        
        // Generate quality stars
        const qualityStars = entry.quality_stars.map((filled, i) => 
            `<span class="sleep-quality-star ${filled ? 'filled' : ''}">★</span>`
        ).join('');
        
        // Generate sleep factors
        const sleepFactors = entry.sleep_factors.map(factor => 
            `<span class="sleep-factor ${factor.type}">${factor.name}</span>`
        ).join('');
        
        popup.innerHTML = `
            <div class="entry-detail-header">
                <button class="entry-detail-close" onclick="this.closest('.entry-detail-popup').remove(); document.querySelectorAll('.popup-backdrop').forEach(el => el.remove());">
                    <i class="bi bi-x-lg"></i>
                </button>
                <div class="entry-detail-date">${entry.sleep_date_formatted}</div>
                <div class="entry-detail-time">${entry.relative_time}</div>
            </div>
            <div class="entry-detail-body">
                <div class="entry-detail-sleep">
                    <div class="entry-detail-sleep-quality">${entry.quality_label} Sleep</div>
                    <div class="entry-detail-sleep-duration">${entry.duration_formatted}</div>
                </div>
                
                <!-- Sleep Quality Stars -->
                <div class="sleep-quality-indicator text-center mb-3">
                    <div class="sleep-quality-stars">${qualityStars}</div>
                </div>
                
                <!-- Sleep Times -->
                <div class="sleep-detail-stats">
                    <div class="sleep-detail-stat">
                        <span class="sleep-detail-stat-value">${entry.bedtime}</span>
                        <div class="sleep-detail-stat-label">Bedtime</div>
                    </div>
                    <div class="sleep-detail-stat">
                        <span class="sleep-detail-stat-value">${entry.wake_time}</span>
                        <div class="sleep-detail-stat-label">Wake Time</div>
                    </div>
                    ${entry.sleep_efficiency ? `
                        <div class="sleep-detail-stat">
                            <span class="sleep-detail-stat-value">${entry.sleep_efficiency.toFixed(0)}%</span>
                            <div class="sleep-detail-stat-label">Efficiency</div>
                        </div>
                    ` : ''}
                    ${entry.times_woken !== null ? `
                        <div class="sleep-detail-stat">
                            <span class="sleep-detail-stat-value">${entry.times_woken}</span>
                            <div class="sleep-detail-stat-label">Times Woken</div>
                        </div>
                    ` : ''}
                </div>
                
                ${entry.notes ? `
                    <div class="entry-detail-note">
                        ${this.escapeHtml(entry.notes)}
                    </div>
                ` : ''}
                
                ${sleepFactors ? `
                    <div class="sleep-factors">
                        ${sleepFactors}
                        ${entry.feeling_rested ? '<span class="sleep-factor positive">✓ Felt Rested</span>' : '<span class="sleep-factor negative">✗ Didn\'t Feel Rested</span>'}
                    </div>
                ` : ''}
                
                ${entry.mood_data ? `
                    <div class="entry-detail-mood-data">
                        <h6><i class="bi bi-emoji-smile"></i> Mood That Day</h6>
                        <div class="mood-detail-info">
                            <span class="mood-detail-emoji">${entry.mood_data.emoji}</span>
                            <span class="mood-detail-label">${entry.mood_data.label}</span>
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

// Sleep insights helper functions
class SleepInsights {
    static generateWeeklyInsights(entries) {
        if (!entries || entries.length < 3) {
            return null;
        }

        const avgDuration = entries.reduce((sum, entry) => sum + entry.duration_hours, 0) / entries.length;
        const avgQuality = entries.reduce((sum, entry) => sum + entry.quality, 0) / entries.length;
        
        return {
            averageDuration: avgDuration.toFixed(1),
            averageQuality: avgQuality.toFixed(1),
            consistency: this.calculateConsistency(entries),
            trends: this.identifyTrends(entries)
        };
    }

    static calculateConsistency(entries) {
        const durations = entries.map(entry => entry.duration_hours);
        const mean = durations.reduce((sum, d) => sum + d, 0) / durations.length;
        const variance = durations.reduce((sum, d) => sum + Math.pow(d - mean, 2), 0) / durations.length;
        const standardDeviation = Math.sqrt(variance);
        
        if (standardDeviation < 0.5) return 'Very Consistent';
        if (standardDeviation < 1) return 'Consistent';
        if (standardDeviation < 1.5) return 'Somewhat Variable';
        return 'Highly Variable';
    }

    static identifyTrends(entries) {
        // Simple trend analysis
        const recentEntries = entries.slice(0, 3);
        const olderEntries = entries.slice(-3);
        
        const recentAvgQuality = recentEntries.reduce((sum, e) => sum + e.quality, 0) / recentEntries.length;
        const olderAvgQuality = olderEntries.reduce((sum, e) => sum + e.quality, 0) / olderEntries.length;
        
        if (recentAvgQuality > olderAvgQuality + 0.5) return 'Improving';
        if (recentAvgQuality < olderAvgQuality - 0.5) return 'Declining';
        return 'Stable';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.sleepTracker = new SleepTracker();
    
    // Add CSS animations dynamically
    const style = document.createElement('style');
    style.textContent = `
        .sleep-timer-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        
        .duration-feedback, .quality-feedback {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .validation-error {
            animation: shake 0.5s ease-in-out;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SleepTracker, SleepInsights };
}