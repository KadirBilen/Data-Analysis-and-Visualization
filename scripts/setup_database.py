#!/usr/bin/env python3
"""
Database setup script for storing analysis results and user data
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Create SQLite database and tables"""
    db_path = 'data_analysis.db'
    
    # Remove existing database for fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create analysis_sessions table
    cursor.execute('''
        CREATE TABLE analysis_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename VARCHAR(255),
            file_type VARCHAR(10),
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_results TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create data_files table
    cursor.execute('''
        CREATE TABLE data_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            original_filename VARCHAR(255),
            stored_filename VARCHAR(255),
            file_size INTEGER,
            file_path VARCHAR(500),
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (id)
        )
    ''')
    
    # Insert sample users
    sample_users = [
        ('admin', 'admin@example.com'),
        ('demo_user', 'demo@example.com'),
        ('test_user', 'test@example.com')
    ]
    
    cursor.executemany(
        'INSERT INTO users (username, email) VALUES (?, ?)',
        sample_users
    )
    
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print("Sample users added:")
    for username, email in sample_users:
        print(f"  - {username} ({email})")

if __name__ == '__main__':
    create_database()
