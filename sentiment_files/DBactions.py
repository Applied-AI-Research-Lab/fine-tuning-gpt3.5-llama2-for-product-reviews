from DBmethods import DBmethods

DB = DBmethods()

# Create 1st the dataset.csv
# for non-split datasets
# print(DB.create_csv_from_db())
# for ready-split datasets
# print(DB.create_csv_from_db_split('train'))
# print(DB.create_csv_from_db_split('validation'))
# print(DB.create_csv_from_db_split('test'))

# Upload it to Colab
# Split dataset to Train, Validation, Test
# Fine-tune the BERT and RoBERTa models
# Make prediction using the fine-tuned models
# Get the Predictions and store them to /datasets

# Update ft_type_100 column to train, validation, test
# print(DB.train_validation_test_to_db('datasets/test_dataset.csv', 'datasets/database.db', 'reviews', 'review_id',
#                                      'ft_type_100', 'test'))
# print(DB.train_validation_test_to_db('datasets/train_dataset.csv', 'datasets/database.db', 'reviews', 'review_id',
#                                      'ft_type_100', 'train'))
# print(DB.train_validation_test_to_db('datasets/validation_dataset.csv', 'datasets/database.db', 'reviews', 'review_id',
#                                      'ft_type_100', 'validation'))

# Get the review_rating values from csv and store them to the appropriate column
# DB.importPredictions('bert-adam-predictions.csv', 'ft_bert_adam')
# DB.importPredictions('bert-adamw-predictions.csv', 'ft_bert_adamw')
# DB.importPredictions('bert-sgd-predictions.csv', 'ft_bert_sgd')
# DB.importPredictions('roberta-adam-predictions.csv', 'ft_roberta_adam')
# DB.importPredictions('roberta-adamw-predictions.csv', 'ft_roberta_adamw')
# DB.importPredictions('roberta-sgd-predictions.csv', 'ft_roberta_sgd')



