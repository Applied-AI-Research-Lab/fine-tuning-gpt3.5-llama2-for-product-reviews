from flask import Flask, request
from sentiment_files.DBmethods import DBmethods

DB = DBmethods('sentiment_files/database.db')  # Instantiate DBmethods class


# Main Function
def sentiment_product_main():
    product_code = ''
    product_title = ''
    product_description = ''
    product_reviews = ''
    product_category = ''
    if request.method == 'GET':
        # Handle GET request & Access the query parameters
        product_code = request.args.get('code', '')
        product_title = request.args.get('title', '')
        product_description = request.args.get('description', '')
        product_reviews = request.args.get('reviews', '')
        product_category = request.args.get('category', '')
    elif request.method == 'POST':
        # Handle POST request & Access the query parameters
        data = request.get_json()
        product_code = data.get('code', '')
        product_title = data.get('title', '')
        product_description = data.get('description', '')
        product_reviews = data.get('reviews', '')
        product_category = data.get('category', '')

    # Check if there is product with the same product_code
    code_exists = DB.select_query("SELECT * FROM products WHERE product_code= ? LIMIT 1", [product_code])
    if code_exists['status'] is False:
        # Insert product
        ins_product = DB.insert_query(
            "INSERT OR IGNORE INTO products (product_code, product_title, product_description, product_category) VALUES (?, ?, ?, ?)",
            [product_code, product_title, product_description, product_category])
        if ins_product['status']:

            count_reviews_test = []
            # ins_product['data'] is the product id
            for review in product_reviews:
                # if the review rating is integer >=1 and <=5
                if 'rating' in review and review['rating'].isnumeric():
                    rating = int(review['rating'])
                    if 1 <= rating <= 5:
                        # Insert review
                        # Check if the review is already inserted for this specific product
                        review_exists = DB.select_query(
                            "SELECT * FROM products INNER JOIN reviews on reviews.product_id=products.product_id WHERE product_code= ? AND (review_title = ? OR review_body = ?) LIMIT 1",
                            [product_code, review['title'], review['body']])
                        if review_exists['status'] is False:
                            count_reviews_test.append(review)
                            ins_review = DB.insert_query(
                                "INSERT OR IGNORE INTO reviews (product_id, review_rating, review_title, review_body, before_gpt, before_llama, after_gpt, after_llama, rating_type, review_extra) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                [ins_product['data'], review['rating'], review['title'], review['body'], 0, 0, 0, 0,
                                 '', ''])
                            if not ins_review['status']:
                                return {'status': False, 'data': ins_review['data']}
            # If success show a message
            return {'status': True, 'data': ins_product['data']}
        else:
            return {'status': False, 'data': ins_product['data']}
    else:
        return {'status': False, 'data': 'Product already exists'}