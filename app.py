from flask import Flask, render_template
import os
from dotenv import load_dotenv, find_dotenv

from routes.seeds import seeds_bp
from routes.sales import sales_bp
from routes.suppliers import suppliers_bp
from routes.customers import customers_bp
from routes.seed_types import seed_types_bp



load_dotenv(find_dotenv())


app = Flask(__name__)

# Add blueprint routes to app
app.register_blueprint(seeds_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(suppliers_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(seed_types_bp)

# Main/Index Route
@app.route('/')
def root():
    return render_template("main.j2")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT'))     
    app.run(port=port) 

