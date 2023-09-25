from flask import Blueprint, render_template, request, redirect, jsonify
import database.db_connector as db

seed_types_bp = Blueprint('seed_types', __name__, url_prefix='/seed_types')

# Read Seed_Types
@seed_types_bp.route('/', methods=['GET'])
def seed_types():
    """
    Retreives all Seed_Types from the database and renders the seed_types template
    with the Seed_Types data and column names.
    """
    db_connection = db.connect_to_database()
    query = "SELECT Seed_Types.seed_type as 'Seed Type' \
            FROM Seed_Types;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()

    # Filter out the column names 
    # (otherwise you need at least 1 row in the table to get the column names)
    col_names = [col[0] for col in cursor.description]

    return render_template("seed_types.j2", seed_types=results, col_names=col_names)

# Create Seed_Types
@seed_types_bp.route('/create', methods=['POST'])
def seed_types_create():
    """
    Inserts a new Seed_Type into the database using the seed_type from the request
    form data. Redirects to the /seed_types route.
    """
    db_connection = db.connect_to_database()
    new_seed_type = request.form.get('seed-type')

    query = "INSERT INTO Seed_Types (seed_type) VALUES (%s);"
    try:
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(new_seed_type,))
    except Exception as e:
        print("Error creating seed type: ", e)
    return redirect('/seed_types')
