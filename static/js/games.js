// Games.js - Interactive mental health games functionality

class GamesManager {
    constructor() {
        this.currentGame = null;
        this.gameModal = null;
        this.init();
    }

    init() {
        // Initialize Bootstrap modal
        this.gameModal = new bootstrap.Modal(document.getElementById('gameModal'));
        
        // Add fade-in animation to cards
        this.animateCards();
        
        // Initialize progress tracking
        this.loadProgress();
    }

    animateCards() {
        const cards = document.querySelectorAll('.game-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    }

    loadProgress() {
        // Load user progress from localStorage (in a real app, this would be from the backend)
        const progress = JSON.parse(localStorage.getItem('gamesProgress')) || {
            gamesPlayed: 0,
            minutesPracticed: 0,
            streakDays: 0,
            achievementLevel: 'Beginner'
        };

        // Update progress display
        document.querySelectorAll('.progress-text')[0].textContent = progress.gamesPlayed;
        document.querySelectorAll('.progress-text')[1].textContent = progress.minutesPracticed;
        document.querySelectorAll('.progress-text')[2].textContent = progress.streakDays;
        document.querySelectorAll('.progress-text')[3].textContent = this.getAchievementEmoji(progress.achievementLevel);
    }

    getAchievementEmoji(level) {
        const levels = {
            'Beginner': '🌱',
            'Explorer': '🌿',
            'Practitioner': '🌳',
            'Master': '🏆',
            'Zen': '✨'
        };
        return levels[level] || '🌱';
    }

    updateProgress(gameType, minutes = 1) {
        const progress = JSON.parse(localStorage.getItem('gamesProgress')) || {
            gamesPlayed: 0,
            minutesPracticed: 0,
            streakDays: 0,
            achievementLevel: 'Beginner'
        };

        progress.gamesPlayed += 1;
        progress.minutesPracticed += minutes;
        
        // Update achievement level based on games played
        if (progress.gamesPlayed >= 50) progress.achievementLevel = 'Zen';
        else if (progress.gamesPlayed >= 25) progress.achievementLevel = 'Master';
        else if (progress.gamesPlayed >= 10) progress.achievementLevel = 'Practitioner';
        else if (progress.gamesPlayed >= 5) progress.achievementLevel = 'Explorer';

        localStorage.setItem('gamesProgress', JSON.stringify(progress));
        this.loadProgress();
    }

    showModal(title, content) {
        document.getElementById('gameModalLabel').textContent = title;
        document.getElementById('gameModalBody').innerHTML = content;
        this.gameModal.show();
    }

    closeModal() {
        this.gameModal.hide();
    }
}

// Game implementations
class BreathingGame {
    constructor(manager) {
        this.manager = manager;
        this.isRunning = false;
        this.cycle = 'inhale';
        this.cycleCount = 0;
        this.maxCycles = 5;
    }

    start() {
        const content = `
            <div class="game-interface">
                <h4>Breathing Garden</h4>
                <p>Follow the breathing circle to practice the 4-7-8 breathing technique.</p>
                <div class="breathing-circle" id="breathingCircle">
                    <div class="breathing-text" id="breathingText">Get Ready</div>
                </div>
                <div class="breathing-instructions">
                    <p><strong>Inhale</strong> for 4 seconds, <strong>Hold</strong> for 7 seconds, <strong>Exhale</strong> for 8 seconds</p>
                </div>
                <div class="breathing-progress">
                    <p>Cycle: <span id="cycleCounter">0</span> / ${this.maxCycles}</p>
                </div>
            </div>
        `;

        this.manager.showModal('Breathing Garden', content);
        
        setTimeout(() => this.startBreathing(), 1000);
    }

    startBreathing() {
        this.isRunning = true;
        this.cycleCount = 0;
        this.breathingCycle();
    }

    breathingCycle() {
        if (!this.isRunning || this.cycleCount >= this.maxCycles) {
            this.completeGame();
            return;
        }

        const circle = document.getElementById('breathingCircle');
        const text = document.getElementById('breathingText');
        const counter = document.getElementById('cycleCounter');

        // Inhale phase (4 seconds)
        text.textContent = 'Inhale';
        circle.classList.remove('exhale');
        circle.classList.add('inhale');

        setTimeout(() => {
            // Hold phase (7 seconds)
            text.textContent = 'Hold';
            
            setTimeout(() => {
                // Exhale phase (8 seconds)
                text.textContent = 'Exhale';
                circle.classList.remove('inhale');
                circle.classList.add('exhale');
                
                setTimeout(() => {
                    this.cycleCount++;
                    counter.textContent = this.cycleCount;
                    
                    if (this.cycleCount < this.maxCycles) {
                        text.textContent = 'Rest';
                        setTimeout(() => this.breathingCycle(), 2000);
                    } else {
                        this.breathingCycle();
                    }
                }, 8000);
            }, 7000);
        }, 4000);
    }

    completeGame() {
        const text = document.getElementById('breathingText');
        const circle = document.getElementById('breathingCircle');
        
        text.textContent = 'Well Done!';
        circle.classList.remove('inhale', 'exhale');
        circle.classList.add('pulse');
        
        this.manager.updateProgress('breathing', 5);
        
        setTimeout(() => {
            this.manager.closeModal();
            this.showCompletionMessage();
        }, 3000);
    }

    showCompletionMessage() {
        // You could show a toast notification here
        console.log('Breathing exercise completed!');
    }
}

class MoodGame {
    constructor(manager) {
        this.manager = manager;
        this.selectedMood = null;
        this.moodHistory = JSON.parse(localStorage.getItem('moodHistory')) || [];
    }

    start() {
        const moods = [
            { emoji: '😊', label: 'Happy', value: 5, color: '#4CAF50' },
            { emoji: '😌', label: 'Calm', value: 4, color: '#2196F3' },
            { emoji: '😐', label: 'Neutral', value: 3, color: '#9E9E9E' },
            { emoji: '😔', label: 'Sad', value: 2, color: '#FF9800' },
            { emoji: '😰', label: 'Anxious', value: 1, color: '#F44336' }
        ];

        const moodButtons = moods.map(mood => `
            <div class="mood-option" onclick="moodGame.selectMood(${mood.value}, '${mood.label}', '${mood.emoji}', '${mood.color}')">
                <div class="mood-emoji">${mood.emoji}</div>
                <div class="mood-label">${mood.label}</div>
            </div>
        `).join('');

        const content = `
            <div class="game-interface">
                <h4>Mood Constellation</h4>
                <p>How are you feeling right now? Select your current mood to add a star to your constellation.</p>
                <div class="mood-selector">
                    ${moodButtons}
                </div>
                <div id="moodResult" class="mood-result" style="display: none;">
                    <h5>Thank you for sharing!</h5>
                    <p>Your mood has been added to your personal constellation.</p>
                    <div class="constellation-preview">
                        <canvas id="constellationCanvas" width="300" height="200"></canvas>
                    </div>
                </div>
            </div>
            <style>
                .mood-selector { display: flex; justify-content: space-around; flex-wrap: wrap; margin: 2rem 0; }
                .mood-option { cursor: pointer; text-align: center; padding: 1rem; border-radius: 10px; transition: all 0.3s ease; }
                .mood-option:hover { background: #f0f0f0; transform: scale(1.05); }
                .mood-emoji { font-size: 3rem; margin-bottom: 0.5rem; }
                .mood-label { font-weight: 500; }
                .constellation-preview { margin-top: 1rem; text-align: center; }
                #constellationCanvas { border: 1px solid #ddd; border-radius: 10px; }
            </style>
        `;

        this.manager.showModal('Mood Constellation', content);
    }

    selectMood(value, label, emoji, color) {
        this.selectedMood = { value, label, emoji, color, timestamp: new Date() };
        this.moodHistory.push(this.selectedMood);
        localStorage.setItem('moodHistory', JSON.stringify(this.moodHistory));

        document.querySelector('.mood-selector').style.display = 'none';
        document.getElementById('moodResult').style.display = 'block';

        this.drawConstellation();
        this.manager.updateProgress('mood', 2);

        setTimeout(() => {
            this.manager.closeModal();
        }, 4000);
    }

    drawConstellation() {
        const canvas = document.getElementById('constellationCanvas');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.fillStyle = '#1a1a2e';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw stars for recent moods
        const recentMoods = this.moodHistory.slice(-10); // Last 10 moods
        
        recentMoods.forEach((mood, index) => {
            const x = (index + 1) * (canvas.width / (recentMoods.length + 1));
            const y = canvas.height - (mood.value * 30) - 20;
            
            // Draw star
            ctx.fillStyle = mood.color;
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fill();
            
            // Connect stars
            if (index > 0) {
                const prevX = index * (canvas.width / (recentMoods.length + 1));
                const prevY = canvas.height - (recentMoods[index - 1].value * 30) - 20;
                
                ctx.strokeStyle = '#4a4a6a';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(prevX, prevY);
                ctx.lineTo(x, y);
                ctx.stroke();
            }
        });
    }
}

class GratitudeGame {
    constructor(manager) {
        this.manager = manager;
        this.gratitudeEntries = JSON.parse(localStorage.getItem('gratitudeEntries')) || [];
    }

    start() {
        const content = `
            <div class="game-interface">
                <h4>Gratitude Tree</h4>
                <p>Add something you're grateful for today to help your tree grow.</p>
                <div class="gratitude-input">
                    <textarea id="gratitudeText" placeholder="I am grateful for..." maxlength="200" rows="3"></textarea>
                    <div class="char-counter">
                        <span id="charCount">0</span>/200 characters
                    </div>
                    <button class="btn btn-primary mt-2" onclick="gratitudeGame.addGratitude()">Add to Tree</button>
                </div>
                <div id="gratitudeResult" class="gratitude-result" style="display: none;">
                    <div class="tree-container">
                        <div class="tree">🌳</div>
                        <div class="gratitude-count">
                            <p><strong>${this.gratitudeEntries.length + 1}</strong> gratitudes in your tree</p>
                        </div>
                    </div>
                    <div class="recent-gratitudes">
                        <h6>Recent Gratitudes:</h6>
                        <ul id="recentList"></ul>
                    </div>
                </div>
            </div>
            <style>
                .gratitude-input textarea { width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 10px; resize: none; }
                .char-counter { text-align: right; color: #666; margin-top: 0.5rem; }
                .tree-container { text-align: center; margin: 2rem 0; }
                .tree { font-size: 4rem; margin-bottom: 1rem; animation: bounce 2s infinite; }
                @keyframes bounce { 0%, 20%, 50%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(-10px); } 60% { transform: translateY(-5px); } }
                .recent-gratitudes ul { list-style: none; padding: 0; }
                .recent-gratitudes li { background: #f8f9fa; padding: 0.5rem 1rem; margin: 0.5rem 0; border-radius: 20px; border-left: 4px solid var(--primary-color); }
            </style>
        `;

        this.manager.showModal('Gratitude Tree', content);

        // Add character counter
        document.getElementById('gratitudeText').addEventListener('input', (e) => {
            document.getElementById('charCount').textContent = e.target.value.length;
        });
    }

    addGratitude() {
        const text = document.getElementById('gratitudeText').value.trim();
        if (!text) {
            alert('Please enter something you\'re grateful for.');
            return;
        }

        const gratitude = {
            text: text,
            timestamp: new Date(),
            id: Date.now()
        };

        this.gratitudeEntries.push(gratitude);
        localStorage.setItem('gratitudeEntries', JSON.stringify(this.gratitudeEntries));

        document.querySelector('.gratitude-input').style.display = 'none';
        document.getElementById('gratitudeResult').style.display = 'block';

        // Show recent gratitudes
        const recentList = document.getElementById('recentList');
        const recent = this.gratitudeEntries.slice(-3).reverse();
        recentList.innerHTML = recent.map(g => `<li>${g.text}</li>`).join('');

        this.manager.updateProgress('gratitude', 3);

        setTimeout(() => {
            this.manager.closeModal();
        }, 5000);
    }
}

class WorryStoneGame {
    constructor(manager) {
        this.manager = manager;
        this.polishCount = 0;
        this.maxPolish = 10;
    }

    start() {
        const content = `
            <div class="game-interface">
                <h4>Digital Worry Stone</h4>
                <p>Think of a worry, then "polish" the stone by clicking on it. With each polish, try to reframe your worry more positively.</p>
                <div class="worry-input">
                    <textarea id="worryText" placeholder="What's worrying you today?" maxlength="200" rows="3"></textarea>
                    <button class="btn btn-primary mt-2" onclick="worryStoneGame.startPolishing()">Start Polishing</button>
                </div>
                <div id="polishingArea" class="polishing-area" style="display: none;">
                    <div class="worry-stone" id="worryStone" onclick="worryStoneGame.polish()">
                        <div class="stone-shine"></div>
                    </div>
                    <div class="polish-progress">
                        <p>Polish count: <span id="polishCount">0</span>/${this.maxPolish}</p>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                        </div>
                    </div>
                    <div class="reframing-text" id="reframingText">
                        Click the stone to begin transforming your worry...
                    </div>
                </div>
            </div>
            <style>
                .worry-input textarea { width: 100%; padding: 1rem; border: 2px solid #ddd; border-radius: 10px; resize: none; }
                .worry-stone { width: 150px; height: 100px; background: linear-gradient(45deg, #8e8e93, #c7c7cc); border-radius: 50px; margin: 2rem auto; cursor: pointer; position: relative; transition: all 0.3s ease; box-shadow: inset -5px -5px 10px rgba(0,0,0,0.3), inset 5px 5px 10px rgba(255,255,255,0.5); }
                .worry-stone:hover { transform: scale(1.05); }
                .worry-stone:active { transform: scale(0.95); }
                .stone-shine { position: absolute; top: 20%; left: 30%; width: 30px; height: 15px; background: rgba(255,255,255,0.6); border-radius: 50%; opacity: 0; transition: opacity 0.3s ease; }
                .worry-stone.polished .stone-shine { opacity: 1; }
                .progress-bar { width: 100%; height: 10px; background: #ddd; border-radius: 5px; overflow: hidden; margin: 1rem 0; }
                .progress-fill { height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); width: 0%; transition: width 0.5s ease; }
                .reframing-text { background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 1rem; font-style: italic; border-left: 4px solid var(--primary-color); }
            </style>
        `;

        this.manager.showModal('Digital Worry Stone', content);
    }

    startPolishing() {
        const worryText = document.getElementById('worryText').value.trim();
        if (!worryText) {
            alert('Please enter a worry to work with.');
            return;
        }

        this.currentWorry = worryText;
        this.polishCount = 0;
        
        document.querySelector('.worry-input').style.display = 'none';
        document.getElementById('polishingArea').style.display = 'block';
    }

    polish() {
        this.polishCount++;
        const stone = document.getElementById('worryStone');
        const progressFill = document.getElementById('progressFill');
        const polishCountSpan = document.getElementById('polishCount');
        const reframingText = document.getElementById('reframingText');

        // Update UI
        polishCountSpan.textContent = this.polishCount;
        progressFill.style.width = `${(this.polishCount / this.maxPolish) * 100}%`;
        stone.classList.add('polished');

        // Show reframing prompts
        const reframingPrompts = [
            "What's one small step you could take to address this worry?",
            "Is this worry about something within your control?",
            "What would you tell a friend who had this same worry?",
            "What's the worst that could realistically happen? How would you cope?",
            "Can you find any opportunities or learning in this situation?",
            "What are three things going well in your life right now?",
            "How might you feel about this worry a year from now?",
            "What strengths do you have that could help with this situation?",
            "Is there a way to reframe this worry as a preference rather than a need?",
            "You've transformed your worry into wisdom. Well done!"
        ];

        if (this.polishCount <= reframingPrompts.length) {
            reframingText.textContent = reframingPrompts[this.polishCount - 1];
        }

        // Complete the exercise
        if (this.polishCount >= this.maxPolish) {
            setTimeout(() => {
                this.completeExercise();
            }, 2000);
        }

        // Remove polished class for next click
        setTimeout(() => {
            stone.classList.remove('polished');
        }, 300);
    }

    completeExercise() {
        this.manager.updateProgress('worry_stone', 4);
        setTimeout(() => {
            this.manager.closeModal();
        }, 3000);
    }
}

class MemoryPalaceGame {
    constructor(manager) {
        this.manager = manager;
    }

    start() {
        const content = `
            <div class="game-interface">
                <h4>Mindful Memory Palace</h4>
                <p>Create your personal safe space. Choose elements to build a calming environment you can return to anytime.</p>
                <div class="palace-builder">
                    <div class="scene" id="scene">
                        <div class="sky" id="sky">🌅</div>
                        <div class="ground" id="ground">🌿</div>
                        <div class="elements" id="elements"></div>
                    </div>
                    <div class="element-chooser">
                        <h6>Add to your space:</h6>
                        <div class="element-options">
                            <span class="element-option" onclick="memoryPalaceGame.addElement('🌳', 'tree')">🌳 Tree</span>
                            <span class="element-option" onclick="memoryPalaceGame.addElement('🏡', 'house')">🏡 House</span>
                            <span class="element-option" onclick="memoryPalaceGame.addElement('🌸', 'flowers')">🌸 Flowers</span>
                            <span class="element-option" onclick="memoryPalaceGame.addElement('🦋', 'butterfly')">🦋 Butterfly</span>
                            <span class="element-option" onclick="memoryPalaceGame.addElement('💎', 'crystal')">💎 Crystal</span>
                            <span class="element-option" onclick="memoryPalaceGame.addElement('🌊', 'water')">🌊 Water</span>
                        </div>
                        <button class="btn btn-primary mt-3" onclick="memoryPalaceGame.saveScene()">Save My Safe Space</button>
                    </div>
                </div>
            </div>
            <style>
                .scene { background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; min-height: 200px; position: relative; text-align: center; }
                .sky { font-size: 2rem; position: absolute; top: 10px; right: 20px; }
                .ground { font-size: 1.5rem; position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); }
                .elements { position: absolute; inset: 0; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-around; padding: 1rem; }
                .element-options { display: flex; flex-wrap: wrap; gap: 1rem; margin: 1rem 0; }
                .element-option { background: #f8f9fa; padding: 0.5rem 1rem; border-radius: 20px; cursor: pointer; transition: all 0.3s ease; border: 2px solid transparent; }
                .element-option:hover { background: var(--primary-color); color: white; transform: scale(1.05); }
                .scene-element { font-size: 2rem; margin: 0.5rem; animation: fadeIn 0.5s ease-in; cursor: pointer; }
                .scene-element:hover { transform: scale(1.2); }
            </style>
        `;

        this.manager.showModal('Mindful Memory Palace', content);
        this.elements = [];
    }

    addElement(emoji, type) {
        if (this.elements.length >= 6) {
            alert('Your safe space is complete! You can save it now.');
            return;
        }

        const element = document.createElement('div');
        element.className = 'scene-element';
        element.textContent = emoji;
        element.title = type;
        
        document.getElementById('elements').appendChild(element);
        this.elements.push({ emoji, type });
    }

    saveScene() {
        const scenes = JSON.parse(localStorage.getItem('memoryPalaceScenes')) || [];
        const newScene = {
            id: Date.now(),
            elements: this.elements,
            createdAt: new Date(),
            name: `Safe Space ${scenes.length + 1}`
        };

        scenes.push(newScene);
        localStorage.setItem('memoryPalaceScenes', JSON.stringify(scenes));

        alert('Your safe space has been saved! You can return to it anytime.');
        this.manager.updateProgress('memory_palace', 5);
        
        setTimeout(() => {
            this.manager.closeModal();
        }, 2000);
    }
}

// Initialize games when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.gamesManager = new GamesManager();
    window.breathingGame = new BreathingGame(gamesManager);
    window.moodGame = new MoodGame(gamesManager);
    window.gratitudeGame = new GratitudeGame(gamesManager);
    window.worryStoneGame = new WorryStoneGame(gamesManager);
    window.memoryPalaceGame = new MemoryPalaceGame(gamesManager);
});

// Game launcher functions
function startBreathingGame() {
    breathingGame.start();
}

function startMoodGame() {
    moodGame.start();
}

function startGratitudeGame() {
    gratitudeGame.start();
}

function startWorryStoneGame() {
    worryStoneGame.start();
}

function startMemoryPalaceGame() {
    memoryPalaceGame.start();
}