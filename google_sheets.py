"""
Інтеграція з Google Sheets для PrometeyLabs Bot
"""
import os
import json
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

logger = logging.getLogger(__name__)

# Якщо змінюються ці області, видаліть файл token.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_google_sheets_service():
    """Отримання сервісу Google Sheets"""
    creds = None
    
    # Файл token.json зберігає токени доступу користувача
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Якщо немає валідних креденшлів, запитуємо користувача авторизуватися
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Зберігаємо креденшлі для наступного запуску
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        return service
    except HttpError as error:
        logger.error(f'Помилка при створенні сервісу: {error}')
        return None

def read_sheet_data(spreadsheet_id, range_name):
    """Читання даних з Google Sheets"""
    try:
        service = get_google_sheets_service()
        if not service:
            return None
            
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        return values
        
    except HttpError as error:
        logger.error(f'Помилка при читанні даних: {error}')
        return None

def get_client_projects(client_id):
    """Отримання проектів клієнта з Google Sheets"""
    if not config.GOOGLE_SHEETS_ID:
        return []
    
    range_name = 'Projects!A:Z'  # Припускаємо, що проекти в аркуші Projects
    data = read_sheet_data(config.GOOGLE_SHEETS_ID, range_name)
    
    if not data:
        return []
    
    # Перший рядок - заголовки
    headers = data[0]
    projects = []
    
    for row in data[1:]:
        if len(row) > 0 and str(row[0]) == str(client_id):
            project = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    project[header] = row[i]
            projects.append(project)
    
    return projects

def get_client_payments(client_id):
    """Отримання платежів клієнта з Google Sheets"""
    if not config.GOOGLE_SHEETS_ID:
        return []
    
    range_name = 'Payments!A:Z'  # Припускаємо, що платежі в аркуші Payments
    data = read_sheet_data(config.GOOGLE_SHEETS_ID, range_name)
    
    if not data:
        return []
    
    # Перший рядок - заголовки
    headers = data[0]
    payments = []
    
    for row in data[1:]:
        if len(row) > 0 and str(row[0]) == str(client_id):
            payment = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    payment[header] = row[i]
            payments.append(payment)
    
    return payments

def get_client_statistics(client_id):
    """Отримання статистики клієнта з Google Sheets"""
    if not config.GOOGLE_SHEETS_ID:
        return {}
    
    range_name = 'Statistics!A:Z'  # Припускаємо, що статистика в аркуші Statistics
    data = read_sheet_data(config.GOOGLE_SHEETS_ID, range_name)
    
    if not data:
        return {}
    
    # Перший рядок - заголовки
    headers = data[0]
    statistics = {}
    
    for row in data[1:]:
        if len(row) > 0 and str(row[0]) == str(client_id):
            for i, header in enumerate(headers):
                if i < len(row):
                    statistics[header] = row[i]
            break
    
    return statistics
