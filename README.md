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
- **Analytics Dashboard** - Monitor usage trends and mental health indicators
- **User Activity Tracking** - Anonymous data collection for policy decisions
- **Alert System** - Notifications for unusual patterns or crisis situations
- **Resource Management** - Add and manage educational content
- **Counselor Scheduling** - Manage appointment availability and counselor profiles

### For Counselors
- **Appointment Management** - View and manage scheduled sessions
- **Resource Creation** - Contribute educational materials
- **Student Progress** - Anonymous tracking of intervention effectiveness

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
