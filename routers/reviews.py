from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.dbConnect import get_db
from Database.dbModels import Review, ReviewResponse, ReviewCreate

router = APIRouter()

@router.get("/", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.status=="approved").all()

@router.post("/")
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = Review(
        rating=review.rating,
        comment=review.comment,
        status="pending",
        user_id=review.username,
        item_id=review.item_id
    )
    db.add(new_review)
    db.commit()
    return {"message": f"Review for item {review.item_id} created!"}
