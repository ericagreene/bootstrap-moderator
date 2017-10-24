import http.client
import datetime, json, random, re, os


# A JWT generated for a service Moderator user
AUTH = os.getenv("MODERATOR_AUTH")

# The URL of the Moderator API
API_URL = os.getenv("MODERATOR_API", "127.0.0.1:8080")

# The number of reviews per category to import into Moderator
REVIEWS_PER_CATEGORY = 100

class moderator_client(object):

    def __init__(self, auth, api_url):
        self.api_url = api_url
        self.__conn = http.client.HTTPConnection(api_url)
        self.__headers = {
            'content-type': "application/json",
            'authorization': auth,
            'cache-control': "no-cache",
        }

    def create_article(self, sourceId, title, text, url, category):
        '''
        Create an article in Moderator using the publisher API.
        '''

        data = {
            "data": [
                {
                    "sourceId": sourceId,

                    "categoryId": category,
                    "title": title,
                    "createdAt": str(datetime.datetime.now()),
                    "text": text,
                    "url": url,
                }
            ]
        }

        payload = json.dumps(data)
        self.__conn.request("POST", "/publisher/articles", payload, self.__headers)

        try:
            print("Adding article", sourceId)

            res = self.__conn.getresponse()

            if res.status != 200:
                print("Received non-200 response from /publisher/articles:", res.status)

            print("Response:", json.loads(res.read()))
            print()

        except Exception as e:
            print("Error calling /publisher/articles:", e)

    def create_comment(self, review_id, product_id, text, author_location, author_name):
        '''
        Create a comment in Moderator using the publisher API.
        '''

        data = {
            "data": [
                {
                    "articleId": product_id,
                    "sourceId": review_id,
                    "authorSourceId": "4",
                    "text": text,
                    "author": {
                        "email": "person@email.com",
                        "location": author_location,
                        "name": author_name,
                        "avatarURL": "www.purple.com",
                    },
                    "createdAt":str(datetime.datetime.now()),
                }
            ]
        }

        payload = json.dumps(data)
        self.__conn.request("POST", "/publisher/comments", payload, self.__headers)

        try:
            print("Adding comment {0} to product {1}".format(review_id, product_id))
            res = self.__conn.getresponse()

            if res.status != 200:
                print("Received non-200 response from /publisher/comments:", res.status)

            print("Response:", json.loads(res.read()))
            print()

        except Exception as e:
            print("Error calling /publisher/comments:", e)


def get_product_title(product_id):
    '''
    Utility method to hit the Amazon website to get the page title of
    the product associated with the specified product_id.

    Returns the product title. If no title is found, we return the title
    "Product - {product_id}".
    '''

    default_title = "Product - {0}".format(product_id)

    headers = {
        'cache-control': "no-cache",
        }

    conn = http.client.HTTPSConnection("www.amazon.com")
    conn.request("GET", "/dp/" + product_id, headers=headers)

    res = conn.getresponse()
    data = res.read()
    text = data.decode("utf-8")

    pattern = re.compile("<title>(.+)</title>")

    m = pattern.search(text)

    if m is None:
        return default_title

    title = m.group(1)
    return title.replace("Amazon.com : ", "").replace("Amazon.com:","")

if __name__ == "__main__":

    review_files = [
        {
            "path": "reviews_Baby.json",
            "category": "Baby"
        },
        {
            "path": "reviews_Video_Games.json",
            "category": "Video Games"
        },
        {
            "path": "reviews_Grocery_and_Gourmet_Food.json",
            "category": "Gourmet Food"
        },
    ]

    moderator = moderator_client(AUTH, API_URL)

    for r in review_files:
        with open(r["path"], 'r') as reviews:
            product_ids =[]

            for i in range(REVIEWS_PER_CATEGORY):
                review = reviews.readline()
                data = json.loads(review)

                review_id = data.get("reviewerID", "")
                reviewer_name = data.get("reviewerName", "")
                review_text = data.get("reviewText", "")
                product_id = data.get("asin", "")

                # create a product
                if product_id not in product_ids:
                    title = get_product_title(product_id)
                    url = "http://www.amazon.com/dp/{}".format(product_id)
                    summary = "Some text."

                    moderator.create_article(product_id, title, summary, url, r["category"])
                    product_ids += [product_id]

                # create a comment
                moderator.create_comment(review_id, product_id, review_text, "USA", reviewer_name)
