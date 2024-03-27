import random

from backend.repositories.category_repository import CategoryRepository
from backend.repositories.event_repository import EventRepository
from backend.repositories.order_item_repository import OrderItemRepository
from backend.repositories.order_repository import OrderRepository
from backend.repositories.product_repository import ProductRepository
from backend.repositories.visitor_repository import VisitorRepository
from backend.services.data_generator_service import DataGeneratorService
from backend.utils.database import init_db, session_scope


def main():
    init_db()

    with session_scope() as db:
        event_repo = EventRepository(db)
        order_repo = OrderRepository(db)
        order_item_repo = OrderItemRepository(db)
        product_repo = ProductRepository(db)
        visitor_repo = VisitorRepository(db)
        category_repo = CategoryRepository(db)

        data_gen_service = DataGeneratorService(
            event_repo=event_repo,
            order_repo=order_repo,
            order_item_repo=order_item_repo,
            product_repo=product_repo,
            visitor_repo=visitor_repo,
            category_repo=category_repo
        )

        data_gen_service.seed_categories()

        number_of_visitors=10
        for _ in range(number_of_visitors):
            visitor = data_gen_service.generate_visitor()

            number_of_events = random.randint(1,10)
            for _ in range(number_of_events):
                data_gen_service.generate_event(visitor.id)

        print("Data generation completed successfully")

if __name__ == "__main__":
    main()