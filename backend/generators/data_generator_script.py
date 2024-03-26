from services.data_generator_service import DataGeneratorService
from repositories.event_repository import EventRepository
from repositories.order_repository import OrderRepository

def main():
    event_repo = EventRepository(...)
    order_repo = OrderRepository(...)

    data_gen_service = DataGeneratorService(event_repo, order_repo, ...)

    data_gen_service.seed_categories()

if __name__ == "__main__":
    main()