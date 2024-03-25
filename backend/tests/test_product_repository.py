
from datetime import datetime
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from backend.repositories.models import Product
from backend.repositories.product_repository import ProductRepository
from backend.tests.factories import ProductFactory
from backend.utils.database import Base

class TestProductRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:', echo=False, connect_args={"check_same_thread": False})
        Base.metadata.create_all(cls.engine)
        cls.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=cls.engine))

    @classmethod
    def tearDownClass(cls):
        try:
            Base.metadata.drop_all(cls.engine)
        finally:
            cls.engine.dispose()

    def setUp(self):
        self.session = self.Session()
        self.transaction = self.session.begin()
        ProductFactory._meta.sqlalchemy_session = self.session
        self.repository = ProductRepository(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_product(self):
        product_data = ProductFactory.build()

        created_product = self.repository.create(product_data)
        self.session.commit()

        product_in_db = self.session.query(Product).filter_by(name=product_data.name).first()
        self.assertIsNotNone(created_product.id, "Product ID should not be none")
        self.assertEqual(product_in_db.name, created_product.name, "Product names should match")
        self.assertEqual(product_in_db.price, created_product.price, "Product prices should match")
        self.assertEqual(product_in_db.description, created_product.description, "Product descriptions should match")
        self.assertEqual(product_in_db.quantity, created_product.quantity, "Product quantities should match")

    def test_get_product(self):
        inserted_product = ProductFactory()
        fetched_product = self.repository.get(inserted_product.id)

        self.assertIsNotNone(fetched_product, "Fetched product should not be None")
        self.assertEqual(fetched_product.id, inserted_product.id, "Product IDs should match")
        self.assertEqual(fetched_product.name, inserted_product.name, "Product names should match")

    def test_update_product(self):
        inserted_product = ProductFactory()
        self.session.commit()

        updated_name = "Updated Product Name"
        updated_price = 20.0
        inserted_product.name = updated_name
        inserted_product.price = updated_price

        self.repository.update(inserted_product)
        self.session.commit()

        updated_product = self.session.get(Product, inserted_product.id)

        self.assertEqual(updated_product.name, updated_name, "Product name should be updated")
        self.assertEqual(updated_product.price, updated_price, "Product price should be updated")

    def test_soft_delete_product(self):
        inserted_product = ProductFactory()
        self.session.commit()

        self.repository.soft_delete(inserted_product.id)
        self.session.commit()

        deleted_product = self.session.get(Product, inserted_product.id)
        all_products = self.repository.get_all()
        this_product = self.repository.get(inserted_product.id)

        self.assertIsNotNone(deleted_product.deleted_at, "Product should have a deleted_at timestamp")
        self.assertNotIn(deleted_product, all_products, "Soft-deleted products should not be included in get_all results (get_all)")
        self.assertIsNone(this_product, "Soft-deleted products should not be included in get_all results (get)")

    def test_restore_product(self):
        inserted_product = ProductFactory()
        self.session.commit()

        self.repository.soft_delete(inserted_product.id)
        self.session.commit()

        self.repository.restore(inserted_product.id)
        self.session.commit()

        restored_product = self.session.get(Product, inserted_product.id)
        all_products = self.repository.get_all()

        self.assertIsNone(restored_product.deleted_at, "Product's deleted_at should be None after restore")
        self.assertIn(restored_product, all_products, "Restored product should be included in get_all results")

    def test_hard_delete_product(self):
        inserted_product = ProductFactory()
        self.session.commit()

        self.repository.hard_delete(inserted_product.id)
        self.session.commit()

        deleted_product = self.session.get(Product, inserted_product.id)
        all_products = self.repository.get_all()
        
        self.assertIsNone(deleted_product, "The product should be completely removed from the database")
        self.assertNotIn(inserted_product, all_products, "Hard-deleted product should not be included in the results")


    def test_find_available_products(self):
        available_product = ProductFactory(quantity=10)
        out_of_stock_product = ProductFactory(quantity=0)
        deleted_product = ProductFactory(quantity=5, deleted_at=datetime.now())
        self.session.commit()

        available_products = self.repository.find_available_products()

        self.assertIn(available_product, available_products, "Product should be included in the results")
        self.assertNotIn(out_of_stock_product, available_products, "Out of stock product should not be included in the results")
        self.assertNotIn(deleted_product, available_products, "Soft-deleted product should not be included in the results")
