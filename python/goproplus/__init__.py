import urllib.request
import re
import json
import sys
import requests

class plus:
	def __init__(self, email, password):
		if sys.version_info[0] < 3:
			print("Python 3 is needed.")
			exit()
		# Constants:
		self.GOPRO_API_ENDPOINT = "https://api.gopro.com"
		self.GOPRO_API_OAUTH2_TOKEN = "https://api.gopro.com/v1/oauth2/token"
		self.GOPRO_API_GET_MEDIA = "https://api.gopro.com/media/search"
		self.GOPRO_API_CLIENT_ID = "71611e67ea968cfacf45e2b6936c81156fcf5dbe553a2bf2d342da1562d05f46"
		self.GOPRO_API_CLIENT_SECRET = "3863c9b438c07b82f39ab3eeeef9c24fefa50c6856253e3f1d37e0e3b1ead68d"
		
		self.USER_EMAIL = email
		self.USER_PASSWORD = password
		
	def getToken(self):
		data = {
			"client_id": self.GOPRO_API_CLIENT_ID,
			"client_secret": self.GOPRO_API_CLIENT_SECRET,
			"grant_type": "password",
			"scope": "root root:channels public me upload media_library_beta live",
			"username": self.USER_EMAIL,
			"password": self.USER_PASSWORD
		}
		data_encoded = urllib.parse.urlencode(data).encode("utf-8")
		response = urllib.request.urlopen(self.GOPRO_API_OAUTH2_TOKEN, data_encoded).read()
		jsonResponse = json.loads(response)
		return jsonResponse["access_token"]
	def getMediaList(self):
		headers = {
			'Accept-Charset': 'utf-8',
			'Accept': 'application/vnd.gopro.jk.media+json; version=2.0.0',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + self.getToken()
		}
		url = self.GOPRO_API_GET_MEDIA + "?fields=captured_at,content_title,content_type,created_at,gopro_user_id,file_size,id,token,type,resolution,filename,file_extension"
		request = urllib.request.Request(url, headers=headers)
		resp = urllib.request.urlopen(request)
		content = resp.read()
		print(content)
	def test(self):
		url = "%s/media/search" % self.GOPRO_API_ENDPOINT
		token = self.getToken()
		params = {'fields': 'id,filename,file_extension'}
		headers = {
			'Accept-Charset': 'utf-8',
			'Accept': 'application/vnd.gopro.jk.media+json; version=2.0.0',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer %s' % token
		}
		response = requests.get(url, params=params, headers=headers)
		response.raise_for_status()
		print(response.json())