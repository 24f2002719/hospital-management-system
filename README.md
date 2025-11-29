# Hospital Management System

hospital-management-system is a modern application project of full-stack Hospital Management System (HMS) that replaces manual registers with an efficient digital workflow. It helps hospitals manage patients, doctors, appointments, treatments, billing, and reporting.

## 🚀 Features at a Glance
- Role-based Access Control
  - Admin: full system management (doctors, patients, appointments)
  - Doctor: manage availability, view and treat patients
  - Patient: register, book appointments, view history
- Smart Scheduling: prevent double-booking and manage availability
- Digital Prescriptions: create diagnoses and treatment plans
- Search & Filter: doctors by specialization, patients by name/ID
- Interactive Dashboards with role-specific stats
- Analytics: appointment trends and specialization demand (Chart.js)
- Redis caching for frequently-accessed endpoints

## ⚡ Advanced Features
- Background Jobs (Celery)
  - Daily Reminders — emails patients with same-day appointments
  - Monthly Reports — HTML/CSV/PDF emails to doctors summarizing activity
  - Export Patient History — CSV export via asynchronous task
- Performance: Redis caching to reduce DB load for common endpoints

## 🛠️ Tech Stack
- Backend: Flask + Flask-Security-Too + SQLAlchemy
- Database: SQLite (for dev)
- Async Jobs & Broker: Celery + Redis
- Caching: Flask-Caching (Redis)
- Mail: Flask-Mail (use MailHog for local testing)
- Frontend: Vue 3 (Composition API) + Pinia + Bootstrap 5
- Charts: Chart.js

---

## ⚙️ Prerequisites
- Python 3.8+
- Node.js & npm
- Redis server
- MailHog (for local email testing)

---

## 🔧 Installation & Setup

### Backend Setup (Windows PowerShell)
1. Clone the repository and go to backend:
```powershell
git clone <repository_url>
cd "e:\Project\Python\Mad 2 Project\hospital-management-system\backend"
```

2. Create and activate a virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Start Redis and MailHog (examples using Docker):
```powershell
docker run -d -p 6379:6379 --name redis redis
docker run -d -p 1025:1025 -p 8025:8025 --name mailhog mailhog/mailhog
```

4. Configure environment variables if needed (SECRET_KEY, CELERY_BROKER_URL, MAIL settings) — edit `config.py` or set environment vars.

5. Initialize DB and seed (if a seeder exists):
```powershell
python -m scripts.init_db

python seed.py
```

6. Start the Flask app:
```powershell
python app.py
```

7. Start Celery worker & beat (from backend folder):
```powershell
# Set the PYTHONPATH to backend folder if running from backend
$env:PYTHONPATH = (Get-Location).Path

# Worker:
celery -A celery_worker.celery worker --pool=eventlet --loglevel=info

# Or single command (worker + beat):
celery -A celery_worker.celery worker --beat --loglevel=info
```

> If Celery can’t find `celery_worker`, run commands from the backend folder or use `-A backend.celery_worker.celery` from project root.

---

### Frontend Setup
1. Go to the frontend folder:
```powershell
cd ..\frontend
npm install
npm run dev
```

2. Open the Dev Server: http://localhost:5173

---

## 🔑 Default Credentials (seeded)
After seeding/initialization:
- Admin: admin@gmail.com / admin123
- Doctor: doctor@gmail.com / doctor123
- Patient: patient@gmail.com / patient123
(Confirm values from `scripts/init_db.py` or `seed.py` as they may differ.)

---

## 📖 Usage Guide
Basic workflow:
1. Admin creates specializations and doctors.
2. Doctor logs in and configures weekly availability.
3. Patient registers, searches for available doctors, and books a slot.
4. Doctor marks appointment `Completed` and adds treatment, diagnosis, and prescription.
5. Patient can pay (dummy payment) and request history exports.

---

## 📂 API & Cache Strategy
- `/api/public/doctors` — cached (TTL: 600s)
- `/api/doctors/<id>/slots` — short TTL (60s) so availability stays fresh
- Caches invalidate when admin updates doctors or availability

---

## 🤖 Celery Jobs & Testing
- `send_daily_reminders` — daily scheduled — notifies patients for that day
- `send_monthly_reports` — monthly scheduled — sends report to doctors
- `export_patient_history` — triggered by user — async CSV export

### Quick test for send_daily_reminders (synchronous)
Run from backend folder:
```powershell
python -c "
from tasks import send_daily_reminders
send_daily_reminders()"
    
```

### Enqueue the task (async)
```powershell
python - <<'PY'
from app import app
from tasks import send_daily_reminders
with app.app_context():
    send_daily_reminders.delay()
    print("Enqueued send_daily_reminders")
PY
```

- Check MailHog to confirm emails: http://localhost:8025
- Validate Celery worker logs to see task registrations and outcomes.

---

## 🧩 Debugging & Common Issues
- 401 Unauthorized: ensure Authorization header: `Authorization: Bearer <token>` after login.
- Celery import errors: run the `celery` command from backend folder or use `-A backend.celery_worker.celery`.
- Mail not sent by Celery: Verify Celery worker wraps tasks in Flask app context and the Mail extension is configured. See `celery_worker.py` using ContextTask to add app context.
- Circular imports: avoid importing `app` at module import time from modules used by `app` — use `current_app` or lazy imports.

---

## 📄 Reports & Export Formats
- Reports include a CSV and HTML attachment; PDFs generated via WeasyPrint or pdfkit/wkhtmltopdf if installed.
- If PDF generation fails, HTML and CSV fall back.

---

## 🧪 Testing Checklist
- Redis & MailHog up and running
- Flask app running (python app.py)
- Celery worker running (Celery logs should show registered tasks)
- Test sending a reminder by creating a `BOOKED` appointment for today and running `send_daily_reminders.run()` (synchronous) or queuing it.



## 📜 License
This repository is for educational purposes — part of the Modern Application Development II course.
