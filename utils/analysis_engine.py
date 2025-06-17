import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings('ignore')


class AnalysisEngine:
    def __init__(self):
        self.available_analyses = {
            'descriptive': 'Tanımlayıcı İstatistikler',
            'correlation': 'Korelasyon Analizi',
            'distribution': 'Dağılım Analizi',
            'outlier': 'Aykırı Değer Analizi',
            'clustering': 'Kümeleme Analizi',
            'pca': 'Temel Bileşen Analizi',
            'trend': 'Trend Analizi',
            'comparison': 'Karşılaştırmalı Analiz'
        }

    def get_available_analyses(self):
        return self.available_analyses

    def perform_analysis(self, data, analysis_types):
        """Seçilen analiz türlerini gerçekleştir"""
        results = {}

        for analysis_type in analysis_types:
            if analysis_type in self.available_analyses:
                try:
                    method_name = f'_perform_{analysis_type}_analysis'
                    if hasattr(self, method_name):
                        results[analysis_type] = getattr(self, method_name)(data)
                    else:
                        results[analysis_type] = {'error': f'Analiz metodu bulunamadı: {analysis_type}'}
                except Exception as e:
                    results[analysis_type] = {'error': str(e)}

        return results

    def _perform_descriptive_analysis(self, data):
        """Tanımlayıcı istatistikler"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns

        result = {
            'type': 'descriptive',
            'title': 'Tanımlayıcı İstatistikler',
            'numerical_summary': {},
            'categorical_summary': {},
            'visualizations': ['histogram', 'box', 'bar']
        }

        # Sayısal değişkenler için
        if len(numerical_cols) > 0:
            for col in numerical_cols:
                result['numerical_summary'][col] = {
                    'mean': float(data[col].mean()),
                    'median': float(data[col].median()),
                    'std': float(data[col].std()),
                    'min': float(data[col].min()),
                    'max': float(data[col].max()),
                    'skewness': float(stats.skew(data[col].dropna())),
                    'kurtosis': float(stats.kurtosis(data[col].dropna()))
                }

        # Kategorik değişkenler için
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                value_counts = data[col].value_counts()
                result['categorical_summary'][col] = {
                    'unique_count': int(data[col].nunique()),
                    'most_frequent': str(value_counts.index[0]),
                    'most_frequent_count': int(value_counts.iloc[0]),
                    'distribution': value_counts.head(10).to_dict()
                }

        return result

    def _perform_correlation_analysis(self, data):
        """Korelasyon analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) < 2:
            return {'error': 'Korelasyon analizi için en az 2 sayısal sütun gerekli'}

        correlation_matrix = data[numerical_cols].corr()

        # En yüksek korelasyonları bul
        high_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.5:  # Yüksek korelasyon eşiği
                    high_correlations.append({
                        'var1': correlation_matrix.columns[i],
                        'var2': correlation_matrix.columns[j],
                        'correlation': float(corr_value),
                        'strength': 'Güçlü' if abs(corr_value) > 0.7 else 'Orta'
                    })

        return {
            'type': 'correlation',
            'title': 'Korelasyon Analizi',
            'correlation_matrix': correlation_matrix.to_dict(),
            'high_correlations': high_correlations,
            'visualizations': ['heatmap', 'scatter']
        }

    def _perform_distribution_analysis(self, data):
        """Dağılım analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) == 0:
            return {'error': 'Dağılım analizi için sayısal veri gerekli'}

        distribution_tests = {}

        for col in numerical_cols:
            col_data = data[col].dropna()

            # Normallik testi
            shapiro_stat, shapiro_p = stats.shapiro(col_data.sample(min(5000, len(col_data))))

            distribution_tests[col] = {
                'shapiro_stat': float(shapiro_stat),
                'shapiro_p': float(shapiro_p),
                'is_normal': shapiro_p > 0.05,
                'skewness': float(stats.skew(col_data)),
                'kurtosis': float(stats.kurtosis(col_data))
            }

        return {
            'type': 'distribution',
            'title': 'Dağılım Analizi',
            'distribution_tests': distribution_tests,
            'visualizations': ['histogram', 'box']
        }

    def _perform_outlier_analysis(self, data):
        """Aykırı değer analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) == 0:
            return {'error': 'Aykırı değer analizi için sayısal veri gerekli'}

        outlier_results = {}

        for col in numerical_cols:
            col_data = data[col].dropna()

            # IQR yöntemi
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]

            # Z-score yöntemi
            z_scores = np.abs(stats.zscore(col_data))
            z_outliers = col_data[z_scores > 3]

            outlier_results[col] = {
                'iqr_outliers': len(outliers),
                'iqr_percentage': float(len(outliers) / len(col_data) * 100),
                'z_outliers': len(z_outliers),
                'z_percentage': float(len(z_outliers) / len(col_data) * 100),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }

        return {
            'type': 'outlier',
            'title': 'Aykırı Değer Analizi',
            'outlier_results': outlier_results,
            'visualizations': ['box', 'scatter']
        }

    def _perform_clustering_analysis(self, data):
        """Kümeleme analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) < 2:
            return {'error': 'Kümeleme analizi için en az 2 sayısal sütun gerekli'}

        # Veriyi standartlaştır
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data[numerical_cols].fillna(0))

        # Optimal küme sayısını bul (elbow method)
        inertias = []
        k_range = range(2, min(11, len(data) // 10 + 2))

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(scaled_data)
            inertias.append(kmeans.inertia_)

        # En iyi k değerini seç (basit elbow detection)
        optimal_k = 3  # Default
        if len(inertias) > 2:
            diffs = np.diff(inertias)
            optimal_k = k_range[np.argmax(diffs[:-1] - diffs[1:]) + 1]

        # Final clustering
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(scaled_data)

        # Küme istatistikleri
        cluster_stats = {}
        for i in range(optimal_k):
            cluster_data = data[clusters == i]
            cluster_stats[f'Küme {i + 1}'] = {
                'size': len(cluster_data),
                'percentage': float(len(cluster_data) / len(data) * 100)
            }

        return {
            'type': 'clustering',
            'title': 'Kümeleme Analizi',
            'optimal_k': optimal_k,
            'cluster_stats': cluster_stats,
            'inertias': [float(x) for x in inertias],
            'k_range': list(k_range),
            'visualizations': ['scatter', 'bar']
        }

    def _perform_pca_analysis(self, data):
        """Temel bileşen analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) < 3:
            return {'error': 'PCA analizi için en az 3 sayısal sütun gerekli'}

        # Veriyi standartlaştır
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data[numerical_cols].fillna(0))

        # PCA uygula
        pca = PCA()
        pca_result = pca.fit_transform(scaled_data)

        # Açıklanan varyans
        explained_variance = pca.explained_variance_ratio_
        cumulative_variance = np.cumsum(explained_variance)

        # Bileşen yükleri
        components = pca.components_

        return {
            'type': 'pca',
            'title': 'Temel Bileşen Analizi',
            'explained_variance': [float(x) for x in explained_variance[:5]],
            'cumulative_variance': [float(x) for x in cumulative_variance[:5]],
            'n_components_90': int(np.argmax(cumulative_variance >= 0.9) + 1),
            'feature_importance': {
                col: float(abs(components[0][i]))
                for i, col in enumerate(numerical_cols)
            },
            'visualizations': ['scatter', 'bar']
        }

    def _perform_trend_analysis(self, data):
        """Trend analizi"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns

        if len(numerical_cols) == 0:
            return {'error': 'Trend analizi için sayısal veri gerekli'}

        trend_results = {}

        for col in numerical_cols:
            col_data = data[col].dropna()

            # Basit trend hesaplama
            x = np.arange(len(col_data))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, col_data)

            trend_results[col] = {
                'slope': float(slope),
                'r_squared': float(r_value ** 2),
                'p_value': float(p_value),
                'trend_direction': 'Artan' if slope > 0 else 'Azalan' if slope < 0 else 'Sabit',
                'trend_strength': 'Güçlü' if abs(r_value) > 0.7 else 'Orta' if abs(r_value) > 0.3 else 'Zayıf'
            }

        return {
            'type': 'trend',
            'title': 'Trend Analizi',
            'trend_results': trend_results,
            'visualizations': ['line', 'scatter']
        }

    def _perform_comparison_analysis(self, data):
        """Karşılaştırmalı analiz"""
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns

        if len(numerical_cols) == 0 or len(categorical_cols) == 0:
            return {'error': 'Karşılaştırmalı analiz için hem sayısal hem kategorik veri gerekli'}

        comparison_results = {}

        # Her kategorik değişken için sayısal değişkenleri karşılaştır
        for cat_col in categorical_cols[:2]:  # İlk 2 kategorik sütun
            for num_col in numerical_cols[:3]:  # İlk 3 sayısal sütun
                groups = []
                group_names = []

                for category in data[cat_col].unique()[:5]:  # İlk 5 kategori
                    group_data = data[data[cat_col] == category][num_col].dropna()
                    if len(group_data) > 0:
                        groups.append(group_data)
                        group_names.append(str(category))

                if len(groups) >= 2:
                    # ANOVA testi
                    try:
                        f_stat, p_value = stats.f_oneway(*groups)

                        comparison_results[f'{cat_col}_vs_{num_col}'] = {
                            'f_statistic': float(f_stat),
                            'p_value': float(p_value),
                            'significant': p_value < 0.05,
                            'group_means': {
                                name: float(group.mean())
                                for name, group in zip(group_names, groups)
                            }
                        }
                    except:
                        continue

        return {
            'type': 'comparison',
            'title': 'Karşılaştırmalı Analiz',
            'comparison_results': comparison_results,
            'visualizations': ['bar', 'box', 'scatter']
        }
