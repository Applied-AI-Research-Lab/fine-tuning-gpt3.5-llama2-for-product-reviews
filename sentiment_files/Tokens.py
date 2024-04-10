import tiktoken
from DBmethods import DBmethods

# Use the TikToken Library to count tokens
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    # https://github.com/openai/tiktoken/tree/main
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Use the TikToken Library to count tokens per review and update review_extra
def count_token_reviews():
    # Test Tokens: 13128
    # Train Tokens: 53359
    # GPT Model Run. Input: $0.0015 / 1K tokens Output: $0.002 / 1K tokens (13128/1000)*0.0015=0.019$
    # GPT Model Fine-Tuning. Training: $0.0080 / 1K tokens Input: $0.0120 / 1K tokens, Output: $0.0160 / 1K tokens (53359/1000)*0.008=1314$
    DB = DBmethods('datasets/database.db')
    data_dict = DB.select_query(
        "SELECT review_id, review_title, review_body FROM reviews",[])
    if data_dict['status']:
        for review in data_dict['data']:
            review_id = review['review_id']
            review_title = review['review_title']
            review_body = review['review_body']
            review_sum = DB.preprocess_text(review_title + ' ' + review_body)
            tokens = num_tokens_from_string(review_sum, "cl100k_base")
            update = DB.update_query("UPDATE reviews SET tokens = ? WHERE review_id=?", [tokens, review_id])
            if update['status'] == False:
                return update
    else:
        print('error')