import os
from dotenv import load_dotenv
import random
from datetime import datetime
from faker import Faker
from entities import Event, OrderItem, Visitor, Product, Order
import psycopg2

fake = Faker()

def seed_categories(conn):
    with open("categories.txt", "r") as f:
        existing_categories = conn.execute("SELECT name FROM categories").fetchall()
        existing_category_names = [item[0] for item in existing_categories]

        for line in f:
            category_name = line.strip()
            if category_name not in existing_category_names:
                conn.execute(
                    "INSERT INTO categories (name) VALUES ?", (category_name)
                )
    
    conn.commit()

def generate_event(visitor):
    event_types = ["view_homepage", "view_product", "add_to_cart", "purachase"]
    event_type = random.choice(event_types)

    event = Event(
        timestamp=datetime.now(),
        visitor_id=visitor.id,
        event_type=event_type
    )

    if event_type == "view_product":
        event.product_id = get_random_product(conn).id
    elif event_type == "purchase":
        num_items = random.randint(1, 3)
        products = [get_random_product() for _ in range(num_items)]
        order_items = []
        total_amount = 0.0

        for product in products:
            quantity = random.randint(1, 2)
            order_items.append(OrderItem(product_id=product.id, quantity=quantity))
            total_amount += product.price * quantity

        order = Order(timestamp=datetime.now(), visitor_id=visitor.id, items=order_items, total_amount=total_amount)

        insert_order(conn, order)

    return event

def insert_event(conn, event):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO events (timestamp, visitor_id, event_type, page_url, product_id, referrer)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (event.timestamp, event.visitor_id, event.event_type, event.page_url, event.product_id, event.referrer)
        )
    conn.commit()

def generate_visitor():
    ip_address = fake.ipv4()
    country = fake.country()
    return Visitor(id=random.randint(1, 1000),
                   approximate_location=country,
                   session_start_time=fake.date_time_this_year())

def insert_visitor(conn, visitor):
    with conn.cursor() as cur:
        print(f"Inserting: location={visitor.approximate_location}, time={visitor.session_start_time}")
        cur.execute(
            "INSERT INTO visitors (approximate_location, session_start_time) VALUES (%s, %s) RETURNING id",
            (visitor.approximate_location, visitor.session_start_time)
        )
        visitor_id = cur.fetchone()[0]
        conn.commit()
        return visitor_id

def insert_order(conn, order):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO orders (timestamp, visitor_id, total_amount) VALUES (%s, %s, %s)",
            (order.timestamp, order.visitor_id, order.total_amount)
        )
        order_id = cur.fetchone()[0]

        for item in order.items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item.product_id, item.quantity)
            )
    conn.commit()

def get_random_product(conn):

    product_name = fake.sentence(nb_words=4)
    price_str = fake.pricetag()[1:].replace(',', '')
    price = float(price_str)
    result = conn.cursor.execute("SELECT id FROM categories ORDER BY RANDOM() LIMIT 1").fetchone()
    category_id = result[0]

    return Product(
        id=random.randint(1, 100),
        name=product_name,
        category=category_id,
        price=price,
        description=fake.paragraph(nb_sentences=2),
    )

def connect_to_db():
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
    )
    return conn

load_dotenv()
conn = connect_to_db()

while True:
    visitor = generate_visitor()
    visitor_id = insert_visitor(conn, visitor)
    
    for _ in range(random.randint(1, 5)):
        event = generate_event(visitor)
        event.visitor_id = visitor_id
        insert_event(conn, event)