from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
# import routes
# import helper   # add this one

from database_inventory import Product, Base, Location, ProductMovement

engine = create_engine('sqlite:///inventory.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# items = session.query(Location).all()
# products = session.query(Product).all()
def makeList(items):
    locationName = []
    for item in items:
        locationName.append(item.name)
    return locationName

# def makeList(items, table):
#     arr = []
#     product = session.query(table).filter_by(id=id)
#     for item in items:
#         arr.append(item.id)

# @app.context_processor
def print_location(id):
    name =""
    locationid = session.query(Location).filter_by(id=id).one_or_none()
    if locationid==None:
        name =""
    else:
        name = locationid.name
    return name

def print_product(id):
    productid = session.query(Product).filter_by(id=id).one()
    return productid.name

def convert_int(i):
    return str(i)

app.jinja_env.globals.update(print_location=print_location, print_product=print_product, convert_int=convert_int, int=int)


def addProduct(name, location, qyt):
    product = Product(name = name, locationproduct = location, qyt = qyt)
    session.add(product)
    session.commit()

def addLocation(name):
    location = Location(name = name)
    session.add(location)
    session.commit()


def valed(input):
    return input

def error_input(input, itemList, errorExest, errorEmpty):
    error=""
    if input in makeList(itemList):
        error +="\n" + errorExest

    if input == "" or input.isspace() or input == None:
        error +="\n" + errorEmpty
    if error:
        return error
    else:
        return None

def error_qty(input):
    error = ""
    if input <=0 or input.isspace() or input =="":
        error += "error product Quantity"
    return error




# def mainInventory():
#     return render_template('index.html')
@app.route('/inventory/Location')
def inventoryLocation():
    items = session.query(Location).all()
    return render_template('locations.html', items = items)
@app.route('/')
@app.route('/inventory/product')
def inventoryProduct():
    items = session.query(Location).all()
    products = session.query(Product).order_by(Product.name)
    return render_template('products.html', items = products)



@app.route('/inventory/product-movement')
def inventoryProductMovement():
    items = session.query(Location).all()
    productMovement = session.query(ProductMovement).all()
    return render_template('product-movement.html', items = productMovement)

@app.route('/inventory/product-movement/new', methods=['GET', 'POST'])
def newProductMovement():
    error = ""
    items = session.query(Location).all()
    products = session.query(Product).all()
    if request.method == 'POST':
        fromLocation = request.form['fromlocation']
        toLocation = request.form['tolocation']
        # time = datetime.datetime.strptime(request.form['time'], '%Y-%m-%d %H:%M:%S.%f')
        qty = int(request.form['qty'])
        product_id = int(request.form['product'])
        thisProduct = session.query(Product).filter_by(id=product_id).one()
        locationProduct = session.query(Location).filter_by(id=thisProduct.locationproduct).one()
        if fromLocation:
            fromLoc = session.query(Location).filter_by(id=fromLocation).one()
            if fromLoc.name != locationProduct.name:
                error += "this location not contain this product"

        if (fromLocation=="" or fromLocation.isspace()) and (toLocation=="" or toLocation.isspace()) :
            error += "you must be entered one location"

        if not qty:
            error +="/n Quantity is Empty"
        if  qty > int(thisProduct.qyt):
            error += " Quantity you need is so large onle provide is %s" % thisProduct.qyt
        if error:
            return render_template('new-product-movement.html', error = error, items=items, products = products)
        else:
            if (fromLocation=="" or fromLocation.isspace()) and toLocation:
                movement = ProductMovement(to_location = toLocation, product_id = product_id, qyt = qty)
                session.add(movement)
                session.commit()
                flash("new Product Movement created!")
                return redirect(url_for('inventoryProductMovement'))
            elif (toLocation=="" or toLocation.isspace()) and fromLocation:
                movement = ProductMovement(from_location = fromLocation, product_id = product_id, qyt = qty)
                session.add(movement)
                session.commit()
                thisProduct.qyt =  int(thisProduct.qyt) - qty
                session.add(thisProduct)
                session.commit()
                flash("new Product Movement created!")
                return redirect(url_for('inventoryProductMovement'))

            else:
                thisProduct.qyt =  int(thisProduct.qyt) - qty
                session.add(thisProduct)
                session.commit()

                newProd = Product(name = thisProduct.name, locationproduct = toLocation, qyt=qty)
                session.add(newProd)
                session.flush()
                session.refresh(newProd)
                movement = ProductMovement(from_location = fromLocation, to_location = toLocation, product_id = newProd.id, qyt = qty)
                session.add(movement)
                session.commit()
                flash("new Product Movement created!")
                return redirect(url_for('inventoryProductMovement'))


    else:
        return render_template('new-product-movement.html' , items=items, products = products)


@app.route('/inventory/product-movement/<int:movement_id>/edit', methods=['GET', 'POST'])
def productMovementEdit(movement_id):
    error = ""
    items = session.query(Location).all()
    products = session.query(Product).all()
    thisMovement = session.query(ProductMovement).filter_by(id=movement_id).one()
    if request.method == 'POST':
        fromLocation = request.form['fromlocation']
        toLocation = request.form['tolocation']
        # time = datetime.datetime.strptime(request.form['time'], '%Y-%m-%d %H:%M:%S.%f')
        qty = request.form['qty']
        product_id = int(request.form['product'])
        thisProduct = session.query(Product).filter_by(id=product_id).one()
        # iid = int(thisProduct.locationproduct)
        locationProduct = session.query(Location).filter_by(id=thisProduct.locationproduct).one()
        oldProduct = session.query(Product).filter_by(id=thisMovement.product_id).one()

        # fromLoc = None


            # fromLoc = oldProduct.locationproduct
            # if fromLoc != locationProduct.name:
            #     error += "this location not contain this product"

        # if fromLoc.name != locationProduct.name:
        #     error += "this location not contain this product"
        if (fromLocation=="" or fromLocation.isspace()) and (toLocation=="" or toLocation.isspace()) :
            error += "you must be entered one location"

        if fromLocation:
            fromLoc = session.query(Location).filter_by(id=fromLocation).one()
            if fromLoc.name != locationProduct.name:
                error += "this location not contain this product"
        elif toLocation:
            if oldProduct.locationproduct != toLocation and oldProduct.locationproduct !="":
                error += "not into location"
            # elif oldProduct.locationproduct == "":

            else:
                fromLoc = oldProduct.locationproduct

        # elif not time:
        #     error +="/n time is Empty"
        if not qty:
            error +="/n Quantity is Empty"
        if int(qty) > (int(thisProduct.qyt) + int(oldProduct.qyt)):
            error += " Quantity you need is so large onle provide is %s" % thisProduct.qyt
        if error:
            return render_template('product-movement-edit.html',movement_id=movement_id, error = error, thisMovement=thisMovement, items=items, products = products)
        else:
            # thisProduct.qyt =  int(thisProduct.qyt) + int(oldProduct.qyt) - qty
            # thisMovement = session.query(ProductMovement).filter_by(id=movement_id).one()



            thisProductMovement = session.query(Product).filter_by(id=thisMovement.product_id).one()
            origenProduct = session.query(Product).filter_by(locationproduct=thisMovement.from_location).one()
            if thisProductMovement.name != thisProduct.name:
                origenProduct.qyt = int(origenProduct.qyt) + int(thisProductMovement.qyt)
                session.add(origenProduct)
                session.commit()
                # thisProduct.qyt = int(thisProduct.qyt) + qty
            else:
                if thisProductMovement.qyt != int(qty):
                    if thisProductMovement.qyt < int(qty):
                        difference =  int(qty) - int(thisProductMovement.qyt)
                        thisProduct.qyt = int(thisProduct.qyt) - difference
                    elif thisProductMovement.qyt > int(qty):
                        difference =  int(thisProductMovement.qyt) - int(qty)
                        thisProduct.qyt = int(thisProduct.qyt) + difference

                        session.add(thisProduct)
                        session.commit()

            thisMovement.from_location = fromLocation
            thisMovement.to_location = toLocation
            thisMovement.product_id = thisProductMovement.id
            thisMovement.qyt = int(qty)
            session.add(thisMovement)
            session.commit()
            thisProductMovement.name = thisProduct.name
            thisProductMovement.qyt = int(qty)
            thisProductMovement.locationproduct = toLocation
            session.add(thisProductMovement)
            session.commit()




            # newProd = Product(name = thisProduct.name, locationproduct = toLocation, qyt=qty)
            # session.add(newProd)
            # session.commit()
            # movement = ProductMovement(from_location = fromLocation, to_location = toLocation, product_id = product_id, qyt = qty)
            # session.add(movement)
            # session.commit()
            flash("new Product Movement created!")
            return redirect(url_for('inventoryProductMovement'))

    else:
        return render_template('product-movement-edit.html' , movement_id=movement_id, thisMovement=thisMovement, items=items, products = products)



@app.route('/inventory/new-location/', methods=['GET', 'POST'])
def newLocation():
    items = session.query(Location).all()
    if request.method == 'POST':
        nameLocation = request.form['name']
        error = error_input(nameLocation, items, "location %s is alreade exist" % nameLocation, "location is Empty")
        if error == None:
            addLocation(nameLocation)
            flash("new location created!")
            return redirect(url_for('inventoryLocation'))
        else:
            return render_template('newLocation.html', error = error)

    else:
        return render_template('newLocation.html')


def EditLocation(name, location_id):
    editlocation = session.query(Location).filter_by(id=location_id).one()
    editlocation.name = name
    session.add(editlocation)
    session.commit()


@app.route('/inventory/location/<int:location_id>/edit/', methods=['GET', 'POST'])
def editLocation(location_id):
    # items = session.query(Location).all()
    locations = session.query(Location).filter(id != location_id)
    editlocation = session.query(Location).filter_by(id=location_id).one()
    if request.method == 'POST':
        nameLocation = request.form['name']
        error = error_input(nameLocation, locations, "location %s is alreade exist" % nameLocation, "location is Empty")
        if error == None:
            EditLocation(nameLocation, location_id)
            flash(" location is edit!")
            return redirect(url_for('inventoryLocation'))
        else:
            return render_template('editLocation.html', location_id=location_id ,namelocation=editlocation.name, error = error)

    else:
        return render_template('editLocation.html', location_id=location_id ,namelocation=editlocation.name)



@app.route('/inventory/new-product/', methods=['GET', 'POST'])
def newProduct():
    items = session.query(Location).all()
    products = session.query(Product).all()

    if request.method == 'POST':
        name = request.form['name']
        qty = request.form['qty']
        error1 = error_input(name, products, "Product %s is alreade exist" % name, "product is Empty")
        error2 = error_qty(qty)
        # result = valed(error_input(name, products, 'newProduct.html', "Product %s is alreade exist" % name, "product is Empty", items))
        if error1 == None and error2 == "" :
            addProduct(request.form['name'], request.form['location'], request.form['qty'])
            flash("new product created!")
            return redirect(url_for('inventoryProduct'))
        else:
            return render_template('newProduct.html', error = error1 + " " + error2, items=items)


    else:
        return render_template('newProduct.html', items=items)


def EditProduct(product_id, name, location, qty):
    editProduct = session.query(Product).filter_by(id=product_id).one()
    editProduct.name = request.form['name']
    editProduct.locationproduct = request.form['location']
    editProduct.qyt = request.form['qty']
    session.add(editProduct)
    session.commit()

@app.route('/inventory/product/<int:product_id>/edit/', methods=['GET', 'POST'])
def editProduct(product_id):
    error =""
    editProduct = session.query(Product).filter_by(id=product_id).one()
    items = session.query(Location).all()
    products = session.query(Product).all()
    if request.method == 'POST':
        name = request.form['name']
        qty = request.form['qty']
        error1 = error_input(name, products, "Product %s is alreade exist" % name, "product is Empty")
        error2 = error_qty(qty)
        # result = valed(error_input(name, products, 'newProduct.html', "Product %s is alreade exist" % name, "product is Empty", items))
        if error1 == None and error2 == "" :

            EditProduct(product_id, name, request.form['location'], qty)
            flash("product "+name+ " is edit!")
            return redirect(url_for('inventoryProduct'))
        else:
            if error1 == None:
                error1 = ""
            return render_template('editProduct.html', error = error1 + "\n" + error2, product_id=product_id, items=items ,nameproduct=editProduct.name,locationid=editProduct.locationproduct, qty=editProduct.qyt)

    else:
        return render_template('editProduct.html',product_id=product_id, items=items ,nameproduct=editProduct.name,locationid=editProduct.locationproduct, qty=editProduct.qyt)


TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.template_folder = TEMPLATE_DIR
    app.static_folder = STATIC_DIR
    app.run(host='0.0.0.0', port=5000)
