from flask import Flask, jsonify, make_response, request, render_template, flash
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

def data_fetch(query):
      cur = mysql.connection.cursor()
      cur.execute(query)
      data = cur.fetchall()
      cur.close()
      return data

@app.route("/", methods=["GET"])
def get_dogs():
   data = data_fetch(" SELECT * FROM dogs ")
   data = make_response(jsonify(data), 200)
   return render_template("index.html", data, dogs=data)
   

@app.route("/dogs/<int:id>", methods=["GET"])
def get_dog_by_id(id):
   data = data_fetch(" SELECT * FROM dogs WHERE dog_id = {}".format(id))
   return make_response(jsonify(data), 200)

@app.route("/dogs/<int:id>/relationship_id", methods=["GET"])
def get_dog_relationships(id):
    data = data_fetch(""" 
        SELECT relationships.relationship_id, dogs.dogs_name AS dog_1_name, dogs_2.dogs_name AS dog_2_name, relationship_Types.relationship_description
        FROM relationships
        JOIN dogs ON relationships.dog_1_id = dogs.dog_id
        JOIN dogs AS dogs_2 ON relationships.dog_2_id = dogs_2.dog_id
        JOIN relationship_Types ON relationships.relationship_code = relationship_Types.relationship_code;
    """.format(id))
    
    return make_response(jsonify({"relationship_id":id, "relationship":data, "count":len(data), }), 200)


# Create Dogs
@app.route("/dogs", methods=["POST"])
def add_dogs():
    cur = mysql.connection.cursor()
    info = request.get_json()

    dogs_name = info["dogs_name"]
    gender_mf = info["gender_mf"]
    date_of_birth = info["date_of_birth"]
    place_of_birth = info["place_of_birth"]
    other_details = info["other_details"]

    cur.execute(
            """INSERT INTO dogs (dogs_name, gender_mf, date_of_birth, place_of_birth, other_details)
               VALUES (%s, %s, %s, %s, %s,) """, (dogs_name, gender_mf, date_of_birth, place_of_birth, other_details)
    )

    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "dog added sucessfully", "rows_affected": cur.rowcount}), 201)

@app.route("/actors/<int:id>",methods=["PUT"])
def update_dogs(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    dogs_name = info["dogs_name"]
    gender_mf = info["gender_mf"]
    date_of_birth = info["date_of_birth"]
    place_of_birth =  info["place_of_birth"]
    other_details = info["other_details"]
    cur.execute(
        """
            UPDATE dogs SET 
            dogs_name = %s, gender_mf = %s, date_of_birth = %s, place_of_birth = %s
            WHERE dog_id = %s
        """, (dogs_name, gender_mf, date_of_birth, place_of_birth, other_details, id)
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "dog updated sucessfully", "row affected": rows_affected}), 201)


@app.route("/dogs/<int:id>", methods=["DELETE"])
def delete_actor(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM dogs where dog_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "dog deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


@app.route("/dogs/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)





if __name__ == "__main__":
  app.run(debug=True)