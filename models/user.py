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

class User:
    def __init__(self, user_id, email, name, avatar):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.avatar = avatar

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "avatar": self.name
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["user_id"],
            data["email"],
            data["name"],
            data["avatar"]
        )
    
    def __repr__(self):
        return json.dumps(self.to_dict())
        
    def __eq__(self, other):
        return (
            self.email == other.email
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)    