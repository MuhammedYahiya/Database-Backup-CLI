# Database Backup CLI

## About

**Database Backup CLI** is a command-line tool designed to help you easily back up and restore databases such as **MySQL**, **PostgreSQL**, **MongoDB**, and **SQLite**.

It supports features like full, incremental, and differential backups, compression of backup files, local and cloud storage options (AWS S3, Google Cloud Storage, Azure), and automated scheduling.

With a simple and user-friendly interface, Database Backup CLI ensures your data is securely backed up and easily recoverable whenever needed.

---

## Features (Current Progress)

- ✅ Test connection to a MySQL database via CLI prompts
- ✅ Prompt for Host, Port, Username, Password, Database name
- ✅ Secure password entry (hidden input for security)
- ✅ Perform a **full database backup** for MySQL
- ✅ Store backup to:
  - Local Storage (as a `.zip` file)
  - Google Cloud Storage
  - AWS S3
  - Both Local and Cloud (Google or AWS)
- 🚧 Restore functionality - Google/AWS (Coming soon)
- 🚧 Compression improvements and options (Coming soon)
- 🚧 Support for PostgreSQL, MongoDB, SQLite (Coming soon)
- 🚧 Automated scheduling of backups (Coming soon)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/db-backup-cli.git
cd db-backup-cli

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Backup MySQL Database

```bash
python3 cli.py backup
```

You will be prompted to enter:
- Database connection details
- Backup file name (without extension)
- Where to store the backup (Local / Cloud (Google or AWS)/ Both)

Backups are saved in the `backups/mysql` directory and uploaded to your configured Google Cloud Storage bucket if selected.

> **Note:** Set your Google Cloud bucket name in the `.env` file:

```bash
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
GOOGLE_CLOUD_BUCKET=your-bucket-name
AWS_ACCESS_KEY=your-access-key-id
AWS_SECRET_KEY=your-secret-access-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-s3-bucket-name
```

Also, ensure your environment has access to Google Cloud credentials (`GOOGLE_APPLICATION_CREDENTIALS` env variable if required).

---

###Restore MySQL Backup

```bash
python3 cli.py restore
```
---

## Upcoming Features

- Restore from backup files(Googel Cloud / AWS S3)
- Incremental and differential backup support
- PostgreSQL, MongoDB, and SQLite support
- AWS S3 and Azure Storage integration
- Backup scheduling (daily, weekly, custom)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

