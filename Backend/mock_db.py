import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Any

class MockDatabase:
    def __init__(self):
        # Email (lowercased) -> User record
        self.users: Dict[str, Dict[str, Any]] = {}
        # Token string -> User email
        self.tokens: Dict[str, Dict[str, Any]] = {}

        self._seed_data()

    def _seed_data(self):
        seed_users = [
            {
                "id": str(uuid.uuid4()),
                "name": "PrimeCloud Admin",
                "email": "test@primecloud.io",
                "password": "password123",
                "role": "admin",
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Prime Developer",
                "email": "developer@primecloud.io",
                "password": "devpass456",
                "role": "developer",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        for user in seed_users:
            self.users[user["email"].lower()] = user

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.users.get(email.strip().lower())

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        for user in self.users.values():
            if user["id"] == user_id:
                return user
        return None

    def create_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        normalized_email = email.strip().lower()
        if normalized_email in self.users:
            raise ValueError("Email is already registered")

        new_user = {
            "id": str(uuid.uuid4()),
            "name": name.strip(),
            "email": normalized_email,
            "password": password,
            "role": "user",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.users[normalized_email] = new_user
        return new_user

    def reset_password(self, email: str, new_password: str) -> Dict[str, Any]:
        normalized_email = email.strip().lower()
        user = self.users.get(normalized_email)
        if not user:
            raise ValueError("No user found with the provided email")
        
        user["password"] = new_password
        user["updated_at"] = datetime.now(timezone.utc).isoformat()
        return user

    def create_token(self, email: str) -> str:
        token = f"prime_{uuid.uuid4().hex}"
        self.tokens[token] = {
            "email": email.strip().lower(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        return token

    def get_user_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        token_info = self.tokens.get(token)
        if not token_info:
            return None
        return self.get_user_by_email(token_info["email"])

    def revoke_token(self, token: str) -> bool:
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

# Global singleton mock instance
db = MockDatabase()
