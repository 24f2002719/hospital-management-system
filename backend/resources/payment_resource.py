from flask_restful import Resource
from flask_security import auth_token_required
from models import db, Appointment

# DELETE THIS LINE: from tasks import send_payment_invoice

class PaymentResource(Resource):
    @auth_token_required
    def post(self, appt_id):
        
        # --- FIX: IMPORT HERE (Local Import) ---
        from tasks import send_payment_invoice
        # ---------------------------------------

        appt = Appointment.query.get(appt_id)
        if not appt:
            return {"message": "Appointment not found"}, 404
        
        # 1. Update Database
        appt.is_paid = True
        db.session.commit()
        
        # 2. Trigger Email Job (Async)
        send_payment_invoice.delay(appt.id)
        
        return {"message": "Payment successful! Invoice sent."}, 200