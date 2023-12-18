from flask import Flask, jsonify, make_response, request
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

def data_fetch(query):
      cur = mysql.connection.cursor()
      cur.execute(query)
      data = cur.fetchall()
      cur.close()
      return data


@app.route("/dogs", methods=["GET"])
def get_dogs():
   data = data_fetch(" SELECT * FROM dogs ")
   return make_response(jsonify(data), 200)
   

@app.route("/dogs/<int:id>", methods=["GET"])
def get_dog_by_id(id):
   data = data_fetch(" SELECT * FROM dogs WHERE dog_id = {}".format(id))
   return make_response(jsonify(data), 200)

@app.route("/dogs/<int:id>/relationship_id", methods=["GET"])
def get_dog_relationships(id):
    data = data_fetch(""" 
          SELECT relationships.relationship_id, dog_1_id, dog_2_id, relationship_Types.relationship_description
          FROM relationships
          JOIN dogs ON relationships.dog_1_id = dogs.dog_id
          JOIN dogs AS dogs_2 ON relationships.dog_2_id = dogs_2.dog_id
          JOIN relationship_Types ON relationships.relationship_code = relationship_Types.relationship_code;
    """.format(id))
    
    return make_response(jsonify({"relationship_id":id, "relationship":data, "count":len(data), }), 200)


# Create Dogs
@app.route("/dogs", methods=["POST"])
def add_actor():
    cur = mysql.connection.cursor()
    info = request.get_json()

    dogs_name = info["dogs_name"]
    born_in_litter_id = info["born_in_litter_id"]
    gender_mf = info["gender_mf"]
    date_of_birth = info["date_of_birth"]
    place_of_birth = info["place_of_birth"]
    other_details = info["other_details"]

    cur.execute(
            """INSERT INTO dogs (dogs_name, born_in_litter_id, gender_mf, date_of_birth, place_of_birth, other_details)
               VALUES (%s, %s, %s, %s, %s, %s,) """, (dogs_name, born_in_litter_id, gender_mf, date_of_birth, place_of_birth, other_details)
    )

    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "dog added sucessfully", "rows_affected": cur.rowcount}), 201)











if __name__ == "__main__":
  app.run(debug=True)