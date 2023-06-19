import pandas as pd

def perform_etl():
    users_df = pd.read_csv('../../data/users.csv')
    experiments_df = pd.read_csv('../../data/user_experiments.csv')
    compounds_df = pd.read_csv('../../data/compounds.csv')

    users_df.columns = users_df.columns.str.strip()
    experiments_df.columns = experiments_df.columns.str.strip()
    compounds_df.columns = compounds_df.columns.str.strip()

    experiments_df['experiment_compound_ids'] = experiments_df['experiment_compound_ids'].apply(lambda x: [int(i) for i in x.split(';')])

    experiments_df = experiments_df.explode('experiment_compound_ids')
    experiments_df.columns = experiments_df.columns.str.strip()

    total_experiments = experiments_df.groupby('user_id')['experiment_id'].nunique().reset_index(name='total_experiments')
    avg_experiment_time = experiments_df.groupby('user_id')['experiment_run_time'].mean().reset_index(name='average_experiment_run_time')

    def get_most_common_compounds(x):
        most_common = x.value_counts()
        max_count = most_common.max()
        return most_common[most_common == max_count].index.tolist()

    most_common_compounds = experiments_df.groupby('user_id')['experiment_compound_ids'].apply(get_most_common_compounds).reset_index()
    most_common_compounds = most_common_compounds.explode('experiment_compound_ids')
    most_common_compounds.columns = ['user_id', 'compound_id']
    most_common_compounds = most_common_compounds.merge(compounds_df, on='compound_id', how='left')

    most_common_compounds = most_common_compounds.groupby('user_id')['compound_name'].apply(lambda x: ', '.join(x.str.strip())).reset_index()

    final_df = users_df.merge(total_experiments, on='user_id', how='left')
    final_df = final_df.merge(avg_experiment_time, on='user_id', how='left')
    final_df = final_df.merge(most_common_compounds, on='user_id', how='left')

    # Remove unnecessary columns
    final_df = final_df.drop(['name', 'email', 'signup_date'], axis=1)

    print("Consolidated Data:")
    print(final_df)

    extracted_data = {
        'consolidated_data': final_df.to_dict(orient='records')
    }

    return extracted_data

if __name__ == '__main__':
    extracted_data = perform_etl()





















# import pandas as pd

# def perform_etl():
#     users_df = pd.read_csv('../../data/users.csv')
#     experiments_df = pd.read_csv('../../data/user_experiments.csv')
#     compounds_df = pd.read_csv('../../data/compounds.csv')

#     users_df.columns = users_df.columns.str.strip()
#     experiments_df.columns = experiments_df.columns.str.strip()
#     compounds_df.columns = compounds_df.columns.str.strip()

#     experiments_df['experiment_compound_ids'] = experiments_df['experiment_compound_ids'].apply(lambda x: [int(i) for i in x.split(';')])

#     experiments_df = experiments_df.explode('experiment_compound_ids')
#     experiments_df.columns = experiments_df.columns.str.strip()

#     total_experiments = experiments_df.groupby('user_id').size().reset_index(name='total_experiments')
#     avg_experiment_time = experiments_df.groupby('user_id')['experiment_run_time'].mean().reset_index(name='average_experiment_run_time')

#     def get_most_common_compounds(x):
#         most_common = x.value_counts()
#         max_count = most_common.max()
#         return most_common[most_common == max_count].index.tolist()

#     most_common_compounds = experiments_df.groupby('user_id')['experiment_compound_ids'].apply(get_most_common_compounds).reset_index()
#     most_common_compounds = most_common_compounds.explode('experiment_compound_ids')
#     most_common_compounds.columns = ['user_id', 'compound_id']
#     most_common_compounds = most_common_compounds.merge(compounds_df, on='compound_id', how='left')

#     most_common_compounds = most_common_compounds.groupby('user_id')['compound_name'].apply(lambda x: ', '.join(x.str.strip())).reset_index()

#     final_df = users_df.merge(total_experiments, on='user_id', how='left')
#     final_df = final_df.merge(avg_experiment_time, on='user_id', how='left')
#     final_df = final_df.merge(most_common_compounds, on='user_id', how='left')

#     final_df = final_df[['user_id', 'total_experiments', 'average_experiment_run_time', 'compound_name']]

#     print("Consolidated Data:")
#     print(final_df)

#     extracted_data = {
#         'consolidated_data': final_df.to_dict(orient='records')
#     }

#     return extracted_data

# if __name__ == '__main__':
#     extracted_data = perform_etl()












# import pandas as pd

# def perform_etl():
#     # Read the csv files
#     users_df = pd.read_csv('../../data/users.csv')
#     experiments_df = pd.read_csv('../../data/user_experiments.csv')
#     compounds_df = pd.read_csv('../../data/compounds.csv')

#     # Remove extra tabs from column names and values
#     compounds_df.columns = compounds_df.columns.str.strip()
#     experiments_df.columns = experiments_df.columns.str.strip()
#     compounds_df['compound_name'] = compounds_df['compound_name'].str.strip()
#     compounds_df['compound_structure'] = compounds_df['compound_structure'].str.strip()
#     compounds_df['compound_id'] = compounds_df['compound_id'].astype(int)

#     # Group by 'user_id' and calculate total experiments per user
#     total_experiments_per_user = experiments_df.groupby('user_id').size().reset_index(name='total_experiments')

#     # Calculate average experiment run time per user
#     average_experiment_run_time_per_user = experiments_df.groupby('user_id')['experiment_run_time'].mean().reset_index(name='average_experiment_run_time')

#     # Find the most commonly experimented compound per user
#     most_common_compound_per_user = experiments_df.groupby('user_id')['experiment_compound_ids'].apply(lambda x: x.str.split(';').explode().value_counts().index[0]).reset_index(name='most_common_compound_id')
#     most_common_compound_per_user['most_common_compound_id'] = most_common_compound_per_user['most_common_compound_id'].astype(int)
#     most_common_compound_per_user = most_common_compound_per_user.merge(compounds_df, left_on='most_common_compound_id', right_on='compound_id')
#     most_common_compound_per_user = most_common_compound_per_user[['user_id', 'compound_name']]

#     # Consolidate the data into a single DataFrame
#     consolidated_data = pd.merge(users_df, total_experiments_per_user, on='user_id')
#     consolidated_data = pd.merge(consolidated_data, average_experiment_run_time_per_user, on='user_id')
#     consolidated_data = pd.merge(consolidated_data, most_common_compound_per_user, on='user_id')

#     # Remove the "name" and "email" columns
#     consolidated_data = consolidated_data.drop(['\tname', '\temail', '\tsignup_date'], axis=1)

#     # Log the consolidated data
#     print("Consolidated Data:")
#     print(consolidated_data)

#     # Return the consolidated data as a dictionary
#     extracted_data = {
#         'consolidated_data': consolidated_data.to_dict(orient='records')
#     }

#     return extracted_data

# if __name__ == '__main__':
#     extracted_data = perform_etl()



































