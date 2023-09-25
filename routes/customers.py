from flask import Blueprint, render_template, request, redirect, jsonify
import database.db_connector as db

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# Read Customers
@customers_bp.route('/', methods=['GET'])
def customers():
    """
    Retreives all Customers from the database and renders the customers template
    with the Customers data and column names.
    """
    db_connection = db.connect_to_database()
    query = "SELECT Customers.customer_id as 'Customer ID', \
            CONCAT_WS(' ', first_name, last_name) as 'Customer Name', \
            Customers.email as 'Email', Customers.phone_number as 'Phone Number', \
            CONCAT_WS(', ', street_address, street_address2, city, state, zip) as 'Address' \
            FROM Customers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    # Filter out the column names 
    # (otherwise you need at least 1 row in the table to get the column names)
    col_names = [col[0] for col in cursor.description]

    return render_template("customers.j2", customers=results, col_names=col_names)

# Create Customers
@customers_bp.route('/create', methods=['POST'])
def customers_create():
    """
    Inserts a new Customer into the database using the first name, last name, email, phone,
    street address 1, street address 2, city, state, and zip from the request form data. 
    Redirects to the /customers route.
    """
    db_connection = db.connect_to_database()
    new_first_name = request.form.get('first-name')
    new_last_name = request.form.get('last-name')
    new_email = request.form.get('email')
    new_phone = request.form.get('phone')
    new_street_address_1 = request.form.get('street-address1')
    new_street_address_2 = request.form.get('street-address2')
    new_city = request.form.get('city')
    new_state = request.form.get('state')
    new_zip = request.form.get('zip')

    # null street address 2 input
    if not new_street_address_2:
        new_street_address_2 = None
    query = "INSERT INTO Customers (first_name, last_name, email, phone_number, street_address, \
            street_address2, city, state, zip) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    cursor = db.execute_query(db_connection=db_connection, query=query, 
                              query_params=(new_first_name, new_last_name, new_email, new_phone, 
                                            new_street_address_1, new_street_address_2, 
                                            new_city, new_state, new_zip))
    return redirect('/customers')
