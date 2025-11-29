from flask_restful import Resource
from flask_security import auth_token_required, current_user
from models import db, Appointment, Specialization, Doctor
from sqlalchemy import func

class AdminAnalyticsResource(Resource):
    @auth_token_required
    def get(self):
        if not current_user.has_role('admin'):
            return {"message": "Unauthorized"}, 403

        # 1. Appointments per Specialization (Pie Chart)
        # SQL: SELECT name, COUNT(*) FROM appointment JOIN doctor ... GROUP BY spec_id
        spec_stats = db.session.query(Specialization.name, func.count(Appointment.id))\
            .join(Doctor, Appointment.doctor_id == Doctor.id)\
            .join(Specialization, Doctor.specialization_id == Specialization.id)\
            .group_by(Specialization.name).all()
        
        pie_labels = [row[0] for row in spec_stats]
        pie_data = [row[1] for row in spec_stats]

        # 2. Appointments per Date (Last 7 dates found) (Line Chart)
        date_stats = db.session.query(Appointment.appointment_date, func.count(Appointment.id))\
            .group_by(Appointment.appointment_date)\
            .order_by(Appointment.appointment_date.desc())\
            .limit(7).all()
        
        # Reverse to show oldest to newest
        date_stats.reverse()
        line_labels = [str(row[0]) for row in date_stats]
        line_data = [row[1] for row in date_stats]

        return {
            "pie": {"labels": pie_labels, "data": pie_data},
            "line": {"labels": line_labels, "data": line_data}
        }, 200