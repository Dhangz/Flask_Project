from flask import Flask, render_template, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dog_breeding'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dogs")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', dogs=data)


@app.route('/insert', methods = ['POST'])
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
               VALUES (%s, %s, %s, %s, %s, %s) """, ( born_in_litter_id, dog_name, gender_mf, date_of_birth, place_of_birth, other_details))

        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'POST':
        dog_id = request.form.get("dog_id", None)
        dog_name = request.form.get("dog_name", None)
        gender_mf = request.form.get("gender_mf", None)
        date_of_birth = request.form.get("date_of_birth", None)
        place_of_birth = request.form.get("place_of_birth", None)
        other_details = request.form.get("other_details", None)

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE dogs SET 
            dog_name = %s, gender_mf = %s, date_of_birth = %s, place_of_birth = %s, other_details = %s
            WHERE dog_id = %s
        """, (dog_name, gender_mf, date_of_birth, place_of_birth, other_details, dog_id))
        mysql.connection.commit()  # Add this line to commit the changes
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))

    

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    print(f"Deleting record with id: {id}")
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dogs WHERE dog_id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))


@app.route('/api', methods=['GET'])
def api():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dogs")
    data = cur.fetchall()
    cur.close()

    format_type = request.args.get('format', 'json')  # Default to JSON if not specified

    if format_type == 'xml':
        response = app.response_class(response=render_template('data.xml', dogs=data), status=200, mimetype='application/xml')
    elif format_type == 'json':
        response = jsonify(dogs=data)
    else:
        response = jsonify({'error': 'Invalid format specified'})

    return response

if __name__ == "__main__":
    app.run(debug=True)
