# This file is testing purpose

from flask import Flask, redirect, request

app = Flask(__name__)

# Set your client ID and redirect URI
client_id = '702026008809922'
redirect_uri = 'http://127.0.0.1:5000/callback/'

@app.route('/login')
def login():
    # Generate the Instagram login URL
    login_url = f'https://api.instagram.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    
    # Redirect the user to the Instagram login page
    return redirect(login_url)

@app.route('/callback')
def callback():
    # Get the authorization code from the callback URL
    authorization_code = request.args.get('code')
    
    # Process the authorization code and obtain the access token
    # Add your code here to exchange the authorization code for an access token
    
    # Redirect the user to a success page or perform further actions
    return redirect('/success')

if __name__ == '__main__':
    app.run()





























# import requests
# import facebook as fb

# # Your Access Keys
# page_id = 219862181207340
# access_token = 'EAAK4EHZAfxuQBOZBOjK0nqxtW8GP0BfR0HmeXSGB28NHVnDFALhiZA6Cjs0aXkrokp7CTtDvslVfUVpVxI5FJcMqcCjPYp0pTonbnmoHVuR1nNqvWZB6lIZACqWjpF9vJjFEW0MZBhsP4YMeVp4SPTtCmVnqT2EhrxKZAk2C8Apw0ZCesNwJ0nsTgoXKZCz19iQHax596GDIKsZCNnEhZCexGvuENFOuzCt8f2TbmFyGoX1slQ4kQmf5KY4ZCrU3ZBmgh'

# # Use your user access token to obtain a page access token
# graph = fb.GraphAPI(access_token=access_token, version='3.0')
# page_info = graph.get_object(f'/{page_id}?fields=access_token')
# page_access_token = page_info.get('access_token')

# # Now use page_access_token for posting
# post_url = f'https://graph.facebook.com/{page_id}/feed'
# response = requests.post(post_url, params={'message': "hey guys I will updated you about fastapi new trends.", 'access_token': page_access_token})

# if response.status_code == 200:
#     print("Post successfully created!")
# else:
#     print(response.text)
#     print("Error creating the post.")



# import requests

# def post_photo(access_token, image_url, caption):
#     url = f"https://graph.instagram.com/me/media"

#     # Parameters for the POST request
#     params = {
#         "access_token": access_token,
#         "image_url": image_url,
#         "caption": caption
#     }
#     try:
#         response = requests.post(url, data=params)
#         if response.status_code == 200:
#             print("Photo posted successfully!")
#         else:
#             print(f"Error posting photo: {response.json()}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage
# access_token = "EAAGIksWmAjgBOyF9x05Rm3IHNZAWuJlTPnLAwVjlZCBB9KaEfP0lZBmFHnENEIrMO7nTzovJ3MJfkZCnnPaJY8ssp3bqtUAdJlyJF2VsQa4NJj5hZAcUydZBxl71I9nisTbIaATMGgIgzjqZBUY7JMbH9210ogfzNl2ShOPCljWknQCqiZBzgbhFh0hcU2aSJZAsavqJ6DvGyIr2PiK7woto4i9jwELHCUOoHjh2gGQwAK4vyjwDpIgXbtKj6olFJeAZDZD"
# image_url = "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg"
# caption = "Your caption here"

# post_photo(access_token, image_url, caption)

