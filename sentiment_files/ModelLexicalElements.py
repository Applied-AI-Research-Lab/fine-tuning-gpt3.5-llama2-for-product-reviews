from GPTmethods import GPTmethods
from LLAMAmethods import LLAMAmethods
from DBmethods import DBmethods
import json
import re
import os
import csv


def detect_lexical_elements(model, review_text, review_rating):
    my_prompt = f'''Please carefully analyze the review text provided and identify the words or phrases that played a significant role in influencing both your and the reviewer's rating decision. Your response should be in JSON format, listing the words or phrases and their corresponding influence on the rating. For example: {{"1": "word or phrase", "2": "word or phrase", "3": "word or phrase", ...}} \n
Review text: {review_text}\n
Review rating: {review_rating}'''
    if model == 'gpt':
        conversation = []
        conversation.append({'role': 'system', 'content': my_prompt})
        GPT = GPTmethods(model_id='ft:gpt-3.5-turbo-0613:personal::86btcxwz')
        conversation = GPT.gpt_conversation(conversation)  # get the response from GPT model
        return clean_responses(conversation[-1]['content'])  # clean the response to be sure for the outcome
    elif model == 'llama':
        conversation = my_prompt
        LLAMA = LLAMAmethods(
            model_id='kroumeliotis/sentiment100:cef8e152137a3d7345317691a8842bf1358881fa055185af5684765d77c9a4dd')
        conversation = LLAMA.llama_conversation(conversation)  # get the response from LLAMA2 model
        return clean_responses(conversation)  # clean the response to be sure for the outcome


def clean_responses(conversation):
    json_pattern = r'{.*?}'  # detect the json format
    match = re.search(json_pattern, conversation, re.DOTALL)  # match the json
    response = json.loads(match.group(0))  # json load
    return list(response.values())  # turn json to list


def append_data_to_csv(data_to_append):
    directory = "datasets"  # Directory
    csv_file_path = os.path.join(directory, "lexical-elements.csv")

    if not os.path.exists(csv_file_path):  # If the CSV file does not exist, create it and write the header
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['id', 'review_rating', 'review_text', 'gpt', 'llama']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(csv_file_path, 'a', newline='') as csvfile:  # Append the data to the CSV file
        fieldnames = ['id', 'review_rating', 'review_text', 'gpt', 'llama']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if os.path.getsize(csv_file_path) == 0:  # If the file is empty, write the header
            writer.writeheader()
        writer.writerow(data_to_append)


def run_lexical():
    # Find the common correct answers of the fine-tuned models
    DB = DBmethods('datasets/database.db')
    data_dict = DB.select_query(
        "SELECT * FROM reviews WHERE review_rating=ft_llama_100 AND review_rating=ft_gpt_100 ORDER BY RANDOM() LIMIT 20",
        [])
    if data_dict['status']:
        for review in data_dict['data']:
            review_id = review['review_id']
            review_text = review['review_title'] + ' ' + review['review_body']
            review_rating = review['review_rating']
            # Ask the fine-tuned models to find those lexical elements that led both the reviewer and themselves
            # to evaluate the review with the specific rating star
            llama = detect_lexical_elements('llama', review_text, review_rating)  # Llama 2 model
            gpt = detect_lexical_elements('gpt', review_text, review_rating)  # GPT 3.5 model

            # Save the results in a CSV file
            append_data_to_csv({
                'id': review_id,
                'review_rating': review_rating,
                'review_text': review_text,
                'gpt': gpt,
                'llama': llama
            })
            exit()


run_lexical()
