from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurant/new'>Make new restaurant</a>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<h1>"+ restaurant.name +"</h1>"
                    id = str(restaurant.id)
                    output += "<a href ='/restaurant/%s/edit'>Edit</a><br>" % restaurant.id
                    output += "<a href ='/restaurant/%s/delet'>Delet</a><br>" % restaurant.id
                # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                # output += "<a href = '/restaurant/new'>Make new restaurant</a>"
                # restaurants = session.query(Restaurant).all()

                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><h2>Make a New Restaurant</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Create"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/delet"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are you sure you want to delet %s" % myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/delet' >" % restaurantIDPath
                    # output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Delet'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.send_response(301)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     # messagecontent =0
            #     ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('message')
            #
            #
            #         output = ""
            #
            #
            #         output += "<html><body>"
            #         output += " <h2> Okay, how about this: </h2>"
            #         output += "<h1> %s </h1>" % messagecontent[0]
            #         output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #         output += "</body></html>"
            #         self.wfile.write(output)
            #         print output


            # if self.path.endswith("/restaurant/new"):
            #
            #     ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         newrestaurant = fields.get('newRestaurant')
            #         newRestaurant = Restaurant(name = newRestaurant)
            #         session.add(restaurant)
            #         session.commit()
            #
            #
            #         self.send_response(301)
            #         self.send_header('Content-type', 'text/html')
            #         self.send_header('Location', '/restaurant')
            #         self.end_headers()
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

                # self.path = "/restaurant"

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    # Create new Restaurant Object
                    updateRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if updateRestaurant != []:
                        updateRestaurant.name = messagecontent[0]
                        session.add(updateRestaurant)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()

            if self.path.endswith("/delet"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    # Create new Restaurant Object
                    deletRestaurant = session.query(Restaurant).filter_by(id=restaurantIDPath).one()

                    session.delete(deletRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

            # self.path = "/restaurant"

        except:
            pass
    # def do_POST(self):
    #     try:
    #         self.send_response(301)
    #         self.send_header('Content-type', 'text/html')
    #         self.end_headers()
    #         ctype, pdict = cgi.parse_header(
    #             self.headers.getheader('content-type'))
    #         if ctype == 'multipart/form-data':
    #             fields = cgi.parse_multipart(self.rfile, pdict)
    #             messagecontent = fields.get('message')
    #         output = ""
    #         output += "<html><body>"
    #         output += " <h2> Okay, how about this: </h2>"
    #         output += "<h1> %s </h1>" % messagecontent[0]
    #         output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
    #         output += "</body></html>"
    #         self.wfile.write(output)
    #         print output
    #     except:
    #         pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
