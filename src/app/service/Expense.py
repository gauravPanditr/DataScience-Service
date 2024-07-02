from langchain_core.pydantic_v1 import BaseModel, Field

class Expense(BaseModel):
    """Information about a transaction made on any Bank"""
    amount: str = Field(title="amount", description="Amount debited in the transaction")
    merchant: str = Field(title="merchant_name", description="Name of the merchant to which the amount was sent")
    TransactionDate: str = Field(title="transaction_date", description="Date of the transaction")
   
    def serialize(self):
        return {
            "amount": self.amount,
            "merchant": self.merchant_name,
            "transaction_date": self.transaction_date
        }
