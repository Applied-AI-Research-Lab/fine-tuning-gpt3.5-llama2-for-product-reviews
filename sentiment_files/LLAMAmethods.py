import replicate
import json
import re


class LLAMAmethods:
    def __init__(self,
                 model_id="replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781"):
        self.model_id = model_id
        # self.prompt = "Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in json format like this example {'rating1':integer,'rating2':integer,...}. Please avoid providing additional explanations. Reviews:\n"
        # self.prompt = 'Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in json format like this example {"rating1":integer,"rating2":integer,...}. Please avoid providing additional explanations. Reviews:\n'
        # self.prompt = 'Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in JSON format like this example: {"rating1":integer, "rating2":integer, ...}. Do not provide explanations or justifications for the ratings. Reviews"\n'
        self.prompt = 'Assign integer star ratings (between 1 and 5) to the following product reviews. Return your response in json format like this example {"rating1":integer,"rating2":integer,...}. Do not provide explanations or justifications for the ratings. Reviews:\n'

    """
    Create a conversation with LLAMA2 model
    """

    def llama_conversation(self, conversation):
        result_string = ""
        for event in replicate.stream(
                self.model_id,
                input={"prompt": conversation}
        ):
            result_string += str(event)

        return result_string
        # older version
        # output = replicate.run(
        #     self.model_id,
        #     input={"prompt": conversation}
        # )
        # response = ""
        # for item in output:
        #     # https://replicate.com/replicate/llama-2-70b-chat/versions/58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781/api#output-schema
        #     response += item
        # return response

    """
    Clean the response
    """

    def llama_clean_response(self, conversation):
        try:
            # Attempt to parse the response as JSON
            result = json.loads(conversation)
            ratings = []
            for key, value in result.items():
                if isinstance(value, int):
                    ratings.append(value)
            return ratings
        except json.JSONDecodeError:
            # If it's not valid JSON, use regular expressions to extract the JSON part
            json_pattern = r'{.*?}'
            match = re.search(json_pattern, conversation, re.DOTALL)
            if match:
                json_response = match.group(0)
                result = json.loads(json_response) # Parse the JSON
                ratings = []
                for key, value in result.items():
                    if isinstance(value, int):
                        ratings.append(value)
                return ratings
            else:
                return "JSON not found in the response."

        # # Parse the JSON-like string into a Python dictionary
        # data = json.loads(conversation)
        #
        # # Extract all the numbers (ratings) from the dictionary
        # ratings = []
        # for key, value in data.items():
        #     if isinstance(value, int):
        #         ratings.append(value)
        #
        # return ratings

    """
    Handle the response of LLAMA 2 model
    """

    def llama_ratings(self, reviews):
        if not isinstance(reviews, list):
            return {'status': False, 'data': 'Reviews variable is not a list'}
        else:
            my_prompt = self.prompt
            ii = 1
            for review in reviews:  # add the reviews into the prompt
                my_prompt += f"{ii}. \"{review}\"\n"
                ii += 1
            # print(my_prompt)
            # exit()
            # my_prompt += '\n'.join(reviews)
            conversation = my_prompt
            conversation = self.llama_conversation(conversation)  # get the response from LLAMA2 model
            print(conversation)
            # exit()
            ratings = self.llama_clean_response(conversation)  # Clean the output of LLAMA2 model

            if len(ratings) == len(reviews):
                return {'status': True, 'data': ratings}
            else:
                return {'status': False,
                        'data': 'The ratings returned by the model do not match the number of reviews.\nConversation:' + conversation}

    """
    Train Llama 2 model
    """

    def llama_train(self, destination, train_data):
        # https://replicate.com/blog/fine-tune-llama-2
        # https://replicate.com/docs/guides/fine-tune-a-language-model
        training = replicate.trainings.create(
            version=self.model_id,
            # ex. "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"
            input={
                "train_data": train_data,
                # Uploaded data to a live web server ex. "https://acloud.gr/ai/train-data-llama.jsonl"
                "num_train_epochs": 3,  # Number of epochs (iterations over the entire training dataset) to train for.
            },
            destination=destination  # Trained Model ex."kroumeliotis/sentiment"
        )

        return training
