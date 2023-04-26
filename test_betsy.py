import unittest
import main
from models import db, ProductTag
from main import (
    search,
    list_user_products,
    list_products_per_tag,
    add_product_to_catalog,
    update_stock,
    purchase_product,
    remove_product,
    validate_product_data,
    User,
    Product,
    Tag,
    Transaction,
)


class TestBetsy(unittest.TestCase):
    user_counter = 1
    @classmethod
    def setUpClass(cls):
        db.create_tables([User, Product, Tag, ProductTag, Transaction])

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([User, Product, Tag, ProductTag, Transaction])

    def setUp(self):
        main.populate_test_database()
        user_name = f"Alice{TestBetsy.user_counter}"
        TestBetsy.user_counter += 1
        User.create(name=user_name, address="123 Main St", billing_info="Visa 1234")

    def tearDown(self):
        Transaction.delete().execute()
        main.ProductTag.delete().execute()
        Tag.delete().execute()
        Product.delete().execute()
        User.delete().execute()

    def test_search(self):
        results = search("Sweater")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Sweater")

    def test_list_user_products(self):
        user_products = list_user_products(1)
        self.assertEqual(len(user_products), 3)

    def test_list_products_per_tag(self):
        products = list_products_per_tag(1)
        self.assertEqual(len(products), 2)

    def test_add_product_to_catalog(self):
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": 10.0,
            "quantity": 5
        }
        new_product = add_product_to_catalog(1, product_data)
        self.assertEqual(new_product.name, "Test Product")

    def test_update_stock(self):
        update_stock(1, 20)
        product = Product.get_by_id(1)
        self.assertEqual(product.quantity, 20)

    def test_purchase_product(self):
        transaction = purchase_product(1, 1, 1)
        self.assertEqual(transaction.quantity, 1)

    def test_remove_product(self):
        remove_product(1)
        with self.assertRaises(Product.DoesNotExist):
            Product.get_by_id(1)

    def test_validate_product_data(self):
        valid_data = {
            "name": "Valid Product",
            "description": "A valid product",
            "price": 10.0,
            "quantity": 5
        }
        self.assertIsNone(validate_product_data(valid_data))

        with self.assertRaises(ValueError):
            invalid_data = valid_data.copy()
            invalid_data["name"] = ""
            validate_product_data(invalid_data)

        with self.assertRaises(ValueError):
            invalid_data = valid_data.copy()
            invalid_data["price"] = -1
            validate_product_data(invalid_data)


if __name__ == "__main__":
    unittest.main()
