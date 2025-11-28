from Database.dbConnect import SessionLocal, engine, Base
from Database.dbModels import User, Item, Order, Review, StatusName, ReviewStatus
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database():
    """Seed the database with initial test data"""

    # Create a new session
    db = SessionLocal()

    try:
        logger.info("Starting database seeding...")

        # Clear existing data
        logger.info("Clearing existing data...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        # Seed Users
        logger.info("Seeding users...")
        users = [
            User(name="John Doe", email="john@example.com", password="password123"),
            User(name="Jane Smith", email="jane@example.com", password="password123"),
            User(name="Bob Wilson", email="bob@example.com", password="password123"),
            User(name="Alice Johnson", email="alice@example.com", password="password123"),
            User(name="Charlie Brown", email="charlie@example.com", password="password123"),
        ]
        db.add_all(users)
        db.commit()
        logger.info(f"Created {len(users)} users")

        # Seed Items
        logger.info("Seeding items...")
        items = [
            Item(name="Classic Burger", price=8.99,
                 description="Juicy beef patty with lettuce, tomato, and special sauce"),
            Item(name="Chicken Sandwich", price=7.99, description="Crispy chicken breast with mayo and pickles"),
            Item(name="Veggie Wrap", price=6.99, description="Fresh vegetables wrapped in a whole wheat tortilla"),
            Item(name="French Fries", price=3.99, description="Crispy golden fries with sea salt"),
            Item(name="Onion Rings", price=4.99, description="Beer-battered onion rings"),
            Item(name="Caesar Salad", price=7.49, description="Romaine lettuce with parmesan and croutons"),
            Item(name="Milkshake", price=4.99, description="Thick and creamy - vanilla, chocolate, or strawberry"),
            Item(name="Soda", price=1.99, description="Coca-Cola, Sprite, or Fanta"),
            Item(name="Pizza Slice", price=3.49, description="New York style cheese pizza"),
            Item(name="Hot Dog", price=4.49, description="All-beef hot dog with your choice of toppings"),
        ]
        db.add_all(items)
        db.commit()
        logger.info(f"Created {len(items)} items")

        # Seed Orders
        logger.info("Seeding orders...")
        orders = [
            Order(status=StatusName.DONE, user_id=1, phone_num="555-0101"),
            Order(status=StatusName.DONE, user_id=2, phone_num="555-0102"),
            Order(status=StatusName.PENDING, user_id=3, phone_num="555-0103"),
            Order(status=StatusName.DONE, user_id=4, phone_num="555-0104"),
            Order(status=StatusName.CANCELLED, user_id=1, phone_num="555-0101"),
            Order(status=StatusName.DONE, user_id=5, phone_num="555-0105"),
            Order(status=StatusName.PENDING, user_id=2, phone_num="555-0102"),
        ]
        db.add_all(orders)
        db.commit()
        logger.info(f"Created {len(orders)} orders")

        # Seed Reviews
        logger.info("Seeding reviews...")
        reviews = [
            # Approved reviews
            Review(rating=5, comment="Best burger in town! Will definitely order again.",
                   user_id=1, item_id=1, status=ReviewStatus.APPROVED),
            Review(rating=4, comment="Really good chicken sandwich, crispy and flavorful.",
                   user_id=2, item_id=2, status=ReviewStatus.APPROVED),
            Review(rating=5, comment="Love the veggie wrap! Fresh ingredients and great taste.",
                   user_id=3, item_id=3, status=ReviewStatus.APPROVED),
            Review(rating=4, comment="Fries were hot and crispy, perfect!",
                   user_id=4, item_id=4, status=ReviewStatus.APPROVED),

            # Pending reviews (waiting for admin approval)
            Review(rating=5, comment="Amazing milkshake! So thick and creamy.",
                   user_id=5, item_id=7, status=ReviewStatus.PENDING),
            Review(rating=3, comment="Pizza was okay, but a bit cold when it arrived.",
                   user_id=1, item_id=9, status=ReviewStatus.PENDING),
            Review(rating=4, comment="Great hot dog, love the toppings selection.",
                   user_id=2, item_id=10, status=ReviewStatus.PENDING),

            # Rejected reviews (inappropriate content)
            Review(rating=1, comment="This place is terrible! Never ordering again!",
                   user_id=3, item_id=1, status=ReviewStatus.REJECTED),
            Review(rating=2, comment="Food took forever and was cold.",
                   user_id=4, item_id=2, status=ReviewStatus.REJECTED),
        ]
        db.add_all(reviews)
        db.commit()
        logger.info(f"Created {len(reviews)} reviews")

        logger.info("✅ Database seeding completed successfully!")
        logger.info(f"   - {len(users)} users")
        logger.info(f"   - {len(items)} items")
        logger.info(f"   - {len(orders)} orders")
        logger.info(f"   - {len(reviews)} reviews")

    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()