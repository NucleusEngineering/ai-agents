class Order:
    def __init__(self, order_id, user_id, product_id, total_price, quantity, transaction_type):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.total_price = total_price
        self.quantity = quantity
        self.transaction_type = transaction_type

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "total_price": self.total_price,
            "quantity": self.quantity,
            "transaction_type": self.transaction_type
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["order_id"],
            data["user_id"],
            data["product_id"],
            data["total_price"],
            data["quantity"],
            data["transaction_type"]
        )
    
    def __repr__(self):
        return f"Order(order_id={self.order_id}, user_id={self.user_id}, product_id={self.product_id}, total_price={self.total_price}, quantity={self.quantity}, transaction_type={self.transaction_type})"
    
    def __str__(self):
        return f"ID: {self.order_id}; Transaction Type: {self.transaction_type}; Total price: {self.total_price}"

    def __add__(self, other):
        return str(self) + other    
    
    def __eq__(self, other):
        return (
            self.order_id == other.order_id
        )
    
    def __ne__(self, other):
        return not self.__eq__(other)
        