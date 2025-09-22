// Firebase Assessments Service
import { 
    db, 
    collection, 
    doc, 
    getDocs, 
    addDoc, 
    updateDoc,
    query, 
    where, 
    orderBy, 
    limit,
    COLLECTIONS 
} from './firebase-config.js';

export class FirebaseAssessmentsService {
    
    // Get all active questionnaires
    async getQuestionnaires() {
        try {
            const q = query(
                collection(db, COLLECTIONS.QUESTIONNAIRES), 
                where("is_active", "==", true),
                orderBy("created_at", "desc")
            );
            
            const querySnapshot = await getDocs(q);
            const questionnaires = [];
            
            querySnapshot.forEach((doc) => {
                questionnaires.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            return questionnaires;
        } catch (error) {
            console.error('Error fetching questionnaires:', error);
            throw error;
        }
    }
    
    // Get a specific questionnaire by ID
    async getQuestionnaireById(questionnaireId) {
        try {
            const questionnaires = await this.getQuestionnaires();
            return questionnaires.find(q => q.id === questionnaireId);
        } catch (error) {
            console.error('Error fetching questionnaire:', error);
            throw error;
        }
    }
    
    // Start a new assessment
    async startAssessment(userId, questionnaireId) {
        try {
            const assessment = {
                user_id: userId || 'anonymous',
                questionnaire_id: questionnaireId,
                status: 'started',
                started_at: new Date().toISOString(),
                completed_at: null,
                total_score: null,
                severity_level: null,
                responses: []
            };
            
            const docRef = await addDoc(collection(db, COLLECTIONS.ASSESSMENTS), assessment);
            
            return {
                id: docRef.id,
                ...assessment
            };
        } catch (error) {
            console.error('Error starting assessment:', error);
            throw error;
        }
    }
    
    // Submit assessment responses
    async submitAssessment(assessmentId, responses, questionnaire) {
        try {
            // Calculate total score
            let totalScore = 0;
            responses.forEach(response => {
                totalScore += response.score;
            });
            
            // Determine severity level
            const severityLevel = this.calculateSeverityLevel(totalScore, questionnaire.scoring_ranges);
            
            // Update assessment
            const assessmentRef = doc(db, COLLECTIONS.ASSESSMENTS, assessmentId);
            const updateData = {
                status: 'completed',
                completed_at: new Date().toISOString(),
                total_score: totalScore,
                severity_level: severityLevel,
                responses: responses
            };
            
            await updateDoc(assessmentRef, updateData);
            
            // Generate recommendations based on results
            await this.generateRecommendations(assessmentId, severityLevel, questionnaire.questionnaire_type);
            
            return {
                id: assessmentId,
                totalScore,
                severityLevel,
                responses
            };
        } catch (error) {
            console.error('Error submitting assessment:', error);
            throw error;
        }
    }
    
    // Calculate severity level based on score
    calculateSeverityLevel(score, scoringRanges) {
        for (const [level, range] of Object.entries(scoringRanges)) {
            if (score >= range.min && score <= range.max) {
                return level;
            }
        }
        return 'unknown';
    }
    
    // Generate recommendations based on assessment results
    async generateRecommendations(assessmentId, severityLevel, assessmentType) {
        try {
            // Get all recommendations
            const recommendationsSnapshot = await getDocs(collection(db, COLLECTIONS.RECOMMENDATIONS));
            const allRecommendations = [];
            
            recommendationsSnapshot.forEach((doc) => {
                allRecommendations.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            // Filter recommendations based on severity and assessment type
            let filteredRecommendations = [];
            
            if (severityLevel === 'severe' || severityLevel === 'moderately_severe') {
                // High priority recommendations
                filteredRecommendations = allRecommendations.filter(rec => 
                    rec.urgency === 'high' || rec.category === 'Professional Help'
                );
            } else if (severityLevel === 'moderate') {
                // Medium priority recommendations
                filteredRecommendations = allRecommendations.filter(rec => 
                    rec.urgency === 'medium' || rec.urgency === 'high'
                );
            } else {
                // General wellness recommendations
                filteredRecommendations = allRecommendations.filter(rec => 
                    rec.urgency === 'low' || rec.urgency === 'medium'
                );
            }
            
            // Add assessment type specific recommendations
            if (assessmentType === 'SQI') {
                const sleepRecs = allRecommendations.filter(rec => 
                    rec.category.includes('Sleep') || rec.title.includes('Sleep')
                );
                filteredRecommendations = [...filteredRecommendations, ...sleepRecs];
            }
            
            // Remove duplicates and limit to top 5
            const uniqueRecommendations = filteredRecommendations
                .filter((rec, index, self) => index === self.findIndex(r => r.id === rec.id))
                .slice(0, 5);
            
            // Create user recommendations
            for (const rec of uniqueRecommendations) {
                const userRecommendation = {
                    user_id: 'anonymous', // Replace with actual user ID
                    recommendation_id: rec.id,
                    assessment_id: assessmentId,
                    status: 'not_started',
                    suggested_at: new Date().toISOString(),
                    completed_at: null,
                    rating: null
                };
                
                await addDoc(collection(db, COLLECTIONS.USER_RECOMMENDATIONS), userRecommendation);
            }
            
        } catch (error) {
            console.error('Error generating recommendations:', error);
            throw error;
        }
    }
    
    // Get user's assessment history
    async getUserAssessments(userId = 'anonymous') {
        try {
            const q = query(
                collection(db, COLLECTIONS.ASSESSMENTS),
                where("user_id", "==", userId),
                orderBy("started_at", "desc")
            );
            
            const querySnapshot = await getDocs(q);
            const assessments = [];
            
            querySnapshot.forEach((doc) => {
                assessments.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            return assessments;
        } catch (error) {
            console.error('Error fetching user assessments:', error);
            throw error;
        }
    }
    
    // Get assessment results by ID
    async getAssessmentResults(assessmentId) {
        try {
            const assessments = await getDocs(collection(db, COLLECTIONS.ASSESSMENTS));
            let assessment = null;
            
            assessments.forEach((doc) => {
                if (doc.id === assessmentId) {
                    assessment = {
                        id: doc.id,
                        ...doc.data()
                    };
                }
            });
            
            if (!assessment) {
                throw new Error('Assessment not found');
            }
            
            // Get related questionnaire
            const questionnaire = await this.getQuestionnaireById(assessment.questionnaire_id);
            
            // Calculate additional metrics
            const scorePercentage = questionnaire ? (assessment.total_score / questionnaire.max_score * 100) : 0;
            const averagePerQuestion = assessment.responses?.length ? (assessment.total_score / assessment.responses.length) : 0;
            
            return {
                ...assessment,
                questionnaire,
                score_percentage: scorePercentage,
                average_per_question: averagePerQuestion
            };
        } catch (error) {
            console.error('Error fetching assessment results:', error);
            throw error;
        }
    }
    
    // Get dashboard statistics
    async getDashboardStats() {
        try {
            const assessments = await getDocs(collection(db, COLLECTIONS.ASSESSMENTS));
            const stats = {
                total_assessments: 0,
                completed_assessments: 0,
                severity_distribution: {},
                assessment_types: {},
                completion_rate: 0
            };
            
            assessments.forEach((doc) => {
                const assessment = doc.data();
                stats.total_assessments++;
                
                if (assessment.status === 'completed') {
                    stats.completed_assessments++;
                    
                    // Count severity levels
                    if (assessment.severity_level) {
                        stats.severity_distribution[assessment.severity_level] = 
                            (stats.severity_distribution[assessment.severity_level] || 0) + 1;
                    }
                }
            });
            
            stats.completion_rate = stats.total_assessments > 0 ? 
                Math.round((stats.completed_assessments / stats.total_assessments) * 100) : 0;
            
            return stats;
        } catch (error) {
            console.error('Error fetching dashboard stats:', error);
            throw error;
        }
    }
}

// Export singleton instance
export const assessmentsService = new FirebaseAssessmentsService();