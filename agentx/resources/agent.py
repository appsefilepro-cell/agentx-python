from typing import Optional, List
from pydantic import BaseModel, Field
import requests
from agentx.util import get_headers
from .conversation import Conversation


class Agent(BaseModel):
    id: str = Field(alias="_id")
    name: str
    avatar: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    class Config:
        populate_by_name = True
        extra = "ignore"

    def __init__(self, **data):
        super().__init__(**data)

    def get_conversation(self, id: str) -> Conversation:
        list_of_conversations = self.list_conversations()
        conversation = next(
            (conv for conv in list_of_conversations if conv.id == id),
            None,
        )
        if conversation is None:
            raise Exception("404 - Conversation not found")
        return conversation

    def list_conversations(self) -> List[Conversation]:
        url = f"https://api.agentx.so/api/v1/access/agents/{self.id}/conversations"
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return [
                Conversation(
                    agent_id=self.id,
                    id=conv_res.get("_id"),
                    title=conv_res.get("title"),
                    users=conv_res.get("users"),
                    agents=conv_res.get("bots"),
                    createdAt=conv_res.get("createdAt"),
                    updatedAt=conv_res.get("updatedAt"),
                )
                for conv_res in response.json()
            ]
        else:
            raise Exception(f"Failed to retrieve agent details: {response.reason}")
