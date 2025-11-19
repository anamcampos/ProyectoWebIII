import os
from sqlalchemy import (create_engine, Column, Integer, String, Text,
                        DateTime, JSON, func)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = os.getenv("DATABASE_URL") or \
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(Text)
    price = Column(String)
    url = Column(Text)
    last_seen = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "external_id": self.external_id,
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer)
    event_type = Column(String)
    details = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)

def upsert_items(items):
    """
    items: list of dicts with keys: external_id, title, price, url
    returns list of events created
    """
    events = []
    session = SessionLocal()
    try:
        for it in items:
            db_item = session.query(Item).filter_by(external_id=it["external_id"]).one_or_none()
            if db_item is None:
                db_item = Item(
                    external_id=it["external_id"],
                    title=it.get("title"),
                    price=it.get("price"),
                    url=it.get("url")
                )
                session.add(db_item)
                session.flush()
                events.append({"item_id": db_item.id, "event_type": "new", "details": it})
            else:
                changed = False
                changes = {}
                for f in ("title", "price", "url"):
                    if getattr(db_item, f) != it.get(f):
                        changes[f] = {"old": getattr(db_item, f), "new": it.get(f)}
                        setattr(db_item, f, it.get(f))
                        changed = True
                if changed:
                    events.append({"item_id": db_item.id, "event_type": "modified", "details": changes})
            db_item.last_seen = func.now()
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    return events

def list_items(limit=100):
    session = SessionLocal()
    items = session.query(Item).limit(limit).all()
    result = [i.to_dict() for i in items]
    session.close()
    return result
