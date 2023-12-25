from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, make_response, abort
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dog_breeding'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def Index():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dogs WHERE dog_name LIKE %s", ('%' + search_query + '%',))
        data = cur.fetchall()
        cur.close()

        return render_template('index.html', dogs=data, search_query=search_query)

    data = data_fetch("SELECT * FROM dogs")
    return render_template('index.html', dogs=data, search_query=None)



def data_fetch(query):
      cur = mysql.connection.cursor()
      cur.execute(query)
      data = cur.fetchall()
      cur.close()
      return data

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        
        born_in_litter_id = request.form.get("born_in_litter_id")
        dog_name = request.form.get("dog_name")
        gender_mf = request.form.get("gender_mf")
        date_of_birth = request.form.get("date_of_birth")
        place_of_birth = request.form.get("place_of_birth")
        other_details = request.form.get("other_details")

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO dogs (born_in_litter_id, dog_name, gender_mf, date_of_birth, place_of_birth, other_details)
               VALUES (%s, %s, %s, %s, %s, %s) """, (born_in_litter_id, dog_name, gender_mf, date_of_birth, place_of_birth, other_details))

        mysql.connection.commit()
        return redirect(url_for('Index'))

    # Add a return statement for the 'GET' method
    return render_template('Insert_dog.html')



@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dogs WHERE dog_id = %s", (id,))
    data = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        born_in_litter_id = request.form.get("born_in_litter_id")
        dog_name = request.form.get("dog_name")
        gender_mf = request.form.get("gender_mf")
        date_of_birth = request.form.get("date_of_birth")
        place_of_birth = request.form.get("place_of_birth")
        other_details = request.form.get("other_details")

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE dogs SET 
            born_in_litter_id = %s, 
            dog_name = %s, 
            gender_mf = %s, 
            date_of_birth = %s, 
            place_of_birth = %s, 
            other_details = %s 
            WHERE dog_id = %s
        """, (born_in_litter_id, dog_name, gender_mf, date_of_birth, place_of_birth, other_details, id))
        
        mysql.connection.commit()
        flash("Data Updated Successfully", 'success')
        return redirect(url_for('Index'))

    return render_template("update_dog.html", dog=data)


    

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dogs WHERE dog_id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/format', methods=['GET'])
def api():
    try:
        if request.method == "GET":
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM dogs")
            data = cur.fetchall()
            cur.close()

            format_type = request.args.get('format', ' ').lower() # Default to JSON if not specified

            if format_type == 'xml':
                # Render an XML template and return it as a response
                response = make_response(render_template('data.xml', dogs=data), 200)
                response.headers['Content-Type'] = 'application/xml'
                return response
            elif format_type == 'json':
                # Convert data to a list of dictionaries and return a JSON response
                data_dict = [{'dog_id': row[0],
                              'born_in_litter_id': row[1],
                              'dog_name': row[2],
                              'gender_mf': row[3],
                              'date_of_birth': row[4],
                              'place_of_birth': row[5],
                              'other_details': row[6]
                              } for row in data]
                return make_response(jsonify(data=data_dict), 200)
            else:
                return render_template('formatter.html')  # Display formatter page for selecting format
            
    except Exception as e:
        # Log the exception or handle it appropriately
        print(f"Error: {e}")
        # Return an error response to the client
        abort(500, description="Internal Server Error")

@app.route('/formatter', methods=['GET', 'POST'])
def formatter():
    if request.method == 'POST':
        # If the form is submitted, redirect to the /format endpoint with the selected format
        selected_format = request.form.get('format', 'json').lower()
        return redirect(url_for('api', format=selected_format))

    # If it's a GET request, render the formatter.html template
    return render_template('formatter.html')

if __name__ == "__main__":
    app.run(debug=True)
