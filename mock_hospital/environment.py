from pydantic import BaseModel


class Patient(BaseModel):
    patient_id: str
    name: str
    current_medication: str
    allergies: list[str] = []


class HospitalEnvironment(BaseModel):
    patients: list[Patient] = []
    prescriptions_log: list[dict] = []