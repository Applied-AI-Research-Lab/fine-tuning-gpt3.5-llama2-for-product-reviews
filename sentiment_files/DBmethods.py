import sqlite3
import re
import unicodedata
import json
import csv
import pandas as pd
import csv


class DBmethods:
    def __init__(self, db_path='datasets/database.db'):
        self.db_path = db_path

    # Alter Add Column
    def alter_add_column(self, table, column_name, column_type):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)  # sentiment_files/datasets/database.db

        cursor = connection.cursor()

        try:
            alter_table_sql = '''
                ALTER TABLE {}
                ADD COLUMN {} {}
            '''.format(table, column_name, column_type)  # Define the SQL statement with placeholders

            cursor.execute(alter_table_sql)
            connection.commit()
            return {'status': True, 'data': True}
        except sqlite3.Error as error:
            return {'status': False, 'data': "An error occurred:" + str(error)}
        finally:
            connection.close()

    # Alter Drop Column
    def alter_drop_column(self, table, column_name):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)  # sentiment_files/datasets/database.db
        cursor = connection.cursor()

        try:
            alter_table_sql = '''
                ALTER TABLE {}
                DROP COLUMN {}
            '''.format(table, column_name)  # Define the SQL statement with placeholders

            cursor.execute(alter_table_sql)
            connection.commit()
            return {'status': True, 'data': True}
        except sqlite3.Error as error:
            return {'status': False, 'data': "An error occurred:" + str(error)}
        finally:
            connection.close()

    # Create products' table
    def create_products_table(self):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)

        cursor = connection.cursor()

        try:
            # Create the "products" table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_code TEXT,
                    product_title TEXT,
                    product_description TEXT,
                    product_category TEXT
                )
            ''')  # product_code is the URL code (product_id) in content.js

            # Commit the changes
            connection.commit()
            return {'status': True, 'data': True}
        except sqlite3.Error as error:
            return {'status': False, 'data': "An error occurred:" + str(error)}
        finally:
            connection.close()

    # Create reviews' table
    def create_reviews_table(self):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)

        cursor = connection.cursor()

        try:
            # Create the "reviews" table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    review_rating INTEGER,
                    review_title TEXT,
                    review_body TEXT,
                    gpt INTEGER,
                    llama INTEGER,
                    ft_gpt_50 INTEGER,
                    ft_llama_50 INTEGER,
                    ft_gpt_100 INTEGER,
                    ft_llama_100 INTEGER,
                    ft_type_50 TEXT,
                    ft_type_100 TEXT,
                    tokens TEXT,
                    FOREIGN KEY (product_id) REFERENCES products (product_id)
                )
            ''')

            # Commit the changes
            connection.commit()
            return {'status': True, 'data': True}
        except sqlite3.Error as error:
            return {'status': False, 'data': "An error occurred:" + str(error)}
        finally:
            connection.close()

    # Empty table
    def empty_table(self, table_name):
        # Connect to the SQLite database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        cursor.execute(f"DELETE FROM {table_name}")

        # Commit the transaction
        connection.commit()

        # Reset the auto-increment counters using VACUUM
        cursor.execute("VACUUM")

        # Commit again to apply the VACUUM operation
        connection.commit()

        # Close the connection
        connection.close()

    # Select a table with query and params arguments
    def select_query(self, query, params):
        # Create a connection to the database
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row  # Set the row factory to sqlite3.Row
        cursor = connection.cursor()

        try:
            # Execute the SELECT query
            cursor.execute(query, params)

            rows = cursor.fetchall()

            # Get the column names from the cursor description
            column_names = [column[0] for column in cursor.description]

            # Process the rows and create dictionaries
            rows_as_dicts = []
            for row in rows:
                row_dict = {}
                for column_name in column_names:
                    row_dict[column_name] = row[column_name]
                rows_as_dicts.append(row_dict)
            if not rows_as_dicts:  # if the dictionary is empty
                return {'status': False, 'data': []}
            else:
                return {'status': True, 'data': rows_as_dicts}
        except sqlite3.Error as error:
            return {'status': False, 'data': "An error occurred:" + str(error)}
        finally:
            connection.close()

    # Insert query
    def insert_query(self, query, params):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Execute the insert query with parameters
            cursor.execute(query, params)

            # Get the last insert ID
            last_insert_id = cursor.lastrowid

            # Commit the transaction
            conn.commit()

            # Close the database connection
            conn.close()

            # Return the last insert ID
            return {'status': True, 'data': last_insert_id}

        except sqlite3.Error as e:
            # If there is an error, return an error message
            return {'status': False, 'data': "An error occurred:" + str(e)}

    # Update query
    def update_query(self, query, params):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Execute the update query with parameters
            cursor.execute(query, params)

            # Commit the transaction
            conn.commit()

            # Get the ID of the last updated row
            last_updated_id = cursor.lastrowid

            # Close the database connection
            conn.close()

            # Return the ID of the last updated row
            return {'status': True, 'data': last_updated_id}

        except sqlite3.Error as e:
            # Handle any database errors here
            return {'status': False, 'data': "An error occurred:" + str(e)}

    # Delete query
    def delete_query(self, query, params=None):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Execute the delete query with optional parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Commit the changes and close the connection
            conn.commit()
            conn.close()

            # Return success status
            return {'status': True, 'message': 'Delete operation successful'}

        except sqlite3.Error as e:
            # Handle any database errors
            return {'status': False, 'error': str(e)}

    # Preprocess Data. Remove unwanted chars
    def preprocess_text(self, text):
        # Remove special characters and extra white spaces
        text = re.sub(r'[^\w\s]', '', text)
        text = ' '.join(text.split())

        # Normalize text (e.g., convert accented characters to their base form)
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

        # Convert to lowercase
        text = text.lower()

        return text

    # Create a JSONL file with train data from db
    def create_jsonl(self, model, datatype, dataset_type=100):
        ft_type = 'ft_type_' + str(dataset_type)
        conn = sqlite3.connect('datasets/database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT review_title,review_body,review_rating FROM reviews WHERE " + ft_type + "='" + datatype + "'")
        data_from_db = cursor.fetchall()  # Fetch all the records as a list of tuples

        data = []  # Define a list to store the dictionaries
        for row in data_from_db:
            review_title, review_body, review_rating = row

            if model == 'llama':
                # llama_prompt = "Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in json format like this example {'rating1':integer,'rating2':integer,...}. Please avoid providing additional explanations. Reviews:\n"
                # llama_prompt = 'You are a product reviewer. Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in JSON format like this example: {"rating1":integer, "rating2":integer, ...}. Do not provide explanations or justifications for the ratings. Reviews"\n'
                llama_prompt = 'Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in json format like this example {"rating1":integer,"rating2":integer,...}. Do not provide explanations or justifications for the ratings. Reviews:\n'
                data.append({"prompt": llama_prompt + '1. ' + review_title + ' ' + review_body,
                             "completion": '{"rating1":' + str(
                                 review_rating) + '}'})  # The prompt and completion should be strings
            elif model == 'gpt':
                data.append(
                    {
                        "messages": [
                            {"role": "system", "content": "You are a product reviewer"},
                            {"role": "user",
                             "content": 'Predict the star ratings (integer between 1 and 5) to the following product reviews. Return your response in json format like this example {"rating1":integer,"rating2":integer,...}. Please avoid providing additional explanations. Reviews:\n1. ' + review_title + ' ' + review_body+''},
                            {"role": "assistant", "content": '{"rating1":' + str(review_rating) + '}'}
                        ]
                    }
                )
            else:
                return 'Wrong model'
        output_file_path = "datasets/ft_"+datatype+"_dataset_" + model + ".jsonl"  # Define the path
        # Write data to the JSONL file
        with open(output_file_path, 'w') as output_file:
            for record in data:
                # Convert the dictionary to a JSON string and write it to the file
                json_record = json.dumps(record)
                output_file.write(json_record + '\n')

        return f"JSONL file '{output_file_path}' has been created."

    def create_train_dataset_csv(self, type):
        conn = sqlite3.connect('datasets/database.db')
        cursor = conn.cursor()
        # Execute a query to get specific columns and concatenate review_title and review_body
        cursor.execute(
            'SELECT review_id, review_title || " " || review_body as review, review_rating FROM reviews WHERE ft_type_100=\'' + type + '\'')

        # Fetch all the rows
        rows = cursor.fetchall()

        # Specify the CSV file path
        csv_file_path = 'datasets/dataset-' + type + '.csv'

        # Write the data to a CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row with column names
            csv_writer.writerow(['review_id', 'review_rating', 'review'])

            # Write the data rows
            csv_writer.writerows(rows)

        # Close the database connection
        conn.close()

    def train_validation_test_to_db(self, csv_file, db_file, table_name, id_column, update_column, update_value):
        df = pd.read_csv(csv_file)  # Load the CSV file into a DataFrame
        conn = sqlite3.connect(db_file)  # DB Connection
        cursor = conn.cursor()
        for index, row in df.iterrows():  # Iterate through the DataFrame
            record_id = row[id_column]
            update_query = f"UPDATE {table_name} SET {update_column}='{update_value}' WHERE {id_column}={record_id};"  # update the SQLite table
            cursor.execute(update_query)
        conn.commit()  # Commit the changes
        conn.close()
        return {'status': True, 'data': True}

    def importPredictions(self, csv_file_name, column):
        csv_file_path = 'datasets/' + csv_file_name
        DB = DBmethods('datasets/database.db')
        # Open the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader, None)

            # Loop through each row in the CSV
            for row in csv_reader:
                review_id = row[0]
                prediction_rating = row[1]
                print(DB.update_query("UPDATE reviews SET " + column + " = ? WHERE review_id=?",
                                      [prediction_rating, review_id]))


    def create_csv_from_db(self):
        conn = sqlite3.connect('datasets/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT review_id, review_rating, review_title, review_body FROM reviews')
        rows = cursor.fetchall()
        conn.close()
        with open('datasets/dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['review_id', 'review_rating', 'review'])
            for row in rows:
                review_id, review_rating, review_title, review_body = row
                review = f'{review_title} {review_body}'
                csv_writer.writerow([review_id, review_rating, review])
        return True

    def create_csv_from_db_split(self, type):
        conn = sqlite3.connect('datasets/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT review_id, review_rating, review_title, review_body FROM reviews WHERE ft_type_100=?', (type,))
        rows = cursor.fetchall()
        conn.close()
        with open('datasets/'+type+'_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['review_id', 'review_rating', 'review'])
            for row in rows:
                review_id, review_rating, review_title, review_body = row
                review = f'{review_title} {review_body}'
                csv_writer.writerow([review_id, review_rating, review])
        return True

    def rename_column(self, before, after):
        conn = sqlite3.connect('datasets/database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE reviews RENAME COLUMN "+before+" TO "+after)
        except sqlite3.Error as e:
            print("SQLite error:", e)
        conn.commit()
        conn.close()