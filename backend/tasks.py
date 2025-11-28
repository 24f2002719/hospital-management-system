from celery_worker import celery
from flask_mail import Message 
from database import cache
from flask import current_app
from models import db, User, Appointment, Doctor, AppointmentStatus
from datetime import datetime, timedelta
import csv
from io import StringIO
from sqlalchemy import func

# Import configured mail instance from app.py
from app import mail

try:
    from weasyprint import HTML as WeasyHTML
    _HAS_WEASY = True
except Exception:
    _HAS_WEASY = False


# -------------------------------------
# 1. TRIGGERED JOB: EXPORT CSV
# -------------------------------------
@celery.task(name='export_patient_history')
def export_patient_history(user_id, email):
    """Generates CSV of past treatments and emails it"""
    with current_app.app_context():
        user = User.query.get(user_id)
        if not user or not user.patient_profile:
            return "User not found"

        patient = user.patient_profile

        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['Date', 'Doctor', 'Diagnosis', 'Prescription'])

        for appt in patient.appointments:
            if appt.treatment:
                cw.writerow([
                    appt.appointment_date,
                    appt.doctor.user.name,
                    appt.treatment.diagnosis,
                    appt.treatment.prescription
                ])

        msg = Message(
            subject="Your Medical History Export 📂",
            recipients=[email],
            body="Please find your medical history attached."
        )

        msg.attach("history.csv", "text/csv", si.getvalue())
        mail.send(msg)
        return f"CSV exported for {email}"


# -------------------------------------
# 2. DAILY REMINDER
# -------------------------------------
@celery.task(name='send_daily_reminders')
def send_daily_reminders():
    """Sends email to patients having appointments today"""
    with current_app.app_context():
        today = datetime.now().date()
        # Use func.date to support DateTime columns
        appointments = Appointment.query.filter(
            func.date(Appointment.appointment_date) == today,
            Appointment.status == AppointmentStatus.BOOKED
        ).all()

        if not appointments:
            return "No appointments today."

        count = 0
        for appt in appointments:
            if appt.patient and appt.patient.user:
                patient_email = appt.patient.user.email
                msg = Message(
                    subject="Appointment Reminder ⏰",
                    recipients=[patient_email],
                    body=f"Hello {appt.patient.user.name},\n\nReminder: You have an appointment with Dr. {appt.doctor.user.name} today at {appt.appointment_time}."
                )
                mail.send(msg)
                count += 1

        return f"Sent reminders for {count} appointments."


# -------------------------------------
# 3. MONTHLY REPORT (FIXED DATE FILTER & DEBUG)
# -------------------------------------
@celery.task(name='send_monthly_reports')
def send_monthly_reports(days: int = 30):
    """
    Generates detailed monthly report (or last `days`) for doctors and email as HTML, CSV and PDF.
    Fix: use func.date(...) between(start_date, end_date) to correctly match Date or DateTime columns.
    """

    with current_app.app_context():
        end_date = datetime.now().date()
        # include today in the period (last `days` days)
        start_date = end_date - timedelta(days=days - 1)

        doctors = Doctor.query.all()
        if not doctors:
            current_app.logger.info("No doctors found for monthly report.")
            return "No doctors."

        for doc in doctors:
            # If there's no user/email skip
            if not getattr(doc, "user", None) or not getattr(doc.user, "email", None):
                current_app.logger.info("Skipping doctor id=%s - no user/email.", getattr(doc, "id", None))
                continue

            # Use func.date so both Date and DateTime columns match correctly
            appts = Appointment.query.filter(
                Appointment.doctor_id == doc.id,
                func.date(Appointment.appointment_date).between(start_date, end_date)
            ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()

            # Debugging info - count all and matched appointment ids
            total_db_count = Appointment.query.filter_by(doctor_id=doc.id).count()
            matched_count = len(appts)
            current_app.logger.info(
                "Doctor id=%s email=%s total_in_db=%s matched_period=%s appt_ids=%s",
                doc.id, doc.user.email, total_db_count, matched_count, [a.id for a in appts]
            )

            if not appts:
                current_app.logger.info("No appointments for %s between %s and %s", doc.user.email, start_date, end_date)
                continue

            # Summary counters
            total_appts = matched_count
            status_counts = {}
            revenue_total = 0.0

            # Build CSV
            si = StringIO()
            cw = csv.writer(si)
            cw.writerow(['Date', 'Time', 'Patient', 'Status', 'Diagnosis', 'Prescription'])

            # Build HTML rows
            rows_html = ""
            for a in appts:
                status_name = getattr(a, "status", None)
                status_str = status_name.name if hasattr(status_name, "name") else str(status_name)
                diagnosis = getattr(a.treatment, "diagnosis", "") if getattr(a, "treatment", None) else ""
                prescription = getattr(a.treatment, "prescription", "") if getattr(a, "treatment", None) else ""
                patient_name = getattr(a.patient.user, "name", "") if getattr(a, "patient", None) and getattr(a.patient, "user", None) else ""

                cw.writerow([
                    a.appointment_date,
                    getattr(a, "appointment_time", ""),
                    patient_name,
                    status_str,
                    diagnosis,
                    prescription,
                ])

                rows_html += f"""
                <tr>
                    <td>{a.appointment_date}</td>
                    <td>{getattr(a, 'appointment_time', '')}</td>
                    <td>{patient_name}</td>
                    <td>{status_str}</td>
                    <td>{diagnosis}</td>
                    <td>{prescription}</td>
                </tr>
                """

                # update counters
                status_counts[status_str] = status_counts.get(status_str, 0) + 1

            # Build full HTML
            summary_html = "<ul>"
            summary_html += f"<li>Total Appointments: {total_appts}</li>"
            for st, cnt in status_counts.items():
                summary_html += f"<li>{st}: {cnt}</li>"
            summary_html += "</ul>"

            html_content = f"""<html>
              <head><meta charset="utf-8"><title>Monthly Report</title></head>
              <body>
                <h1>Monthly Activity Report</h1>
                <p>Doctor: Dr. {doc.user.name}</p>
                <p>Period: {start_date} — {end_date}</p>
                {summary_html}
                <table border="1" cellpadding="5" cellspacing="0">
                  <thead>
                    <tr>
                      <th>Date</th><th>Time</th><th>Patient</th><th>Status</th>
                      <th>Diagnosis</th><th>Prescription</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows_html}
                  </tbody>
                </table>
              </body>
            </html>"""

            # prepare message
            text_body = f"Dr. {doc.user.name}, monthly summary: {total_appts} appointments."

            msg = Message(
                subject=f"Monthly Activity Report - Dr. {doc.user.name}",
                recipients=[doc.user.email],
                body=text_body,
                html=html_content
            )

            # attach CSV
            csv_filename = f"monthly_report_doctor_{doc.id}.csv"
            msg.attach(csv_filename, "text/csv", si.getvalue())

            # convert to PDF if weasy is available
            pdf_bytes = None
            if _HAS_WEASY:
                try:
                    pdf_bytes = WeasyHTML(string=html_content).write_pdf()
                except Exception as e:
                    current_app.logger.warning("WeasyPrint failed for doc %s: %s", doc.id, e)
                    pdf_bytes = None

            if pdf_bytes:
                msg.attach(f"monthly_report_doctor_{doc.id}.pdf", "application/pdf", pdf_bytes)
            else:
                msg.attach(f"monthly_report_doctor_{doc.id}.html", "text/html", html_content)

            try:
                mail.send(msg)
                current_app.logger.info("Sent monthly report to %s", doc.user.email)
            except Exception as e:
                current_app.logger.error("Failed to send monthly report to %s: %s", doc.user.email, e)

        return "Monthly reports processed."