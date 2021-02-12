import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy import create_engine

Base = declarative_base()



class Location(Base):
    __tablename__= 'location'
    name = Column(String(80), nullable = False)

    id = Column(Integer, primary_key = True)

class Product(Base):
    __tablename__= 'product'

    name = Column(String(80), nullable = False)

    id = Column(Integer, primary_key = True)


    locationproduct = Column(Integer, ForeignKey('location.id'), nullable = False)

    qyt = Column(Integer, nullable = False)

    location = relationship(Location)
    # location = relationship("Location",
    #                 primaryjoin="and_(Product.location==Location.id,")

class ProductMovement(Base):
    __tablename__ = 'productMovement'

    id = Column(Integer, primary_key = True)

    from_location = Column(Integer, ForeignKey('location.id'), nullable = True)

    to_location = Column(Integer, ForeignKey('location.id'), nullable = True)

    timestamp = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    # timestamp = Column(TIMESTAMP)

    # timestamp = DateTime(DateTime(timezone=True))

    # timestamp = Column(DateTime(timezone=True), server_default=func.now())

    product_id = Column(Integer, ForeignKey('product.id'), nullable = False)

    qyt = Column(Integer, nullable = False)

    product = relationship(Product)
    relation = relationship("Location",
                    primaryjoin="and_(ProductMovement.from_location==Location.id, "
                        "ProductMovement.to_location==Location.id)")

    # product = relationship(Product)
    # location = relationship(Location)


engine = create_engine('sqlite:///inventory.db')

Base.metadata.create_all(engine)
