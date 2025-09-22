// Firebase Configuration and Initialization
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-analytics.js";
import { getFirestore, collection, doc, getDocs, addDoc, updateDoc, deleteDoc, query, where, orderBy, limit } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-firestore.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-storage.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBFCfyGCNWATIx5StSZ-1ILtOCIWcPHWVw",
    authDomain: "mentalproject-e569a.firebaseapp.com",
    projectId: "mentalproject-e569a",
    storageBucket: "mentalproject-e569a.firebasestorage.app",
    messagingSenderId: "856443071962",
    appId: "1:856443071962:web:1a8842e3f1e15614fd64e3",
    measurementId: "G-PFE3N8PMH9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
const auth = getAuth(app);
const storage = getStorage(app);

// Export Firebase services for use in other modules
export {
    db,
    auth,
    storage,
    analytics,
    // Firestore functions
    collection,
    doc,
    getDocs,
    addDoc,
    updateDoc,
    deleteDoc,
    query,
    where,
    orderBy,
    limit,
    // Auth functions
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    // Storage functions
    ref,
    uploadBytes,
    getDownloadURL
};

// Database Collections Structure
export const COLLECTIONS = {
    USERS: 'users',
    QUESTIONNAIRES: 'questionnaires',
    ASSESSMENTS: 'assessments',
    RECOMMENDATIONS: 'recommendations',
    USER_RECOMMENDATIONS: 'userRecommendations',
    DASHBOARD_METRICS: 'dashboardMetrics',
    DASHBOARD_ALERTS: 'dashboardAlerts'
};

// Initialize sample data if needed
export async function initializeSampleData() {
    try {
        // Check if questionnaires exist
        const questionnairesSnapshot = await getDocs(collection(db, COLLECTIONS.QUESTIONNAIRES));
        
        if (questionnairesSnapshot.empty) {
            console.log('Initializing sample questionnaires...');
            await createSampleQuestionnaires();
        }
        
        // Check if recommendations exist
        const recommendationsSnapshot = await getDocs(collection(db, COLLECTIONS.RECOMMENDATIONS));
        
        if (recommendationsSnapshot.empty) {
            console.log('Initializing sample recommendations...');
            await createSampleRecommendations();
        }
        
    } catch (error) {
        console.error('Error initializing sample data:', error);
    }
}

// Create sample questionnaires
async function createSampleQuestionnaires() {
    const questionnaires = [
        {
            title: "PHQ-9 Depression Assessment",
            questionnaire_type: "PHQ9",
            description: "A reliable and validated 9-question instrument for screening, diagnosing, monitoring and measuring the severity of depression.",
            instructions: "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            is_active: true,
            created_at: new Date().toISOString(),
            max_score: 27,
            scoring_ranges: {
                minimal: { min: 0, max: 4, description: "Minimal depression" },
                mild: { min: 5, max: 9, description: "Mild depression" },
                moderate: { min: 10, max: 14, description: "Moderate depression" },
                moderately_severe: { min: 15, max: 19, description: "Moderately severe depression" },
                severe: { min: 20, max: 27, description: "Severe depression" }
            },
            questions: [
                {
                    text: "Little interest or pleasure in doing things",
                    order: 1,
                    choices: [
                        { text: "Not at all", score: 0, order: 1 },
                        { text: "Several days", score: 1, order: 2 },
                        { text: "More than half the days", score: 2, order: 3 },
                        { text: "Nearly every day", score: 3, order: 4 }
                    ]
                },
                {
                    text: "Feeling down, depressed, or hopeless",
                    order: 2,
                    choices: [
                        { text: "Not at all", score: 0, order: 1 },
                        { text: "Several days", score: 1, order: 2 },
                        { text: "More than half the days", score: 2, order: 3 },
                        { text: "Nearly every day", score: 3, order: 4 }
                    ]
                },
                {
                    text: "Trouble falling or staying asleep, or sleeping too much",
                    order: 3,
                    choices: [
                        { text: "Not at all", score: 0, order: 1 },
                        { text: "Several days", score: 1, order: 2 },
                        { text: "More than half the days", score: 2, order: 3 },
                        { text: "Nearly every day", score: 3, order: 4 }
                    ]
                }
            ]
        },
        {
            title: "GAD-7 Anxiety Assessment",
            questionnaire_type: "GAD7",
            description: "A reliable and validated 7-question instrument for screening and measuring the severity of generalized anxiety disorder.",
            instructions: "Over the last 2 weeks, how often have you been bothered by the following problems?",
            is_active: true,
            created_at: new Date().toISOString(),
            max_score: 21,
            scoring_ranges: {
                minimal: { min: 0, max: 4, description: "Minimal anxiety" },
                mild: { min: 5, max: 9, description: "Mild anxiety" },
                moderate: { min: 10, max: 14, description: "Moderate anxiety" },
                severe: { min: 15, max: 21, description: "Severe anxiety" }
            },
            questions: [
                {
                    text: "Feeling nervous, anxious, or on edge",
                    order: 1,
                    choices: [
                        { text: "Not at all", score: 0, order: 1 },
                        { text: "Several days", score: 1, order: 2 },
                        { text: "More than half the days", score: 2, order: 3 },
                        { text: "Nearly every day", score: 3, order: 4 }
                    ]
                },
                {
                    text: "Not being able to stop or control worrying",
                    order: 2,
                    choices: [
                        { text: "Not at all", score: 0, order: 1 },
                        { text: "Several days", score: 1, order: 2 },
                        { text: "More than half the days", score: 2, order: 3 },
                        { text: "Nearly every day", score: 3, order: 4 }
                    ]
                }
            ]
        },
        {
            title: "Sleep Quality Index",
            questionnaire_type: "SQI",
            description: "An assessment to evaluate your sleep patterns and quality of rest.",
            instructions: "Please answer the following questions about your sleep patterns over the past month.",
            is_active: true,
            created_at: new Date().toISOString(),
            max_score: 15,
            scoring_ranges: {
                excellent: { min: 0, max: 3, description: "Excellent sleep quality" },
                good: { min: 4, max: 6, description: "Good sleep quality" },
                fair: { min: 7, max: 9, description: "Fair sleep quality" },
                poor: { min: 10, max: 15, description: "Poor sleep quality" }
            },
            questions: [
                {
                    text: "How would you rate your sleep quality overall?",
                    order: 1,
                    choices: [
                        { text: "Very good", score: 0, order: 1 },
                        { text: "Fairly good", score: 1, order: 2 },
                        { text: "Fairly bad", score: 2, order: 3 },
                        { text: "Very bad", score: 3, order: 4 }
                    ]
                }
            ]
        }
    ];
    
    for (const questionnaire of questionnaires) {
        await addDoc(collection(db, COLLECTIONS.QUESTIONNAIRES), questionnaire);
    }
}

// Create sample recommendations
async function createSampleRecommendations() {
    const recommendations = [
        {
            title: "Sleep Hygiene Routine",
            description: "Establish a consistent bedtime routine to improve sleep quality and duration.",
            category: "Sleep & Wellness",
            urgency: "medium",
            duration_minutes: 30,
            instructions: "Create a calming pre-sleep routine: dim lights 1 hour before bed, avoid screens, practice relaxation techniques.",
            resources: ["Sleep hygiene guide", "Bedtime routine checklist"],
            is_active: true,
            created_at: new Date().toISOString()
        },
        {
            title: "Mindfulness Meditation",
            description: "Daily mindfulness practice to reduce anxiety and improve emotional regulation.",
            category: "Mindfulness & Meditation",
            urgency: "low",
            duration_minutes: 15,
            instructions: "Start with 5-10 minutes daily. Use guided meditations or focus on breath awareness.",
            resources: ["Mindfulness app recommendations", "Breathing exercises guide"],
            is_active: true,
            created_at: new Date().toISOString()
        },
        {
            title: "Professional Counseling",
            description: "Connect with a licensed mental health professional for personalized support.",
            category: "Professional Help",
            urgency: "high",
            duration_minutes: 60,
            instructions: "Schedule an appointment with a counselor. Prepare questions and concerns beforehand.",
            resources: ["Counseling center contact", "How to prepare for therapy"],
            is_active: true,
            created_at: new Date().toISOString()
        },
        {
            title: "Daily Physical Activity",
            description: "Regular exercise to boost mood and reduce symptoms of depression and anxiety.",
            category: "Physical Health",
            urgency: "medium",
            duration_minutes: 30,
            instructions: "Aim for 30 minutes of moderate activity daily. Start small and gradually increase.",
            resources: ["Exercise routines for mental health", "Campus gym information"],
            is_active: true,
            created_at: new Date().toISOString()
        },
        {
            title: "Social Connection",
            description: "Build and maintain supportive relationships to improve mental wellbeing.",
            category: "Social Support",
            urgency: "low",
            duration_minutes: 60,
            instructions: "Reach out to friends, join clubs, or participate in group activities regularly.",
            resources: ["Campus clubs directory", "Social skills tips"],
            is_active: true,
            created_at: new Date().toISOString()
        },
        {
            title: "Stress Management Techniques",
            description: "Learn and practice effective strategies for managing academic and life stress.",
            category: "Stress Management",
            urgency: "medium",
            duration_minutes: 20,
            instructions: "Practice deep breathing, time management, and healthy coping strategies.",
            resources: ["Stress management workbook", "Time management tools"],
            is_active: true,
            created_at: new Date().toISOString()
        }
    ];
    
    for (const recommendation of recommendations) {
        await addDoc(collection(db, COLLECTIONS.RECOMMENDATIONS), recommendation);
    }
}

console.log('Firebase initialized successfully!');