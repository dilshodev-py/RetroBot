from dataclasses import dataclass

from db.settings import CRUD


@dataclass
class User(CRUD):
    id : int = None
    first_name : str = None
    last_name : str = None
    phone_number : str = None
    latitude : float = None
    longitude : float = None

@dataclass
class Food(CRUD):
    id: int = None
    name: str = None
    quantity: int = None
    price: float = None
    description: str = None
    photo: str = None
    status: str = None

@dataclass
class Order(CRUD):
    id : int = None
    user_id : int = None
    total : float = None
    order_date : str = None
    status : str = None

@dataclass
class OrderItem(CRUD):
    id : int = None
    order_id : int = None
    count : int = None
    food_id : int = None

@dataclass
class BotEnv(CRUD):
    id : int = None
    deliver_price : float = None

@dataclass
class Payment(CRUD):
    id : int = None
    order_id : int = None
    user_id : int = None
    pay_amount : float = None
    pay_date : str = None
