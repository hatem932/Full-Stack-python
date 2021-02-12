import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Product(Base):
	__tablename__= 'product'
	name = Column(String(80), nullable = False)

	id = Column(Integer, primary_key = True)

class Location(Base):
	__tablename__= 'location'
	name = Column(String(80), nullable = False)

	id = Column(Integer, primary_key = True)


class ProductMovement(Base):
	__tablename__ = 'ProductMovement'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)

	from_location = Column(Integer, ForeignKey('location.id'), nullable = True)

	to_location = Column(Integer, ForeignKey('location.id'), nullable = True)

	timestamp = Column(DateTime, default=datetime.datetime.utcnow)

	product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

    qyt = Column(Integer, nullable=False)


	product = relationship(Product)
    location = relationship(Location)
