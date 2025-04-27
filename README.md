# Database Backup CLI

## About

Database Backup CLI is a command-line tool designed to help you easily back up and restore databases such as MySQL, PostgreSQL, MongoDB, and SQLite.

It supports features like full, incremental, and differential backups, compression of backup files, local and cloud storage options (AWS S3, Google Cloud Storage, Azure), and automated scheduling.

With a simple and user-friendly interface, Database Backup CLI ensures your data is securely backed up and easily recoverable whenever needed.

---

## Features (Current Progress)

- ✅ Test connection to a MySQL database via CLI prompts
- ✅ Prompt for Host, Port, Username, Password, Database name
- ✅ Password input hidden for security
- 🚧 Backup, Restore, and other DBMS support (Coming soon)

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/db-backup-cli.git
cd db-backup-cli
pip install -r requirements.txt
