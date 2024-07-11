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

class Character:
    def __init__(self, character_id, c1, c2, c3, c4):
        self.character_id = character_id
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

    def to_dict(self):
        return {
            "character_id": self.character_id,
            "c1": self.c1,
            "c2": self.c2,
            "c3": self.c3,
            "c4": self.c4
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["character_id"],
            data["c1"],
            data["c2"],
            data["c3"],
            data["c4"]
        )
    
    def __repr__(self):
        return json.dumps(self.to_dict())
    
    def __eq__(self, other):
        return (
            self.character_id == other.character_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        