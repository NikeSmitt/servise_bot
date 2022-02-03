from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import create_session, declarative_base

from data.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

# engine = create_engine(
#             f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
#             echo=True
#         )


Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    category_code = Column(String(20))
    category_name = Column(String(50))
    
    subcategory_code = Column(String(20))
    subcategory_name = Column(String(50))
    
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)
    
    def __repr__(self):
        return f"""
            Товар № {self.id} название {self.name}
        """

engine = create_engine('sqlite://', echo=True)
session = create_session(bind=engine)

Base.metadata.create_all(engine)
