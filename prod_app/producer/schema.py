from pydantic import BaseModel, Field
# from typing import Optional, List


class MessageRequest(BaseModel):
    topic: str = "my_topic"
    message: str = "Testing message for MF"