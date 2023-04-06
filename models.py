import peewee as pw

db = pw.SqliteDatabase('betsy.db')
__all__ = ["db"]


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    name = pw.CharField(unique=True)
    address = pw.TextField()
    billing_info = pw.TextField()


class Product(BaseModel):
    name = pw.CharField()
    description = pw.TextField()
    price = pw.FloatField()
    quantity = pw.IntegerField()
    owner = pw.ForeignKeyField(User, backref='products')


class Tag(BaseModel):
    name = pw.CharField(unique=True)


class ProductTag(BaseModel):
    product = pw.ForeignKeyField(Product, backref='tags')
    tag = pw.ForeignKeyField(Tag, backref='tagged_products')


class Transaction(BaseModel):
    buyer = pw.ForeignKeyField(User, backref='transactions')
    product = pw.ForeignKeyField(Product)
    quantity = pw.IntegerField()
