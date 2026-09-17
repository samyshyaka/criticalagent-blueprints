from pydantic import BaseModel


class Account(BaseModel):
    account_id: str
    customer_name: str
    balance: float
    routing_number: str


class BankEnvironment(BaseModel):
    accounts: list[Account] = []
    transactions_log: list[dict] = []