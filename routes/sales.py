from flask import Blueprint, render_template, request, redirect, jsonify
import database.db_connector as db

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

# Read Sales
@sales_bp.route('/', methods=['GET'])
def sales():
    """
    Retreives all Sales from the db, and Customer and Seed dropdown data from
    the db, and renders the sales template with Sales data, column names, and 
    the drop down data.
    """
    db_connection = db.connect_to_database()
    sales_query = "SELECT Sales.sale_id as 'Sale ID', \
                    Customers.customer_id as 'Customer ID', \
                    CONCAT(Customers.first_name, ' ', Customers.last_name) \
                        AS 'Customer Name', \
                    Sales.date AS 'Date' FROM Sales \
                    INNER JOIN Customers ON Sales.customer_id = Customers.customer_id;"
    cursor = db.execute_query(db_connection=db_connection, query=sales_query)
    sales_res = cursor.fetchall()

    # Filter out the column names 
    # (otherwise you need at least 1 row in the table to get the column names)
    col_names = [col[0] for col in cursor.description]

    # Dropdown Selects
    # Select Customers
    customer_query = "SELECT customer_id, CONCAT(first_name, ' ', last_name) AS 'Customer Name' FROM Customers;"
    cursor.execute(customer_query)
    customer_res = cursor.fetchall()
    # Select Seeds
    seed_query = "SELECT seed_id, seed_name FROM Seeds;"
    cursor.execute(seed_query)
    seed_res = cursor.fetchall()

    return render_template("sales.j2", sales=sales_res, col_names=col_names, 
                           customers=customer_res, seeds=seed_res)

# Read Sales Details
@sales_bp.route('/<sale_id>', methods=['GET'])
def sales_details(sale_id):
    """
    Gets all Sales Details that corresponds to the sale_id.
    Returns JSON with sales_details: a list of sales details with a Seed Name and Quantity.
    """
    db_connection = db.connect_to_database()
    sales_details_query = "SELECT Seeds.seed_name, Sales_Details.quantity FROM Sales_Details \
                            INNER JOIN Seeds ON Sales_Details.seed_id = Seeds.seed_id \
                            WHERE Sales_Details.sale_id = %s;"
    cursor = db.execute_query(db_connection=db_connection, query=sales_details_query, query_params=(sale_id,))
    sales_details_res = cursor.fetchall()

    res = {'sales_details': sales_details_res}
    
    return jsonify(res)

# Create Sales and Sales Details
@sales_bp.route('/create', methods=['POST'])
def sales_create():
    """
    Inserts a new Sale into the db, along with one or more Sales Details, using 
    the customer id, and sale date for the Sale, and seed ids and quantities for 
    the Sales Details from the request form data. Redirects to the /sales route.
    """
    db_connection = db.connect_to_database()
    new_customer_id = request.form.get('customer')
    new_sale_date = request.form.get('date')
    new_seeds = request.form.getlist('seed[]')
    new_quantities = request.form.getlist('quantity[]')

    # Add new Sales
    add_sale_query = "INSERT INTO Sales (customer_id, date) \
                        VALUES (%s, %s);" # :new_customer_id, :new_sale_date
    
    cursor = db.execute_query(db_connection=db_connection, query=add_sale_query, 
                              query_params=(new_customer_id, new_sale_date))
    
    get_id_query = "SELECT LAST_INSERT_ID();"
    cursor.execute(get_id_query)
    new_sale_id = cursor.fetchone()['LAST_INSERT_ID()']

    # Add Sales Details for the Sale
    add_sd_query = "INSERT INTO Sales_Details (sale_id, seed_id, quantity) \
                    VALUES (%s, %s, %s)" # :new_sale_id, :new_seed_id, :new_quantity
    inserts =  [(new_sale_id, seed, quantity) for seed, quantity in zip(new_seeds, new_quantities)]
    cursor.executemany(add_sd_query, inserts)
    db_connection.commit()
    return redirect('/sales')

# Delete Sales
@sales_bp.route('/delete/<sale_id>', methods=['DELETE'])
def sales_delete(sale_id):
    """
    Deletes a Sale in the db, using the sale id, and returns a JSON response.
    """
    db_connection = db.connect_to_database()
    query = "DELETE FROM Sales WHERE sale_id = %s"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(sale_id,))
    
    if cursor.rowcount == 0:
        # the seed_id does not exist
        response = {'message': 'Sale not found'}
        return jsonify(response), 404
    
    response = {'message': 'Sale deleted successfully'}
    return jsonify(response), 200