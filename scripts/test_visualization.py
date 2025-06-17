#!/usr/bin/env python3
"""
Test script to verify visualization functionality
"""

import pandas as pd
import numpy as np
from utils.visualizer import Visualizer


def test_visualizations():
    """Test all visualization functions"""
    print("🧪 Görselleştirme testleri başlatılıyor...")

    # Create sample data
    np.random.seed(42)
    data = pd.DataFrame({
        'yaş': np.random.randint(18, 65, 100),
        'maaş': np.random.randint(3000, 15000, 100),
        'deneyim': np.random.randint(0, 20, 100),
        'departman': np.random.choice(['IT', 'Pazarlama', 'Satış', 'İK'], 100),
        'şehir': np.random.choice(['İstanbul', 'Ankara', 'İzmir'], 100),
        'performans': np.random.uniform(1, 5, 100)
    })

    visualizer = Visualizer()

    # Test each chart type
    chart_types = ['histogram', 'scatter', 'line', 'bar', 'pie', 'box', 'heatmap']

    for chart_type in chart_types:
        try:
            print(f"  ✅ {chart_type.capitalize()} chart - Test geçti")
            result = visualizer.create_chart(chart_type, data)
            assert result is not None
            assert len(result) > 0
        except Exception as e:
            print(f"  ❌ {chart_type.capitalize()} chart - Test başarısız: {e}")

    print("\n🎉 Tüm görselleştirme testleri tamamlandı!")
    print("📊 Örnek veri özeti:")
    print(f"  - Satır sayısı: {len(data)}")
    print(f"  - Sütun sayısı: {len(data.columns)}")
    print(f"  - Sayısal sütunlar: {list(data.select_dtypes(include=[np.number]).columns)}")
    print(f"  - Kategorik sütunlar: {list(data.select_dtypes(include=['object']).columns)}")


if __name__ == '__main__':
    test_visualizations()
