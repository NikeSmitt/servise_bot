from sqlalchemy import Column, String, Integer, Boolean

from utils.db_api.database import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    authorization = Column(Boolean, nullable=False, default=0)
    admin = Column(Boolean, nullable=False, default=False)
    
    def __init__(self, name: str, surname: str, auth=False, admin=False):
        self.name = name
        self.surname = surname
        self.authorization = auth
        self.admin = admin
    
    def __repr__(self):
        return f'User<{self.id=}, ' \
               f'{self.name=}, ' \
               f'{self.surname=}>'


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
