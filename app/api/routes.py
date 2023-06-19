from flask import Blueprint, jsonify
from etl.etl_logic import perform_etl
from main import db

# Create a Blueprint for the routes
api = Blueprint('api', __name__)

@api.route('/etl', methods=['POST'])
def etl():
    # Perform ETL and extract the data
    extracted_data = perform_etl()

    # Save extracted data to the database
    save_to_database(extracted_data)

    # Return a response indicating the success or failure of the ETL process
    return jsonify({'message': 'ETL process completed successfully'})

def save_to_database(data):
    # Extract the required fields from the data
    total_experiments_per_user = data['total_experiments_per_user']
    average_experiments_per_user = data['average_experiments_per_user']
    most_common_compound_per_user = data['most_common_compound_per_user']

    # Prepare the data for insertion
    rows = []
    for user_data in total_experiments_per_user:
        user_id = user_data['user_id']
        total_experiments = user_data['total_experiments']
        average_experiments = next(
            (x['average_experiments'] for x in average_experiments_per_user if x['user_id'] == user_id),
            None
        )
        most_common_compound = next(
            (x['compound_name'] for x in most_common_compound_per_user if x['user_id'] == user_id),
            None
        )
        rows.append((user_id, total_experiments, average_experiments, most_common_compound))

    # Perform a single bulk insert query
    query = """
    INSERT INTO experiment_summary (user_id, total_experiments, average_experiments, most_common_compound)
    VALUES %s
    """
    values = ','.join(['(%s, %s, %s, %s)'] * len(rows))
    query = query % values
    flattened_rows = [item for sublist in rows for item in sublist]
    db.session.execute(query, flattened_rows)

    # Commit the changes to the database
    db.session.commit()


