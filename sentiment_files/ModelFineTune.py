from DBmethods import DBmethods
from LLAMAmethods import LLAMAmethods
# from GPTmethods import GPTmethods

"""
Create the json files
"""
DB = DBmethods()
# print(DB.create_jsonl('gpt', 'train'))
# print(DB.create_jsonl('gpt', 'validation'))
# print(DB.create_jsonl('llama', 'train'))
# print(DB.create_jsonl('llama', 'validation'))
# exit()
"""
Train Llama 2 Model
"""
destination = "kroumeliotis/ecommerce-reviews50"  # Which is the new model you created in replicate?
train_data = "https://acloud.gr/ai/50/ft_train_dataset_llama.jsonl"  # Where the training data are hosted?
version = "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3"  # Which version of Llama you want to train?
LLAMA = LLAMAmethods(model_id=version)  # Instantiate the LLAMAmethods class
print(LLAMA.llama_train(destination, train_data))  # Run the train
"""
Run Llama 2 Trained Model
DO NOT USE IT! JUST AN EXAMPLE
"""
# LLAMA = LLAMAmethods(model_id="kroumeliotis/sentiment:df179eef934e986eb88d513262e5e25831d9df89369e42afac7cddbc0358d2af")
# print(LLAMA.llama_ratings(["theres cheaper ones with better fans it has extremely low fan speed does heat tho", "works fine good purchase experience works fine good purchase experience"]))


"""
Upload Dataset for GPT Fine-tuning
SOS Now you can upload the training dataset along with validation using OpenAI's graphical interface
"""
# GPT = GPTmethods()

# Upload train-data-gpt-50.jsonl file
# file_id = GPT.upload_file(dataset="datasets/train-data-gpt-50.jsonl").id
# print(file_id)

# Upload train-data-gpt-100.jsonl file
# file_id = GPT.upload_file(dataset="datasets/train-data-gpt-100.jsonl").id
# print(file_id)
"""
Train GPT Model
"""
# Train GPT Model using the train-data-gpt-50.jsonl
# file_id = "file-j8qxeLfVbyU3fb86Q6F7VmC3"
# train_id = GPT.train_gpt(file_id).id
# print(train_id)

# Train GPT Model using the train-data-gpt-100.jsonl
# file_id = "file-4DeHbaacd2bDZTcYTaY9fnPt"
# train_id = GPT.train_gpt(file_id).id
# print(train_id)