import requests

def get_user_by_id(id):
    url = f"https://jsonplaceholder.typicode.com/users/{id}"
    response = requests.get(url)
    return response.json()

def get_all_posts():
    url = f"https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json()

