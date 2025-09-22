/**
 * Assessment functionality for psychological screening tools
 * Handles PHQ-9, GAD-7, and GHQ-12 assessments
 */

class PsychologicalAssessment {
    constructor() {
        this.completedAssessments = {
            phq9: false,
            gad7: false,
            ghq: false
        };
        this.scores = {
            phq9: null,
            gad7: null,
            ghq: null
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateProgress();
        
        // Check for crisis indicators in real-time
        this.setupCrisisDetection();
    }

    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('#assessmentTabs button').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.onTabSwitch(e.target);
            });
        });

        // Form input changes
        document.querySelectorAll('input[type="radio"]').forEach(input => {
            input.addEventListener('change', (e) => {
                this.onAnswerChange(e.target);
            });
        });

        // Prevent form submission until all assessments are complete
        document.getElementById('comprehensiveAssessmentForm').addEventListener('submit', (e) => {
            if (!this.allAssessmentsComplete()) {
                e.preventDefault();
                this.showIncompleteMessage();
            }
        });
    }

    setupCrisisDetection() {
        // Monitor PHQ-9 question 9 (self-harm) for immediate intervention
        document.querySelectorAll('input[name="phq9_q9"]').forEach(input => {
            input.addEventListener('change', (e) => {
                if (parseInt(e.target.value) > 0) {
                    this.showEmergencyAlert();
                }
            });
        });
    }

    onTabSwitch(tab) {
        // Update active states and validate current assessment
        const tabId = tab.getAttribute('data-bs-target').substring(1);
        
        // Save current assessment state if switching away
        if (tab.getAttribute('aria-selected') === 'true') {
            this.saveCurrentAssessmentState();
        }
    }

    onAnswerChange(input) {
        const assessmentType = this.getAssessmentType(input.name);
        this.validateAssessment(assessmentType);
        this.updateQuestionCount(assessmentType);
    }

    getAssessmentType(inputName) {
        if (inputName.startsWith('phq9_')) return 'phq9';
        if (inputName.startsWith('gad7_')) return 'gad7';
        if (inputName.startsWith('ghq_')) return 'ghq';
        return null;
    }

    validateAssessment(type) {
        const isComplete = this.checkAssessmentComplete(type);
        
        if (isComplete) {
            this.markAssessmentComplete(type);
            this.calculateScore(type);
        } else {
            this.markAssessmentIncomplete(type);
        }
        
        this.updateProgress();
    }

    checkAssessmentComplete(type) {
        let requiredQuestions = 0;
        let answeredQuestions = 0;

        switch (type) {
            case 'phq9':
                requiredQuestions = 9;
                for (let i = 1; i <= 9; i++) {
                    if (document.querySelector(`input[name="phq9_q${i}"]:checked`)) {
                        answeredQuestions++;
                    }
                }
                break;
            case 'gad7':
                requiredQuestions = 7;
                for (let i = 1; i <= 7; i++) {
                    if (document.querySelector(`input[name="gad7_q${i}"]:checked`)) {
                        answeredQuestions++;
                    }
                }
                break;
            case 'ghq':
                requiredQuestions = 12;
                for (let i = 1; i <= 12; i++) {
                    if (document.querySelector(`input[name="ghq_q${i}"]:checked`)) {
                        answeredQuestions++;
                    }
                }
                break;
        }

        return answeredQuestions === requiredQuestions;
    }

    markAssessmentComplete(type) {
        this.completedAssessments[type] = true;
        
        // Update status badge
        const statusBadge = document.querySelector(`.${type}-status`);
        if (statusBadge) {
            statusBadge.textContent = 'Complete';
            statusBadge.classList.remove('bg-secondary');
            statusBadge.classList.add('bg-success');
        }

        // Enable next tab if applicable
        this.enableNextTab(type);
    }

    markAssessmentIncomplete(type) {
        this.completedAssessments[type] = false;
        
        // Update status badge
        const statusBadge = document.querySelector(`.${type}-status`);
        if (statusBadge) {
            statusBadge.textContent = 'Pending';
            statusBadge.classList.remove('bg-success');
            statusBadge.classList.add('bg-secondary');
        }
    }

    enableNextTab(type) {
        const tabOrder = ['phq9', 'gad7', 'ghq'];
        const currentIndex = tabOrder.indexOf(type);
        
        if (currentIndex < tabOrder.length - 1) {
            const nextTab = tabOrder[currentIndex + 1];
            const nextTabButton = document.getElementById(`${nextTab}-tab`);
            if (nextTabButton) {
                nextTabButton.classList.remove('disabled');
            }
        }
    }

    calculateScore(type) {
        let score = 0;

        switch (type) {
            case 'phq9':
                for (let i = 1; i <= 9; i++) {
                    const checked = document.querySelector(`input[name="phq9_q${i}"]:checked`);
                    if (checked) {
                        score += parseInt(checked.value);
                    }
                }
                this.scores.phq9 = {
                    total: score,
                    severity: this.getPHQ9Severity(score)
                };
                break;

            case 'gad7':
                for (let i = 1; i <= 7; i++) {
                    const checked = document.querySelector(`input[name="gad7_q${i}"]:checked`);
                    if (checked) {
                        score += parseInt(checked.value);
                    }
                }
                this.scores.gad7 = {
                    total: score,
                    severity: this.getGAD7Severity(score)
                };
                break;

            case 'ghq':
                // GHQ-12 has reverse scoring for positive items
                const positiveItems = [1, 3, 4, 7, 8, 12];
                for (let i = 1; i <= 12; i++) {
                    const checked = document.querySelector(`input[name="ghq_q${i}"]:checked`);
                    if (checked) {
                        let value = parseInt(checked.value);
                        if (positiveItems.includes(i)) {
                            value = 3 - value; // Reverse score
                        }
                        score += value;
                    }
                }
                this.scores.ghq = {
                    total: score,
                    severity: this.getGHQRisk(score)
                };
                break;
        }

        console.log(`${type.toUpperCase()} Score:`, this.scores[type]);
    }

    getPHQ9Severity(score) {
        if (score <= 4) return 'minimal';
        if (score <= 9) return 'mild';
        if (score <= 14) return 'moderate';
        if (score <= 19) return 'moderately_severe';
        return 'severe';
    }

    getGAD7Severity(score) {
        if (score <= 4) return 'minimal';
        if (score <= 9) return 'mild';
        if (score <= 14) return 'moderate';
        return 'severe';
    }

    getGHQRisk(score) {
        if (score <= 15) return 'low_risk';
        if (score <= 20) return 'moderate_risk';
        return 'high_risk';
    }

    updateProgress() {
        const completed = Object.values(this.completedAssessments).filter(Boolean).length;
        const total = 3;
        const percentage = (completed / total) * 100;

        // Update progress bar
        const progressBar = document.getElementById('assessmentProgress');
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
        }

        // Update progress text
        const progressText = document.querySelector('.progress-text');
        if (progressText) {
            progressText.textContent = `${completed}/3 Complete`;
        }

        // Show final submit section if all complete
        if (this.allAssessmentsComplete()) {
            document.getElementById('finalSubmitSection').style.display = 'block';
            this.scrollToFinalSubmit();
        } else {
            document.getElementById('finalSubmitSection').style.display = 'none';
        }
    }

    updateQuestionCount(type) {
        const answeredCount = this.getAnsweredQuestionCount(type);
        const totalQuestions = this.getTotalQuestions(type);
        
        // Update question counter in tab if exists
        const tab = document.getElementById(`${type}-tab`);
        if (tab) {
            const counter = tab.querySelector('.question-counter');
            if (counter) {
                counter.textContent = `${answeredCount}/${totalQuestions}`;
            }
        }
    }

    getAnsweredQuestionCount(type) {
        let count = 0;
        const maxQuestions = this.getTotalQuestions(type);
        
        for (let i = 1; i <= maxQuestions; i++) {
            if (document.querySelector(`input[name="${type}_q${i}"]:checked`)) {
                count++;
            }
        }
        
        return count;
    }

    getTotalQuestions(type) {
        switch (type) {
            case 'phq9': return 9;
            case 'gad7': return 7;
            case 'ghq': return 12;
            default: return 0;
        }
    }

    allAssessmentsComplete() {
        return Object.values(this.completedAssessments).every(Boolean);
    }

    showIncompleteMessage() {
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning alert-dismissible fade show';
        alert.innerHTML = `
            <strong>Assessment Incomplete!</strong> 
            Please complete all three assessments before submitting.
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const form = document.getElementById('comprehensiveAssessmentForm');
        form.insertBefore(alert, form.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    showEmergencyAlert() {
        const emergencyAlert = document.getElementById('emergencyAlert');
        if (emergencyAlert) {
            emergencyAlert.style.display = 'block';
            emergencyAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    scrollToFinalSubmit() {
        setTimeout(() => {
            const finalSection = document.getElementById('finalSubmitSection');
            if (finalSection) {
                finalSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }, 500);
    }

    saveCurrentAssessmentState() {
        // Save to localStorage for persistence
        const assessmentData = {
            completedAssessments: this.completedAssessments,
            scores: this.scores,
            formData: this.getFormData()
        };
        
        localStorage.setItem('psychAssessmentState', JSON.stringify(assessmentData));
    }

    loadSavedState() {
        const saved = localStorage.getItem('psychAssessmentState');
        if (saved) {
            const data = JSON.parse(saved);
            this.completedAssessments = data.completedAssessments || this.completedAssessments;
            this.scores = data.scores || this.scores;
            
            // Restore form values
            this.restoreFormData(data.formData || {});
            this.updateProgress();
        }
    }

    getFormData() {
        const formData = {};
        const inputs = document.querySelectorAll('input[type="radio"]:checked');
        
        inputs.forEach(input => {
            formData[input.name] = input.value;
        });
        
        return formData;
    }

    restoreFormData(formData) {
        Object.entries(formData).forEach(([name, value]) => {
            const input = document.querySelector(`input[name="${name}"][value="${value}"]`);
            if (input) {
                input.checked = true;
            }
        });
    }

    getAssessmentResults() {
        return {
            phq9: this.scores.phq9,
            gad7: this.scores.gad7,
            ghq: this.scores.ghq,
            overallRisk: this.calculateOverallRisk()
        };
    }

    calculateOverallRisk() {
        const risks = [];
        
        if (this.scores.phq9) {
            const severity = this.scores.phq9.severity;
            if (['moderate', 'moderately_severe', 'severe'].includes(severity)) {
                risks.push('high');
            } else if (severity === 'mild') {
                risks.push('moderate');
            } else {
                risks.push('low');
            }
        }
        
        if (this.scores.gad7) {
            const severity = this.scores.gad7.severity;
            if (['moderate', 'severe'].includes(severity)) {
                risks.push('high');
            } else if (severity === 'mild') {
                risks.push('moderate');
            } else {
                risks.push('low');
            }
        }
        
        if (this.scores.ghq) {
            const risk = this.scores.ghq.severity;
            if (risk === 'high_risk') {
                risks.push('high');
            } else if (risk === 'moderate_risk') {
                risks.push('moderate');
            } else {
                risks.push('low');
            }
        }
        
        // Return highest risk level
        if (risks.includes('high')) return 'high';
        if (risks.includes('moderate')) return 'moderate';
        return 'low';
    }
}

// Individual assessment submission functions
function submitPHQ9() {
    if (assessment.checkAssessmentComplete('phq9')) {
        assessment.calculateScore('phq9');
        assessment.markAssessmentComplete('phq9');
        
        // Show success message
        showAssessmentSuccess('PHQ-9', assessment.scores.phq9);
        
        // Move to next tab
        const gad7Tab = new bootstrap.Tab(document.getElementById('gad7-tab'));
        gad7Tab.show();
    } else {
        showAssessmentError('PHQ-9');
    }
}

function submitGAD7() {
    if (assessment.checkAssessmentComplete('gad7')) {
        assessment.calculateScore('gad7');
        assessment.markAssessmentComplete('gad7');
        
        // Show success message
        showAssessmentSuccess('GAD-7', assessment.scores.gad7);
        
        // Move to next tab
        const ghqTab = new bootstrap.Tab(document.getElementById('ghq-tab'));
        ghqTab.show();
    } else {
        showAssessmentError('GAD-7');
    }
}

function submitGHQ() {
    if (assessment.checkAssessmentComplete('ghq')) {
        assessment.calculateScore('ghq');
        assessment.markAssessmentComplete('ghq');
        
        // Show success message
        showAssessmentSuccess('GHQ-12', assessment.scores.ghq);
    } else {
        showAssessmentError('GHQ-12');
    }
}

function showAssessmentSuccess(type, score) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show mt-3';
    alert.innerHTML = `
        <strong>${type} Complete!</strong> 
        Score: ${score.total} (${getSeverityLabel(score.severity)})
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const activeTab = document.querySelector('.tab-pane.active .assessment-footer');
    if (activeTab) {
        activeTab.appendChild(alert);
    }
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 3000);
}

function showAssessmentError(type) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-warning alert-dismissible fade show mt-3';
    alert.innerHTML = `
        <strong>Incomplete Assessment!</strong> 
        Please answer all questions in the ${type} assessment.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const activeTab = document.querySelector('.tab-pane.active .assessment-footer');
    if (activeTab) {
        activeTab.appendChild(alert);
    }
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function getSeverityLabel(severity) {
    const labels = {
        'minimal': 'Minimal',
        'mild': 'Mild',
        'moderate': 'Moderate', 
        'moderately_severe': 'Moderately Severe',
        'severe': 'Severe',
        'low_risk': 'Low Risk',
        'moderate_risk': 'Moderate Risk',
        'high_risk': 'High Risk'
    };
    
    return labels[severity] || severity;
}

// Initialize assessment when DOM is loaded
let assessment;
document.addEventListener('DOMContentLoaded', function() {
    assessment = new PsychologicalAssessment();
    assessment.loadSavedState();
});

// Save state before page unload
window.addEventListener('beforeunload', function() {
    if (assessment) {
        assessment.saveCurrentAssessmentState();
    }
});