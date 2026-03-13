import uuid
from datetime import datetime


def generate_transaction_id() -> str:
    date = datetime.now().strftime("%Y%m%d")
    unique = str(uuid.uuid4()).split("-")[0]
    return f"RCP-{date}-{unique}"