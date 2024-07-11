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

class Order:
    def __init__(self, order_id, game, product, total_price, quantity, transaction_type, transaction_date):
        self.order_id = order_id
        self.game = game
        self.product = product
        self.total_price = total_price
        self.quantity = quantity
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "game": self.game,
            "product": self.product,
            "total_price": self.total_price,
            "quantity": self.quantity,
            "transaction_type": self.transaction_type,
            "transaction_date": self.transaction_date
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["order_id"],
            data["game"],
            data["product"],
            data["total_price"],
            data["quantity"],
            data["transaction_type"],
            data["transaction_date"]
        )
    
    def __repr__(self):
        return json.dumps(self.to_dict())

    def __add__(self, other):
        return str(self) + other    
    
    def __eq__(self, other):
        return (
            self.order_id == other.order_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        