# PostgreSql Table Backup to S3

This script allows you to back up specified PostgreSQL database tables to Amazon S3 as `.sql` files.

---

## Features
- Backs up specified tables from your PostgreSQL database.
- Saves backups as `.sql` files in the configured S3 bucket.
- Easy-to-use configuration for database and S3 settings.

---

## How to Use

1. **Start Backup Process**  
   Run `backup_start.sh` script to begin the backup process.

   ```bash
   ./backup_start.sh
   ```
2. **Configure Settings**  
   Update `config.ini` file to set your database connection and S3 configurations.

   Example structure for `config.ini`:

   ```ini
   [database]
   host = <your-database-host>
   port = <your-database-port>
   user = <your-database-user>
   password = <your-database-password>
   database = <your-database-name>

   [s3]
   bucket_name = <your-s3-bucket-name>
   bucket_backup_path = <your-s3-backup-path>
   region = <your-s3-bucket-region>
   access_key = <your-iam-access_key>
   secret_key = <your-s3-iam-secret_key>
   destination_file = <your-s3-destination_file>
   ```
   
3. **Specify Tables to Back Up**  
   List the names of the tables you want to back up in the `tables_name.txt` file, one table name per line.

4. **Notes**  
   - Ensure the `config.ini` is properly configured for both the database and S3 settings before starting the backup.
   - Double-check the `tables_name.txt` file to include only the tables you wish to back up.
   - Keep the `requirements.txt` file untouched unless dependency updates are required.

5. **Example Execution**  
   After configuring `config.ini` and `tables_name.txt`, execute the following command to start the backup:

   ```bash
   ./backup_start.sh