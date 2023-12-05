from fastapi import FastAPI, HTTPException
from .models.models import Product

app = FastAPI()


sample_products = [
    {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "Iphone", "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99},
]


@app.get("/product/{product_id}", response_model=Product)
async def read_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/search", response_model=list[Product])
async def search_products(
    keyword: str,
    category: str = None,
    limit: int = 10
):
    filtered_products = [
        product for product in sample_products
        if (keyword.lower() in product["name"].lower() and
            (category is None or
            category.lower() == product["category"].lower()))
            ][:limit]

    if not filtered_products:
        raise HTTPException(status_code=404, detail="No products found")

    return filtered_products
