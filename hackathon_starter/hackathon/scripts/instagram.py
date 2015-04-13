import requests
import urllib
import urllib2
import json
import simplejson as json2

authorization_url = 'https://api.instagram.com/oauth/authorize/?client_id='
access_token_url = 'https://api.instagram.com/oauth/access_token'

class InstagramOauthClient(object):

	access_token = None
	user_data = None

	def __init__(self, client_id, client_secret):
		self.client_id 		= client_id
		self.client_secret 	= client_secret


	def get_authorize_url(self):
		''' Obtains the authorization url. '''
		auth_url = authorization_url + self.client_id +'&redirect_uri=http://localhost:8000/hackathon/instagram&response_type=code'
		return auth_url

	def get_access_token(self, code):
		''' Obtains access token. '''

		auth_setting = {'client_id': self.client_id,
						'client_secret': self.client_secret,
						'grant_type': 'authorization_code',
						'redirect_uri': 'http://localhost:8000/hackathon/instagram',
						'code': code
						}

		auth_setting_url =  urllib.urlencode(auth_setting)
		req  = urllib2.Request(access_token_url, auth_setting_url)
		content = urllib2.urlopen(req)
		jsonlist = json.load(content)
		self.access_token = jsonlist['access_token']
		self.user_data = jsonlist['user']
		print self.user_data
		#print self.access_token


	def get_tagged_media(self, tag):
		''' Get recent tagged media. '''
		tagged_media_url = 'https://api.instagram.com/v1/tags/'+tag+'/media/recent?access_token='+self.access_token# +'&count=2'
		req = requests.get(tagged_media_url)
		content = json2.loads(req.content)
		data = content['data']

		while len(data) <= 100:
			next_url= content['pagination']['next_url']
			req = requests.get(next_url)
			content = json2.loads(req.content)
			for i in content['data']:
				data.append(i)
		print len(data)
		return data

	def get_user_info(self, access_token):
		user_info = 'https://api.instagram.com/v1/users/32833691/?access_token='+access_token
		req = requests.get(user_info)
		content = json2.loads(req.content)
		data = content['data']
		return data


