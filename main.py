from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from Database.dbModels import Item, ItemResponse, Review, ReviewStatus, ReviewResponse
from Database.dbConnect import dbSession, engine, Base
from starlette import status
from tests.seed import seed_database
import logging
from owner.admin import setup_admin

Base.metadata.create_all(bind=engine)
app = FastAPI(title="J-Bites")
setup_admin(app)

@app.on_event("startup")
def reset_database():
    Base.metadata.drop_all(bind=engine)  # Drop all tables
    Base.metadata.create_all(bind=engine)  # Recreate fresh
    seed_database()
    logging.basicConfig(level=logging.INFO)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, session: dbSession):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=List[ItemResponse])
def get_all_items(session: dbSession):
    items = session.query(Item).all()
    return items

@app.post("/reviews", status_code=201, response_model=ReviewResponse)
def create_review(item_id: int, rating: int, comment: str, user_id: int, session: dbSession):
    #sends to the DB a review that is pending and through /admin the admin will change
    review = Review(
        item_id=item_id,
        rating=rating,
        comment=comment,
        user_id=user_id,
        status=ReviewStatus.PENDING,
    )

    session.add(review)
    session.commit()
    return {"message": "Review created and submitted for approval.", "review": review.id}
#shows approved reviews
@app.get("/items/{item_id}/reviews")
def get_reviews(item_id: int, session: dbSession):
    #gets reviews based on id and approved status
    reviews = session.query(Review).filter(
        Review.item_id == item_id,
        Review.status == ReviewStatus.APPROVED
    ).all()
    return reviews

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)