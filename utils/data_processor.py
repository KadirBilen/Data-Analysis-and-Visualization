import pandas as pd
import numpy as np
import json
from io import StringIO


class DataProcessor:
    def __init__(self):
        self.data = None

    def load_data(self, filepath):
        """Load data from various file formats with better error handling"""
        try:
            file_extension = filepath.split('.')[-1].lower()
            print(f"🔍 Loading file: {filepath}")
            print(f"📄 Extension: {file_extension}")

            if file_extension == 'csv':
                # Try different encodings for CSV
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                for encoding in encodings:
                    try:
                        print(f"🔄 Trying encoding: {encoding}")
                        self.data = pd.read_csv(filepath, encoding=encoding)
                        print(f"✅ CSV loaded successfully with {encoding} encoding")
                        break
                    except UnicodeDecodeError:
                        print(f"❌ Failed with {encoding}, trying next...")
                        continue
                    except Exception as e:
                        print(f"❌ Error with {encoding}: {str(e)}")
                        continue

                if self.data is None:
                    raise ValueError("CSV dosyası hiçbir encoding ile okunamadı")

            elif file_extension in ['xlsx', 'xls']:
                print(f"📊 Loading Excel file...")
                self.data = pd.read_excel(filepath)
                print(f"✅ Excel loaded successfully")

            elif file_extension == 'json':
                print(f"📋 Loading JSON file...")
                self.data = pd.read_json(filepath)
                print(f"✅ JSON loaded successfully")
            else:
                raise ValueError(f"Desteklenmeyen dosya formatı: {file_extension}")

            print(f"📊 Final data shape: {self.data.shape}")
            print(f"📋 Columns: {list(self.data.columns)}")
            print(f"🔢 Data types: {self.data.dtypes.to_dict()}")

            # Clean column names
            self.data.columns = self.data.columns.astype(str)

            return self.data

        except Exception as e:
            print(f"❌ Data loading error: {str(e)}")
            raise e

    def parse_manual_data(self, data_text, data_format):
        """Parse manually entered data"""
        if data_format == 'csv':
            self.data = pd.read_csv(StringIO(data_text))
        elif data_format == 'json':
            data_dict = json.loads(data_text)
            self.data = pd.DataFrame(data_dict)
        else:
            raise ValueError(f"Desteklenmeyen veri formatı: {data_format}")

        return self.data

    def analyze_data(self, data):
        """Perform comprehensive data analysis"""
        if data is None or data.empty:
            raise ValueError("Analiz edilecek veri bulunamadı")

        analysis = {
            'basic_info': self._get_basic_info(data),
            'statistical_summary': self._get_statistical_summary(data),
            'missing_values': self._get_missing_values(data),
            'data_types': self._get_data_types(data),
            'correlations': self._get_correlations(data)
        }

        return analysis

    def _get_basic_info(self, data):
        """Get basic information about the dataset"""
        return {
            'shape': data.shape,
            'columns': list(data.columns),
            'memory_usage': data.memory_usage(deep=True).sum(),
            'total_rows': len(data),
            'total_columns': len(data.columns)
        }

    def _get_statistical_summary(self, data):
        """Get statistical summary for numerical columns"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            return data[numerical_cols].describe().to_dict()
        return {}

    def _get_missing_values(self, data):
        """Analyze missing values"""
        missing_count = data.isnull().sum()
        missing_percentage = (missing_count / len(data)) * 100

        return {
            'missing_count': missing_count.to_dict(),
            'missing_percentage': missing_percentage.to_dict(),
            'total_missing': missing_count.sum()
        }

    def _get_data_types(self, data):
        """Get data types information"""
        return {
            'dtypes': data.dtypes.astype(str).to_dict(),
            'numerical_columns': list(data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(data.select_dtypes(include=['object']).columns),
            'datetime_columns': list(data.select_dtypes(include=['datetime64']).columns)
        }

    def _get_correlations(self, data):
        """Calculate correlations for numerical columns"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 1:
            correlation_matrix = data[numerical_cols].corr()
            return correlation_matrix.to_dict()
        return {}

    def get_column_unique_values(self, data, column_name, limit=10):
        """Get unique values for a specific column"""
        if column_name in data.columns:
            unique_values = data[column_name].unique()
            return list(unique_values[:limit])
        return []
