# 🏥 Physiotherapy Clinic Management System

A comprehensive web-based application for managing physiotherapy clinic operations, patient care, and clinical documentation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- pip (Python package manager)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd clinic-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb clinicdb
psql -d postgres -c "CREATE USER clinicuser WITH PASSWORD 'admin';"
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE clinicdb TO clinicuser;"

# Initialize database
flask init-db

# Run the application
python app.py
```

**Access**: http://localhost:5050

## 📋 Features

### Core Functionality
- ✅ **Patient Management**: Registration, profiles, medical history
- ✅ **Appointment Scheduling**: Booking, conflict detection, status tracking
- ✅ **Clinical Documentation**: Comprehensive physiotherapy assessments
- ✅ **User Management**: Role-based access control (Admin, Receptionist, Doctor)
- ✅ **Treatment Packages**: Session-based treatment planning
- ✅ **Data Export**: CSV and calendar exports
- ✅ **Backup System**: Automated daily database backups

### Advanced Features
- ✅ **Comprehensive Assessments**: 50+ clinical fields in structured format
- ✅ **Treatment Methods**: Advanced physiotherapy interventions
- ✅ **Equipment Tracking**: State-of-the-art facility usage
- ✅ **Progress Monitoring**: Pre/post treatment measurements
- ✅ **Patient Education**: Home exercise programs, activity modifications
- ✅ **Safety Protocols**: Consent, contraindications, safety checks

## 👥 User Roles

### Administrator
- Full system access
- User management
- System configuration
- Database backups

### Receptionist
- Patient registration and management
- Appointment scheduling
- Doctor management
- Basic reporting

### Doctor
- Clinical documentation
- Patient history review
- Treatment planning
- Comprehensive assessments

## 🗄️ Database

The system uses PostgreSQL with 6 main tables:
- `users` - Authentication and authorization
- `patients` - Patient demographics and medical history
- `doctors` - Healthcare provider information
- `appointments` - Scheduling and management
- `packages` - Treatment package management
- `notes` - Clinical documentation (JSON storage)

## 📚 Documentation

- **[System Documentation](SYSTEM_DOCUMENTATION.md)** - Complete technical documentation
- **[Database Schema](database_schema.md)** - Detailed database structure
- **[API Documentation](SYSTEM_DOCUMENTATION.md#api-documentation)** - API endpoints and usage

## 🔐 Security

- Password hashing with Werkzeug
- Role-based access control
- Session management
- Input validation
- SQL injection prevention
- XSS protection

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 app:app

# Using Docker
docker build -t clinic-system .
docker run -p 5050:5050 clinic-system
```

## 🛠️ Configuration

### Environment Variables
```bash
SQLALCHEMY_DATABASE_URI=postgresql://clinicuser:admin@localhost/clinicdb
SECRET_KEY=your-secure-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False
```

## 📞 Support

- **Technical Support**: [support@clinic-system.com]
- **Documentation**: [docs@clinic-system.com]
- **Emergency Contact**: [emergency@clinic-system.com]

## 📄 License

This software is proprietary and confidential. Unauthorized copying, distribution, or modification is prohibited.

---

**Version**: 1.0  
**Last Updated**: January 2024 