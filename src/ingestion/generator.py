"""Faker generator za e-commerce podatke."""

import random 
from datetime import datetime 
from decimal import Decimal
from typing import List 
from uuid import uuid4

from faker import Faker 


from models import (Customer, Order, Product, OrderItem, OrderStatus, ProductCategory)


fake = Faker()
Faker.seed(42)
random.seed(42) 

def generate_customer_id() -> str:
    """Generira unique customer ID."""
    return f"CUST-{uuid4().hex[:8].upper()}"


def generate_product_id() -> str:
    """Generira unique product ID."""
    return f"PROD-{uuid4().hex[:8].upper()}"


def generate_order_id() -> str:
    """Generira unique order ID."""
    return f"ORD-{uuid4().hex[:8].upper()}"


def generate_order_item_id() -> str:
    """Generira unique order item ID."""
    return f"ITEM-{uuid4().hex[:8].upper()}"

def generate_customers(n: int = 100) -> List[Customer]:
    """
    Generira listu kupaca.
    
    Args:
        n: Broj kupaca za generiranje
        
    Returns:
        Lista Customer objekata
    """
    customers = []
    
    for _ in range(n):
        customer = Customer(
            customer_id=generate_customer_id(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            country=fake.country(),
            created_at=fake.date_time_between(
                start_date="-2y",  # Zadnje 2 godine
                end_date="now"
            )
        )
        customers.append(customer)
    
    return customers



    # Realistični nazivi proizvoda po kategoriji
PRODUCT_NAMES = {
    ProductCategory.ELECTRONICS: [
        "Wireless Mouse", "Mechanical Keyboard", "USB-C Hub",
        "Webcam HD", "Bluetooth Speaker", "Laptop Stand"
    ],
    ProductCategory.CLOTHING: [
        "Cotton T-Shirt", "Denim Jeans", "Winter Jacket",
        "Running Shoes", "Wool Sweater", "Baseball Cap"
    ],
    ProductCategory.HOME: [
        "Coffee Maker", "Desk Lamp", "Storage Box",
        "Wall Clock", "Throw Pillow", "Plant Pot"
    ],
    ProductCategory.SPORTS: [
        "Yoga Mat", "Dumbbells Set", "Resistance Bands",
        "Water Bottle", "Fitness Tracker", "Jump Rope"
    ],
    ProductCategory.BOOKS: [
        "Python Cookbook", "Data Science Guide", "Fiction Novel",
        "Biography", "Self-Help Book", "History Book"
    ],
}


def generate_products(n: int = 50) -> List[Product]:
    """Generira listu proizvoda."""
    products = []
    
    for _ in range(n):
        category = random.choice(list(ProductCategory))
        name = random.choice(PRODUCT_NAMES[category])
        
        product = Product(
            product_id=generate_product_id(),
            name=name,
            category=category,
            price=Decimal(str(round(random.uniform(9.99, 299.99), 2))),
            stock_quantity=random.randint(0, 500),
            created_at=fake.date_time_between(start_date="-1y", end_date="now")
        )
        products.append(product)
    
    return products





def generate_orders(
    customers: List[Customer],
    products: List[Product],
    n: int = 200
) -> tuple[List[Order], List[OrderItem]]:
    """
    Generira narudžbe i stavke narudžbi.
    
    Args:
        customers: Lista kupaca (za customer_id)
        products: Lista proizvoda (za order items)
        n: Broj narudžbi
        
    Returns:
        Tuple (orders, order_items)
    """
    orders = []
    order_items = []
    
    for _ in range(n):
        # Nasumično odaberi kupca
        customer = random.choice(customers)
        
        # Generiraj 1-5 stavki po narudžbi
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        # Kreiraj stavke narudžbe
        current_order_items = []
        total = Decimal("0.00")
        
        order_id = generate_order_id()
        
        for product in selected_products:
            quantity = random.randint(1, 3)
            
            item = OrderItem(
                order_item_id=generate_order_item_id(),
                order_id=order_id,
                product_id=product.product_id,
                quantity=quantity,
                unit_price=product.price
            )
            current_order_items.append(item)
            total += item.line_total
        
        # Kreiraj narudžbu
        order = Order(
            order_id=order_id,
            customer_id=customer.customer_id,
            order_date=fake.date_time_between(
                start_date="-6m",
                end_date="now"
            ),
            status=random.choice(list(OrderStatus)),
            total_amount=total
        )
        
        orders.append(order)
        order_items.extend(current_order_items)
    
    return orders, order_items



def generate_all_data(
    num_customers: int = 100,
    num_products: int = 50,
    num_orders: int = 200
) -> dict:
    """
    Generira sve podatke za e-commerce.
    
    Returns:
        Dictionary s svim generiranim podacima
    """
    print(f"Generating {num_customers} customers...")
    customers = generate_customers(num_customers)
    
    print(f"Generating {num_products} products...")
    products = generate_products(num_products)
    
    print(f"Generating {num_orders} orders...")
    orders, order_items = generate_orders(customers, products, num_orders)
    
    print(f"Generated {len(order_items)} order items")
    
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }


if __name__ == "__main__":
    # Generiraj podatke
    data = generate_all_data(
        num_customers=10,   # Mali broj za test
        num_products=5,
        num_orders=15
    )
    
    # Prikaži primjere
    print("\n=== Sample Customer ===")
    print(data["customers"][0].model_dump())
    
    print("\n=== Sample Product ===")
    print(data["products"][0].model_dump())
    
    print("\n=== Sample Order ===")
    print(data["orders"][0].model_dump())
    
    print("\n=== Sample Order Item ===")
    print(data["order_items"][0].model_dump())
    
    # Statistika
    print("\n=== Statistics ===")
    print(f"Total customers: {len(data['customers'])}")
    print(f"Total products: {len(data['products'])}")
    print(f"Total orders: {len(data['orders'])}")
    print(f"Total order items: {len(data['order_items'])}")