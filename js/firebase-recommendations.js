// Firebase Recommendations Service
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

export class FirebaseRecommendationsService {
    
    // Get all active recommendations
    async getRecommendations() {
        try {
            const q = query(
                collection(db, COLLECTIONS.RECOMMENDATIONS), 
                where("is_active", "==", true),
                orderBy("created_at", "desc")
            );
            
            const querySnapshot = await getDocs(q);
            const recommendations = [];
            
            querySnapshot.forEach((doc) => {
                recommendations.push({
                    id: doc.id,
                    ...doc.data()
                });
            });
            
            return recommendations;
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            throw error;
        }
    }
    
    // Get user's personalized recommendations
    async getUserRecommendations(userId = 'anonymous', filters = {}) {
        try {
            let q = query(
                collection(db, COLLECTIONS.USER_RECOMMENDATIONS),
                where("user_id", "==", userId),
                orderBy("suggested_at", "desc")
            );
            
            const querySnapshot = await getDocs(q);
            const userRecommendations = [];
            
            // Get all recommendations first
            const allRecommendations = await this.getRecommendations();
            const recommendationsMap = {};
            allRecommendations.forEach(rec => {
                recommendationsMap[rec.id] = rec;
            });
            
            querySnapshot.forEach((doc) => {
                const userRec = doc.data();
                const recommendation = recommendationsMap[userRec.recommendation_id];
                
                if (recommendation) {
                    userRecommendations.push({
                        id: doc.id,
                        ...userRec,
                        recommendation: recommendation
                    });
                }
            });
            
            // Apply filters
            let filteredRecommendations = userRecommendations;
            
            if (filters.status && filters.status !== 'all') {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.status === filters.status
                );
            }
            
            if (filters.urgency) {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.recommendation.urgency === filters.urgency
                );
            }
            
            if (filters.category) {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.recommendation.category === filters.category
                );
            }
            
            return filteredRecommendations;
        } catch (error) {
            console.error('Error fetching user recommendations:', error);
            throw error;
        }
    }
    
    // Get recommendations for a specific assessment
    async getRecommendationsForAssessment(assessmentId) {
        try {
            const q = query(
                collection(db, COLLECTIONS.USER_RECOMMENDATIONS),
                where("assessment_id", "==", assessmentId),
                orderBy("suggested_at", "desc")
            );
            
            const querySnapshot = await getDocs(q);
            const userRecommendations = [];
            
            // Get all recommendations first
            const allRecommendations = await this.getRecommendations();
            const recommendationsMap = {};
            allRecommendations.forEach(rec => {
                recommendationsMap[rec.id] = rec;
            });
            
            querySnapshot.forEach((doc) => {
                const userRec = doc.data();
                const recommendation = recommendationsMap[userRec.recommendation_id];
                
                if (recommendation) {
                    userRecommendations.push({
                        id: doc.id,
                        ...userRec,
                        recommendation: recommendation
                    });
                }
            });
            
            // Group by category
            const groupedRecommendations = {};
            userRecommendations.forEach(rec => {
                const category = rec.recommendation.category;
                if (!groupedRecommendations[category]) {
                    groupedRecommendations[category] = [];
                }
                groupedRecommendations[category].push(rec);
            });
            
            return {
                recommendations: userRecommendations,
                grouped: groupedRecommendations,
                stats: {
                    total: userRecommendations.length,
                    urgent: userRecommendations.filter(r => r.recommendation.urgency === 'high').length,
                    categories: Object.keys(groupedRecommendations).length,
                    total_duration: userRecommendations.reduce((sum, r) => sum + (r.recommendation.duration_minutes || 0), 0)
                }
            };
        } catch (error) {
            console.error('Error fetching recommendations for assessment:', error);
            throw error;
        }
    }
    
    // Update recommendation status
    async updateRecommendationStatus(userRecommendationId, status, rating = null) {
        try {
            const userRecRef = doc(db, COLLECTIONS.USER_RECOMMENDATIONS, userRecommendationId);
            const updateData = {
                status: status
            };
            
            if (status === 'completed') {
                updateData.completed_at = new Date().toISOString();
            }
            
            if (rating !== null) {
                updateData.rating = rating;
            }
            
            await updateDoc(userRecRef, updateData);
            
            return { success: true };
        } catch (error) {
            console.error('Error updating recommendation status:', error);
            throw error;
        }
    }
    
    // Bookmark a recommendation
    async bookmarkRecommendation(userId, recommendationId) {
        try {
            const bookmark = {
                user_id: userId || 'anonymous',
                recommendation_id: recommendationId,
                bookmarked_at: new Date().toISOString()
            };
            
            const docRef = await addDoc(collection(db, 'bookmarks'), bookmark);
            
            return {
                id: docRef.id,
                ...bookmark
            };
        } catch (error) {
            console.error('Error bookmarking recommendation:', error);
            throw error;
        }
    }
    
    // Get recommendation statistics
    async getRecommendationStats(userId = 'anonymous') {
        try {
            const userRecommendations = await this.getUserRecommendations(userId);
            
            const stats = {
                total: userRecommendations.length,
                completed: userRecommendations.filter(r => r.status === 'completed').length,
                in_progress: userRecommendations.filter(r => r.status === 'in_progress').length,
                not_started: userRecommendations.filter(r => r.status === 'not_started').length,
                high_priority: userRecommendations.filter(r => r.recommendation.urgency === 'high').length,
                categories: {}
            };
            
            // Count by category
            userRecommendations.forEach(rec => {
                const category = rec.recommendation.category;
                stats.categories[category] = (stats.categories[category] || 0) + 1;
            });
            
            stats.completion_rate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0;
            
            return stats;
        } catch (error) {
            console.error('Error fetching recommendation stats:', error);
            throw error;
        }
    }
    
    // Get recommendation categories
    async getRecommendationCategories() {
        try {
            const recommendations = await this.getRecommendations();
            const categories = [...new Set(recommendations.map(rec => rec.category))];
            return categories;
        } catch (error) {
            console.error('Error fetching recommendation categories:', error);
            throw error;
        }
    }
    
    // Search recommendations
    async searchRecommendations(searchTerm, filters = {}) {
        try {
            const recommendations = await this.getRecommendations();
            
            let filteredRecommendations = recommendations;
            
            // Text search
            if (searchTerm) {
                const searchLower = searchTerm.toLowerCase();
                filteredRecommendations = filteredRecommendations.filter(rec =>
                    rec.title.toLowerCase().includes(searchLower) ||
                    rec.description.toLowerCase().includes(searchLower) ||
                    rec.category.toLowerCase().includes(searchLower)
                );
            }
            
            // Apply filters
            if (filters.category) {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.category === filters.category
                );
            }
            
            if (filters.urgency) {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.urgency === filters.urgency
                );
            }
            
            if (filters.duration) {
                filteredRecommendations = filteredRecommendations.filter(
                    rec => rec.duration_minutes <= filters.duration
                );
            }
            
            return filteredRecommendations;
        } catch (error) {
            console.error('Error searching recommendations:', error);
            throw error;
        }
    }
    
    // Generate personalized recommendations based on user profile
    async generatePersonalizedRecommendations(userId, userProfile) {
        try {
            const allRecommendations = await this.getRecommendations();
            let personalizedRecommendations = [];
            
            // Filter based on user profile
            if (userProfile.primary_concerns) {
                userProfile.primary_concerns.forEach(concern => {
                    const relevant = allRecommendations.filter(rec =>
                        rec.title.toLowerCase().includes(concern.toLowerCase()) ||
                        rec.description.toLowerCase().includes(concern.toLowerCase()) ||
                        rec.category.toLowerCase().includes(concern.toLowerCase())
                    );
                    personalizedRecommendations = [...personalizedRecommendations, ...relevant];
                });
            }
            
            // Add general wellness recommendations
            const generalWellness = allRecommendations.filter(rec =>
                rec.urgency === 'low' && 
                !personalizedRecommendations.some(p => p.id === rec.id)
            );
            personalizedRecommendations = [...personalizedRecommendations, ...generalWellness.slice(0, 3)];
            
            // Remove duplicates
            personalizedRecommendations = personalizedRecommendations.filter(
                (rec, index, self) => index === self.findIndex(r => r.id === rec.id)
            );
            
            // Create user recommendations
            for (const rec of personalizedRecommendations) {
                const userRecommendation = {
                    user_id: userId,
                    recommendation_id: rec.id,
                    assessment_id: null,
                    status: 'not_started',
                    suggested_at: new Date().toISOString(),
                    completed_at: null,
                    rating: null,
                    source: 'personalized'
                };
                
                await addDoc(collection(db, COLLECTIONS.USER_RECOMMENDATIONS), userRecommendation);
            }
            
            return personalizedRecommendations;
        } catch (error) {
            console.error('Error generating personalized recommendations:', error);
            throw error;
        }
    }
}

// Export singleton instance
export const recommendationsService = new FirebaseRecommendationsService();