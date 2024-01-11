import sqlalchemy

metadata = sqlalchemy.MetaData()


products_table = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("count", sqlalchemy.Integer),
    sqlalchemy.Column("description", sqlalchemy.String(250)),
)
