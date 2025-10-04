# WorkConnect Architecture Documentation

## 📋 Table of Contents

This repository contains comprehensive architecture documentation for the WorkConnect application, a blue-collar worker marketplace platform.

### Documentation Files

1. **[ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md)** ⭐ **START HERE**
   - Quick overview of the entire system
   - Project responsibilities and how they work together
   - Technology stack summary
   - Key features by role
   - Quick start guide

2. **[ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)** 📊 **DETAILED ANALYSIS**
   - Comprehensive system architecture breakdown
   - Three-tier architecture explanation
   - Detailed project breakdown (UI, API, AI)
   - Communication patterns
   - Security architecture
   - Data model and relationships
   - Design patterns used
   - Strengths and areas for improvement

3. **[TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md)** 🔧 **API REFERENCE**
   - Complete API endpoint documentation
   - Request/response examples
   - Data models and interfaces
   - Authentication and authorization details
   - Frontend routes
   - Database schema
   - Integration points
   - Error handling

4. **Architecture Diagrams** 📈 **VISUAL GUIDES**
   - System architecture diagram
   - Data flow and communication patterns
   - Component relationships

---

## 🏗️ System Overview

WorkConnect consists of **three separate projects**:

```
┌─────────────────────────────────────────────────────────────┐
│  workconnect-ui (Frontend)                                  │
│  Angular 19 • TypeScript • Material Design                  │
│  Port: 4200                                                 │
│  → User Interface & Client-Side Logic                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  workconnect-api (Backend)                                  │
│  Spring Boot 3.5.3 • Java 21 • PostgreSQL                  │
│  Port: 8080                                                 │
│  → Business Logic & Data Management                         │
└─────────────────────────────────────────────────────────────┘
         ↓                              ↓
┌──────────────────────┐    ┌──────────────────────────────┐
│  PostgreSQL          │    │  workconnect-ai (AI Service) │
│  Port: 5432          │    │  FastAPI • Python • ML       │
│  → Data Storage      │    │  Port: 8000                  │
└──────────────────────┘    │  → Job Recommendations       │
                            └──────────────────────────────┘
```

---

## 🎯 Quick Reference

### Project Locations

Assuming the three projects are in the same parent directory:

```
/parent-directory/
├── workconnect-ui/          # This repository (Frontend)
├── workconnect-api/         # Backend API
└── workconnect-ai/          # AI Service
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Angular | 19.0.6 |
| **Backend** | Spring Boot | 3.5.3 |
| **Backend Language** | Java | 21 |
| **AI Service** | FastAPI | Latest |
| **AI Language** | Python | 3.x |
| **Database** | PostgreSQL | Latest |
| **File Storage** | Cloudinary | Latest |

### Default Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 4200 | http://localhost:4200 |
| Backend | 8080 | http://localhost:8080 |
| AI Service | 8000 | http://localhost:8000 |
| Database | 5432 | localhost:5432 |

---

## 👥 User Roles

### 👷 Worker
- Browse and search jobs
- Apply for jobs
- Track applications
- Manage profile and resume
- Receive AI-powered recommendations

### 🏢 Employer
- Post and manage jobs
- Review applications
- Accept/reject candidates
- Manage company profile
- Upload job images

### 👨‍💼 Admin
- System-wide management
- User moderation
- Job moderation
- View statistics
- Export data

---

## 🔐 Security Features

- **JWT Authentication** - Stateless token-based auth
- **Role-Based Access Control** - WORKER, EMPLOYER, ADMIN
- **Automatic Token Refresh** - Seamless session management
- **Password Encryption** - BCrypt hashing
- **Route Guards** - Frontend route protection
- **Method-Level Security** - Backend endpoint protection

---

## 🤖 AI Features

The AI service provides intelligent job recommendations using:

- **Natural Language Processing** (NLTK)
- **TF-IDF Vectorization** (scikit-learn)
- **Cosine Similarity** - Skill matching algorithm
- **Fallback Mechanism** - Basic matching if AI unavailable

**How it works:**
1. Worker's skills are analyzed
2. Job requirements are processed
3. Text is vectorized using TF-IDF
4. Similarity scores calculated
5. Jobs ranked by relevance
6. Top recommendations returned

---

## 📊 Key Features

### Job Management
- ✅ Post jobs (ONE_DAY or CONTRACT types)
- ✅ Job search and filtering
- ✅ Job image uploads
- ✅ Application tracking
- ✅ Status management

### Profile Management
- ✅ Worker profiles (skills, experience, resume)
- ✅ Employer profiles (company info, logo)
- ✅ Profile picture uploads
- ✅ Public profile viewing

### Application System
- ✅ One-click job applications
- ✅ Cover letter support
- ✅ Application status tracking
- ✅ Employer review system

### Admin Portal
- ✅ User management
- ✅ Job moderation
- ✅ System statistics
- ✅ Data export (CSV)

---

## 🔄 Communication Flow

### Frontend → Backend
```
HTTP/REST + JSON
Authorization: Bearer <JWT_TOKEN>
```

### Backend → Database
```
JPA/Hibernate → PostgreSQL
HikariCP Connection Pool
```

### Backend → AI Service
```
HTTP POST → http://localhost:8000/recommendations/jobs
Request: { worker_profile, job_postings }
Response: { ranked_job_ids }
```

### Backend → Cloudinary
```
Cloudinary SDK
Upload: Images, Resumes, Documents
Response: Public URLs
```

---

## 📁 Project Structure

### workconnect-ui (Frontend)
```
src/
├── app/
│   ├── components/       # Reusable UI components
│   ├── pages/           # Page components
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── job-list/
│   │   ├── admin/
│   │   └── ...
│   ├── services/        # Business logic services
│   │   ├── auth.service.ts
│   │   ├── job.service.ts
│   │   ├── profile.service.ts
│   │   └── ...
│   ├── guards/          # Route guards
│   ├── interceptors/    # HTTP interceptors
│   ├── models/          # TypeScript interfaces
│   └── app.routes.ts    # Route configuration
└── environments/        # Environment configs
```

### workconnect-api (Backend)
```
src/main/java/com/workconnect/api/
├── controller/          # REST controllers
│   ├── UserAuthController.java
│   ├── JobController.java
│   ├── ProfileController.java
│   └── ...
├── service/            # Business logic
│   ├── UserService.java
│   ├── JobService.java
│   └── ...
├── repository/         # Data access
│   ├── UserRepository.java
│   ├── JobRepository.java
│   └── ...
├── entity/            # JPA entities
│   ├── User.java
│   ├── JobPosting.java
│   └── ...
├── config/            # Configuration
│   ├── SecurityConfig.java
│   ├── JwtUtil.java
│   └── ...
└── dto/               # Data transfer objects
```

### workconnect-ai (AI Service)
```
workconnect-ai/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── test_ai_integration.py    # Integration tests
└── README.md                 # AI service documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Java 21 and Maven
- Python 3.8+
- PostgreSQL 12+

### Setup Steps

**1. Database Setup**
```bash
# Create database
createdb workconnect_db

# Database will be auto-configured by Spring Boot
```

**2. Start Backend API**
```bash
cd workconnect-api
mvn clean install
mvn spring-boot:run

# Backend runs on http://localhost:8080
```

**3. Start AI Service**
```bash
cd workconnect-ai
pip install -r requirements.txt
python app.py

# AI service runs on http://localhost:8000
```

**4. Start Frontend**
```bash
cd workconnect-ui
npm install
ng serve

# Frontend runs on http://localhost:4200
```

**5. Access Application**
- Open browser: http://localhost:4200
- Register a new account
- Login and explore!

---

## 📖 API Documentation

### Main Endpoints

**Authentication:**
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token

**Jobs:**
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create job (Employer)
- `POST /api/jobs/{id}/apply` - Apply for job (Worker)

**Profiles:**
- `GET /api/profiles/me` - Get own profile
- `PUT /api/profiles/me/worker` - Update worker profile
- `PUT /api/profiles/me/employer` - Update employer profile

**Admin:**
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/users` - List users
- `GET /api/admin/jobs` - List jobs

**AI Service:**
- `POST /recommendations/jobs` - Get recommendations

For complete API documentation, see [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md)

---

## 🏛️ Architecture Patterns

### Frontend
- Component-Based Architecture
- Service Layer Pattern
- Interceptor Pattern
- Guard Pattern
- Observer Pattern (RxJS)

### Backend
- MVC Pattern
- Repository Pattern
- DTO Pattern
- Dependency Injection
- Layered Architecture

### Integration
- RESTful API
- Microservices
- Circuit Breaker (AI fallback)
- JWT Authentication

---

## 🎨 Design Decisions

### Why Angular?
- Enterprise-grade framework
- Strong typing with TypeScript
- Built-in dependency injection
- Comprehensive routing
- Material Design components

### Why Spring Boot?
- Industry standard for Java
- Excellent security framework
- Powerful ORM (JPA/Hibernate)
- Production-ready features
- Large ecosystem

### Why FastAPI?
- High performance
- Easy ML integration
- Automatic API docs
- Type hints
- Fast development

### Why PostgreSQL?
- Robust and reliable
- ACID compliance
- Advanced features
- Excellent performance
- Open source

---

## 📈 Scalability Considerations

### Current Architecture
- Microservices design
- Stateless authentication (JWT)
- Connection pooling (HikariCP)
- Independent service scaling

### Future Enhancements
- Service discovery (Eureka)
- API Gateway (Spring Cloud Gateway)
- Distributed caching (Redis)
- Message queue (RabbitMQ/Kafka)
- Container orchestration (Kubernetes)
- Monitoring (Prometheus/Grafana)

---

## 🧪 Testing

### Frontend Testing
- Unit tests: Jasmine/Karma
- E2E tests: Protractor/Cypress
- Component testing

### Backend Testing
- Unit tests: JUnit 5
- Integration tests: Spring Boot Test
- Repository tests: H2 in-memory DB

### AI Service Testing
- Integration tests included
- Edge case testing
- Performance testing

---

## 📝 Additional Resources

### Documentation Files
- `ARCHITECTURE_SUMMARY.md` - Quick overview
- `ARCHITECTURE_ANALYSIS.md` - Detailed analysis
- `TECHNICAL_SPECIFICATION.md` - API reference

### Diagrams
- System Architecture Diagram
- Data Flow Diagram
- Component Relationships Diagram

### External Links
- [Angular Documentation](https://angular.io/docs)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🤝 Contributing

When working on this project:

1. **Frontend changes** → `workconnect-ui` repository
2. **Backend changes** → `workconnect-api` repository
3. **AI changes** → `workconnect-ai` repository

Ensure all three services are running for full functionality.

---

## 📞 Support

For questions about the architecture:
1. Check the documentation files
2. Review the diagrams
3. Examine the code structure
4. Refer to the technical specification

---

## 📄 License

This documentation is part of the WorkConnect project.

---

**Last Updated:** 2025-10-04  
**Architecture Version:** 1.0  
**Documentation Status:** Complete

