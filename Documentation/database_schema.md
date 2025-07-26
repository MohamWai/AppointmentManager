# 🏥 Clinic Management System - Database Schema

## 📋 Database Overview
This document describes the complete database schema for the Physiotherapy Clinic Management System, including all tables, relationships, and data structures.

---

## 🗄️ Tables

### Table users {
  id integer [primary key]
  username varchar [unique, not null]
  password_hash varchar [not null]
  role varchar [not null]               // 'admin', 'receptionist'
  doctor_id integer                     // FK to doctors.id (nullable)
  is_active boolean [default: true]
}

**Description**: User authentication and authorization system
- **role**: Limited to 'admin' and 'receptionist' (doctor accounts created separately)
- **doctor_id**: Links to existing doctor records (nullable for non-doctor users)
- **is_active**: Controls account status

### Table patients {
  id integer [primary key]
  name varchar
  phone varchar [not null]              // Removed unique constraint
  gender varchar
  date_of_birth date                    // Added for comprehensive patient history
  contact_info varchar                   // Additional contact information
  medical_history text                   // Patient's medical background
  family_history text                    // Family medical history
  social_history text                    // Social and lifestyle information
}

**Description**: Patient demographic and medical information
- **phone**: Multiple patients can share same phone number
- **date_of_birth**: Used for age calculation and patient profiling
- **medical_history**: Comprehensive medical background
- **family_history**: Family medical conditions
- **social_history**: Lifestyle, occupation, social factors

### Table doctors {
  id integer [primary key]
  name varchar [not null]
  specialty varchar
  phone varchar
  email varchar
  status varchar
}

**Description**: Healthcare provider information
- **specialty**: Doctor's area of expertise
- **status**: Active, inactive, on leave, etc.

### Table appointments {
  id integer [primary key]
  patient_id integer [not null]
  doctor_id integer [not null]
  date date
  time time
  duration integer
  reason text
  status varchar
  package_id integer
  appointment_type varchar
}

**Description**: Appointment scheduling and management
- **status**: Confirmed, Pending, Completed, Cancelled, Show, No-show
- **package_id**: Links to treatment packages
- **appointment_type**: Consultation, Procedure, Follow-up, Package Session, Other
- **duration**: Appointment length in minutes

### Table packages {
  id integer [primary key]
  patient_id integer [not null]
  start_date date
  weekdays varchar                       // Comma-separated string of weekdays
  total_sessions integer [default: 12]
  status varchar
}

**Description**: Treatment package management
- **weekdays**: Stored as comma-separated string (e.g., "Monday,Wednesday,Friday")
- **total_sessions**: Default 12 sessions per package
- **status**: Active, Completed, Cancelled, etc.

### Table notes {
  id integer [primary key]
  appointment_id integer [not null]
  doctor_id integer [not null]
  patient_id integer [not null]
  note_type varchar
  content text
  created_at timestamp
  updated_at timestamp
}

**Description**: Clinical documentation and notes
- **note_type**: "Comprehensive Physiotherapy Assessment", "Observation", "Prescription", etc.
- **content**: JSON-formatted data for comprehensive assessments, plain text for simple notes
- **created_at/updated_at**: Audit trail for note modifications

---

## 🔗 Relationships

### Primary Relationships
Ref: users.doctor_id > doctors.id
Ref: appointments.patient_id > patients.id
Ref: appointments.doctor_id > doctors.id
Ref: appointments.package_id > packages.id
Ref: packages.patient_id > patients.id
Ref: notes.appointment_id > appointments.id [delete: cascade]
Ref: notes.doctor_id > doctors.id
Ref: notes.patient_id > patients.id

### Cascade Delete Rules
- **notes.appointment_id**: CASCADE - Notes are deleted when appointment is deleted
- **All other relationships**: RESTRICT - Prevents deletion of referenced records

---

## 📊 Data Types and Constraints

### String Fields
- **varchar**: Variable-length strings (usernames, names, phone numbers)
- **text**: Long-form content (medical history, notes, reasons)

### Numeric Fields
- **integer**: IDs, durations, session counts
- **date**: Birth dates, appointment dates, package start dates
- **time**: Appointment times
- **timestamp**: Created/updated timestamps

### Boolean Fields
- **boolean**: Active status flags

### JSON Storage
- **content** field in notes table stores comprehensive physiotherapy data as JSON:
  ```json
  {
    "chief_complaint": "Patient reports...",
    "pain_scale": "7",
    "treatment_methods": ["Manual therapy", "Electrical therapy"],
    "equipment_used": ["Ultrasound", "Laser therapy"],
    "clinical_impression": "Diagnosis...",
    "treatment_goals": "Goals...",
    "home_exercise_program": "Exercises...",
    "next_appointment_date": "2024-01-15",
    "consent_given": true,
    "safety_checked": true,
    "contraindications_checked": true
  }
  ```

---

## 🔐 Security and Access Control

### User Roles
1. **Admin**: Full system access, user management, all operations
2. **Receptionist**: Patient management, appointment scheduling, basic operations
3. **Doctor**: Clinical notes, appointment management (linked to specific doctor)

### Authentication
- **password_hash**: Securely hashed passwords using Werkzeug
- **is_active**: Account status control
- **Session-based authentication** with role-based access control

---

## 📈 Data Flow

### Appointment Workflow
1. **Receptionist** creates appointment → `appointments` table
2. **Doctor** conducts session → `notes` table (comprehensive assessment)
3. **System** tracks progress → Status updates in `appointments` table

### Patient Journey
1. **Patient registration** → `patients` table
2. **Package creation** → `packages` table (optional)
3. **Appointment scheduling** → `appointments` table
4. **Clinical documentation** → `notes` table
5. **Progress tracking** → Multiple notes per patient

---

## 🛠️ Database Management

### Backup Strategy
- **Daily automated backups** to `backups/` directory
- **Manual backup triggers** via admin interface
- **PostgreSQL native backup** with timestamped files

### Indexes
- **Primary keys**: All tables have auto-incrementing primary keys
- **Unique constraints**: username in users table
- **Foreign keys**: All relationships properly indexed

### Data Integrity
- **Foreign key constraints** ensure referential integrity
- **Cascade deletes** for dependent records (notes → appointments)
- **Nullable fields** where appropriate for flexibility

---

## 📋 Sample Queries

### Get Patient's Complete History
```sql
SELECT 
    p.name as patient_name,
    a.date as appointment_date,
    d.name as doctor_name,
    n.note_type,
    n.content
FROM patients p
JOIN appointments a ON p.id = a.patient_id
JOIN doctors d ON a.doctor_id = d.id
LEFT JOIN notes n ON a.id = n.appointment_id
WHERE p.id = 1
ORDER BY a.date DESC, a.time DESC;
```

### Get Comprehensive Assessment Data
```sql
SELECT 
    content->>'chief_complaint' as chief_complaint,
    content->>'pain_scale' as pain_scale,
    content->>'treatment_methods' as treatment_methods,
    content->>'equipment_used' as equipment_used,
    content->>'clinical_impression' as clinical_impression
FROM notes 
WHERE note_type = 'Comprehensive Physiotherapy Assessment'
AND patient_id = 1;
```

### Get Doctor's Appointments
```sql
SELECT 
    a.date,
    a.time,
    p.name as patient_name,
    a.status,
    a.appointment_type
FROM appointments a
JOIN patients p ON a.patient_id = p.id
WHERE a.doctor_id = 1
AND a.date >= CURRENT_DATE
ORDER BY a.date, a.time;
```

---

## 🚀 System Features Supported

### Core Functionality
- ✅ **Patient Management**: Registration, profiles, medical history
- ✅ **Doctor Management**: Provider information, specialties
- ✅ **Appointment Scheduling**: Booking, status tracking, conflict detection
- ✅ **Package Management**: Treatment packages, session tracking
- ✅ **Clinical Documentation**: Comprehensive physiotherapy assessments
- ✅ **User Authentication**: Role-based access control
- ✅ **Data Export**: CSV and ICS calendar exports
- ✅ **Backup System**: Automated and manual backups

### Advanced Features
- ✅ **Comprehensive Assessments**: 50+ clinical fields in structured format
- ✅ **Treatment Methods**: Advanced physiotherapy interventions
- ✅ **Equipment Tracking**: State-of-the-art facility usage
- ✅ **Progress Monitoring**: Pre/post treatment measurements
- ✅ **Patient Education**: Home exercise programs, activity modifications
- ✅ **Safety Protocols**: Consent, contraindications, safety checks
- ✅ **Follow-up Planning**: Next appointments, treatment frequency
- ✅ **File Attachments**: Progress photos, documents

---

*This schema supports a complete physiotherapy clinic management system with comprehensive clinical documentation, patient tracking, and administrative functions.* 