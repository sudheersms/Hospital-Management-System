"""SQLite database setup and reusable data-access functions."""
import sqlite3
from datetime import date
from pathlib import Path
import pandas as pd

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "hospital.db"

# -------------------- Database --------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            blood_group TEXT,
            disease TEXT,
            admission_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Admitted'
        );
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            availability TEXT
        );
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT,
            status TEXT NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        );
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            bill_date TEXT NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            diagnosis TEXT,
            treatment TEXT,
            doctor_notes TEXT,
            record_date TEXT NOT NULL,
            ward TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        CREATE TABLE IF NOT EXISTS op_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            visit_time TEXT NOT NULL,
            symptoms TEXT,
            diagnosis TEXT,
            consultation_fee REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Completed',
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        );
        CREATE TABLE IF NOT EXISTS lab_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            test_date TEXT NOT NULL,
            result TEXT,
            notes TEXT,
            amount REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        """)
        # Seed sample data only when the corresponding tables are empty.
        if conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0] == 0:
            conn.executemany(
                """INSERT INTO patients(name,age,gender,phone,address,blood_group,disease,admission_date,status)
                   VALUES(?,?,?,?,?,?,?,?,?)""",
                [
                    ("Ananya Rao", 28, "Female", "9876501001", "MVP Colony, Visakhapatnam", "O+", "General check-up", date.today().isoformat(), "Admitted"),
                    ("Rahul Varma", 42, "Male", "9876501002", "Gajuwaka, Visakhapatnam", "B+", "Fever", date.today().isoformat(), "Admitted"),
                    ("Meera Sharma", 35, "Female", "9876501003", "Madhurawada, Visakhapatnam", "A+", "Migraine", date.today().isoformat(), "Discharged"),
                    ("Arjun Kumar", 51, "Male", "9876501004", "Seethammadhara, Visakhapatnam", "AB+", "Diabetes review", date.today().isoformat(), "Admitted"),
                    ("Priya Reddy", 23, "Female", "9876501005", "MVP Colony, Visakhapatnam", "O-", "Seasonal allergy", date.today().isoformat(), "Discharged"),
                ],
            )
        if conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO doctors(name,specialization,phone,email,availability) VALUES(?,?,?,?,?)",
                [
                    ("Dr. Kavya Rao", "Cardiologist", "9876511001", "kavya.rao@example.com", "Mon–Fri, 9 AM–1 PM"),
                    ("Dr. Arvind Kumar", "General Physician", "9876511002", "arvind.kumar@example.com", "Mon–Sat, 10 AM–4 PM"),
                    ("Dr. Neha Sharma", "Dermatologist", "9876511003", "neha.sharma@example.com", "Tue–Sat, 11 AM–3 PM"),
                    ("Dr. Sandeep Reddy", "Orthopedic", "9876511004", "sandeep.reddy@example.com", "Mon–Fri, 2 PM–6 PM"),
                    ("Dr. Divya Menon", "Pediatrician", "9876511005", "divya.menon@example.com", "Mon–Sat, 9 AM–12 PM"),
                ],
            )
        if conn.execute("SELECT COUNT(*) FROM op_visits").fetchone()[0] == 0:
            pids = [r[0] for r in conn.execute("SELECT id FROM patients ORDER BY id LIMIT 2").fetchall()]
            dids = [r[0] for r in conn.execute("SELECT id FROM doctors ORDER BY id LIMIT 2").fetchall()]
            if pids and dids:
                conn.executemany(
                    """INSERT INTO op_visits(patient_id,doctor_id,visit_date,visit_time,symptoms,diagnosis,consultation_fee,status)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    [
                        (pids[0], dids[1], date.today().isoformat(), "09:30", "Mild fever and headache", "Viral fever suspected", 500, "Completed"),
                        (pids[1], dids[0], date.today().isoformat(), "10:30", "Routine cardiac review", "Routine follow-up", 700, "Completed"),
                    ],
                )
        if conn.execute("SELECT COUNT(*) FROM lab_tests").fetchone()[0] == 0:
            pids = [r[0] for r in conn.execute("SELECT id FROM patients ORDER BY id LIMIT 2").fetchall()]
            if pids:
                conn.executemany(
                    """INSERT INTO lab_tests(patient_id,test_name,test_date,result,notes,amount,status)
                       VALUES(?,?,?,?,?,?,?)""",
                    [
                        (pids[0], "Complete Blood Count (CBC)", date.today().isoformat(), "Demo result: within reference range", "Sample report for demonstration", 450, "Completed"),
                        (pids[1], "Blood Glucose", date.today().isoformat(), "", "Fasting sample collected", 250, "Pending"),
                    ],
                )


init_db()


def query_df(sql, params=()):
    with get_conn() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def execute(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def scalar(sql):
    with get_conn() as conn:
        return conn.execute(sql).fetchone()[0]


def flash_success(message):
    st.success(message)


def patient_options(admitted_only=False):
    condition = "WHERE status='Admitted'" if admitted_only else ""
    return query_df(f"SELECT id, name FROM patients {condition} ORDER BY name")


def doctor_options():
    return query_df("SELECT id, name, specialization FROM doctors ORDER BY name")


