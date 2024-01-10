# from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Product(Base):
#     __tablename__ = 'products'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     price = Column(Float)
#     count = Column(Integer)

import sqlalchemy

metadata = sqlalchemy.MetaData()


products_table = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("count", sqlalchemy.Integer),
)
