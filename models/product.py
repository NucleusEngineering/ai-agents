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

class Product:
    def __init__(self, product_id, title, description, price, is_active):
        self.product_id = product_id
        self.title = title
        self.description = description
        self.price = price
        self.is_active = is_active

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "is_active": self.is_active,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["product_title"],
            data["product_description"],
            data["product_price"],
            data["is_product_active"],
        )
    
    def __repr__(self):
        return json.dumps(self.to_dict())
    
    def __eq__(self, other):
        return (
            self.product_id == other.product_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        