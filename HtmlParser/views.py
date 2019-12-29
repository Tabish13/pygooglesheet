from django.http import HttpResponse
from django.http import JsonResponse

from google.oauth2 import service_account

from django.conf import settings
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request





def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")

def HtmlParse(request):
	#if request.method == 'POST':

	#identify the input format @json @csv @googlesheet

	#Fetch KM id from the input formats


	#make API call to the KM for token request cache the token for complete request.


	#make API call to get the FAQ 


	#Fetch the text from the FAQ along with the link
	#Massaging of the text fetched
	
	read_gsheet =  GoogleSheets('14IJw5pOtvRgf-pscySHKdU-1_0TEqlYxDfJ-KUyq-WQ','km')
	
	write_gsheet =  GoogleSheets('14IJw5pOtvRgf-pscySHKdU-1_0TEqlYxDfJ-KUyq-WQ','km')
	#updated_results = write_gsheet.insertRowSheet([["12345"]])
	
	response = JsonResponse({"body":{"data":read_gsheet.getAllRows()},"message":"Success"})
	response.status_code = 200
	return response



class GoogleSheets:
	
	def __init__(self, sheet_id, sheet_range_name, value_input_option = "USER_ENTERED"):
		self.sheet_id = sheet_id
		self.sheet_range_name = sheet_range_name	
		self.value_input_option = value_input_option
		self.google_service_auth()	

	#Set google path in the setting page which should be in the projects folder
	def get_google_config(self):
		#ToDO update this config function to accepts config from some secure location
		with open(getattr(settings, "GOOGLE_CONFIG", None)) as json_data_file:
			data = json.load(json_data_file)
		return data

	'''
		Make auth with the get_google_config method store to instance of the class object for future refrences
		To make get/put/update function call using this auth.
	'''
	def google_service_auth(self):
		SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
		SERVICE_ACCOUNT_FILE = self.get_google_config()		
		credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
		service = build('sheets', 'v4', credentials=credentials)
		# Call the Sheets API
		self.sheet = service.spreadsheets()		

	def getAllRows(self, sheet_range_name= None ):
		SPREADSHEET_ID = self.sheet_id
		RANGE_NAME = sheet_range_name if sheet_range_name else self.sheet_range_name
		result = self.sheet.values().get(spreadsheetId = SPREADSHEET_ID, range=RANGE_NAME).execute()
		#result = sheet.values().batchGet(spreadsheetId=SPREADSHEET_ID,ranges=RANGE_NAME).execute()		
		return result["values"]


	def insertRowSheet(self,  values= None, sheet_range_name = None, value_input_option = None):
		if values:
			SPREADSHEET_ID = self.sheet_id
			RANGE_NAME = sheet_range_name if sheet_range_name else self.sheet_range_name
			value_input_option = value_input_option if value_input_option else self.value_input_option
			body = {
			    'values': values
			}
			try:
				result = self.sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()				
				return result["updates"]
			except Exception as e:
				return False			
		else:
			return False

