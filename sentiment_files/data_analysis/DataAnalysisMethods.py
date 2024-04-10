import sqlite3
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sentiment_files.DBmethods import DBmethods

class DataAnalysisMethods:
    def __init__(self, db_path='../datasets/database.db'):
        self.db_path = db_path

    # Export table to CSV
    def export_table_to_csv(self, table_name, csv_file):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Retrieve all data from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Get the column names from the table
            cursor.execute(f"PRAGMA table_info({table_name})")
            column_names = [column[1] for column in cursor.fetchall()]

            # Write the data to the CSV file
            with open(csv_file, "w", newline="") as file:
                writer = csv.writer(file)

                # Write the column names as the header
                writer.writerow(column_names)

                # Write the data rows
                writer.writerows(rows)

            # Close the database connection
            conn.close()

            print(f"Data from table '{table_name}' exported to '{csv_file}'")

        except sqlite3.Error as e:
            # Handle any database errors here
            print(f"Error: {e}")

    # Spit dataset into training and test data
    def split_data(self, dataset, train, test):
        dataset = pd.read_csv(dataset)  # Read the CSV dataset into a DataFrame
        selected_columns = ["review_id", "review_title", "review_body", "review_rating"]  # Select specific columns
        dataset_subset = dataset[selected_columns]  # Select the specified columns from the dataset
        train_data, test_data = train_test_split(dataset_subset, test_size=0.2,
                                                 random_state=42)  # Split the subset dataset into training (80%) and test (20%) sets
        train_data.to_csv(train, index=False)  # Save the training and test sets into separate CSV files
        test_data.to_csv(test, index=False)

    # Update DB from CSV
    def csv_update_db(self, csv_file, id_alias, update_column_alias, update_column_value):
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)  # Create a CSV reader
            DB = DBmethods('../datasets/database.db')  # Instantiate the DBmethods class
            for row in csv_reader:  # Iterate through each row in the CSV file
                id_value = row[id_alias]
                query = DB.update_query(f"UPDATE reviews SET {update_column_alias} = ? WHERE {id_alias} = ?",
                                        [update_column_value, id_value])
                # query = DB.update_query("UPDATE reviews SET {update_column_alias} = ? WHERE {id_alias} = ?",
                #                         [update_column_value, id_value])
                if "status" in query and query["status"] == False:
                    return query

            # Else show success
            return {'status': True, 'data': 'Success'}

    """
    Randomly select the 50% of the data from the 'dataset_100_train.csv'
    """
    def randomly_select_50_percent_of(self, dataset, output):
        df = pd.read_csv(dataset)
        train_df, test_df = train_test_split(df, test_size=0.5,
                                             random_state=42)
        train_df.to_csv(output, index=False)


    # Export table to CSV
    def csv_for_plot(self, table_name, csv_file):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Retrieve all data from the table
            cursor.execute(f"SELECT * FROM {table_name} WHERE gpt!=0 and llama!=0")
            rows = cursor.fetchall()

            # Get the column names from the table
            cursor.execute(f"PRAGMA table_info({table_name})")
            column_names = [column[1] for column in cursor.fetchall()]

            # Write the data to the CSV file
            with open(csv_file, "w", newline="") as file:
                writer = csv.writer(file)

                # Write the column names as the header
                writer.writerow(column_names)

                # Write the data rows
                writer.writerows(rows)

            # Close the database connection
            conn.close()

            print(f"Data from table '{table_name}' exported to '{csv_file}'")

        except sqlite3.Error as e:
            # Handle any database errors here
            print(f"Error: {e}")

    def db_to_csv(self, csv_file):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT review_id, review_rating, (review_title || ' ' || review_body) AS review
            FROM reviews
        '''
        cursor.execute(query)
        # Fetch all the rows
        rows = cursor.fetchall()

        # Write the result to a CSV file
        with open(csv_file, 'w', newline='') as file:
            # Create a CSV writer object
            csv_writer = csv.writer(file)

            # Write headers
            csv_writer.writerow(['review_id', 'review_rating', 'review'])

            # Write rows
            csv_writer.writerows(rows)

        # Close the database connection
        conn.close()