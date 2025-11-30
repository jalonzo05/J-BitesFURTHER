from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Database.dbConnect import get_db
from Database.dbModels import Item, ItemResponse

router = APIRouter()

@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
