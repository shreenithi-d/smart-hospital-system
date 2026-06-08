from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# ==========================================
# User Table
# ==========================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )  # patient / doctor

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    patient = db.relationship(
        "Patient",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    doctor = db.relationship(
        "Doctor",
        backref="user",
        uselist=False,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<User {self.name}>"



# ==========================================
# Patient Table
# ==========================================

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    gender = db.Column(
        db.String(20),
        nullable=False
    )

    blood_group = db.Column(
        db.String(10),
        nullable=False
    )

    appointments = db.relationship(
        "Appointment",
        backref="patient",
        lazy=True,
        cascade="all, delete-orphan"
    )

    medical_records = db.relationship(
        "MedicalRecord",
        backref="patient",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Patient {self.user.name}>"



# ==========================================
# Doctor Table
# ==========================================

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    appointments = db.relationship(
        "Appointment",
        backref="doctor",
        lazy=True,
        cascade="all, delete-orphan"
    )

    medical_records = db.relationship(
        "MedicalRecord",
        backref="doctor",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Doctor {self.user.name}>"



# ==========================================
# Appointment Table
# ==========================================

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Appointment "
            f"{self.patient_id}-{self.doctor_id}>"
        )



# ==========================================
# Medical Record Table
# ==========================================

class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    diagnosis = db.Column(
        db.Text,
        nullable=False
    )

    prescription = db.Column(
        db.Text,
        nullable=False
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    visit_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<MedicalRecord "
            f"{self.patient_id}>"
        )