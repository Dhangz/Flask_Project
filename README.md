# Dog Breeding Management System

## Overview

This is a web application built with Flask and MySQL for managing dog breeding information. Users can insert, update, delete, and search for dog records. The application also provides an API for retrieving data in JSON or XML format.

## Features

- Insert, update, and delete dog records
- Search for dogs based on various criteria
- API for data retrieval in JSON or XML format
- ...

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/dog-breeding-app.git
   cd dog-breeding-app
   ```

2. Install dependencies:

pip install -r requirements.txt

3. Set up the database:

Create a MySQL database named dog_breeding.
Update the MYSQL_USER and MYSQL_PASSWORD in api.py with your MySQL credentials.

4. Run the application:
   python app.py

5. Access the application in your browser at http://127.0.0.1:5000/

## Retrieve Data

1. JSON Format
   http://127.0.0.1:5000/format?format=json

2. XML Format
   http://127.0.0.1:5000/format?format=xml
