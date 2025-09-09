# System Architecture

## Overview

The Digital Psychological Intervention System follows a modern, scalable architecture designed to handle sensitive mental health data securely while providing an intuitive user experience.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React/TS)    │───▶│   (Node.js)     │───▶│   (MongoDB)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PWA Service   │    │   Socket.IO     │    │   Redis Cache   │
│   Worker        │    │   (Real-time)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   External      │
                       │   Services      │
                       │   (AI, SMS)     │
                       └─────────────────┘
```

## Frontend Architecture

### Technology Stack
- **React 18** with TypeScript
- **Material-UI (MUI)** for component library
- **React Router** for navigation
- **Redux Toolkit** for state management
- **Axios** for API communication
- **Socket.IO Client** for real-time features
- **PWA** capabilities for mobile experience

### Component Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # Reusable components
│   │   ├── ai-support/       # AI chatbot components
│   │   ├── booking/          # Appointment booking
│   │   ├── resources/        # Educational resources
│   │   ├── peer-support/     # Forum components
│   │   └── admin/           # Dashboard components
│   ├── pages/               # Page components
│   ├── services/            # API service layer
│   ├── store/              # Redux store
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   └── types/              # TypeScript definitions
```

### Key Features
- **Responsive Design**: Mobile-first approach
- **Offline Support**: PWA with service worker
- **Accessibility**: WCAG 2.1 AA compliance
- **Internationalization**: Multi-language support
- **Real-time Updates**: Socket.IO integration

## Backend Architecture

### Technology Stack
- **Node.js** with Express.js framework
- **TypeScript** for type safety
- **MongoDB** with Mongoose ODM
- **Redis** for caching and sessions
- **Socket.IO** for real-time communication
- **JWT** for authentication
- **Bcrypt** for password hashing
- **Helmet** for security headers

### API Structure
```
backend/
├── src/
│   ├── controllers/         # Request handlers
│   ├── models/             # Database models
│   ├── routes/             # API routes
│   ├── middleware/         # Custom middleware
│   ├── services/           # Business logic
│   ├── utils/             # Utility functions
│   ├── config/            # Configuration files
│   └── types/             # TypeScript definitions
├── tests/                 # Test files
└── docs/                  # API documentation
```

### Security Measures
- **Data Encryption**: AES-256 for sensitive data
- **API Rate Limiting**: Prevent abuse
- **Input Validation**: Joi schema validation
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Restricted origins
- **Audit Logging**: Track sensitive operations

## Database Design

### MongoDB Collections

#### Users
```javascript
{
  _id: ObjectId,
  email: String,
  passwordHash: String,
  profile: {
    name: String,
    role: String, // student, counselor, admin
    institution: String,
    preferences: Object
  },
  createdAt: Date,
  lastLogin: Date
}
```

#### Appointments
```javascript
{
  _id: ObjectId,
  studentId: ObjectId,
  counselorId: ObjectId,
  datetime: Date,
  status: String, // scheduled, completed, cancelled
  type: String, // individual, group
  notes: String, // encrypted
  createdAt: Date
}
```

#### ChatSessions
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  messages: [{
    role: String, // user, assistant
    content: String, // encrypted
    timestamp: Date
  }],
  sentiment: String,
  riskLevel: String,
  createdAt: Date
}
```

#### Resources
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  type: String, // video, audio, article
  category: String,
  language: String,
  content: Object,
  tags: [String],
  published: Boolean
}
```

### Data Security
- **Encryption at Rest**: MongoDB encryption
- **Field-Level Encryption**: Sensitive fields
- **Access Control**: Role-based permissions
- **Data Retention**: Automatic cleanup policies

## External Integrations

### AI Services
- **OpenAI GPT**: Chatbot responses
- **Sentiment Analysis**: Message analysis
- **Risk Assessment**: Crisis detection

### Communication
- **Email Service**: Appointment notifications
- **SMS Gateway**: Emergency alerts
- **Push Notifications**: Real-time updates

### Analytics
- **Data Anonymization**: Privacy-preserving analytics
- **Trend Analysis**: Mental health insights
- **Reporting**: Administrative dashboards

## Deployment Architecture

### Development Environment
```
Docker Compose Setup:
├── frontend (React dev server)
├── backend (Node.js with nodemon)
├── mongodb (Docker container)
├── redis (Docker container)
└── nginx (Reverse proxy)
```

### Production Environment
```
Kubernetes Cluster:
├── Frontend Pods (React build)
├── Backend Pods (Node.js)
├── MongoDB (StatefulSet)
├── Redis (Deployment)
├── Ingress Controller
└── Load Balancer
```

## Performance Considerations

### Frontend Optimization
- Code splitting with React.lazy()
- Image optimization and lazy loading
- Service worker caching
- Bundle size monitoring

### Backend Optimization
- Database indexing strategy
- API response caching
- Connection pooling
- Query optimization

### Scalability
- Horizontal scaling capabilities
- Database sharding strategy
- CDN integration
- Auto-scaling policies

## Security Architecture

### Authentication Flow
1. User login with email/password
2. JWT token generation
3. Token validation on protected routes
4. Refresh token rotation

### Data Protection
- HTTPS everywhere
- OWASP security guidelines
- Regular security audits
- Penetration testing

### Privacy Compliance
- GDPR compliance measures
- Data anonymization
- User consent management
- Right to deletion

## Monitoring and Logging

### Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- User analytics (anonymized)

### Logging Strategy
- Structured logging with Winston
- Log aggregation with ELK stack
- Security event monitoring
- Audit trail maintenance
