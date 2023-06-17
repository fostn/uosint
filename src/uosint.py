from .api import InstagramAPI
from .chatgpt import Chatgbt
from.download import Download
from tabulate import tabulate
import re
import datetime
import time
class Uosint:
	def __init__(self):
		self.api = InstagramAPI()
		self.api.authenticate_user()
		self.Chatgbt = Chatgbt()
		self.Download = Download()
	def extract_email(self,text):
		pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
		matches = re.findall(pattern, str(text).replace(' ',''))
		return matches
	def extract_website_urls(self,text):
		url_pattern = r'\b(?:https?://|www\.)\S+\b'
		urls = re.findall(url_pattern, text)
		return urls
	def extract_phone_numbers(self,text):
		pattern = r'\b(?:\+?\d{1,3}[-.●\s]?)?\(?\d{3}\)?[-.●\s]?\d{3,4}[-.●\s]?\d{4}\b'
		matches = re.findall(pattern, str(text).replace(' ',''))
		return matches
	def get_followers(self,target):
		table_data = []
		users = self.api.get_followers(target)
		if users is None:
			return
		if "Account Private" in str(users) :
			exit("Account Private")
		
		for user in users:
			username = user.get('username')
			user_id = user.get('pk')
			full_name = user.get('full_name')
			is_private = user.get('is_private')
			is_verified = user.get('is_verified')
			table_data.append([username, user_id, full_name, is_private, is_verified])

		headers = ["Username", "ID", "Full Name", "private", "verified"]
		print(tabulate(table_data, headers=headers, tablefmt="grid"))
	def get_following(self,target):
		table_data = []
		users = self.api.get_following(target)
		if users is None:
			exit('username not found') 
		if "Account Private" in str(users) :
			exit("Account Private")
		for user in users:
			username = user.get('username')
			user_id = user.get('pk')
			full_name = user.get('full_name')
			is_private = user.get('is_private')
			is_verified = user.get('is_verified')
			table_data.append([username, user_id, full_name, is_private, is_verified])

		headers = ["Username", "ID", "Full Name", "private", "verified"]
		print(tabulate(table_data, headers=headers, tablefmt="grid"))
	def get_user_info(self,username):
		info = self.api.get_user_info(username)
		if info is None:
			exit('username not found')
		user_table = [
		['Username', info.get("username")],
		['Full Name', info.get("full_name")],
		['ID', info.get("pk")],
		['Followers Count', info.get("follower_count")],
		['Following Count', info.get("following_count")],
		['Media Count', info.get("media_count")],
		['Bio', info.get("biography")],
		['Account Date', self.api.date_joind(username)],
		['Is Private', info.get("is_private")],
		['Is Verified', info.get("is_verified")],
		['Is Business', info.get("is_business")],
		['Extracted Emails', self.extract_email(info['biography'])],
		['Extracted Phone Numbers', self.extract_phone_numbers(info['biography'])],
		['Extracted Urls', self.extract_website_urls(info['biography'])],
		]

		print(tabulate(user_table, tablefmt='plain'))



	def get_posts(self,username):
		posts = self.api.get_posts(username)
		if posts is None:
			exit('username not found')
		if "Account Private" in posts :
			exit("Account Private")
		max_length = 60
		max_words = 5
		user_posts = []
		for index, post in enumerate(posts, 1):
			date = datetime.datetime.fromtimestamp(post.get('taken_at'))
			id = post.get("pk")
			like_count = post.get("like_count")
			if "caption" not in str(posts):
				caption = ""
			else:
				caption = post.get("caption", {}).get("text", "")
			caption = caption.replace('\n', '')
			media_type = post.get("media_type")
			if media_type == 1:
				media_type = "Photo"
			elif media_type == 2:
					media_type = "Video"
			if len(caption) > max_length:
				caption = caption[:max_length] + u"\u2026"

			    # Fix Arabic text reversal
			if any('\u0600' <= c <= '\u06FF' for c in caption):
				caption = caption[::-1]
			words = caption.split()
			caption = ' '.join(words[:max_words])
			

			user_posts.append([index,date.strftime('%Y-%m-%d %H:%M:%S'), id, like_count, caption,media_type])
		headers = ["Post","Date", "ID", "Like Count", "Caption","type"]
		print(tabulate(user_posts, headers=headers ,tablefmt='grid'))
	def get_comments(self,username):
		max_length = 60
		max_words = 6
		data = self.api.get_posts(username)
		if data is None:
			exit("username not found")
		if "Account Private" in data :
			exit("Account Private")
		user_comments = []
		for index, comment in enumerate(data, 1):
			caption = comment.get("caption")
			if caption:
				created_at = date = datetime.datetime.fromtimestamp(caption.get("created_at"))
				text = caption.get("text")
				text = text.replace('\n', '')
				if len(text) > max_length:
					text = text[:max_length] + u"\u2026"

					# Fix Arabic text reversal
				if any('\u0600' <= c <= '\u06FF' for c in text):
					text = text[::-1]
				words = text.split()
				text = ' '.join(words[:max_words])
				user_comments.append([index,created_at,text])
		headers = ["Comment","Created At","Content"]
		if user_comments:
			print(tabulate(user_comments, headers=headers ,tablefmt='grid'))
		else:
			exit("No Comments found")
	def get_posts_comments(self,username):
		posts = self.api.get_posts(username)
		if posts is None:
			exit("username not found")
		if "Account Private" in posts :
			exit("Account Private")
		for post in posts:
			rows = []
			post_id = post.get("pk")
			comments = self.api.get_post_comments(post_id)
			time.sleep(2)
			if comments is None:
				return []
			post_info = [
				["Post ID",post_id,"Comments"]
			]
			print("-"*40)
			print(tabulate(post_info,tablefmt='plain'))
			
			for comment in comments:
				date = datetime.datetime.fromtimestamp(comment.get('created_at'))
				date.strftime('%Y-%m-%d %H:%M:%S')
				username = comment['user']['username']
				text = comment['text']
				rows.append([date, username, text])
			headers = ['date', 'owner', 'text']

			print(tabulate(rows, headers=headers,tablefmt='plain'))
			print("-"*40)
	def get_fwersemail(self,username):
		data = self.api.get_followers(username)
		if data is None:
			exit("username not found")
		if "Account Private" in data :
			exit("Account Private")
		table = [
				["Username","Extracted Emails"]
			]
		print(tabulate(table,tablefmt='plain'))
		for users in data:
			username = users["username"]
			info = self.api.get_user_info(username) 
			bio = info.get("biography")
			print(username,':',self.extract_email(str(bio)))
			time.sleep(1)
   
   
	def get_fwingsemail(self,username):
		data = self.api.get_following(username)
		if data is None:
			exit("username not found")
		if "Account Private" in data :
			exit("Account Private")
		table = [
				["Username","Extracted Emails"]
			]
		print(tabulate(table,tablefmt='plain'))
		for users in data:
			username = users["username"]
			info = self.api.get_user_info(username) 
			bio = info.get("biography")
			print(username,':',self.extract_email(str(bio)))
			time.sleep(1)
	def get_fwersnumber(self,username):
			data = self.api.get_followers(username)
			if data is None:
				exit("username not found")
			if "Account Private" in data :
				exit("Account Private")
			table = [
					["Username","Extracted Phone Numbers"]
				]
			print(tabulate(table,tablefmt='plain'))
			for users in data:
				username = users["username"]
				info = self.api.get_user_info(username) 
				bio = info.get("biography")
				print(username,':',self.extract_phone_numbers(str(bio)))
				time.sleep(1)
	def get_fwingsnumber(self,username):
			data = self.api.get_following(username)
			if data is None:
				exit("username not found")
			if "Account Private" in data :
				exit("Account Private")
			table = [
					["Username","Extracted Phone Numbers"]
				]
			print(tabulate(table,tablefmt='plain'))
			for users in data:
				username = users["username"]
				info = self.api.get_user_info(username) 
				bio = info.get("biography")
				print(bio)
				print(username,':',self.extract_phone_numbers(str(bio)))
				time.sleep(1)
	def find_sensitive_data(self,data):
		if isinstance(data, str):
			# Convert single text input to a list
			data = [data]
		found_sensitive_data = False
		for item in data:
			message = f"if there is sensitive data in this text tell me, only reply yes or no text = '{item}'"
			response = self.Chatgbt.send_message(message)
			if "yes" in str(response).lower():
				print(f"sensitive: {item}")
				found_sensitive_data = True
			else:
				print(f"unsensitive : {item}")
		if not found_sensitive_data:
			print("No sensitive data found".upper())
	def get_sensitive_comments(self, username):
		user_comments = []
		data = self.api.get_posts(username)
		
		if data is None:
			exit("Username not found")
			
		if "Account Private" in data:
			exit("Account Private")
		print("searching for sensitive data in user comments...")
		for comment in data:
			caption = comment.get("caption")
			if caption:
				text = caption.get("text")
				user_comments.append(text)
		
		if user_comments:
			table = [
					["Status",'   ','	',' ',"Comment"]
				]
			print(tabulate(table,tablefmt='plain'))
			self.find_sensitive_data(user_comments)
		else:
			print("No comments found")
	def download_posts(self,username):
		self.Download.posts(username)
  
	def download_stories(self,username):
		self.Download.stories(username)
  
