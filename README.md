# backup-googledrive
# MySQL Database Backup and Upload Script

This Python script automates the backup of a MySQL database and uploads it to Google Drive using the Google Drive API. It schedules daily backups at 5 PM and logs backup activities. The script is configured with dummy values for sensitive information.

## Features

- **Automated Backup:** The script automatically backs up MySQL databases at the scheduled time.
- **Google Drive Upload:** Backups are uploaded to Google Drive using the Google Drive API for safekeeping.
- **Scheduling:** Daily backups are scheduled to run at 5 PM.
- **Logging:** Backup activities and errors are logged for monitoring and troubleshooting.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
  git clone [https://github.com/Shivi0428/backup-googledrive]

2. Install the dependencies:
  pip install -r requirements.txt

## Configuration

1. Obtain a service account key file (`service_account.json`) for Google Drive API access.
2. Replace the placeholder values in the script with your actual details:
- `SERVICE_ACCOUNT_FILE`: Path to the service account key file.
- `BACKUP_FOLDER`: Local folder path for storing backups.
- `GOOGLE_DRIVE_FOLDER_ID`: Google Drive folder ID for storing backups.
- `DATABASES`: List of MySQL databases to backup.
- `MYSQLDUMP_PATH`: Path to the `mysqldump` executable.

## Usage

Run the script:
  python backup_script.py
## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.
