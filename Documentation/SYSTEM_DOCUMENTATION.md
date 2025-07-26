# 🏥 Physiotherapy Clinic Management System
## Professional System Documentation

---

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Configuration](#configuration)
5. [User Guide](#user-guide)
6. [Technical Specifications](#technical-specifications)
7. [API Documentation](#api-documentation)
8. [Database Schema](#database-schema)
9. [Security](#security)
10. [Deployment](#deployment)
11. [Maintenance](#maintenance)
12. [Troubleshooting](#troubleshooting)
13. [Support](#support)

---

## 🎯 System Overview

### Purpose
The Physiotherapy Clinic Management System is a comprehensive web-based application designed to streamline clinic operations, manage patient care, and facilitate clinical documentation for physiotherapy practices.

### Key Features
- **Patient Management**: Complete patient registration and history tracking
- **Appointment Scheduling**: Advanced booking system with conflict detection
- **Clinical Documentation**: Comprehensive physiotherapy assessment forms
- **User Management**: Role-based access control (Admin, Receptionist, Doctor)
- **Treatment Packages**: Session-based treatment planning
- **Data Export**: CSV and calendar export capabilities
- **Backup System**: Automated daily database backups

### Target Users
- **Administrators**: System management and user administration
- **Receptionists**: Patient registration and appointment scheduling
- **Physiotherapists**: Clinical documentation and patient care
- **Clinic Managers**: Reporting and operational oversight

---

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python Flask 2.x
- **Database**: PostgreSQL 14+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Session with Werkzeug security
- **ORM**: SQLAlchemy 2.x
- **Server**: Development server (production: Gunicorn recommended)

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   Flask App     │    │   PostgreSQL    │
│                 │◄──►│                 │◄──►│   Database      │
│  - HTML/CSS/JS  │    │  - Routes       │    │  - 6 Tables     │
│  - Bootstrap    │    │  - Models       │    │  - JSON Storage │
│  - AJAX Calls   │    │  - Templates    │    │  - Relationships│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### File Structure
```
clinic-management-system/
├── app.py                          # Main Flask application
├── database_schema.md              # Database documentation
├── SYSTEM_DOCUMENTATION.md         # This documentation
├── requirements.txt                # Python dependencies
├── static/                         # Static assets
│   ├── css/
│   ├── js/
│   └── uploads/                    # File uploads
├── templates/                      # HTML templates
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── patients.html
│   ├── appointments.html
│   ├── doctor_appointment.html
│   └── ...
├── backups/                        # Database backups
└── README.md                       # Quick start guide
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- pip (Python package manager)
- Git (for version control)

### Installation Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd clinic-management-system
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Database Setup
```bash
# Create PostgreSQL database
createdb clinicdb

# Create database user
psql -d postgres -c "CREATE USER clinicuser WITH PASSWORD 'admin';"
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE clinicdb TO clinicuser;"

# Initialize database tables
flask init-db
```

#### 5. Configuration
```bash
# Edit app.py configuration section
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clinicuser:admin@localhost/clinicdb'
app.config['SECRET_KEY'] = 'your-secure-secret-key-here'
```

#### 6. Run Application
```bash
python app.py
```

### Dependencies
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
psycopg2-binary==2.9.7
Werkzeug==2.3.7
python-dateutil==2.8.2
```

---

## ⚙️ Configuration

### Environment Variables
```bash
# Database Configuration
SQLALCHEMY_DATABASE_URI=postgresql://clinicuser:admin@localhost/clinicdb
SECRET_KEY=your-secure-secret-key-here

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
BACKUP_DONE=False
```

### Database Configuration
```python
# PostgreSQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### Security Configuration
```python
# Session Security
app.config['SECRET_KEY'] = 'your-secure-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
```

---

## 👥 User Guide

### User Roles & Permissions

#### Administrator
**Access Level**: Full system access
**Capabilities**:
- User management (create, edit, delete users)
- System configuration
- Database backups
- All receptionist and doctor functions

**Navigation**:
- Dashboard → User Management
- System Settings
- Backup Management

#### Receptionist
**Access Level**: Patient and appointment management
**Capabilities**:
- Patient registration and management
- Appointment scheduling
- Doctor management
- Basic reporting

**Navigation**:
- Patients → Add/Edit/View patients
- Appointments → Schedule/Manage appointments
- Doctors → Manage doctor information

#### Doctor
**Access Level**: Clinical documentation and patient care
**Capabilities**:
- View assigned appointments
- Create comprehensive physiotherapy assessments
- Patient history review
- Treatment planning

**Navigation**:
- Dashboard → View appointments
- Patient Profile → Clinical documentation
- Comprehensive Assessment Forms

### Workflow Guides

#### Patient Registration Workflow
1. **Login** as Receptionist/Admin
2. **Navigate** to Patients → Add Patient
3. **Fill** patient information:
   - Basic demographics
   - Contact information
   - Medical history
   - Family history
   - Social history
4. **Save** patient record

#### Appointment Scheduling Workflow
1. **Navigate** to Appointments → Add Appointment
2. **Select** patient (or create new)
3. **Choose** doctor and appointment type
4. **Set** date, time, and duration
5. **Check** for scheduling conflicts
6. **Confirm** appointment

#### Clinical Documentation Workflow
1. **Login** as Doctor
2. **Navigate** to Dashboard → Manage Appointment
3. **Complete** comprehensive assessment:
   - Demographics & Chief Complaint
   - History of Present Illness
   - Physical Examination
   - Assessment & Diagnosis
   - Treatment Plan
   - Outcome Measures
   - Patient Education
   - Follow-up Plan
4. **Save** comprehensive note

---

## 🔧 Technical Specifications

### System Requirements

#### Minimum Requirements
- **CPU**: 2 GHz dual-core processor
- **RAM**: 4 GB
- **Storage**: 10 GB available space
- **Network**: Broadband internet connection
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+

#### Recommended Requirements
- **CPU**: 3 GHz quad-core processor
- **RAM**: 8 GB
- **Storage**: 50 GB available space
- **Network**: High-speed internet connection
- **Browser**: Latest version of Chrome/Firefox/Safari

### Performance Specifications
- **Response Time**: < 2 seconds for standard operations
- **Concurrent Users**: Up to 50 simultaneous users
- **Database Size**: Supports up to 100,000 patient records
- **File Upload**: Maximum 10 MB per file
- **Backup Frequency**: Daily automated backups

### Browser Compatibility
- **Chrome**: 90+ (Full support)
- **Firefox**: 88+ (Full support)
- **Safari**: 14+ (Full support)
- **Edge**: 90+ (Full support)
- **Internet Explorer**: Not supported

---

## 🔌 API Documentation

### Authentication Endpoints

#### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=doctor1&password=password123
```

**Response**:
```json
{
  "success": true,
  "redirect": "/dashboard",
  "role": "doctor"
}
```

#### Logout
```http
GET /logout
```

**Response**: Redirects to login page

### Patient Management API

#### Get All Patients
```http
GET /patients
```

**Response**:
```json
{
  "patients": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "+1234567890",
      "gender": "Male",
      "date_of_birth": "1985-03-15"
    }
  ]
}
```

#### Create Patient
```http
POST /patients/add
Content-Type: application/x-www-form-urlencoded

name=Jane Smith&phone=+1234567891&gender=Female&date_of_birth=1990-05-20
```

### Appointment Management API

#### Get Appointments
```http
GET /appointments?status=Confirmed&search=John
```

#### Create Appointment
```http
POST /add
Content-Type: application/x-www-form-urlencoded

patient_id=1&doctor_id=1&date=2024-01-15&time=14:00&duration=60&appointment_type=Consultation
```

### Clinical Documentation API

#### Save Comprehensive Assessment
```http
POST /doctor/appointment/1
Content-Type: application/x-www-form-urlencoded

chief_complaint=Lower back pain&pain_scale=7&treatment_methods=Manual therapy&equipment_used=Ultrasound
```

### Data Export API

#### Export CSV
```http
GET /export/csv
```

**Response**: CSV file download

#### Export Calendar
```http
GET /export/ics
```

**Response**: ICS file download

---

## 🗄️ Database Schema

### Core Tables

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    doctor_id INTEGER REFERENCES doctors(id),
    is_active BOOLEAN DEFAULT TRUE
);
```

#### Patients Table
```sql
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    phone VARCHAR NOT NULL,
    gender VARCHAR,
    date_of_birth DATE,
    contact_info VARCHAR,
    medical_history TEXT,
    family_history TEXT,
    social_history TEXT
);
```

#### Appointments Table
```sql
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    date DATE,
    time TIME,
    duration INTEGER,
    reason TEXT,
    status VARCHAR,
    package_id INTEGER REFERENCES packages(id),
    appointment_type VARCHAR
);
```

#### Notes Table
```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    note_type VARCHAR,
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### JSON Data Structure
Comprehensive physiotherapy assessments are stored as JSON in the `notes.content` field:

```json
{
  "chief_complaint": "Patient reports lower back pain",
  "pain_scale": "7",
  "pain_location": "Lower back, right side",
  "functional_impact": "Difficulty sitting for long periods",
  "treatment_methods": ["Manual therapy", "Electrical therapy"],
  "equipment_used": ["Ultrasound", "Laser therapy"],
  "clinical_impression": "Lumbar disc herniation",
  "treatment_goals": "Reduce pain by 50%",
  "home_exercise_program": "Daily core strengthening",
  "next_appointment_date": "2024-01-15",
  "consent_given": true,
  "safety_checked": true,
  "contraindications_checked": true
}
```

---

## 🔐 Security

### Authentication & Authorization
- **Password Hashing**: Werkzeug security with bcrypt
- **Session Management**: Flask-Session with secure cookies
- **Role-Based Access**: Admin, Receptionist, Doctor roles
- **Session Timeout**: Configurable session expiration

### Data Protection
- **Input Validation**: Server-side validation for all forms
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Protection**: Template escaping and content security policies
- **CSRF Protection**: Form token validation

### File Security
- **Upload Validation**: File type and size restrictions
- **Secure File Storage**: Isolated upload directory
- **Path Traversal Prevention**: Secure file path handling

### Network Security
- **HTTPS**: Recommended for production deployment
- **Secure Headers**: Security headers implementation
- **Rate Limiting**: Request rate limiting (recommended)

---

## 🚀 Deployment

### Development Deployment
```bash
# Run development server
python app.py
```

**Access**: http://localhost:5050

### Production Deployment

#### Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5050 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "app:app"]
```

#### Using Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-clinic-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Setup
```bash
# Production environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host/db
```

---

## 🔧 Maintenance

### Daily Maintenance
- **Database Backups**: Automated daily backups
- **Log Monitoring**: Application and error log review
- **Performance Monitoring**: Response time and resource usage

### Weekly Maintenance
- **User Account Review**: Inactive account cleanup
- **Data Integrity Check**: Database consistency verification
- **Security Updates**: Dependency updates and security patches

### Monthly Maintenance
- **Database Optimization**: Index optimization and cleanup
- **Storage Management**: File upload cleanup and archiving
- **Performance Analysis**: System performance review and optimization

### Backup Procedures
```bash
# Manual backup
flask backup

# Automated backup (cron job)
0 2 * * * /path/to/app/backup_script.sh
```

### Update Procedures
1. **Backup Database**: Create full backup before updates
2. **Update Code**: Pull latest code changes
3. **Update Dependencies**: `pip install -r requirements.txt`
4. **Database Migrations**: Run any schema updates
5. **Test System**: Verify all functionality
6. **Restart Services**: Restart application server

---

## 🛠️ Troubleshooting

### Common Issues

#### Database Connection Issues
**Problem**: Cannot connect to PostgreSQL
**Solution**:
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Check connection settings
psql -U clinicuser -d clinicdb -h localhost

# Verify database exists
psql -U clinicuser -d postgres -c "\l"
```

#### Application Won't Start
**Problem**: Flask application fails to start
**Solution**:
```bash
# Check Python environment
python --version
pip list

# Check configuration
python -c "import app; print(app.config)"

# Check logs
tail -f app.log
```

#### Form Submission Issues
**Problem**: Forms not saving data
**Solution**:
- Check browser console for JavaScript errors
- Verify form validation
- Check database permissions
- Review application logs

#### Performance Issues
**Problem**: Slow application response
**Solution**:
- Check database query performance
- Review server resources
- Optimize database indexes
- Consider caching strategies

### Error Codes

#### HTTP Error Codes
- **400 Bad Request**: Invalid form data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Application error

#### Database Error Codes
- **23505 Unique Violation**: Duplicate entry
- **23503 Foreign Key Violation**: Referenced record not found
- **23514 Check Violation**: Constraint violation

### Log Analysis
```bash
# Application logs
tail -f app.log

# Database logs
tail -f /var/log/postgresql/postgresql-14-main.log

# System logs
journalctl -u clinic-app -f
```

---

## 📞 Support

### Documentation Resources
- **System Documentation**: This document
- **Database Schema**: `database_schema.md`
- **API Documentation**: Section 7 of this document
- **User Guide**: Section 5 of this document

### Contact Information
- **Technical Support**: [support@clinic-system.com]
- **Emergency Contact**: [emergency@clinic-system.com]
- **Documentation**: [docs@clinic-system.com]

### Support Hours
- **Monday - Friday**: 9:00 AM - 6:00 PM EST
- **Weekend**: Emergency support only
- **Holidays**: Limited support

### Issue Reporting
When reporting issues, please include:
1. **Error Description**: Detailed description of the problem
2. **Steps to Reproduce**: Step-by-step reproduction steps
3. **Environment**: Browser, OS, user role
4. **Error Messages**: Complete error messages and logs
5. **Screenshots**: Visual evidence if applicable

### Training Resources
- **User Training**: Available upon request
- **Admin Training**: Comprehensive system administration training
- **Custom Training**: Tailored training for specific workflows

---

## 📄 License & Legal

### Software License
This software is proprietary and confidential. Unauthorized copying, distribution, or modification is prohibited.

### Data Protection
- **HIPAA Compliance**: System designed with healthcare data protection in mind
- **Data Retention**: Configurable data retention policies
- **Privacy Policy**: Separate privacy policy document required

### Warranty
- **Software Warranty**: 90-day warranty from installation
- **Support Warranty**: 1-year support warranty
- **Limitation of Liability**: Standard software liability limitations apply

---

*This documentation is current as of version 1.0. For the latest updates, please refer to the system administrator or contact technical support.*

**Last Updated**: January 2024  
**Version**: 1.0  
**Documentation Version**: 1.0 