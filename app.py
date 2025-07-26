from flask import Flask, render_template, redirect, url_for, request, flash, send_file, session, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta
from sqlalchemy import or_
import pandas as pd
from ics import Calendar, Event
from io import StringIO, BytesIO
from datetime import time as dt_time
import shutil
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clinicuser:admin@localhost/clinicdb'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this in production
app.config['BACKUP_DONE'] = False

db = SQLAlchemy(app)

# Custom Jinja2 filter for converting newlines to <br> tags
@app.template_filter('nl2br')
def nl2br_filter(text):
    if text:
        return text.replace('\n', '<br>')
    return text

# Custom Jinja2 filter for parsing JSON strings
@app.template_filter('fromjson')
def fromjson_filter(text):
    if text and text.strip().startswith('{'):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return None
    return None

# --- Models will be added here ---

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    contact_info = db.Column(db.String)
    medical_history = db.Column(db.Text)
    family_history = db.Column(db.Text)
    social_history = db.Column(db.Text)
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')
    packages = db.relationship('Package', back_populates='patient', cascade='all, delete-orphan')
    notes = db.relationship('Note', back_populates='patient', cascade='all, delete-orphan')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    status = db.Column(db.String)
    appointments = db.relationship('Appointment', back_populates='doctor')
    notes = db.relationship('Note', back_populates='doctor')
    user = db.relationship('User', back_populates='doctor', uselist=False)

class Package(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    start_date = db.Column(db.Date)
    weekdays = db.Column(db.String)  # Store as comma-separated string
    total_sessions = db.Column(db.Integer, default=12)
    status = db.Column(db.String)
    patient = db.relationship('Patient', back_populates='packages')
    appointments = db.relationship('Appointment', back_populates='package')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    duration = db.Column(db.Integer)
    reason = db.Column(db.Text)
    status = db.Column(db.String)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'))
    appointment_type = db.Column(db.String)
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')
    package = db.relationship('Package', back_populates='appointments')
    notes = db.relationship('Note', back_populates='appointment', cascade="all, delete-orphan")

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    note_type = db.Column(db.String)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    appointment = db.relationship('Appointment', back_populates='notes')
    doctor = db.relationship('Doctor', back_populates='notes')
    patient = db.relationship('Patient', back_populates='notes')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'doctor', 'receptionist', 'admin'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    doctor = db.relationship('Doctor', back_populates='user', uselist=False)

def has_conflict(doctor_id, date, start_time, duration, exclude_id=None):
    new_start = datetime.combine(date, start_time)
    new_end = new_start + timedelta(minutes=duration)
    query = Appointment.query.filter_by(doctor_id=doctor_id, date=date)
    if exclude_id:
        query = query.filter(Appointment.id != exclude_id)
    for appt in query:
        existing_start = datetime.combine(appt.date, appt.time)
        existing_end = existing_start + timedelta(minutes=appt.duration)
        if max(existing_start, new_start) < min(existing_end, new_end):
            return True
    return False

def daily_backup():
    today_str = datetime.now().strftime("%Y-%m-%d")
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgresql://','')
    db_path = db_path.replace('@localhost/','/') # Adjust for Windows/Linux
    backup_filename = os.path.join(backup_dir, f"appointments_backup_{today_str}.db")
    if os.path.exists(db_path) and not os.path.exists(backup_filename):
        shutil.copy(db_path, backup_filename)

@app.before_request
def run_daily_backup():
    if not app.config['BACKUP_DONE']:
        daily_backup()
        app.config['BACKUP_DONE'] = True

@app.route('/backup', methods=['POST'])
def manual_backup():
    daily_backup()
    flash('Manual backup completed!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/')
def dashboard():
    from datetime import date, timedelta
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    # Today
    todays_appointments = Appointment.query.filter_by(date=today).order_by(Appointment.time).all()
    # This week (today to Sunday)
    start_of_week = today
    end_of_week = today + timedelta(days=(6 - today.weekday()))  # Sunday
    weeks_appointments = Appointment.query.filter(Appointment.date > today, Appointment.date <= end_of_week).order_by(Appointment.date, Appointment.time).all()
    # Next week (next Monday to next Sunday)
    next_monday = end_of_week + timedelta(days=1)
    next_sunday = next_monday + timedelta(days=6)
    next_weeks_appointments = Appointment.query.filter(Appointment.date >= next_monday, Appointment.date <= next_sunday).order_by(Appointment.date, Appointment.time).all()
    all_statuses = ["Confirmed", "Pending", "Completed", "Cancelled", "Show", "No-show"]
    
    # Get network information for staff
    import socket
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network_url = f"http://{local_ip}:5050"
        server_ip = local_ip
    except:
        network_url = "http://localhost:5050"
        server_ip = "localhost"
    
    return render_template('dashboard.html', 
                         appointments=todays_appointments, 
                         weeks_appointments=weeks_appointments, 
                         next_weeks_appointments=next_weeks_appointments, 
                         all_statuses=all_statuses, 
                         today=today_str,
                         network_url=network_url,
                         server_ip=server_ip)

@app.route('/appointments')
def all_appointments():
    status = request.args.get('status', 'All')
    search = request.args.get('search', '').strip()
    query = Appointment.query
    if status and status != 'All':
        query = query.filter_by(status=status)
    if search:
        query = query.filter(or_(Appointment.patient.has(Patient.name.ilike(f'%{search}%')),
                                 Appointment.patient.has(Patient.phone.ilike(f'%{search}%')),
                                 Appointment.date.ilike(f'%{search}%')))
    appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    all_statuses = ["All", "Confirmed", "Pending", "Completed", "Cancelled", "Show", "No-show"]
    return render_template('all_appointments.html', appointments=appointments, all_statuses=all_statuses, selected_status=status, search_query=search)

@app.route('/add', methods=['GET', 'POST'])
def add_appointment():
    patients = Patient.query.order_by(Patient.name).all()
    doctors = Doctor.query.order_by(Doctor.name).all()
    all_statuses = ["Confirmed", "Pending", "Completed", "Cancelled", "Show", "No-show"]
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        if patient_id == 'new':
            new_name = request.form['new_patient_name']
            new_phone = request.form['new_patient_phone']
            new_gender = request.form['new_patient_gender']
            # Check if patient already exists by phone
            existing = Patient.query.filter_by(phone=new_phone).first()
            if existing:
                patient_id = existing.id
            else:
                new_patient = Patient(name=new_name, phone=new_phone, gender=new_gender)
                db.session.add(new_patient)
                db.session.commit()
                patient_id = new_patient.id
        else:
            patient_id = int(patient_id)
        doctor_id = int(request.form['doctor_id'])
        reason = request.form['reason']
        status = request.form['status']
        duration = int(request.form['duration'])
        appointment_type = request.form['appointment_type']
        if request.form.get('is_package') == 'on':
            package_start_date = request.form['package_start_date']
            package_time = request.form['package_time']
            num_appointments = int(request.form['num_appointments'])
            selected_weekdays = request.form.getlist('selected_weekdays')
            weekday_map = {"Saturday": 5, "Sunday": 6, "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3}
            appointments_list = []
            current_date = datetime.strptime(package_start_date, '%Y-%m-%d')
            while len(appointments_list) < num_appointments:
                if current_date.weekday() in [weekday_map[day] for day in selected_weekdays]:
                    if has_conflict(doctor_id, current_date, dt_time.fromisoformat(package_time), duration):
                        flash('Appointment conflict detected. The doctor is already booked during that time.', 'danger')
                        return redirect(url_for('add_appointment'))
                    appointments_list.append(Appointment(
                        patient_id=patient_id,
                        doctor_id=doctor_id,
                        date=current_date,
                        time=dt_time.fromisoformat(package_time),
                        duration=duration,
                        reason=reason,
                        status=status,
                        appointment_type=appointment_type
                    ))
                current_date += timedelta(days=1)
            db.session.add_all(appointments_list)
            db.session.commit()
            flash('Package appointments added successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            date_str = request.form['date']
            time_str = request.form['time']
            if has_conflict(doctor_id, datetime.strptime(date_str, '%Y-%m-%d'), dt_time.fromisoformat(time_str), duration):
                flash('Appointment conflict detected. The doctor is already booked during that time.', 'danger')
                return redirect(url_for('add_appointment'))
            new_appt = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=datetime.strptime(date_str, '%Y-%m-%d'),
                time=dt_time.fromisoformat(time_str),
                duration=duration,
                reason=reason,
                status=status,
                appointment_type=appointment_type
            )
            db.session.add(new_appt)
            db.session.commit()
            flash('Appointment added successfully!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('add_appointment.html', patients=patients, doctors=doctors, all_statuses=all_statuses)

@app.route('/update_status/<int:appt_id>', methods=['POST'])
def update_status(appt_id):
    new_status = request.form.get('status')
    appt = Appointment.query.get_or_404(appt_id)
    appt.status = new_status
    db.session.commit()
    flash(f'Status updated to {new_status}', 'success')
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:appt_id>', methods=['GET', 'POST'])
def edit_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    patients = Patient.query.order_by(Patient.name).all()
    doctors = Doctor.query.order_by(Doctor.name).all()
    all_statuses = ["Confirmed", "Pending", "Completed", "Cancelled", "Show", "No-show"]
    if request.method == 'POST':
        appt.patient_id = int(request.form['patient_id'])
        appt.doctor_id = int(request.form['doctor_id'])
        appt.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        appt.time = dt_time.fromisoformat(request.form['time'])
        appt.duration = int(request.form['duration'])
        appt.reason = request.form['reason']
        appt.status = request.form['status']
        appt.appointment_type = request.form['appointment_type']
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('all_appointments'))
    return render_template('edit_appointment.html', appt=appt, patients=patients, doctors=doctors, all_statuses=all_statuses)

@app.route('/delete/<int:appt_id>', methods=['POST'])
def delete_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    session['last_deleted'] = {
        'patient_name': appt.patient.name,
        'phone_number': appt.patient.phone,
        'doctor': appt.doctor.name,
        'date': appt.date.isoformat() if appt.date else None,
        'time': appt.time.strftime('%H:%M') if appt.time else None,
        'duration': appt.duration,
        'reason': appt.reason,
        'status': appt.status,
        'appointment_type': appt.appointment_type
    }
    db.session.delete(appt)
    db.session.commit()
    flash('Appointment deleted. You can undo this action.', 'warning')
    return redirect(url_for('all_appointments'))

@app.route('/undo_delete', methods=['POST'])
def undo_delete():
    last = session.pop('last_deleted', None)
    if last:
        doctor = Doctor.query.filter_by(name=last['doctor']).first()
        patient = Patient.query.filter_by(name=last['patient_name']).first()
        from datetime import datetime
        appt = Appointment(
            patient_id=patient.id if patient else None,
            doctor_id=doctor.id if doctor else None,
            date=datetime.fromisoformat(last['date']).date() if last['date'] else None,
            time=datetime.strptime(last['time'], '%H:%M').time() if last['time'] else None,
            duration=last['duration'],
            reason=last['reason'],
            status=last['status'],
            appointment_type=last.get('appointment_type')
        )
        db.session.add(appt)
        db.session.commit()
        flash('Last deleted appointment restored.', 'success')
    else:
        flash('No appointment to restore.', 'danger')
    return redirect(url_for('all_appointments'))

@app.route('/export/csv')
def export_csv():
    appointments = Appointment.query.order_by(Appointment.date, Appointment.time).all()
    df = pd.DataFrame([{
        'Patient Name': a.patient.name,
        'Phone Number': a.patient.phone,
        'Doctor': a.doctor.name,
        'Date': a.date,
        'Time': a.time,
        'Duration': a.duration,
        'Reason': a.reason,
        'Status': a.status
    } for a in appointments])
    csv = df.to_csv(index=False)
    return send_file(BytesIO(csv.encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='appointments.csv')

@app.route('/export/ics')
def export_ics():
    appointments = Appointment.query.order_by(Appointment.date, Appointment.time).all()
    cal = Calendar()
    for a in appointments:
        try:
            start_dt = datetime.strptime(f"{a.date} {a.time}", "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(minutes=a.duration)
            event = Event()
            event.name = f"{a.patient.name} with {a.doctor.name}"
            event.begin = start_dt
            event.end = end_dt
            event.description = f"Reason: {a.reason}\nStatus: {a.status}\nPhone: {a.patient.phone}"
            event.location = "Clinic"
            cal.events.add(event)
        except Exception:
            continue
    ics_bytes = str(cal).encode('utf-8')
    return send_file(BytesIO(ics_bytes), mimetype='text/calendar', as_attachment=True, download_name='appointments.ics')

@app.route('/vacancy', methods=['GET', 'POST'])
def doctor_vacancy():
    doctors = ["Dr. Abrar", "Dr. B", "Dr. C"]
    slots = []
    selected_doctor = None
    selected_date = None
    slot_duration = 60
    if request.method == 'POST':
        selected_doctor = request.form['doctor']
        selected_date = request.form['date']
        slot_duration = int(request.form['slot_duration'])
        # Generate slots: Sat-Thu, 9am-1pm and 5pm-9pm
        def generate_working_slots(start_time, end_time, duration):
            slots = []
            current = datetime.combine(datetime.today(), start_time)
            end = datetime.combine(datetime.today(), end_time)
            while current + timedelta(minutes=duration) <= end:
                slots.append(current.time())
                current += timedelta(minutes=duration)
            return slots
        morning_slots = generate_working_slots(dt_time(9, 0), dt_time(13, 0), slot_duration)
        evening_slots = generate_working_slots(dt_time(17, 0), dt_time(21, 0), slot_duration)
        all_possible_slots = morning_slots + evening_slots
        # Get booked times
        booked = Appointment.query.filter_by(doctor_id=int(selected_doctor), date=datetime.strptime(selected_date, '%Y-%m-%d')).all()
        booked_times = [datetime.strptime(b.time, "%H:%M").time() for b in booked]
        slots = [t.strftime("%H:%M") for t in all_possible_slots if t not in booked_times]
    return render_template('doctor_vacancy.html', doctors=doctors, slots=slots, selected_doctor=selected_doctor, selected_date=selected_date, slot_duration=slot_duration)

@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html')

@app.route('/calendar/events')
def calendar_events():
    appointments = Appointment.query.all()
    events = []
    for a in appointments:
        start = f"{a.date.isoformat()}T{a.time.strftime('%H:%M')}"
        end_dt = datetime.combine(a.date, a.time) + timedelta(minutes=a.duration)
        end = end_dt.strftime("%Y-%m-%dT%H:%M")
        color = '#0f766e' if a.status == 'Confirmed' else '#eab308' if a.status == 'Pending' else '#ef4444'
        events.append({
            'title': f"{a.patient.name} ({a.doctor.name})",
            'start': start,
            'end': end,
            'color': color,
            'description': f"Reason: {a.reason}\nStatus: {a.status}\nDoctor: {a.doctor.name}\nPatient: {a.patient.name}"
        })
    return jsonify(events)

@app.route('/appointments/<int:appt_id>')
def appointment_details(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    notes = Note.query.filter_by(appointment_id=appt_id).order_by(Note.created_at.desc()).all()
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('appointment_details.html', appt=appt, notes=notes, doctors=doctors)

@app.route('/appointments/<int:appt_id>/view')
def view_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    notes = Note.query.filter_by(appointment_id=appt_id).order_by(Note.created_at.desc()).all()
    return render_template('view_appointment.html', appt=appt, notes=notes)

@app.route('/appointments/<int:appt_id>/add_note', methods=['POST'])
def add_note(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    doctor_id = int(request.form['doctor_id'])
    note_type = request.form['note_type']
    content = request.form['content']
    now = datetime.now()
    note = Note(
        appointment_id=appt_id,
        doctor_id=doctor_id,
        patient_id=appt.patient_id,
        note_type=note_type,
        content=content,
        created_at=now,
        updated_at=now
    )
    db.session.add(note)
    db.session.commit()
    flash('Note added!', 'success')
    return redirect(url_for('appointment_details', appt_id=appt_id))

@app.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    doctors = Doctor.query.order_by(Doctor.name).all()
    if request.method == 'POST':
        note.doctor_id = int(request.form['doctor_id'])
        note.note_type = request.form['note_type']
        note.content = request.form['content']
        note.updated_at = datetime.now()
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('appointment_details', appt_id=note.appointment_id))
    return render_template('edit_note.html', note=note, doctors=doctors)

@app.route('/notes/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    appt_id = note.appointment_id
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!', 'warning')
    return redirect(url_for('appointment_details', appt_id=appt_id))

@app.route('/patients')
def list_patients():
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        
        # Handle date of birth
        date_of_birth = None
        if request.form.get('date_of_birth'):
            try:
                date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        contact_info = request.form.get('contact_info', '')
        medical_history = request.form.get('medical_history', '')
        family_history = request.form.get('family_history', '')
        social_history = request.form.get('social_history', '')
        
        patient = Patient(
            name=name, 
            phone=phone, 
            gender=gender,
            date_of_birth=date_of_birth,
            contact_info=contact_info,
            medical_history=medical_history,
            family_history=family_history,
            social_history=social_history
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient added!', 'success')
        return redirect(url_for('list_patients'))
    return render_template('add_patient.html')

@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.phone = request.form['phone']
        patient.gender = request.form['gender']
        
        # Handle date of birth
        if request.form.get('date_of_birth'):
            try:
                patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                patient.date_of_birth = None
        else:
            patient.date_of_birth = None
        
        patient.contact_info = request.form.get('contact_info', '')
        patient.medical_history = request.form.get('medical_history', '')
        patient.family_history = request.form.get('family_history', '')
        patient.social_history = request.form.get('social_history', '')
        
        db.session.commit()
        flash('Patient updated!', 'success')
        return redirect(url_for('list_patients'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted!', 'warning')
    return redirect(url_for('list_patients'))

@app.route('/patients/<int:patient_id>/profile')
def patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    today = datetime.now().date()
    return render_template('patient_profile.html', patient=patient, today=today)

@app.route('/patients/<int:patient_id>/history')
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    type_filter = request.args.get('type_filter', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    query = Appointment.query.filter_by(patient_id=patient_id)
    if type_filter:
        query = query.filter_by(appointment_type=type_filter)
    if date_from:
        query = query.filter(Appointment.date >= date_from)
    if date_to:
        query = query.filter(Appointment.date <= date_to)
    appointments = query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('patient_history.html', patient=patient, appointments=appointments)

# --- Doctor management ---
@app.route('/doctors')
def list_doctors():
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        phone = request.form['phone']
        email = request.form['email']
        status = request.form['status']
        doctor = Doctor(name=name, specialty=specialty, phone=phone, email=email, status=status)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added!', 'success')
        return redirect(url_for('list_doctors'))
    return render_template('add_doctor.html')

@app.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.specialty = request.form['specialty']
        doctor.phone = request.form['phone']
        doctor.email = request.form['email']
        doctor.status = request.form['status']
        db.session.commit()
        flash('Doctor updated!', 'success')
        return redirect(url_for('list_doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted!', 'warning')
    return redirect(url_for('list_doctors'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            session['doctor_id'] = user.doctor_id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/connect')
def connect_guide():
    """Connection guide page for staff to access the clinic system"""
    import socket
    try:
        # Get local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network_url = f"http://{local_ip}:5050"
        server_ip = local_ip
    except:
        network_url = "http://localhost:5050"
        server_ip = "localhost"
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('connect_guide.html', 
                         network_url=network_url,
                         server_ip=server_ip,
                         current_time=current_time)

# Protect register route (simple: only allow if logged in as admin)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            doctor_id=None,  # Only admin and receptionist roles can be created via registration
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database initialized.')

@app.route('/api/doctor_slots', methods=['GET'])
def api_doctor_slots():
    from datetime import time as dt_time
    doctor_id = int(request.args.get('doctor_id'))
    date_str = request.args.get('date')
    duration = int(request.args.get('duration', 60))
    if not doctor_id or not date_str:
        return {'slots': []}
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    def generate_working_slots(start_time, end_time, duration):
        slots = []
        current = datetime.combine(selected_date, start_time)
        end = datetime.combine(selected_date, end_time)
        while current + timedelta(minutes=duration) <= end:
            slots.append(current.time())
            current += timedelta(minutes=duration)
        return slots
    morning_slots = generate_working_slots(dt_time(9, 0), dt_time(13, 0), duration)
    evening_slots = generate_working_slots(dt_time(17, 0), dt_time(21, 0), duration)
    all_possible_slots = morning_slots + evening_slots
    booked = Appointment.query.filter_by(doctor_id=doctor_id, date=selected_date).all()
    booked_times = [b.time for b in booked]
    available = [t.strftime('%H:%M') for t in all_possible_slots if t not in booked_times]
    return {'slots': available}

@app.route('/doctor/appointment/<int:appt_id>', methods=['GET', 'POST'])
def doctor_appointment(appt_id):
    if session.get('role') != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    appt = Appointment.query.get_or_404(appt_id)
    if appt.doctor_id != session.get('doctor_id'):
        flash('You can only access your own appointments.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get notes for this appointment (needed for both GET and POST)
    notes = Note.query.filter_by(appointment_id=appt.id).order_by(Note.created_at.desc()).all()
    for note in notes:
        try:
            note.data = json.loads(note.content)
        except Exception:
            note.data = {}
    
    previous_notes = Note.query.filter(Note.patient_id == appt.patient_id, Note.appointment_id != appt.id).order_by(Note.created_at.desc()).limit(5).all()
    for note in previous_notes:
        try:
            note.data = json.loads(note.content)
        except Exception:
            note.data = {}
    session_number = None
    total_sessions = None
    if appt.package_id:
        package = Package.query.get(appt.package_id)
        if package:
            total_sessions = package.total_sessions
            all_appts = Appointment.query.filter_by(package_id=appt.package_id, patient_id=appt.patient_id).order_by(Appointment.date, Appointment.time).all()
            for idx, a in enumerate(all_appts, 1):
                if a.id == appt.id:
                    session_number = idx
                    break
    if request.method == 'POST':
        if 'end_appointment' in request.form:
            appt.status = 'Completed'
            db.session.commit()
            flash('Appointment marked as completed.', 'success')
            return redirect(url_for('dashboard'))
        
        # Comprehensive note data collection
        note_data = {}
        
        # Demographics & Chief Complaint
        note_data['chief_complaint'] = request.form.get('chief_complaint', '')
        note_data['pain_scale'] = request.form.get('pain_scale', '')
        note_data['pain_location'] = request.form.get('pain_location', '')
        note_data['functional_impact'] = request.form.get('functional_impact', '')
        note_data['aggravating_factors'] = request.form.get('aggravating_factors', '')
        note_data['relieving_factors'] = request.form.get('relieving_factors', '')
        
        # History of Present Illness
        note_data['onset'] = request.form.get('onset', '')
        note_data['duration'] = request.form.get('duration', '')
        note_data['mechanism_of_injury'] = request.form.get('mechanism_of_injury', '')
        note_data['previous_treatment'] = request.form.get('previous_treatment', '')
        note_data['response_to_treatment'] = request.form.get('response_to_treatment', '')
        note_data['red_flags'] = request.form.getlist('red_flags')
        
        # Physical Examination
        note_data['rom_active'] = request.form.get('rom_active', '')
        note_data['rom_passive'] = request.form.get('rom_passive', '')
        note_data['strength_testing'] = request.form.get('strength_testing', '')
        note_data['special_tests'] = request.form.get('special_tests', '')
        note_data['palpation'] = request.form.get('palpation', '')
        note_data['functional_tests'] = request.form.get('functional_tests', '')
        note_data['posture_assessment'] = request.form.get('posture_assessment', '')
        note_data['swelling_edema'] = request.form.get('swelling_edema', '')
        
        # Assessment & Diagnosis
        note_data['clinical_impression'] = request.form.get('clinical_impression', '')
        note_data['differential_diagnosis'] = request.form.get('differential_diagnosis', '')
        note_data['prognosis'] = request.form.get('prognosis', '')
        note_data['treatment_goals'] = request.form.get('treatment_goals', '')
        note_data['barriers_to_recovery'] = request.form.get('barriers_to_recovery', '')
        note_data['risk_factors'] = request.form.get('risk_factors', '')
        
        # Treatment Plan
        note_data['treatment_methods'] = request.form.getlist('treatment_methods')
        note_data['equipment_used'] = request.form.getlist('equipment_used')
        note_data['therapeutic_exercises'] = request.form.get('therapeutic_exercises', '')
        note_data['patient_education'] = request.form.get('patient_education', '')
        note_data['treatment_response'] = request.form.get('treatment_response', '')
        
        # Outcome Measures
        note_data['pain_scale_post'] = request.form.get('pain_scale_post', '')
        note_data['functional_scale'] = request.form.get('functional_scale', '')
        note_data['functional_score'] = request.form.get('functional_score', '')
        note_data['rom_measurements'] = request.form.get('rom_measurements', '')
        note_data['strength_measurements'] = request.form.get('strength_measurements', '')
        note_data['other_measurements'] = request.form.get('other_measurements', '')
        
        # Patient Education
        note_data['home_exercise_program'] = request.form.get('home_exercise_program', '')
        note_data['activity_modifications'] = request.form.get('activity_modifications', '')
        note_data['self_management'] = request.form.get('self_management', '')
        note_data['precautions'] = request.form.get('precautions', '')
        note_data['education_topics'] = request.form.getlist('education_topics')
        
        # Follow-up Plan
        note_data['next_appointment_date'] = request.form.get('next_appointment_date', '')
        note_data['treatment_frequency'] = request.form.get('treatment_frequency', '')
        note_data['estimated_duration'] = request.form.get('estimated_duration', '')
        note_data['referrals'] = request.form.get('referrals', '')
        note_data['imaging_required'] = request.form.get('imaging_required', '')
        note_data['discharge_criteria'] = request.form.get('discharge_criteria', '')
        
        # Attachments & Consent
        file_url = None
        if 'progress_file' in request.files and request.files['progress_file'].filename:
            file = request.files['progress_file']
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            file_url = '/' + file_path
        note_data['file_url'] = file_url
        note_data['vital_signs'] = request.form.get('vital_signs', '')
        note_data['consent_given'] = request.form.get('consent_given') == 'on'
        note_data['safety_checked'] = request.form.get('safety_checked') == 'on'
        note_data['contraindications_checked'] = request.form.get('contraindications_checked') == 'on'
        note_data['additional_notes'] = request.form.get('additional_notes', '')
        
        # Check if there's already a comprehensive note for this appointment
        existing_note = None
        for note in notes:
            if note.note_type == 'Comprehensive Physiotherapy Assessment':
                existing_note = note
                break
        
        now = datetime.now()
        if existing_note:
            # Update existing note
            existing_note.content = json.dumps(note_data)
            existing_note.updated_at = now
            db.session.commit()
            flash('Comprehensive physiotherapy note updated successfully!', 'success')
        else:
            # Create new note
            note = Note(
                appointment_id=appt.id,
                doctor_id=appt.doctor_id,
                patient_id=appt.patient_id,
                note_type='Comprehensive Physiotherapy Assessment',
                content=json.dumps(note_data),
                created_at=now,
                updated_at=now
            )
            db.session.add(note)
            db.session.commit()
            flash('Comprehensive physiotherapy note saved successfully!', 'success')
        return redirect(url_for('doctor_appointment', appt_id=appt.id))
    
    # Check if there's already a comprehensive note for this appointment
    existing_comprehensive_note = None
    for note in notes:
        if note.note_type == 'Comprehensive Physiotherapy Assessment':
            existing_comprehensive_note = note
            break
    
    today = datetime.now().date()
    return render_template('doctor_appointment.html', appt=appt, notes=notes, previous_notes=previous_notes, session_number=session_number, total_sessions=total_sessions, today=today, existing_note=existing_comprehensive_note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True) 