from datetime import datetime
from enum import Enum
from typing import List, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from product import Product
from user import User

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order:
    def __init__(
        self,
        order_id: str,
        user: User,
        items: List[Tuple[Product, int]],
    ):
        if not items:
            raise ValueError("Order must contain at least one item")

        self.order_id = order_id
        self.user = user
        self.items = items
        self.status = OrderStatus.PENDING
        self.creation_date = datetime.now()
        self.total_price = self._calculate_total()

    def _calculate_total(self) -> float:
        return sum(product.price * quantity for product, quantity in self.items)

    def update_status(self, new_status: OrderStatus) -> None:
        self.status = new_status

    def to_xml(self) -> str:
        root = Element("order")
        root.set("id", self.order_id)

        metadata = SubElement(root, "metadata")
        SubElement(metadata, "status").text = self.status.value
        SubElement(metadata, "creation_date").text = self.creation_date.isoformat()
        SubElement(metadata, "total_price").text = str(self.total_price)

        user_elem = SubElement(root, "user")
        SubElement(user_elem, "id").text = self.user.user_id
        SubElement(user_elem, "username").text = self.user.username
        SubElement(user_elem, "email").text = self.user.email

        if self.user.address:
            SubElement(user_elem, "address").text = self.user.address

        items_elem = SubElement(root, "items")
        for product, quantity in self.items:
            item = SubElement(items_elem, "item")
            SubElement(item, "product_id").text = product.product_id
            SubElement(item, "product_name").text = product.name
            SubElement(item, "unit_price").text = str(product.price)
            SubElement(item, "quantity").text = str(quantity)
            item_total = product.price * quantity
            SubElement(item, "item_total").text = str(item_total)

        rough_string = tostring(root, encoding="unicode")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def __repr__(self) -> str:
        return (
            f"Order(id={self.order_id}, user={self.user.username}, "
            f"status={self.status.value}, total={self.total_price})"
        )
