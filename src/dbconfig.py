from sqlalchemy import Integer, String, Column, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from decouple import config


DB_URI = f"sqlite:///../udacity/{config('DB_NAME')}.db"

engine = create_engine(
    url=DB_URI, echo=False, connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessioLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_con() -> Session:
    with SessioLocal() as session:
        return session


# models
class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship(Restaurant)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
