# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

The Digital Psychological Intervention System (DPIS) is a comprehensive mental health platform for educational institutions. It's a full-stack TypeScript application with a React frontend, Node.js/Express backend, MongoDB database, and Redis caching layer, all containerized with Docker.

**Key Domain**: Mental health support system with AI chatbot, appointment booking, peer support forums, educational resources, and administrative analytics.

## Architecture Overview

This is a **monorepo with workspace structure** containing two main applications:

### Frontend (`frontend/`)
- **React 18** with **TypeScript** and **Material-UI (MUI)**
- **Redux Toolkit** for state management
- **Socket.IO Client** for real-time features (chat, notifications)
- **PWA capabilities** with service worker for offline support
- **Component structure**:
  - `components/ai-support/` - AI chatbot interface
  - `components/booking/` - Appointment scheduling
  - `components/peer-support/` - Forum and community features
  - `components/resources/` - Educational content
  - `components/admin/` - Dashboard and analytics
  - `components/common/` - Reusable UI components

### Backend (`backend/src/`)
- **Node.js with Express.js** and **TypeScript**
- **MongoDB with Mongoose ODM** for data persistence
- **Socket.IO** for real-time communication
- **JWT authentication** with bcrypt password hashing
- **Key architecture patterns**:
  - `routes/` - API endpoint definitions
  - `controllers/` - Request handling logic
  - `services/` - Business logic layer
  - `models/` - Database schemas (User, Appointment, ChatSession, Resources)
  - `middleware/` - Authentication, error handling, rate limiting
  - `config/` - Database connection and logging setup

### External Integrations
- **OpenAI API** for AI chatbot responses and sentiment analysis
- **Redis** for session storage and caching
- **Email/SMS services** for notifications
- **MongoDB encryption** for sensitive data protection

## Common Development Commands

### Full Stack Development
```bash
# Install all dependencies (root, frontend, backend)
npm run install:all

# Start both frontend and backend in development mode
npm run dev

# Start individual services
npm run dev:frontend    # React dev server on port 3000
npm run dev:backend     # Node.js with nodemon on port 5000
```

### Building
```bash
# Build both applications for production
npm run build

# Build individual applications
npm run build:frontend  # Creates optimized React build
npm run build:backend   # Compiles TypeScript to JavaScript
```

### Testing
```bash
# Run all tests
npm test

# Run tests individually
npm run test:frontend   # React Testing Library with coverage
npm run test:backend    # Jest unit tests
```

### Linting and Code Quality
```bash
# Lint all code
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Format frontend code (Prettier)
npm run format
```

### Database Operations
```bash
# Seed database with initial data
npm run db:seed

# Reset database (destructive operation)
npm run db:reset
```

### Docker Operations
```bash
# Start all services with Docker Compose
npm run docker:up

# View logs from all containers
npm run docker:logs

# Stop all services
npm run docker:down

# Rebuild containers
npm run docker:build
```

### Running Individual Tests
```bash
# Backend: Run specific test file
cd backend && npm test -- --testPathPattern=controllers/auth.test.ts

# Backend: Run tests in watch mode
cd backend && npm run test:watch

# Frontend: Run specific component tests
cd frontend && npm test -- --testPathPattern=ChatInterface.test.tsx

# Frontend: Generate coverage report
cd frontend && npm test -- --coverage --watchAll=false
```

## Key Development Patterns

### Authentication Flow
- JWT tokens for API authentication
- Socket.IO uses the same JWT for real-time connections
- Role-based access control (student, counselor, admin)
- Protected routes require `authMiddleware`

### Data Security Approach
- Sensitive data (chat messages, appointment notes) is **field-level encrypted**
- All API endpoints use **input validation** with Joi schemas
- **Rate limiting** applied to prevent abuse
- **CORS** configured for specific origins only

### Real-time Features
- **Socket.IO** handles chat messages, appointment notifications
- Users join personal rooms for targeted notifications
- Chat sessions support both AI bot and peer-to-peer communication

### State Management Pattern
- **Redux Toolkit** with feature-based slice organization
- API calls handled through **Redux Toolkit Query** (RTK Query)
- Real-time updates integrated with Redux via Socket.IO middleware

### Database Schema Design
- **User model**: Handles students, counselors, and administrators
- **ChatSession model**: Stores encrypted conversation history with sentiment analysis
- **Appointment model**: Manages booking system with multiple statuses
- **Resources model**: Multi-language educational content system

## Environment Setup Requirements

### Required Environment Variables
**Backend** (`.env` file in `backend/`):
```
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://admin:password123@localhost:27017/dpis?authSource=admin
REDIS_URL=redis://:password123@localhost:6379
JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=your-openai-key
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`.env` file in `frontend/`):
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
```

### Prerequisites
- **Node.js v16+** and **npm v8+**
- **MongoDB** (local or Docker)
- **Redis** (local or Docker)
- **Docker & Docker Compose** for containerized development

## Mental Health Domain Context

When working with this codebase, understand that:

- **Data privacy is paramount** - all sensitive mental health data must be encrypted
- **Crisis detection** features require immediate escalation to human counselors
- **Anonymization** is used for analytics while preserving user privacy
- **Accessibility compliance** (WCAG 2.1 AA) is required for inclusive design
- **Multi-language support** is essential for diverse student populations

## Development Workflow Notes

- The system uses **TypeScript throughout** for type safety in this sensitive domain
- **Socket.IO connections** are authenticated and users join personal rooms
- **AI responses** go through sentiment analysis and risk assessment before delivery
- **Database queries** are optimized for privacy (no joins that could expose sensitive data)
- **API rate limiting** is aggressive to prevent system abuse
- **Logging** excludes sensitive data but maintains audit trails for security events
