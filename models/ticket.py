class Ticket:
    def __init__(self, ticket_id, user_id, ticket_type, message, created_at):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.ticket_type = ticket_type
        self.message = message
        self.created_at = created_at

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "ticket_type": self.ticket_type,
            "message": self.message,
            "created_at": self.created_at,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["ticket_id"],
            data["user_id"],
            data["ticket_type"],
            data["message"],
            data["created_at"],
        )
    
    def __repr__(self):
        return f"Ticket(ticket_id={self.ticket_id}, user_id={self.user_id}, ticket_type={self.ticket_type}, message={self.message}, created_at={self.created_at})"
    
    def __str__(self):
        return f"ID: {self.ticket_id}; Ticket type: {self.ticket_type}; Message: ({self.message}; Created on: {self.created_at})"

    def __add__(self, other):
        return str(self) + other    
    
    def __eq__(self, other):
        return (
            self.ticket_id == other.ticket_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return self.created_at < other.created_at
    
    def __gt__(self, other):
        return self.created_at > other.created_at
    
    def __le__(self, other):
        return self.created_at <= other.created_at
    
    def __ge__(self, other):
        return self.created_at >= other.created_at
    
