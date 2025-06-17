#!/usr/bin/env python3
"""
Main runner script for the Flask data analysis application
"""

import os
import sys
from app import app

def setup_environment():
    """Setup the application environment"""
    # Create necessary directories
    directories = ['uploads', 'sample_data', 'static/charts']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'

def main():
    """Main function to run the application"""
    print("🚀 Veri Analizi Platformu Başlatılıyor...")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Check if sample data exists, if not create it
    if not os.path.exists('sample_data/sales_data.csv'):
        print("📊 Örnek veri setleri oluşturuluyor...")
        from scripts.sample_data_generator import save_sample_datasets
        save_sample_datasets()
    
    # Check if database exists, if not create it
    if not os.path.exists('data_analysis.db'):
        print("🗄️  Veritabanı oluşturuluyor...")
        from scripts.setup_database import create_database
        create_database()
    
    print("\n✅ Kurulum tamamlandı!")
    print("🌐 Uygulama şu adreste çalışıyor: http://localhost:5000")
    print("📁 Örnek veri dosyaları 'sample_data' klasöründe bulunuyor")
    print("\n💡 Kullanım İpuçları:")
    print("   - Dosya yüklemek için: http://localhost:5000/upload")
    print("   - Manuel veri girişi için: http://localhost:5000/manual_input")
    print("   - Ctrl+C ile uygulamayı durdurabilirsiniz")
    print("=" * 50)
    
    try:
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Uygulama kapatılıyor...")
        sys.exit(0)

if __name__ == '__main__':
    main()
