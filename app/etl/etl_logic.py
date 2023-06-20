import pandas as pd
import os

def perform_etl():
    # Get the file paths from environment variables
    users_csv_path = os.environ.get('USERS_CSV_PATH')
    experiments_csv_path = os.environ.get('EXPERIMENTS_CSV_PATH')
    compounds_csv_path = os.environ.get('COMPOUNDS_CSV_PATH')

    # Read the CSV files into DataFrames
    users_df = pd.read_csv(users_csv_path)
    experiments_df = pd.read_csv(experiments_csv_path)
    compounds_df = pd.read_csv(compounds_csv_path)

    # Strip leading and trailing spaces from column names
    users_df.columns = users_df.columns.str.strip()
    experiments_df.columns = experiments_df.columns.str.strip()
    compounds_df.columns = compounds_df.columns.str.strip()

    # Split the semicolon-separated values and convert them to integers
    experiments_df['experiment_compound_ids'] = experiments_df['experiment_compound_ids'].apply(lambda x: [int(i) for i in x.split(';')])

    # Explode the DataFrame to have one row per compound ID
    experiments_df = experiments_df.explode('experiment_compound_ids')
    experiments_df.columns = experiments_df.columns.str.strip()

    # Calculate total experiments per user
    total_experiments = experiments_df.groupby('user_id')['experiment_id'].nunique().reset_index(name='total_experiments')

    # Calculate average experiment run time per user
    avg_experiment_time = experiments_df.groupby('user_id')['experiment_run_time'].mean().reset_index(name='average_experiment_run_time')

    # Get the most commonly experimented compounds per user
    def get_most_common_compounds(x):
        most_common = x.value_counts()
        max_count = most_common.max()
        return most_common[most_common == max_count].index.tolist()

    most_common_compounds = experiments_df.groupby('user_id')['experiment_compound_ids'].apply(get_most_common_compounds).reset_index()
    most_common_compounds = most_common_compounds.explode('experiment_compound_ids')
    most_common_compounds.columns = ['user_id', 'compound_id']
    most_common_compounds = most_common_compounds.merge(compounds_df, on='compound_id', how='left')

    # Combine the compound names for each user
    most_common_compounds = most_common_compounds.groupby('user_id')['compound_name'].apply(lambda x: ', '.join(x.str.strip())).reset_index()

    # Merge all the derived features into the final DataFrame
    final_df = users_df.merge(total_experiments, on='user_id', how='left')
    final_df = final_df.merge(avg_experiment_time, on='user_id', how='left')
    final_df = final_df.merge(most_common_compounds, on='user_id', how='left')

    # Remove unnecessary columns
    final_df = final_df.drop(['name', 'email', 'signup_date'], axis=1)

    # Prepare the data for database insertion
    extracted_data = final_df.to_dict('records')

    # print("Extracted Data:")
    # for record in extracted_data:
    #     print(record)

    return extracted_data





























































