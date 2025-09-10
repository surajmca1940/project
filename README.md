# Digital Psychological Intervention System

## Overview

The Digital Psychological Intervention System is a comprehensive web-based and mobile application designed to address the growing mental health challenges among college students. This system provides scalable, stigma-free psychological intervention tools specifically tailored for higher education institutions.

## Problem Statement

### Context
Mental health issues among college students have significantly increased in recent years, including:
- Anxiety and depression
- Academic burnout
- Sleep disorders
- Academic stress
- Social isolation

There is a major gap in the availability, accessibility, and stigma-free delivery of mental health support in most higher education institutions, especially in rural and semi-urban colleges.

### Current Challenges
- Absence of structured, scalable, and stigma-free psychological intervention systems
- Lack of early detection and preventive mental health tools
- Under-utilization of college counselling centres due to fear of judgment or lack of awareness
- No centralized mental health monitoring or data-driven policy framework within institutions

## Features

### 1. AI-Guided First-Aid Support
- Interactive chatbot offering coping strategies
- Intelligent triage system for professional referrals
- 24/7 availability for immediate support

### 2. Confidential Booking System
- Secure appointment scheduling with on-campus counsellors
- Integration with mental health helplines
- Anonymous booking options

### 3. Psychoeducational Resource Hub
- Mental wellness guides in regional languages
- Relaxation audio and meditation resources
- Educational videos and interactive content

### 4. Peer Support Platform
- Moderated peer-to-peer support forums
- Trained student volunteer network
- Anonymous group discussions

### 5. Admin Dashboard
- Anonymous data analytics for trend recognition
- Policy planning tools for administrators
- Real-time monitoring and reporting

## Technology Stack

### Frontend
- React.js with TypeScript
- Material-UI for consistent design
- PWA capabilities for mobile experience

### Backend
- Node.js with Express.js
- MongoDB for data storage
- Socket.io for real-time communication

### Additional Technologies
- Docker for containerization
- JWT for authentication
- OpenAI API for AI chatbot functionality

## Project Structure

```
# Digital Psychological Intervention System

A comprehensive web-based mental health platform designed specifically for higher education institutions to provide accessible, stigma-free psychological support to college students.

## 🎯 Project Overview

### Problem Statement

Mental health issues among college students have significantly increased, including anxiety, depression, burnout, sleep disorders, academic stress, and social isolation. However, there is a major gap in the availability, accessibility, and stigma-free delivery of mental health support in most higher education institutions, especially in rural and semi-urban colleges.

### Solution

This Digital Psychological Intervention System provides:

1. **AI-guided First-Aid Support** - Interactive chatbot offering coping strategies and professional referrals
2. **Confidential Booking System** - Anonymous appointment scheduling with campus counselors
3. **Psychoeducational Resource Hub** - Videos, audio content, and wellness guides in regional languages
4. **Peer Support Platform** - Moderated peer-to-peer support forum with trained volunteers
5. **Admin Dashboard** - Anonymous analytics for institutional policy planning and intervention recognition

## 🚀 Features

### For Students
- **Anonymous AI Chat Support** - Get immediate help without revealing identity
- **Resource Library** - Access self-help materials in multiple languages
- **Appointment Booking** - Schedule confidential sessions with counselors
- **Peer Community** - Connect with fellow students in a safe, moderated environment
- **Crisis Support** - Immediate access to emergency contacts and helplines

### For Administrators
- **Real-time Analytics Dashboard** - Live monitoring of usage trends and mental health indicators
- **Regional Analytics** - Cultural context-aware insights with regional breakdowns
- **User Activity Tracking** - Anonymous data collection for policy decisions
- **Alert System** - Notifications for unusual patterns, crisis situations, and counselor overloads
- **Resource Management** - Add and manage educational content in multiple languages
- **Counselor Scheduling** - Comprehensive offline support mapping with availability tracking
- **Institution Customization** - Full branding and feature configuration per institution
- **System Health Monitoring** - Real-time system performance and error tracking

### For Counselors
- **Appointment Management** - View and manage scheduled sessions
- **Availability Management** - Set weekly schedules with online/offline preferences
- **Resource Creation** - Contribute educational materials in regional languages
- **Student Progress** - Anonymous tracking of intervention effectiveness
- **Offline Support Ticketing** - Direct integration with campus counseling services
- **Regional Context Awareness** - Cultural sensitivity guidelines and preferences

## 🌟 New Features Added

### 🌍 Regional Cultural Context and Language Support
- **Multi-language Support** - Full localization for 10 Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, English)
- **Cultural Context Awareness** - Region-specific cultural preferences, festivals, values, and communication styles
- **Localized Content** - Mental health resources adapted to regional cultural contexts
- **Language Preference Settings** - Users can set their preferred language for UI and content

### 🏛️ Institution-specific Customization
- **Branding Customization** - Institution logos, color schemes, and custom CSS
- **Feature Toggles** - Enable/disable specific features per institution (AI support, peer support, offline booking, anonymous mode)
- **Working Hours Configuration** - Customizable operational hours and timezone settings
- **Institution Types** - Support for colleges, universities, technical institutes, medical colleges, etc.

### 👥 Offline Support Mapping
- **Counselor Directory** - Complete database of on-campus counselors with contact details
- **Availability Scheduling** - Weekly schedule management for counselors
- **Room Location Tracking** - Physical location mapping for in-person sessions
- **Specialization Tags** - Match students with counselors based on expertise areas
- **Support Ticket System** - Seamless offline referral and follow-up tracking
- **Multi-language Counselor Support** - Language preference matching between students and counselors

### 📊 Real-time Analytics for Admin
- **Live Dashboard** - Real-time metrics with customizable widgets
- **Regional Analytics** - Cultural context-aware insights and regional comparisons
- **System Health Monitoring** - CPU, memory, database, and response time tracking
- **Crisis Alert System** - Automated alerts for unusual patterns and emergency situations
- **Counselor Workload Monitoring** - Track counselor availability and workload distribution
- **Cultural Resource Effectiveness** - Monitor effectiveness of region-specific resources

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Styling**: Custom CSS with Bootstrap components
- **Icons**: Bootstrap Icons
- **Authentication**: Django's built-in authentication system

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd digital-psychological-intervention-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`
├── frontend/           # React frontend application
├── backend/           # Node.js/Express API server
├── database/          # Database schemas and migrations
├── docs/             # Documentation
├── scripts/          # Deployment and utility scripts
├── assets/           # Static assets and resources
└── README.md         # This file
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- MongoDB
- Git

### Installation
1. Clone the repository
2. Install dependencies for both frontend and backend
3. Configure environment variables
4. Run database migrations
5. Start the development servers

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Department of Student Welfare
- Department of Psychology
- Internal Quality Assurance Cell (IQAC)
- Student volunteers and beta testers

## Support

For support, email support@your-institution.edu or create an issue in this repository.
