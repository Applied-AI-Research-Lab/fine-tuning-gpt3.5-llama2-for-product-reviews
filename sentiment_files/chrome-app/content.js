$(document).ready(function () {
    // Get the URL from the user's browser
    const currentURL = window.location.href;

    /**
     * Extract Reviews from a Marketplace
     * @returns {Promise<*[]>}
     */
    async function extractReviews() {
        let productId = extractProductId(currentURL); // Get the product URL
        // const stars = ['one_star', 'two_star', 'three_star', 'four_star', 'five_star'];
        const stars = ['one', 'two', 'three', 'four', 'five'];

        // Create an array to store the promises returned by extractReviewsNew
        const promises = stars.map(star => {
            // let url = 'https://www.amazon.com/product-reviews/' + productId + '/ie=UTF8&filterByStar=' + star + '&reviewerType=all_reviews';
            let url = 'https://www.amazon.com/product-reviews/' + productId + '/ie=UTF8&filterByStar=' + star + '_star/ref=cm_cr_unknown?filterByStar=' + star + '_star&pageNumber=1';
            return extractReviewsDom(url);
        });

        // Wait for all the promises to resolve
        const reviewsArray = await Promise.all(promises);

        // Concatenate all the reviews into a single array
        let reviews = [];
        reviewsArray.forEach(result => {
            if (result.status) {
                reviews = reviews.concat(result.data);
            }
        });

        return reviews;
    }

    /**
     * Extract reviews from dom
     * @param url
     * @returns {Promise<{data: {rating: *|string, title: string, body: string}[], status: boolean} | {data: string, error: *, status: boolean}>}
     */
    function extractReviewsDom(url) {
        return fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                // Extract reviews
                const reviewElements = doc.querySelectorAll('[data-hook="review"]');
                const reviews = Array.from(reviewElements).map(reviewElement => {
                    const ratingElement = reviewElement.querySelector('[data-hook="review-star-rating"]');
                    const rating = ratingElement ? ratingElement.getAttribute('class').match(/\d+/)[0] : '';
                    const titleElement = reviewElement.querySelector('[data-hook="review-title"]');
                    const title = titleElement ? titleElement.textContent.trim() : '';
                    const bodyElement = reviewElement.querySelector('[data-hook="review-body"]');
                    const body = bodyElement ? bodyElement.textContent.trim() : '';
                    return {rating, title, body};
                });

                return {'status': true, 'data': reviews};
            })
            .catch(error => {
                return {'status': false, 'data': 'Error:', error};
            });
    }

    /**
     * Get product data
     * @returns {Promise<{data: string, status: boolean}|boolean>}
     */
    async function getProductData() {
        try {
            if (checkURLContainsDP(currentURL) === false) {
                return {'status': false, 'data': 'Not a product page'};
            }
            const productId = extractProductId(currentURL); // Get the product URL
            const title = $('#productTitle').text().trim();
            const description = $('#productDescription').text().trim();
            let reviews = await extractReviews();
            let firstCategory = $(".a-unordered-list a:first");
            let category = firstCategory.text().trim();
            reviews = cleanReviews(reviews);
            if (title === '' || reviews.length === 0 || category === '') {
                return false;
            }
            console.log([productId, title, description, reviews, category]);

            // Post Request Product Data to PythonAnywhere Server
            $.ajax({
                url: 'http://127.0.0.1:5000/sentiment', // define the url
                type: 'POST', // define the request method as POST
                data: JSON.stringify({
                    project: 'sentiment',
                    code: productId,
                    title: title,
                    description: description,
                    reviews: reviews,
                    category: category
                }), // define the post data
                contentType: "application/json; charset=utf-8",
                success: function (message) { // on success
                    if (message.status) {
                        $('<h1 style="color:green">' + message.data + '</h1>').insertBefore('#title');
                    } else {
                        $('<h1 style="color:red">' + message.data + '</h1>').insertBefore('#title');
                    }
                    return message;
                }, error: function (jqXHR, textStatus, errorThrown) {
                    return 'Error:' + textStatus + errorThrown;
                }
            });

        } catch (error) {
            console.error(error);
        }
    }

    // Call the async function
    getProductData();

    /**
     * Clean title and body from \n and spaces
     * @param reviews
     * @returns {*[]}
     */
    function cleanReviews(reviews) {
        const reviews_c = [];
        Object.entries(reviews).forEach(([key, value]) => {
            let title = value.title;
            title = title.replace(/[\n\r]/g, ''); // remove \ns
            title = title.replace(/^\s+/, ''); // or trimLeft() remove spaces from the beginning
            title = title.replace(/\s+$/, ''); //  remove spaces from the end
            title = title.replace(/1\.0 out of 5 stars\s+/i, '');
            title = title.replace(/2\.0 out of 5 stars\s+/i, '');
            title = title.replace(/3\.0 out of 5 stars\s+/i, '');
            title = title.replace(/4\.0 out of 5 stars\s+/i, '');
            title = title.replace(/5\.0 out of 5 stars\s+/i, '');
            let body = value.body;
            body = body.replace(/[\n\r]/g, '');
            body = body.replace(/^\s+/, ''); // or trimLeft() remove spaces in the beginning
            body = body.replace(/\s+$/, ''); //  remove spaces from the end
            let rating = value.rating;
            // if (!Number.isInteger(rating)) { // turn empty ratings to zero. zero means that user has not rated this product
            //     rating = 0;
            // }
            reviews_c.push({'title': title, 'body': body, 'rating': rating});
        });
        return reviews_c;
    }

    /**
     * Check if the URL is a product
     * @param url
     * @returns {boolean}
     */
    function checkURLContainsDP(url) {
        return url.indexOf("/dp/") !== -1;
    }

    /**
     * Extract the product id given the URL
     * @param url
     * @returns {*|null}
     */
    function extractProductId(url) {
        const regex = /\/dp\/([\w]+)/;
        const match = url.match(regex);
        if (match && match.length > 1) {
            return match[1];
        }
        return null;
    }
});
