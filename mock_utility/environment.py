from pydantic import BaseModel


class UtilityAccount(BaseModel):
    account_id: str
    customer_name: str
    balance_due: float
    service_status: str


class UtilityEnvironment(BaseModel):
    accounts: list[UtilityAccount] = []
    adjustments_log: list[dict] = []