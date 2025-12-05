import configparser
import boto3
import os
import datetime
import psycopg2
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')

postgres_config = config['postgresql']
s3_config = config['S3']


def log_error(message, level):
    try:
        conn = psycopg2.connect(
            host=postgres_config['host'],
            dbname=postgres_config['database'],
            user=postgres_config['user'],
            password=postgres_config['password']
        )
        cursor = conn.cursor()

        logged_time = datetime.datetime.now()

        query = """
            INSERT INTO public.logs (application, logged, level, message)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, ('Backup', logged_time, level, message))

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error while logging: {e}")
        if conn:
            cursor.close()
            conn.close()


def backup(config, s3_config):
    s3_client = boto3.client(
        's3',
        region_name=s3_config['region'],
        aws_access_key_id=s3_config['access_key'],
        aws_secret_access_key=s3_config['secret_key']
    )
    
    backup_filename = f"{datetime.datetime.now().strftime('%d_%m_%Y')}.sql"
    os.environ['PGPASSWORD'] = config['password']

    successful_backups = 0

    with open("tables_name.txt", "r") as file:
        tables = file.readlines()

        for table in tables:
            table_name = table.strip()
            backup_filepath = os.path.join(os.getcwd(), backup_filename)

            try:
                backup_command = f"pg_dump -h {config['host']} -U {config['user']} -d {config['database']} -t \"public.\\\"{table_name}\\\"\" -f {backup_filepath}"
                
                result = subprocess.run(backup_command, shell=True, capture_output=True, text=True)

                if result.returncode != 0:
                    log_error(f"pg_dump failed: {result.stderr}", 'Error')
                    continue

                s3_object_key = f"{s3_config['destination_file']}/{table_name}/{backup_filename}"

                s3_client.upload_file(backup_filepath, s3_config['bucket_name'], s3_object_key)

                if os.path.exists(backup_filepath):
                    os.remove(backup_filepath)

                successful_backups += 1

                log_error(f"{table_name} backup success.\n", 'Info')

            except Exception as e:
                error_message = f"Error backing up {table_name}: {str(e)}"
                log_error(error_message)

    log_error(f"Success backup count -> {successful_backups}\n", 'Info')

if __name__ == '__main__':
    try:
        backup(postgres_config, s3_config)
    except Exception as e:
        log_error(f"Backup process failed: {str(e)}", 'Error')
