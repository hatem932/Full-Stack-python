from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from datetime import datetime
from database_inventory import Product, Base, Location, ProductMovement

engine = create_engine('sqlite:///inventory.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

location1 = Location(name="Rammalla")

session.add(location1)
session.commit()

# move = ProductMovement(from_location=location1,
#                      to_location=location2, product_id=product1, qyt=5)

location2 = Location(name="Jerusalem")

session.add(location2)
session.commit()

location3 = Location(name = "Hebron")

session.add(location3)
session.commit()

location4 = Location(name = "Bethlehem")

session.add(location4)
session.commit()


product1 = Product(name="Head & Shoulders")

session.add(product1)
session.commit()


product2 = Product(name = "Dove")

session.add(product2)
session.commit()


product3 = Product(name = "Pantene")

session.add(product3)
session.commit()


product4 = Product(name = "Sunsilk")

session.add(product4)
session.commit()

# move = ProductMovement(from_location=location1,to_location=location2, timestamp=datetime.now(), product_id=product1, qyt=5)

# session.add(move)
# session.commit()

print "added items!"
