import os
import requests
from datetime import datetime
from .api import InstagramAPI

class Download:
    def __init__(self):
        self.InstagramAPI = InstagramAPI()
        self.InstagramAPI.authenticate_user()
        self.token = self.InstagramAPI.bearer_token

    def stories(self, username):
        id = self.InstagramAPI.get_user_id(username)
        base_url = "https://i.instagram.com/api/v1"
        url = f"{base_url}/feed/user/{id}/story/"
        headers = {
            'User-Agent': 'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
            'Authorization': self.token,
        }
        Is_Private = self.InstagramAPI.get_user_info(username).get("is_private")
        if Is_Private:
            exit(f"Account Private [{username}]")
        response = requests.get(url, headers=headers)
        if 'items' not in response.text:
            exit(f"No stories found for [{username}]")
        if response.status_code == 200:
            data = response.json()
            items = data.get('reel', {}).get('items', [])
            print(f"Downloading stories for [{username}]")
            if not os.path.exists(f"stories/{username}"):
                os.makedirs(f"stories/{username}")

            for index, item in enumerate(items, start=1):
                media_type = item.get('media_type')
                if media_type == 2:  # Video
                    story_url = item.get('video_versions', [])[0].get('url')
                    file_ext = 'mp4'
                else:  # Image
                    story_url = item.get('image_versions2', {}).get('candidates', [])[0].get('url')
                    file_ext = 'jpg'

                taken_at_timestamp = item.get('taken_at')
                taken_at_datetime = datetime.fromtimestamp(taken_at_timestamp)
                taken_at_str = taken_at_datetime.strftime("%Y%m%d_%H%M%S")

                file_name = f"story_{taken_at_str}.{file_ext}"
                file_path = os.path.join(f"stories/{username}", file_name)

                # Check if the file already exists
                if os.path.exists(file_path):
                    print(f"Story {taken_at_str} for {username} already downloaded")
                    continue

                with open(file_path, 'wb') as f:
                    story_response = requests.get(story_url, headers=headers)
                    f.write(story_response.content)

                print(f"Downloaded story {taken_at_str} for {username}")

        else:
            print(f"Failed to download stories for {username}")

    def posts(self, username):
        posts = self.InstagramAPI.get_posts(username)
        headers = {
            'User-Agent': 'Instagram 278.0.0.19.115 (iPhone13,3; iOS 14_4; en_SA@calendar=gregorian; en-SA; scale=3.00; 1170x2532; 463736449) AppleWebKit/420+',
            'Authorization': self.token,
        }
        folder_path = f"posts/{username}"

        # Create the folder if it doesn't exist
        if len(posts) < 1:
            exit(f"No posts found for [{username}]")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        print(f"Downloading posts for [{username}]")

        for i, post in enumerate(posts, start=1):
            media_versions = post.get('image_versions2', {}).get('candidates', [])
            if len(media_versions) > 0:
                media_url = media_versions[0].get('url')
                if media_url:
                    file_ext = 'jpg'

                    taken_at_timestamp = post.get('taken_at')
                    taken_at_datetime = datetime.fromtimestamp(taken_at_timestamp)
                    taken_at_str = taken_at_datetime.strftime("%Y%m%d_%H%M%S")

                    file_name = f"post_{taken_at_str}.{file_ext}"
                    file_path = os.path.join(folder_path, file_name)

                    # Check if the file already exists
                    if os.path.exists(file_path):
                        print(f"Post {taken_at_str} for {username} already downloaded")
                        continue

                    # Download the media file
                    response = requests.get(media_url, headers=headers)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as file:
                            file.write(response.content)
                        print(f"Downloaded post {taken_at_str} for {username}")
                    else:
                        pass
                else:
                    pass
            else:
                pass


