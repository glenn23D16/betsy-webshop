__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


# Importeer de nodige modellen uit models.py
from models import User, Product, Tag, Transaction, ProductTag
from whoosh.index import create_in
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin


def search(term):
    """
    Return a list of products with names or descriptions containing the given term (case-insensitive).
    """
    results = Product.select().where(
        (Product.name ** f'%{term}%') |
        (Product.description ** f'%{term}%')
    )
    return results


def list_user_products(user_id):
    """Return a list of products owned by the user with the given user_id."""
    user = User.get_by_id(user_id)
    return user.products


def list_products_per_tag(tag_id):
    """Return a list of products associated with the tag with the given tag_id."""
    tag = Tag.get_by_id(tag_id)
    return tag.tagged_products


def add_product_to_catalog(user_id, product_data):
    """
    Add a product to the catalog of the user with the given user_id.
    product_data should be a dictionary containing keys 'name', 'description', 'price', and 'quantity'.
    """
    user = User.get_by_id(user_id)
    product = Product.create(**product_data, owner=user)
    return product


def update_stock(product_id, new_quantity):
    """Update the stock quantity of the product with the given product_id to the given new_quantity."""
    product = Product.get_by_id(product_id)
    product.quantity = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):
    """
    Record a purchase of the product with the given product_id by the user with the given buyer_id.
    The given quantity of the product will be deducted from the stock.
    """
    product = Product.get_by_id(product_id)
    buyer = User.get_by_id(buyer_id)

    if product.quantity < quantity:
        raise ValueError("Not enough stock available.")

    product.quantity -= quantity
    product.save()

    transaction = Transaction.create(buyer=buyer, product=product, quantity=quantity)
    return transaction


def remove_product(product_id):
    """Remove the product with the given product_id from the catalog."""
    product = Product.get_by_id(product_id)
    product.delete_instance()


def validate_product_data(product_data):
    """Validate product data before adding it to the database."""
    if not product_data["name"] or not product_data["description"]:
        raise ValueError("Product name and description must not be empty.")

    if product_data["price"] < 0 or product_data["quantity"] < 0:
        raise ValueError("Product price and quantity must be positive numbers.")


class WhooshIndex:
    def __init__(self, index_dir):
        schema = Schema(id=ID(unique=True, stored=True), name=TEXT, description=TEXT)
        self.index = create_in(index_dir, schema)

    def add_document(self, id, name, description):
        writer = self.index.writer()
        writer.add_document(id=str(id), name=name, description=description)
        writer.commit()

    def search(self, term):
        with self.index.searcher() as searcher:
            query_parser = MultifieldParser(["name", "description"], self.index.schema)
            query_parser.add_plugin(FuzzyTermPlugin())
            query = query_parser.parse(term)
            results = searcher.search(query)
            return [result["id"] for result in results]


def populate_test_database():
    """Populate the database with example data for testing purposes.

    This function creates example data in the database for testing purposes. The created data includes users, products,
    tags, and transactions. The created users have ids 1, 2, and 3, and their corresponding passwords are 'password'.
    The created products are a Sweater, a Scarf, a Beanie, and a Jacket. The Sweater and the Scarf have tags 'Winter'
    and 'Clothing'. The Beanie has tag 'Clothing' and the Jacket has tag 'Outerwear'. The created transactions include
    purchases of the Sweater and the Scarf by user 1, and a purchase of the Beanie by user 2.
    """

    # Create users
    user1 = User.create(name="Alice", address="123 Main St", billing_info="Visa 1234")
    user2 = User.create(name="Bob", address="456 Elm St", billing_info="Mastercard 5678")

    # Create products
    product1 = Product.create(name="Sweater", description="Warm and cozy", price=29.99, quantity=10, owner=user1)
    product2 = Product.create(name="Scarf", description="Stylish and warm", price=19.99, quantity=15, owner=user1)
    product3 = Product.create(name="Beanie", description="Warm and stylish", price=14.99, quantity=25, owner=user1)
    product4 = Product.create(name="Jacket", description="Waterproof and warm", price=99.99, quantity=5, owner=user2)

    # Create tags
    tag1, _ = Tag.get_or_create(name="Winter")
    tag2, _ = Tag.get_or_create(name="Clothing")
    tag3, _ = Tag.get_or_create(name="Outerwear")

    # Assign tags to products
    ProductTag.create(product=product1, tag=tag1)
    ProductTag.create(product=product1, tag=tag2)
    ProductTag.create(product=product2, tag=tag1)
    ProductTag.create(product=product2, tag=tag2)
    ProductTag.create(product=product3, tag=tag2)
    ProductTag.create(product=product4, tag=tag3)

    # Index products for search
    index = WhooshIndex(index_dir="index")
    for product in Product.select():
        index.add_document(
            id=product.id,
            name=product.name,
            description=product.description
        )

    # Create transactions
    Transaction.create(buyer=user1, product=product1, quantity=1)
    Transaction.create(buyer=user1, product=product2, quantity=2)
    Transaction.create(buyer=user2, product=product3, quantity=5)