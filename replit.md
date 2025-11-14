# Étude LINE

## Overview
Étude LINE is an educational web application built with FastAPI, designed for professors to share content (courses, exercises, solutions) with students. The platform features content organized hierarchically by university, field, level, semester, subject, and chapter. It includes a complete authentication system, robust content management, and is available as an installable Progressive Web App (PWA). The project aims to facilitate seamless educational content dissemination and access, enabling students to register and access all content freely. The platform supports advanced scientific content creation with rich text editing, mathematical equations, tables, and interactive charts, without requiring technical knowledge in LaTeX or programming.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### UI/UX Decisions
The application uses a server-side rendered architecture with Jinja2 templates, featuring a modern, responsive design with CSS Grid and Flexbox and a gradient color scheme. Key interfaces include dashboards for Professors, Students, and Admins, offering consistent branding, interactive content views, color-coded level cards, and icon-based actions. Admin panels feature consistent button-based forms, animated transitions, real-time search, and detailed student information display. All admin dashboard lists and individual user details are collapsible by default for a clean interface. University statistics are presented in compact, color-coded cards. The homepage includes a redesigned student registration flow with animations. The application is fully responsive for mobile, tablet, and PC, with specific optimizations for forms, notification centers, and dashboards, ensuring touch-friendly elements and readable typography across devices. Scroll position and active tabs are preserved across form submissions in professor and admin dashboards to maintain user context. Semester headers in the professor dashboard are visually distinct with consistent violet/purple styling. The desktop interface features professional full-width optimization with responsive breakpoints at 1400px, 1600px, 1920px, and 2560px (4K), utilizing 95-98% of screen width with progressive scaling of padding, fonts, and element sizes for optimal use of ultra-wide displays. The secondary admin page features a full violet theme with a glassmorphism effect. All `scrollIntoView()` calls that caused unwanted automatic scrolling have been removed to enhance user workflow, while legitimate ones for UX improvement have been retained. Notifications are now fixed toast messages that animate in and out, eliminating forced scrolling.

### Technical Implementations
- **Authentication & Authorization**: `bcrypt` for password hashing, `itsdangerous` for secure cookie-based session management, and role-based access control.
- **Hierarchical Access Control**: Students can only view chapters from their current level and all lower levels within their filière, enforced by SQL-level filtering. Professors have full access within their assigned subject.
- **User & Content Management**: Separate models for professors and students, with content hierarchically organized.
- **University-Based Administration**: Administrators are assigned to specific universities, restricting access to institutional data, with a main administrator having global access.
- **Data Filtering**: Professors can only create content within their assigned university, and dashboards dynamically filter data based on user roles and affiliations.
- **Complete Cascade Deletion**: A comprehensive system with specialized helper functions ensures transaction-safe, permanent removal of all associated data when an entity is deleted, including uploaded files, comments, and notifications.
- **Search Functionality**: Pure frontend, real-time, case-insensitive search across admin and professor dashboards for various entities.
- **Performance Optimization**: Includes database indexing, N+1 query elimination (reducing 54+ queries to ~3-5 for students and professors), eager loading, SQL aggregations, GZip compression, HTTP caching, and optimized frontend polling. Exposed JavaScript functions globally to fix scope issues on Render.
- **Progressive Web App (PWA)**: Full PWA implementation with web app manifest, service worker for intelligent caching (cache-first for static assets, network-only for dynamic content/APIs), offline fallback, iOS meta tags, custom installation banner, and PWA badge API integration. Uses `apple-touch-icon` for correct iOS icon display.
- **Interactive Content Editor**: Integration of Quill.js for rich text editing, with custom buttons for MathJax (LaTeX equations) and Chart.js (interactive graphs) without requiring API keys. Content is stored as HTML.
- **Interactive Comment System**: Real-time commenting with a `Commentaire` database model, RESTful API endpoints, permission-based deletion, visual differentiation for user roles, XSS protection, and reply functionality.
- **Admin Auto-Provisioning**: Automatic creation of a default main administrator at startup.
- **Administrator Edit Capability**: Main administrator can modify usernames and passwords for professors and secondary administrators.
- **Notification System**: Real-time notification system with a `Notification` database model, RESTful API, auto-notifications for new content, UI notification center, and native push notifications via Service Worker API.
- **University-Specific Feature Control System**: Each university has independent control over key features (e.g., download buttons, academic progression activation) via the `ParametreUniversite` model.
- **Academic Progression Hierarchy System**: Comprehensive system for managing student advancement between academic levels and programs, tracking history, and updating student records.
- **File Viewer**: Integrated multi-format file viewer (PDF, Word, images, videos, PowerPoint) that opens within the application, ensuring a fluid user experience. Implemented with robust security against path traversal and XSS vulnerabilities using DOM API for element creation. PDF viewer optimized for mobile with continuous scroll mode.
- **Special Character Handling**: Fixed issues with deletion/modification of entities containing special characters (apostrophes, quotes) by correctly escaping parameters in `onclick` attributes using `|tojson`.

### System Design Choices
- **Monolithic Architecture**: FastAPI handles all backend logic, database interactions, and API endpoints.
- **Session Management**: Cookie-based sessions with `itsdangerous` for secure tokens and automatic role detection.
- **Route Protection**: Dependency injection for automated authentication and authorization.
- **Production Deployment**: Optimized for Render deployment with dynamic port configuration, production/development mode detection, and Gunicorn with Uvicorn workers for better stability.

## External Dependencies

### Core Framework Dependencies
- **FastAPI**: Asynchronous web framework.
- **Uvicorn**: ASGI server.
- **Jinja2**: Server-side template engine.
- **Pydantic**: Data validation and settings.

### Security Dependencies
- **passlib**: Password hashing library.
- **bcrypt**: Bcrypt algorithm.
- **itsdangerous**: Cryptographic signing for session cookies.

### Database Dependencies
- **PostgreSQL**: Persistent relational database provided by Replit for development, and Render PostgreSQL (paid) for production deployment.
- **SQLAlchemy**: ORM for database operations.
- **psycopg2-binary**: PostgreSQL adapter for Python.
- **alembic**: Database migration tool.
- **Data Persistence**: Logos are stored directly in PostgreSQL for persistence across Render redeployments. Uploaded files (videos, PDFs, documents) in production require Render Disk configuration.

### Frontend Libraries (CDN)
- **Quill.js**: WYSIWYG rich text editor.
- **MathJax**: For rendering LaTeX mathematical equations.
- **Chart.js**: For interactive graphs.

### Utility Dependencies
- **python-multipart**: For handling form data and file uploads.
- **Pillow**: For image manipulation (e.g., resizing PWA icons).

### Environment Configuration
- **DATABASE_URL**: PostgreSQL connection URL.
- **ADMIN_USERNAME**: Principal administrator username.
- **ADMIN_PASSWORD**: Principal administrator password.
- **SESSION_SECRET**: Secret key for session signing.
- **PYTHON_VERSION**: 3.11.2.
- **ENVIRONMENT**: (Optional) production/development.

### File System Dependencies
- **Upload Storage**: Local `uploads/` directory for course materials in development. Render Disk mounted at `/opt/render/project/src/uploads` for persistence in production.

### Deployment Configuration
- **render.yaml**: Blueprint configuration file for automatic Render deployment setup.