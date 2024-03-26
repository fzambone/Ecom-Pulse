from datetime import datetime
import random
from backend.repositories.models import Category, Event, Order, OrderItem, Product, Visitor
from repositories.event_repository import EventRepository
from repositories.order_repository import OrderRepository
from repositories.order_item_repository import OrderItemRepository
from repositories.product_repository import ProductRepository
from repositories.visitor_repository import VisitorRepository
from repositories.category_repository import CategoryRepository
from faker import Faker

class DataGeneratorService:
    def __init__(self, event_repo: EventRepository, order_repo: OrderRepository, order_item_repo: OrderItemRepository, product_repo: ProductRepository, 
                 visitor_repo: VisitorRepository, category_repo: CategoryRepository):
        self.event_repo = event_repo
        self.order_repo = order_repo
        self.order_item_repo = order_item_repo
        self.product_repo = product_repo
        self.visitor_repo = visitor_repo
        self.category_repo = category_repo
        self.fake = Faker()

    def seed_categories(self):
        with open("backend/utils/categories.txt", "r") as f:
            existing_categories = self.category_repo.get_all_category_names()
            for line in f:
                category_name = line.strip()
                if category_name not in existing_categories:
                    self.category_repo.create(category_name)
    
    def generate_visitor(self):
        visitor_data = {
            'approximate_location': self.fake.country(),
            'session_start_time': self.fake.date_time_this_year(),
            'ip_address': self.fake.ipv4()
        }

        visitor = Visitor(**visitor_data)

        self.visitor_repo.create(visitor)
        return visitor
    
    def generate_event(self, visitor_id):
        event_types = ["view_homepage", "view_product", "add_to_cart", "purchase"]
        event_type = random.choice(event_types)

        event_data = {
            'timestamp': datetime.now(),
            'visitor_id': visitor_id,
            'event_type': event_type,
            'page_url': self.fake.uri() if event_type != 'purchase' else None,
            'product_id': None if event_type != "view_product" else self.product_repo.get_random_id(Product),
            'referrer': self.fake.uri() if random.choice([True, False]) else None,
        }

        event = Event(**event_data)

        if event_type == 'purchase':
            self.generate_order(visitor_id)

        self.event_repo.create(event)
        return event
    
    def generate_product(self):
        product_data = {
            'name': self.fake.sentence(nb_words=3).strip('.'),
            'category_id': self.category_repo.get_random_id(Category),
            'price': random.uniform(5.0, 200.0),
            'description': self.fake.text(max_nb_chars=200),
        }

        product = Product(**product_data)
        self.product_repo.create(product)
        return product
    
    def generate_order(self, visitor_id):
        num_items = random.randint(1, 3)
        products = [self.generate_product() for _ in range(num_items)]
        total_amount = sum(product.price for product in products)

        order_data = {
            'timestamp': datetime.now(),
            'visitor_id': visitor_id,
            'total_amount': total_amount,
        }
        
        order = Order(**order_data)
        self.order_repo.create(order)

        for product in products:
            quantity = random.randint(1, 2)
            order_item_data = {
                'order_id': order.id,
                'product_id': product.id,
                'quantity': quantity,
            }
            
            order_item = OrderItem(**order_item_data)
            self.order_item_repo.create(order_item)
        
        return order
    