#!/usr/bin/env python3
"""
Generate sample datasets for testing the data analysis platform
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

def generate_sales_data():
    """Generate sample sales data"""
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Sample data
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Tablet', 'Phone']
    regions = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya']
    sales_reps = ['Ali Yılmaz', 'Ayşe Demir', 'Mehmet Kaya', 'Fatma Özkan', 'Can Arslan']
    
    data = []
    for _ in range(1000):
        record = {
            'tarih': pd.to_datetime(np.random.choice(date_range)).strftime('%Y-%m-%d'),
            'ürün': np.random.choice(products),
            'bölge': np.random.choice(regions),
            'satış_temsilcisi': np.random.choice(sales_reps),
            'miktar': np.random.randint(1, 20),
            'birim_fiyat': np.random.uniform(50, 2000),
            'indirim_oranı': np.random.uniform(0, 0.3)
        }
        record['toplam_satış'] = record['miktar'] * record['birim_fiyat'] * (1 - record['indirim_oranı'])
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

def generate_employee_data():
    """Generate sample employee data"""
    np.random.seed(123)
    
    departments = ['IT', 'Pazarlama', 'Satış', 'İK', 'Finans', 'Operasyon']
    positions = ['Uzman', 'Kıdemli Uzman', 'Müdür', 'Direktör', 'Stajyer']
    cities = ['İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya', 'Adana']
    
    data = []
    for i in range(500):
        age = np.random.randint(22, 65)
        experience = min(age - 22, np.random.randint(0, 25))
        
        record = {
            'çalışan_id': f'EMP{i+1:04d}',
            'isim': f'Çalışan {i+1}',
            'yaş': age,
            'departman': np.random.choice(departments),
            'pozisyon': np.random.choice(positions),
            'şehir': np.random.choice(cities),
            'deneyim_yılı': experience,
            'maaş': np.random.randint(3000, 15000),
            'performans_puanı': np.random.uniform(1, 5),
            'işe_başlama_tarihi': (datetime.now() - timedelta(days=np.random.randint(30, 3650))).strftime('%Y-%m-%d')
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

def generate_customer_data():
    """Generate sample customer data"""
    np.random.seed(456)
    
    segments = ['Premium', 'Standard', 'Basic']
    channels = ['Online', 'Mağaza', 'Telefon', 'Mobil App']
    
    data = []
    for i in range(300):
        record = {
            'müşteri_id': f'CUST{i+1:05d}',
            'yaş': np.random.randint(18, 80),
            'cinsiyet': np.random.choice(['Erkek', 'Kadın']),
            'segment': np.random.choice(segments),
            'kayıt_tarihi': (datetime.now() - timedelta(days=np.random.randint(1, 1095))).strftime('%Y-%m-%d'),
            'son_alışveriş_tarihi': (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
            'toplam_harcama': np.random.uniform(100, 10000),
            'alışveriş_sayısı': np.random.randint(1, 50),
            'tercih_edilen_kanal': np.random.choice(channels),
            'müşteri_memnuniyeti': np.random.uniform(1, 5)
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

def save_sample_datasets():
    """Save all sample datasets to files"""
    # Create sample_data directory if it doesn't exist
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate and save sales data
    sales_df = generate_sales_data()
    sales_df.to_csv('sample_data/sales_data.csv', index=False, encoding='utf-8')
    sales_df.to_excel('sample_data/sales_data.xlsx', index=False)
    sales_df.to_json('sample_data/sales_data.json', orient='records', force_ascii=False, indent=2)
    
    # Generate and save employee data
    employee_df = generate_employee_data()
    employee_df.to_csv('sample_data/employee_data.csv', index=False, encoding='utf-8')
    employee_df.to_excel('sample_data/employee_data.xlsx', index=False)
    
    # Generate and save customer data
    customer_df = generate_customer_data()
    customer_df.to_csv('sample_data/customer_data.csv', index=False, encoding='utf-8')
    customer_df.to_json('sample_data/customer_data.json', orient='records', force_ascii=False, indent=2)
    
    print("Sample datasets created successfully:")
    print(f"  - Sales data: {len(sales_df)} records")
    print(f"  - Employee data: {len(employee_df)} records")
    print(f"  - Customer data: {len(customer_df)} records")
    print("\nFiles saved in 'sample_data' directory:")
    print("  - sales_data.csv, sales_data.xlsx, sales_data.json")
    print("  - employee_data.csv, employee_data.xlsx")
    print("  - customer_data.csv, customer_data.json")

if __name__ == '__main__':
    save_sample_datasets()
