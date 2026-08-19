
from pydantic import BaseModel

class AIAssistRequest(BaseModel):
    stagingIds: list[str]
    triggeredBy: str


class ApproveRequest(BaseModel):
    approvedBy: str
    remarks: str