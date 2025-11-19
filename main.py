import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from bson import ObjectId

from schemas import Product, Order
from database import db, create_document, get_documents

app = FastAPI(title="Knee Massager Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_doc(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@app.get("/")
def read_root():
    return {"message": "Knee Massager Store Backend Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/api/products", response_model=List[Product])
def list_products():
    # Ensure collection exists and seed one featured product if empty
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    count = db["product"].count_documents({})
    if count == 0:
        seed_product = Product(
            title="TheraKnee Pro Heat & Air Compression Massager",
            subtitle="Soothe pain, boost circulation, and recover faster",
            description=(
                "Clinically-inspired knee relief with adjustable heat, air compression, and vibration. "
                "Targets soreness from arthritis, workouts, or long days on your feet."
            ),
            price=129.0,
            compare_at_price=199.0,
            category="Knee Massager",
            in_stock=True,
            images=[
                "https://images.unsplash.com/photo-1579154204601-01588f351e67?q=80&w=1200&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1558618666-606ba59b23d5?q=80&w=1200&auto=format&fit=crop",
                "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1200&auto=format&fit=crop"
            ],
            features=[
                "3 heat levels with auto shut-off",
                "Dynamic air compression with 3 intensities",
                "Targeted vibration massage",
                "Breathable, ergonomic wrap design",
                "USB-C fast charging, 2.5h battery life"
            ],
            rating=4.8,
            reviews_count=267
        )
        create_document("product", seed_product)

    docs = get_documents("product")
    return [Product(**serialize_doc(d)) for d in docs]


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    try:
        doc = db["product"].find_one({"_id": ObjectId(product_id)})
    except Exception:
        doc = None
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_doc(doc)


@app.post("/api/orders")
def create_order(order: Order):
    # Basic stock check could be implemented here if needed
    try:
        order_id = create_document("order", order)
        return {"order_id": order_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
