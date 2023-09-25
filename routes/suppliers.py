from flask import Blueprint, render_template, request, redirect, jsonify
import database.db_connector as db

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

# Read Suppliers
@suppliers_bp.route('/', methods=['GET'])
def suppliers():
    """
    Retreives all Suppliers from the database and renders the suppliers template
    with the Suppliers data and column names.
    """
    db_connection = db.connect_to_database()
    query = "SELECT Suppliers.supplier_id as 'Supplier ID', \
            Suppliers.supplier_name as 'Supplier Name', \
            Suppliers.email as 'Email', Suppliers.phone_number as 'Phone Number', \
            CONCAT_WS(', ', Suppliers.street_address, Suppliers.street_address2, \
                Suppliers.city, Suppliers.state, Suppliers.zip) as 'Address' \
            FROM Suppliers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    # Filter out the column names 
    # (otherwise you need at least 1 row in the table to get the column names)
    col_names = [col[0] for col in cursor.description]

    return render_template("suppliers.j2", suppliers=results, col_names=col_names)

# Create Suppliers
@suppliers_bp.route('/create', methods=['POST'])
def suppliers_create():
    """
    Inserts a new Supplier into the database using the supplier name, email, phone,
    street address 1, street address 2, city, state, and zip from the request form data. 
    Redirects to the /suppliers route.
    """
    db_connection = db.connect_to_database()
    new_supplier_name = request.form.get('supplier-name')
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
    query = "INSERT INTO Suppliers (supplier_name, email, phone_number, \
                street_address, street_address2, city, state, zip) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    
    cursor = db.execute_query(db_connection=db_connection, query=query, 
                              query_params=(new_supplier_name, new_email, new_phone, 
                                            new_street_address_1, new_street_address_2, 
                                            new_city, new_state, new_zip))
    return redirect('/suppliers')

# Delete Suppliers
@suppliers_bp.route('/delete/<supplier_id>', methods=['DELETE'])
def suppliers_delete(supplier_id):
    """
    Delete a Supplier in the database using the supplier id and
    returns a JSON response.
    """
    db_connection = db.connect_to_database()
    query = "DELETE FROM Suppliers WHERE supplier_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(supplier_id,))
    
    if cursor.rowcount == 0:
        # the supplier_id does not exist
        response = {'message': 'Supplier not found'}
        return jsonify(response), 404
    
    response = {'message': 'Supplier deleted successfully'}
    return jsonify(response), 200