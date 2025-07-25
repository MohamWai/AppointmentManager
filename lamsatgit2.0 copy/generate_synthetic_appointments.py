import random
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

# Database setup
DB_PATH = "appointments.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Sample data pools
PATIENT_NAMES = [
    "Ali Al-Harthy", "Fatima Al-Zahra", "Mohammed Al-Lawati", "Sara Al-Balushi",
    "Ahmed Al-Maawali", "Mona Al-Hinai", "Salim Al-Shanfari", "Layla Al-Khalili"
]
PHONE_PREFIXES = ["921", "922", "923", "924", "925", "926", "927", "928"]
DOCTORS = ["Dr. Abrar", "Dr. B", "Dr. C"]
REASONS = [
    "Follow-up", "Consultation", "Routine Check", "Flu Symptoms", "Skin Rash",
    "Allergy", "Back Pain", "Headache"
]
STATUSES = ["Confirmed", "Pending", "Completed", "Cancelled", "Show", "No-show"]

def random_phone():
    return "968" + random.choice(PHONE_PREFIXES) + "".join([str(random.randint(0,9)) for _ in range(5)])

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def random_time():
    hour = random.choice(list(range(9, 13)) + list(range(17, 21)))
    minute = random.choice([0, 15, 30, 45])
    return f"{hour:02d}:{minute:02d}"

def generate_appointments(n=100):
    today = datetime.today()
    start_date = today - timedelta(days=60)
    end_date = today + timedelta(days=30)
    data = []
    for _ in range(n):
        name = random.choice(PATIENT_NAMES)
        phone = random_phone()
        doctor = random.choice(DOCTORS)
        date = random_date(start_date, end_date).strftime("%Y-%m-%d")
        time = random_time()
        duration = random.choice([15, 30, 45, 60])
        reason = random.choice(REASONS)
        status = random.choice(STATUSES)
        data.append({
            "Patient Name": name,
            "Phone Number": phone,
            "Doctor": doctor,
            "Date": date,
            "Time": time,
            "Duration": duration,
            "Reason": reason,
            "Status": status
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_appointments(200)  # Generate 200 synthetic appointments
    df.to_sql("appointments", engine, if_exists="append", index=False)
    print("Synthetic data inserted into appointments.db")
