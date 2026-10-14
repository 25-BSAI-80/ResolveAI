import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ayesha2007',
    'database': 'resolveai'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                receipt_id VARCHAR(50) UNIQUE NOT NULL,
                student_name VARCHAR(100) NOT NULL,
                father_name VARCHAR(100),
                roll_number VARCHAR(50) NOT NULL,
                cell_number VARCHAR(20),
                amount VARCHAR(20) NOT NULL,
                payment_date VARCHAR(30),
                bank_name VARCHAR(100),
                status VARCHAR(20) DEFAULT 'VERIFIED',
                generated_on VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("MySQL database ready: resolveai")
    except Error as e:
        print(f"Error: {e}")

def save_receipt(receipt_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO receipts 
            (receipt_id, student_name, father_name, roll_number, cell_number, 
             amount, payment_date, bank_name, status, generated_on)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            receipt_data['receipt_id'],
            receipt_data['student_name'],
            receipt_data['father_name'],
            receipt_data['roll_number'],
            receipt_data['cell_number'],
            receipt_data['amount'],
            receipt_data['payment_date'],
            receipt_data['bank_name'],
            receipt_data['status'],
            receipt_data['generated_on']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Receipt saved: {receipt_data['receipt_id']}")
        return True
    except Error as e:
        print(f"Error saving receipt: {e}")
        return False

def search_by_roll(roll_number):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT receipt_id, student_name, roll_number, amount, payment_date, 
                   status, generated_on
            FROM receipts
            WHERE roll_number LIKE %s
            ORDER BY id DESC
        """, (f"%{roll_number}%",))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Error as e:
        print(f"Error: {e}")
        return []

def get_total_receipts():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM receipts")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count
    except Error as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    init_database()
    print(f"Total receipts: {get_total_receipts()}")