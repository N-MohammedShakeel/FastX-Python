import mysql.connector
from utils.logger import log_error, log_info

def get_connection():
    """Returns a direct database connection object."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MSmysql@1",
            database="fastx"
        )
        log_info("Database Connection Established")
        return conn
    except Exception as exception:
        log_error(f"Database Connection Failed: {exception}")
        print("\n[ERROR] Database is unavailable. Please verify connection credentials.")
        return None