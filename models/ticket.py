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
        return json.dumps(self.to_dict())
    
    def __eq__(self, other):
        return (
            self.ticket_id == other.ticket_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
    