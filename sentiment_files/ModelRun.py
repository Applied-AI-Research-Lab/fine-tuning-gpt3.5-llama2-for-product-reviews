from GPTmethods import GPTmethods
from LLAMAmethods import LLAMAmethods
from DBmethods import DBmethods
# import replicate
import time


def run_sentiment(model, model_id, type_column, type_value, output_column, limit_results):
    DB = DBmethods('datasets/database.db')
    data_dict = DB.select_query(
        "SELECT review_id, review_title, review_body FROM reviews WHERE " + type_column + "=? AND " + output_column + "=0 LIMIT ?",
        [type_value, limit_results])
    ids = []
    reviews = []
    if data_dict['status']:
        for review in data_dict['data']:
            review_id = review['review_id']
            review_title = review['review_title']
            review_body = review['review_body']
            ids.append(review_id)
            reviews.append(review_title + ' ' + review_body)
            print(reviews)
        if model == 'gpt':
            # Run GPT Model
            GPT = GPTmethods(model_id=model_id)
            response = GPT.gpt_ratings(reviews)
        elif model == 'llama':
            # Run LLAMA2 Model
            LLAMA = LLAMAmethods(model_id=model_id)
            response = LLAMA.llama_ratings(reviews)
        else:
            response = {'status': False, 'data': 'Wrong model'}

        if response['status']:
            # Update reviews table
            for id, rating in zip(ids, response['data']):
                update = DB.update_query("UPDATE reviews SET " + output_column + " = ? WHERE review_id=?", [rating, id])
                if update['status'] == False:
                    return update
        else:
            return response

        return {'status': True, 'data': 'Done'}


'''
Run the model with model_id = 'model_id'
Select the reviews where type_column=type_value
And update the output_column
(By changing the 'model_id,' you can run either the fine-tuned or non-fine-tuned model.)
'''
num_calls = 755  # number of test samples

# # Run the Llama 2 model without fine-tuning
# for _ in range(num_calls):
#     response = run_sentiment(model='llama',
#                         model_id='meta/llama-2-70b-chat',
#                         type_column='ft_type_100',  # Run the sentiment only for test data
#                         type_value='test',
#                         output_column='llama',
#                         limit_results=5)
#     print(response)
#     time.sleep(3)  # Wait for 3 seconds before making the next call

# Run the GPT model without fine-tuning
# for _ in range(num_calls):
#     response = run_sentiment(model='gpt',
#                         model_id='gpt-3.5-turbo',
#                         type_column='ft_type_100',  # Run the sentiment only for test data
#                         type_value='test',
#                         output_column='gpt',
#                         limit_results=5)
#     print(response)
#     time.sleep(3)  # Wait for 3 seconds before making the next call

# Run the Llama 2 model with the 'model_id' corresponding to the fine-tuned model
# for _ in range(num_calls):
#     response = run_sentiment(model='llama',
#                         model_id="kroumeliotis/ecommerce-reviews50:b05681bde5e95e234f46b8fd5316c4c829def91ed1507e7f3e129902cfab6d11",
#                         type_column='ft_type_100',
#                         type_value='test',
#                         output_column='ft_llama',
#                         limit_results=5)
#     print(response)
#     time.sleep(3)  # Wait for 3 seconds before making the next call

# Run the GPT model with the 'model_id' corresponding to the fine-tuned model
# for _ in range(num_calls):
#     response = run_sentiment(model='gpt',
#                         model_id='ft:gpt-3.5-turbo-1106:personal::8WKvItrZ',
#                         type_column='ft_type_100',  # The column ft_type_100 is the same for 50 and 100
#                         type_value='test',
#                         output_column='ft_gpt',  # You only have to change the model_id and output_column
#                         limit_results=1)
#     print(response)
#     time.sleep(3)  # Wait for 3 seconds before making the next call
