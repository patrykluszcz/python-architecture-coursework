class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if stock < 0:
            raise ValueError("Stock cannot be negative")

        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def decrease_stock(self, quantity: int) -> bool:
        if quantity > self.stock:
            return False
        self.stock -= quantity
        return True

    def increase_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.stock += quantity

    def __repr__(self) -> str:
        return (
            f"Product(id={self.product_id}, name={self.name}, "
            f"price={self.price}, stock={self.stock})"
        )
