from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config

from models import (
    db,
    User,
    Patient,
    Doctor,
    Appointment,
    MedicalRecord
)

from datetime import datetime


# ==========================================
# Flask App Configuration
# ==========================================

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# ==========================================
# Flask Login Setup
# ==========================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


# ==========================================
# User Loader
# ==========================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================================
# Create Tables
# ==========================================

with app.app_context():
    db.create_all()


# ==========================================
# Home Route
# ==========================================

@app.route("/")
def home():

    if current_user.is_authenticated:

        if current_user.role == "patient":
            return redirect(
                url_for("patient_dashboard")
            )

        elif current_user.role == "doctor":
            return redirect(
                url_for("doctor_dashboard")
            )

    return redirect(url_for("login"))


# ==========================================
# Register Route
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        age = request.form.get("age")
        gender = request.form.get("gender")
        blood_group = request.form.get("blood_group")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        hashed_password = generate_password_hash(
            password
        )

        user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="patient"
        )

        db.session.add(user)
        db.session.commit()

        patient = Patient(
            user_id=user.id,
            age=age,
            gender=gender,
            blood_group=blood_group
        )

        db.session.add(patient)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# ==========================================
# Login Route
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if (
            user and
            check_password_hash(
                user.password,
                password
            )
        ):

            login_user(user)

            flash(
                "Login successful.",
                "success"
            )

            if user.role == "patient":

                return redirect(
                    url_for(
                        "patient_dashboard"
                    )
                )

            elif user.role == "doctor":

                return redirect(
                    url_for(
                        "doctor_dashboard"
                    )
                )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ==========================================
# Logout Route
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )
# ==========================================
# Patient Dashboard
# ==========================================

@app.route("/patient_dashboard")
@login_required
def patient_dashboard():

    if current_user.role != "patient":
        return redirect(url_for("login"))

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    total_appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).count()

    doctors_consulted = len(
        set(
            record.doctor_id
            for record in patient.medical_records
        )
    )

    total_records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).count()

    upcoming_appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).order_by(
        Appointment.appointment_date.desc()
    ).limit(5).all()

    recent_records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(
        MedicalRecord.visit_date.desc()
    ).limit(5).all()

    return render_template(
        "patient_dashboard.html",
        total_appointments=total_appointments,
        doctors_consulted=doctors_consulted,
        total_records=total_records,
        upcoming_appointments=upcoming_appointments,
        recent_records=recent_records
    )


# ==========================================
# Doctor Dashboard
# ==========================================

@app.route("/doctor_dashboard")
@login_required
def doctor_dashboard():

    if current_user.role != "doctor":
        return redirect(url_for("login"))

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    today = datetime.today().date()

    today_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).filter(
        Appointment.appointment_date == today
    ).count()

    total_patients = len(
        set(
            appointment.patient_id
            for appointment in doctor.appointments
        )
    )

    total_records = MedicalRecord.query.filter_by(
        doctor_id=doctor.id
    ).count()

    pending_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id,
        status="Pending"
    ).all()

    recent_records = MedicalRecord.query.filter_by(
        doctor_id=doctor.id
    ).order_by(
        MedicalRecord.visit_date.desc()
    ).limit(10).all()

    return render_template(
        "doctor_dashboard.html",
        specialization=doctor.specialization,
        today_appointments=today_appointments,
        total_patients=total_patients,
        total_records=total_records,
        pending_appointments=pending_appointments,
        recent_records=recent_records
    )


# ==========================================
# Appointments
# ==========================================

@app.route("/appointments")
@login_required
def appointments():

    if current_user.role == "patient":

        patient = Patient.query.filter_by(
            user_id=current_user.id
        ).first()

        appointments = Appointment.query.filter_by(
            patient_id=patient.id
        ).order_by(
            Appointment.appointment_date.desc()
        ).all()

    else:

        doctor = Doctor.query.filter_by(
            user_id=current_user.id
        ).first()

        appointments = Appointment.query.filter_by(
            doctor_id=doctor.id
        ).order_by(
            Appointment.appointment_date.desc()
        ).all()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


# ==========================================
# Book Appointment
# ==========================================

@app.route(
    "/book_appointment",
    methods=["GET", "POST"]
)
@login_required
def book_appointment():

    if current_user.role != "patient":
        return redirect(url_for("login"))

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    doctors = Doctor.query.all()

    if request.method == "POST":

        doctor_id = request.form.get(
            "doctor_id"
        )

        appointment_date = datetime.strptime(
            request.form.get(
                "appointment_date"
            ),
            "%Y-%m-%d"
        ).date()

        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status="Pending"
        )

        db.session.add(appointment)
        db.session.commit()

        flash(
            "Appointment booked successfully.",
            "success"
        )

        return redirect(
            url_for("appointments")
        )

    return render_template(
        "book_appointment.html",
        doctors=doctors
    )


# ==========================================
# Medical History
# ==========================================

@app.route("/medical_history")
@login_required
def medical_history():

    if current_user.role != "patient":
        return redirect(url_for("login"))

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(
        MedicalRecord.visit_date.desc()
    ).all()

    return render_template(
        "medical_history.html",
        records=records
    )


# ==========================================
# Add Medical Record
# ==========================================

@app.route(
    "/add_record/<int:patient_id>",
    methods=["GET", "POST"]
)
@login_required
def add_record(patient_id):

    if current_user.role != "doctor":
        return redirect(url_for("login"))

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    patient = Patient.query.get_or_404(
        patient_id
    )

    previous_records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(
        MedicalRecord.visit_date.desc()
    ).all()

    if request.method == "POST":

        diagnosis = request.form.get(
            "diagnosis"
        )

        prescription = request.form.get(
            "prescription"
        )

        notes = request.form.get(
            "notes"
        )

        record = MedicalRecord(
            patient_id=patient.id,
            doctor_id=doctor.id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )

        db.session.add(record)

        appointments = Appointment.query.filter_by(
            patient_id=patient.id,
            doctor_id=doctor.id,
            status="Pending"
        ).all()

        for appointment in appointments:
            appointment.status = "Completed"

        db.session.commit()

        flash(
            "Medical record added successfully.",
            "success"
        )

        return redirect(
            url_for("doctor_dashboard")
        )

    return render_template(
        "add_record.html",
        patient=patient,
        previous_records=previous_records
    )


# ==========================================
# Seed Doctors
# ==========================================

def seed_doctors():

    if Doctor.query.count() > 0:
        return

    specializations = [
        "Cardiologist",
        "Neurologist",
        "Orthopedic",
        "Dermatologist",
        "Pediatrician",
        "ENT Specialist",
        "General Physician",
        "Psychiatrist",
        "Oncologist",
        "Gynecologist"
    ]

    for i in range(1, 101):

        user = User(
            name=f"Doctor {i}",
            email=f"doctor{i}@hospital.com",
            password=generate_password_hash(
                "doctor123"
            ),
            role="doctor"
        )

        db.session.add(user)
        db.session.flush()

        doctor = Doctor(
            user_id=user.id,
            specialization=specializations[
                (i - 1) % len(specializations)
            ]
        )

        db.session.add(doctor)

    db.session.commit()

    print("100 Doctors Created Successfully")


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        seed_doctors()

    app.run(
        debug=True
    )