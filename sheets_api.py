
import requests
import urllib


class SheetsApi():

	def __init__(self, api_key, sheet_id):
		self.api_key = api_key
		self.sheet_id = sheet_id
		
	def send_request(self, path, param):
		if not param:
			param = {}
		param["key"] = self.api_key
		url = "https://sheets.googleapis.com/v4/spreadsheets/" + urllib.parse.quote(self.sheet_id) + path + "?" + urllib.parse.urlencode(param, True)
		response = requests.get(url)
		if response.status_code != 200:
			print("BAD STATUS: ", response, response.content)
			return
		return response.json()
		
	def get_values(self, ranges):
		param = {
			"ranges": ranges,
		}
		return self.send_request("/values:batchGet", param)
		