from enum import Enum

class UserRole(Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"