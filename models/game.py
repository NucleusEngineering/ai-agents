class Game:
    def __init__(self, game_id, title, description, is_active):
        self.game_id = game_id
        self.title = title
        self.description = description
        self.is_active = is_active

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "title": self.title,
            "description": self.description,
            "is_active": self.is_active,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["game_id"],
            data["title"],
            data["description"],
            data["is_active"],
        )
    
    def __repr__(self):
        return f"Game(game_id={self.game_id}, title={self.title}, description={self.description}, is_active={self.is_active})"
    
    def __str__(self):
        return f"Title: {self.title}; Description: {self.description}"

    def __add__(self, other):
        return str(self) + other    
    
    def __eq__(self, other):
        return (
            self.game_id == other.game_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        