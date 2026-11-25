# MediCare Hospital Management System — Pro Edition

A modular, colorful Streamlit + SQLite hospital management application for an academic demonstration.

## Project structure

```text
MediCare_Hospital_System_Pro/
├── app.py                 # Application entry point and navigation
├── database.py            # SQLite schema, sample data and database helpers
├── shared.py              # Shared imports and page helpers
├── style.py               # Color theme and CSS styling
├── requirements.txt       # Python dependencies
├── README.md              # Setup and project documentation
├── pages/
│   ├── dashboard.py
│   ├── analytics.py
│   ├── patients.py
│   ├── doctors.py
│   ├── op_section.py
│   ├── test_section.py
│   ├── appointments.py
│   ├── medical_records.py
│   ├── billing.py
│   └── __init__.py
└── assets/                # Place optional images/logo here
```

## Features
- Dashboard with patient, doctor, appointment, OP, laboratory and billing summaries
- Analytics charts and CSV exports
- Patient registration, directory, editing and discharge
- Doctor directory and management
- OP visit registration and status tracking
- Appointment scheduling and status updates
- Laboratory test requests, results and status tracking
- Medical records management
- Billing, payment tracking and revenue summaries
- Colorful responsive interface with gradient header, navy sidebar and dashboard cards

## Requirements
- Python 3.9 or newer
- Internet connection on first run if Streamlit needs to download dependencies

## Run on Windows
1. Extract the ZIP file.
2. Open the extracted `MediCare_Hospital_System_Pro` folder in VS Code.
3. Open Terminal and run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

4. Open `http://localhost:8501` in your browser.

## Run on macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Database
The SQLite database `hospital.db` is created automatically in the project folder on first run. Fictional demo doctors, patients, OP visits and lab tests are inserted only when their respective tables are empty. Keep a backup of `hospital.db` if you want to preserve records.

## Academic-use notice
This is an educational demonstration, not a production clinical system. Do not enter real patient information. A real deployment would require authentication, role-based access, audit logging, encryption, backups, privacy controls and clinical validation.


## Visual edition
This edition includes a premium purple-to-blue-to-mint gradient identity, a deep indigo navigation sidebar, soft glass-style cards, refined typography, elevated metric panels, rounded form controls, and responsive spacing. An internet connection is needed to load the optional Google Fonts; the app remains usable without them.
