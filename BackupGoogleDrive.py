import os
import subprocess
from datetime import datetime
from time import sleep
import schedule
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import logging

# Configure logging
LOG_FILE = 'backup_script.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Replace with your details
SERVICE_ACCOUNT_FILE = '/path/to/service_account.json'
BACKUP_FOLDER = 'DummyBackupFolder'
GOOGLE_DRIVE_FOLDER_ID = 'DummyFolderID'


DATABASES = ['dummy_database']
MYSQLDUMP_PATH = '/path/to/mysqldump.exe'
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_authenticated_service():
    """Authenticates with Google Drive API."""
    logging.debug("Authenticating with Google Drive API.")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    service = build('drive', 'v3', http=credentials.authorize(Http()))
    logging.debug("Authenticated successfully.")
    return service

def upload_to_drive(service, filename):
    """Uploads a file to the specified Google Drive folder."""
    media_body = MediaFileUpload(filename)
    body = {'name': os.path.basename(filename), 'parents': [GOOGLE_DRIVE_FOLDER_ID]}
    service.files().create(body=body, media_body=media_body).execute()
    logging.info(f"Uploaded '{filename}' to Google Drive.")

def backup_database():
    """Backups a database and uploads it to Google Drive."""
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{DATABASES[0]}_{timestamp}.sql"
        filepath = os.path.join(BACKUP_FOLDER, filename)

        # Replace with your specific database backup command
        process = subprocess.run([
            MYSQLDUMP_PATH,
            '-u', 'dummy_username', '-pdummy_password', '-h', 'dummy_host', DATABASES[0]
        ], capture_output=True, text=True)

        if process.returncode == 0:
            with open(filepath, 'w') as file:
                file.write(process.stdout)
            logging.info(f"Database '{DATABASES[0]}' backed up to {filepath}")

            service = get_authenticated_service()
            upload_to_drive(service, filepath)
        else:
            logging.error(f"Error backing up database {DATABASES[0]}: {process.stderr}")
    except Exception as e:
        logging.error(f"An error occurred during backup: {e}")

def run_backup():
    """Runs the backup process for all databases."""
    logging.info("Running scheduled backup.")
    for database in DATABASES:
        backup_database()

def schedule_backup():
    """Schedules the backup task to run daily at 5 PM."""
    logging.debug("Scheduling backup task to run daily at 5 PM.")
    schedule.every().day.at("17:00").do(run_backup)

    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    # Create the backup folder if it doesn't exist
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    schedule_backup()
    logging.info("Backup script started. Scheduled tasks will run in the background.")
