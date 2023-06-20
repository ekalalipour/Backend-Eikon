from flask import Blueprint, jsonify
from etl.etl_logic import perform_etl
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Create a Blueprint for the routes
api = Blueprint('api', __name__)

# Initialize SQLAlchemy
db = SQLAlchemy()

#Send the data to database
@api.route('/etl', methods=['POST'])
def etl():
    # Truncate the experiment_summary table
    truncate_statement = text('TRUNCATE TABLE experiment_summary RESTART IDENTITY')
    db.session.execute(truncate_statement)

    # Perform ETL and extract the data
    extracted_data = perform_etl()

    print("Extracted Data:")
    print(extracted_data)

    # Save extracted data to the database
    save_to_database(extracted_data)

    # Return a response indicating the success or failure of the ETL process
    return jsonify({'message': 'ETL process completed successfully'})

@api.route('/experiment_summary', methods=['GET'])
def get_experiment_summary():
    # Fetch the data from the experiment_summary table
    query = text("SELECT user_id, total_experiments, average_experiments, most_common_compound_name FROM experiment_summary")
    result = db.session.execute(query)

    # Get column names
    column_names = result.keys()

    # Convert the result rows to dictionaries
    data = [dict(zip(column_names, row)) for row in result.fetchall()]

    # Return the data as a JSON response
    return jsonify(data)

def save_to_database(data):
    query = text("""
        INSERT INTO experiment_summary (user_id, total_experiments, average_experiments, most_common_compound_name)
        VALUES (:user_id, :total_experiments, :average_experiments, ARRAY[:most_common_compound_name])
        """)

    for user_data in data:
        user_id = user_data['user_id']
        total_experiments = user_data['total_experiments']
        average_experiments = user_data['average_experiment_run_time']
        most_common_compound = user_data['compound_name']

        db.session.execute(
            query,
            {"user_id": user_id, "total_experiments": total_experiments, "average_experiments": average_experiments, "most_common_compound_name": most_common_compound}
        )

    db.session.commit()











