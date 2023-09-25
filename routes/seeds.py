from flask import Blueprint, render_template, request, redirect, jsonify
import database.db_connector as db

seeds_bp = Blueprint('seeds', __name__, url_prefix='/seeds')

# Read Seeds
@seeds_bp.route('/', methods=['GET'])
def seeds():
    """
    Retrives all Seeds from the db, and Supplier and Seed type dropdown data 
    from the db, and renders the seeds template with Seed data, column names, 
    and the drop down data.
    """
    db_connection = db.connect_to_database()
    query = "SELECT Seeds.seed_id, \
                Seeds.seed_name AS 'Seed Name', \
                Seeds.seed_type_id, \
                Seed_Types.seed_type AS 'Seed Type', \
                Seeds.supplier_id AS 'Supplier ID', \
                Suppliers.supplier_name AS 'Supplier Name' \
                    FROM Seeds\
            JOIN Seed_Types ON Seeds.seed_type_id = Seed_Types.seed_type_id\
            LEFT JOIN Suppliers ON Seeds.supplier_id = Suppliers.supplier_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    # Filter out the column names 
    # (otherwise you need at least 1 row in the table to get the column names)
    col_names = [col[0] for col in cursor.description]

    # Dropdown Selects
    # Supplier Select
    supplier_query = "SELECT supplier_id, supplier_name FROM Suppliers;"
    cursor.execute(supplier_query)
    supplier_res = cursor.fetchall()
    # Seed Type Select
    seed_type_query = "SELECT seed_type_id, seed_type FROM Seed_Types;"
    cursor.execute(seed_type_query)
    seed_type_res = cursor.fetchall()

    return render_template("seeds.j2", seeds=results, col_names=col_names, suppliers=supplier_res, seed_types=seed_type_res)

# Create Seeds
@seeds_bp.route('/create', methods=['POST'])
def seeds_create():
    """
    Inserts a new Seed into the db, using the seed name, seed type id, and 
    supplier id from the request form data, and redirects to the /seeds route.
    """
    db_connection = db.connect_to_database()
    new_seed_name = request.form.get('seed-name')
    new_seed_type_id = request.form.get('seed-type')
    new_supplier_id = request.form.get('supplier')
    if new_supplier_id == '0':
        new_supplier_id = None
    query = "INSERT INTO Seeds (seed_name, seed_type_id, supplier_id) \
            VALUES (%s, %s, %s);"
    
    try:
        cursor = db.execute_query(db_connection=db_connection, query=query, 
                                query_params=(new_seed_name, new_seed_type_id, new_supplier_id))
    except Exception as e:
        print("Error creating seed: ", e)
        
    return redirect('/seeds')

# Update Seeds
@seeds_bp.route('/update', methods=['PUT'])
def seeds_update():
    """
    Updates a Seed in the db, using the seed name, seed type id, supplier id,
    and seed id from the request, and returns a JSON response.
    """
    db_connection = db.connect_to_database()
    data = request.get_json()
    new_seed_name = data.get('seed-name')
    new_seed_type_id = data.get('seed-type')
    new_supplier_id = data.get('supplier')
    update_seed_id = data.get('seed-id')

    query = "UPDATE Seeds \
            SET seed_name = %s,\
                seed_type_id = %s,\
                supplier_id = %s\
            WHERE seed_id = %s;"

    try:
        cursor = db.execute_query(db_connection=db_connection, query=query, 
                                query_params=(
                                    new_seed_name, new_seed_type_id, new_supplier_id, update_seed_id))
        if cursor.rowcount > 0:
            response = {'message': 'Seed updated successfully'}
            return jsonify(response), 200
    
    except Exception as e:
        print("Error updating seed: ", e)
    
    # No changes were made, so return an error message with status 404.
    response = {'message': 'Error updating Seed'}
    return jsonify(response), 404

# Delete Seeds
@seeds_bp.route('/delete/<seed_id>', methods=['DELETE'])
def seeds_delete(seed_id):
    """
    Deletes a Seed in the db, using the seed id, and returns a JSON response.
    """
    db_connection = db.connect_to_database()
    query = "DELETE FROM Seeds WHERE seed_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(seed_id,))
    
    if cursor.rowcount == 0:
        # Nothing was deleted, so return an error message with status 404.
        response = {'message': 'Seed not found'}
        return jsonify(response), 404
    
    # Delete any Sales if deleting the Seed left no Sales Details for the Sale
    query = "DELETE FROM Sales WHERE sale_id IN (\
            SELECT Sales.sale_id FROM Sales\
            LEFT JOIN Sales_Details ON Sales.sale_id = Sales_Details.sale_id\
            GROUP BY Sales.sale_id\
            HAVING COUNT(Sales_Details.sale_id) = 0);"
    cursor.execute(query)
    db_connection.commit()
    response = {'message': 'Seed deleted successfully'}
    return jsonify(response), 200