# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json 

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
        return json.dumps(self.to_dict())
    
    def __eq__(self, other):
        return (
            self.game_id == other.game_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        