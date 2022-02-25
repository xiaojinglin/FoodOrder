from sqlalchemy import (create_engine, Column, Integer,
                        String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///catering.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    order = relationship('OrderInfo', back_populates='customer', 
                         cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'Name: {self.name}, Phone: {self.phone}'


class OrderInfo(Base):
    __tablename__ = 'orderinfo'


    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id))
    name = Column(String)
    price = Column(Integer)
    qty = Column(Integer)
    customer = relationship('Customer', back_populates='order')

    def __repr__(self):
        return f'Name: {self.name}, price: ${self.price/100}, qty: {self.qty}'