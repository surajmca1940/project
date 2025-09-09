# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

The Digital Psychological Intervention System (DPIS) is a comprehensive **Django-based web application** providing mental health support for educational institutions. It features AI-guided support, appointment booking, peer support forums, educational resources, and administrative analytics.


**Key Domain**: Mental health platform addressing college student wellness with privacy-first design and institutional analytics.

## Architecture Overview

### Core Technology Stack
- **Backend**: Django 5.2.6 (Python) - Main web framework
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Authentication**: Django's built-in user system
- **Styling**: Custom CSS with Bootstrap components

### Django Application Structure
The project follows Django's modular app architecture:



- **`ai_support/`** - AI chatbot functionality and coping strategies
- **`booking_system/`** - Appointment scheduling with counselors
- **`resources/`** - Educational content and wellness materials
- **`peer_support/`** - Community forums and peer interactions
- **`admin_dashboard/`** - Analytics and administrative tools
- **`mental_health_platform/`** - Main Django project configuration

### Key Models and Data Architecture
- **`ChatSession`** & **`ChatMessage`**: AI support conversation tracking
- **`Counselor`** & **`Appointment`**: Professional booking system
- **`AvailableSlot`**: Counselor availability management
- **`CopingStrategy`**: Multi-language mental health resources
- **Django User Model**: Extended for role-based access (student/counselor/admin)

### Frontend Architecture (Django Templates + Vanilla JS)
- **Template Structure**: Django's MVT pattern with template inheritance
- **Base Template**: `templates/base.html` provides common layout and navigation
- **App Templates**: Each Django app has its own template directory
- **Static Files**: Organized in `static/` directory:
  - `static/css/style.css` - Custom styling with CSS variables and animations
  - `static/js/main.js` - Vanilla JavaScript with ES6 classes for interactivity
- **Bootstrap 5**: CDN-loaded for responsive design and components
- **Progressive Enhancement**: JavaScript enhances basic HTML functionality

## Common Development Commands

### Django Development Workflow
```bash
# Set up virtual environment (first time)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run development server
python manage.py runserver
# Application will be available at http://127.0.0.1:8000/
```

### Database Management
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

### Django Management Commands
```bash
# Open Django shell for data manipulation
python manage.py shell

# Collect static files (production)
python manage.py collectstatic

# Check for Django system issues
python manage.py check

# Show current migrations status
python manage.py showmigrations
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test ai_support
python manage.py test booking_system

# Run specific test class or method
python manage.py test ai_support.tests.ChatSessionTestCase
python manage.py test ai_support.tests.ChatSessionTestCase.test_create_session

# Run tests with coverage (if coverage.py is installed)
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML coverage report
```

### Docker Development (Alternative Setup)
```bash
# Start containerized development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose build
```

### Static Files Development
```bash
# Collect and serve static files in development
python manage.py collectstatic --noinput

# Watch for CSS changes (if using a CSS preprocessor)
# Currently using vanilla CSS, no build process needed

# Static files are served automatically by Django dev server
# Access at: http://127.0.0.1:8000/static/
```

### Frontend Testing & Development
```bash
# Django dev server serves static files automatically
python manage.py runserver

# Templates are in templates/ directory
# Static files (CSS/JS) are in static/ directory
# Changes to templates/static files don't require server restart

# Test JavaScript functionality in browser developer tools
# No separate build process required for vanilla JS
```

## Key Development Patterns

### Django Authentication & Authorization
- **Django's built-in User model** extended for role-based access
- **Session-based authentication** for web interface
- **Role distinction**: Student, Counselor, Admin via user groups or profile fields
- **Django permissions system** for view-level access control
- **Login decorators** (`@login_required`) protect sensitive views

### Django App Architecture
- **Modular app design**: Each feature area is a separate Django app
- **Model-View-Template (MVT)** pattern throughout
- **URL routing** with namespaced patterns (`ai_support:chat_view`)
- **Class-based views (CBVs)** for consistent CRUD operations
- **Django forms** for input validation and security
- **Template inheritance**: Base template with blocks for extensible UI

### Frontend JavaScript Patterns
- **ES6 Classes**: `ChatInterface` and `AppointmentBooking` classes in `main.js`
- **Progressive Enhancement**: JavaScript adds interactivity to functional HTML
- **Event-Driven**: DOM event listeners for user interactions
- **Bootstrap Integration**: Uses Bootstrap's JavaScript components (tooltips, modals, alerts)
- **Vanilla JS**: No frameworks, pure JavaScript for maximum compatibility

### Data Security & Privacy
- **Django ORM** prevents SQL injection by default
- **CSRF protection** enabled across all forms
- **Sensitive data fields** should use Django's encryption utilities
- **User data anonymization** for analytics and reporting
- **Django's security middleware** handles common vulnerabilities

### Database Schema (Django Models)
- **`User` (Django built-in)**: Core authentication, extended via OneToOne profiles
- **`ChatSession`/`ChatMessage`**: AI support conversation tracking with anonymization
- **`Counselor`**: Professional profiles with specializations and availability
- **`Appointment`**: Booking system with status tracking and privacy controls
- **`CopingStrategy`**: Multi-language mental health resources
- **Foreign key relationships** maintain data integrity and enable efficient queries

## Environment Setup Requirements

### Python/Django Environment
- Python 3.8+
- pip (Python package manager)
- Virtual environment (venv recommended)

### Environment Variables
- Configure Django settings via environment variables when deploying (e.g., `SECRET_KEY`, `DEBUG`, `DATABASE_URL`).
- For local development with SQLite, environment variables are optional; defaults are defined in `mental_health_platform/settings.py`.

### Optional (Containerized Dev)
- Docker & Docker Compose if using the alternative setup in `docker-compose.yml`.
- Note: docker-compose includes services for MongoDB/Redis intended for a Node/React stack; these are not required for the Django app and can be ignored unless integrating a separate Node service.

## Mental Health Domain Context

When working with this codebase, understand that:

- **Data privacy is paramount** - Django ORM should handle sensitive mental health data carefully
- **User anonymity options** are crucial for mental health platform adoption
- **Crisis detection** in AI support should escalate to human counselors immediately
- **Accessibility compliance** (WCAG 2.1 AA) is required for inclusive design
- **Multi-language support** is built into the resource system (see `CopingStrategy` model)
- **Institutional analytics** must be anonymized while providing useful insights

## Django Development Notes

- **Django admin interface** (`/admin/`) provides quick access to model management
- **Template inheritance** maintains consistent UI across the platform (`templates/base.html` extends to all pages)
- **Django's security features** (CSRF, SQL injection protection) are leveraged throughout
- **Model relationships** use proper foreign keys for data integrity (see appointment booking system)
- **Django migrations** track all schema changes for reliable deployments
- **Static file handling** serves CSS/JS through Django's staticfiles system
- **URL routing** is organized with app namespaces for maintainability
- **JavaScript Classes**: `ChatInterface` and `AppointmentBooking` provide interactive functionality
- **Bootstrap Integration**: Uses Bootstrap 5 components with custom CSS overrides
- **Progressive Enhancement**: HTML forms work without JavaScript, JS adds enhanced UX

## Important Project Context

### Current Implementation vs. Documentation Mismatch
- **Current**: Django-based web application with HTML/CSS/JS frontend (what actually runs)
- **Unused**: Node.js/React configuration files exist but are not used (`frontend/`, `backend/` dirs)
- **Documentation**: `docs/ARCHITECTURE.md` describes a Node.js/React/MongoDB stack that was planned but not implemented
- **Docker setup**: `docker-compose.yml` is configured for Node.js/MongoDB, not the current Django app
- **Package files**: `package.json` files exist but the Django app doesn't use npm or Node.js

### Key Features (From Current Implementation)
- **AI Support**: `ChatSession` and `ChatMessage` models + `ChatInterface` JavaScript class for real-time chat UI
- **Counselor Booking**: `Counselor`, `Appointment`, and `AvailableSlot` models + `AppointmentBooking` JS class
- **Resource Library**: `CopingStrategy` model with multi-language support and categorized display
- **User Management**: Django User model with role-based navigation and access control
- **Responsive UI**: Bootstrap 5 with custom CSS variables and hover animations
- **Interactive Features**: Form validation, loading states, auto-hiding alerts, emergency modals

### Security & Privacy Design Patterns
- **Django security middleware** provides CSRF protection, clickjacking protection, etc.
- **Sensitive data handling**: Patient/student mental health data requires careful privacy controls
- **Role-based access**: Different user types (students, counselors, admins) have different permissions
- **Audit capabilities**: Track access to sensitive features for compliance and security
