from flask import Flask, jsonify, make_response
from flask_mysqldb import MySQL


#name of my application
app = Flask(__name__)


#Connect to dog_breeding database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "dog_breeding"


app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)



#tell flask what url should trigger our function and return the message we want to display in the browser
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/dogs", methods=["GET"])
def get_dogs():
   cur = mysql.connection.cursor()
   query = " SELECT * FROM dogs; "
   cur.execute(query)
   data = cur.fetchall()
   cur.close()
   return make_response(jsonify(data), 200)

if __name__ == "__main__":
  app.run(debug=True)