import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json


class Visualizer:
    def __init__(self):
        # Neon color palette for dark theme
        self.neon_colors = ['#00FFFF', '#FF00FF', '#00FF00', '#FFFF00', '#8000FF', '#FF8000', '#0080FF', '#FF0040']

    def create_chart(self, chart_type, data, analysis_context=None, selected_columns=None):
        """Create different types of charts with analysis context and column selection"""
        try:
            print(f"=== CREATING CHART ===")
            print(f"Chart type: {chart_type}")
            print(f"Data shape: {data.shape if hasattr(data, 'shape') else 'No shape'}")
            print(f"Selected columns: {selected_columns}")

            if data is None or len(data) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-exclamation-triangle me-2'></i>Görselleştirme için veri bulunamadı.</div>"

            # Convert to DataFrame if it's not already
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)

            if data.empty:
                return "<div class='alert alert-warning'><i class='fas fa-exclamation-triangle me-2'></i>Veri seti boş.</div>"

            chart_methods = {
                'histogram': self._create_histogram,
                'scatter': self._create_scatter_plot,
                'line': self._create_line_plot,
                'bar': self._create_bar_chart,
                'pie': self._create_pie_chart,
                'box': self._create_box_plot,
                'heatmap': self._create_heatmap,
                'correlation': self._create_correlation_matrix
            }

            if chart_type in chart_methods:
                result = chart_methods[chart_type](data, analysis_context, selected_columns)
                print(f"Chart created successfully, HTML length: {len(result)}")
                return result
            else:
                return f"<div class='alert alert-danger'><i class='fas fa-exclamation-triangle me-2'></i>Desteklenmeyen grafik türü: {chart_type}</div>"

        except Exception as e:
            print(f"=== CHART CREATION ERROR ===")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'><i class='fas fa-exclamation-triangle me-2'></i>Grafik oluşturulurken hata: {str(e)}</div>"

    def _apply_dark_theme(self, fig, title=None):
        """Apply professional dark theme with neon colors to plotly figure"""
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#1a1a2e',  # Koyu lacivert
            font=dict(color='#FFFFFF', family='Inter, system-ui, sans-serif', size=12),
            title_font=dict(color='#00FFFF', size=18, family='Inter, system-ui, sans-serif'),
            colorway=self.neon_colors,
            showlegend=True,
            legend=dict(
                bgcolor='rgba(26,26,46,0.9)',  # Koyu lacivert
                bordercolor='#00FFFF',
                borderwidth=1,
                font=dict(color='#FFFFFF', size=11)
            ),
            margin=dict(l=60, r=60, t=80, b=60),
            height=400,
            autosize=True
        )

        if title:
            fig.update_layout(title=title)

        # Update axes with neon styling
        fig.update_xaxes(
            gridcolor='#333366',  # Koyu lacivert grid
            linecolor='#00FFFF',
            tickcolor='#00FFFF',
            title_font=dict(color='#00FFFF', size=14),
            tickfont=dict(color='#FFFFFF', size=11)  # Beyaz tick labels
        )
        fig.update_yaxes(
            gridcolor='#333366',  # Koyu lacivert grid
            linecolor='#00FFFF',
            tickcolor='#00FFFF',
            title_font=dict(color='#00FFFF', size=14),
            tickfont=dict(color='#FFFFFF', size=11)  # Beyaz tick labels
        )

        return fig

    def _create_histogram(self, data, analysis_context=None, selected_columns=None):
        """Create histogram using Plotly"""
        try:
            print("Creating histogram...")
            numerical_cols = data.select_dtypes(include=[np.number]).columns
            print(f"Numerical columns: {list(numerical_cols)}")

            if len(numerical_cols) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-chart-bar me-2'></i>Histogram için sayısal veri bulunamadı.</div>"

            # Use selected column or first numerical column
            col = selected_columns.get('x_column') if selected_columns and selected_columns.get('x_column') else \
            numerical_cols[0]
            print(f"Using column: {col}")

            # Analysis context based title
            title = f'{col} - Histogram Dağılımı'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'distribution':
                    title = f'{col} - Dağılım Analizi (Histogram)'
                elif analysis_type == 'descriptive':
                    title = f'{col} - Tanımlayıcı İstatistik (Histogram)'

            # Create figure
            fig = px.histogram(
                data,
                x=col,
                title=title,
                nbins=min(30, max(10, len(data) // 10)),
                color_discrete_sequence=['#00FFFF']
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                marker_line_color='#333366',
                marker_line_width=1,
                opacity=0.8
            )

            # Convert to HTML with embedded Plotly
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'histogram_{col}',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id=f"histogram-{col.replace(' ', '_').replace('/', '_')}",
                config=config
            )

            print(f"Histogram HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Histogram error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Histogram hatası: {str(e)}</div>"

    def _create_scatter_plot(self, data, analysis_context=None, selected_columns=None):
        """Create scatter plot using Plotly"""
        try:
            print("Creating scatter plot...")
            numerical_cols = data.select_dtypes(include=[np.number]).columns
            print(f"Numerical columns: {list(numerical_cols)}")

            if len(numerical_cols) < 2:
                return "<div class='alert alert-warning'><i class='fas fa-braille me-2'></i>Scatter plot için en az 2 sayısal sütun gerekli.</div>"

            # Use selected columns or first two numerical columns
            x_col = selected_columns.get('x_column') if selected_columns and selected_columns.get('x_column') else \
            numerical_cols[0]
            y_col = selected_columns.get('y_column') if selected_columns and selected_columns.get('y_column') else \
            numerical_cols[1]
            color_col = selected_columns.get('color_column') if selected_columns and selected_columns.get(
                'color_column') else None

            print(f"Using columns: {x_col} vs {y_col}, color: {color_col}")

            # Analysis context based title
            title = f'{x_col} vs {y_col} - Scatter Plot'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'correlation':
                    title = f'{x_col} vs {y_col} - Korelasyon Analizi'
                elif analysis_type == 'clustering':
                    title = f'{x_col} vs {y_col} - Kümeleme Görselleştirmesi'
                elif analysis_type == 'outlier':
                    title = f'{x_col} vs {y_col} - Aykırı Değer Analizi'

            # Create figure
            fig = px.scatter(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                title=title,
                color_discrete_sequence=self.neon_colors
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                marker=dict(
                    size=8,
                    line=dict(width=1, color='#333366'),
                    opacity=0.8
                )
            )

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'scatter_{x_col}_{y_col}',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id=f"scatter-{x_col.replace(' ', '_')}-{y_col.replace(' ', '_')}",
                config=config
            )

            print(f"Scatter plot HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Scatter plot error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Scatter plot hatası: {str(e)}</div>"

    def _create_line_plot(self, data, analysis_context=None, selected_columns=None):
        """Create line plot using Plotly"""
        try:
            print("Creating line plot...")
            numerical_cols = data.select_dtypes(include=[np.number]).columns

            if len(numerical_cols) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-chart-line me-2'></i>Line plot için sayısal veri bulunamadı.</div>"

            # Use selected column or first numerical column
            col = selected_columns.get('y_column') if selected_columns and selected_columns.get('y_column') else \
            numerical_cols[0]
            print(f"Using column: {col}")

            # Analysis context based title
            title = f'{col} - Zaman Serisi'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'trend':
                    title = f'{col} - Trend Analizi'
                elif analysis_type == 'descriptive':
                    title = f'{col} - Veri Sıralaması'

            # Create index for x-axis
            data_with_index = data.reset_index()

            # Create figure
            fig = px.line(
                data_with_index,
                x='index',
                y=col,
                title=title,
                line_shape='spline'
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                line=dict(color='#00FFFF', width=3),
                mode='lines+markers',
                marker=dict(size=6, color='#00FFFF', line=dict(width=1, color='#333366'))
            )

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'line_{col}',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id=f"line-{col.replace(' ', '_')}",
                config=config
            )

            print(f"Line plot HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Line plot error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Line plot hatası: {str(e)}</div>"

    def _create_bar_chart(self, data, analysis_context=None, selected_columns=None):
        """Create bar chart using Plotly"""
        try:
            print("Creating bar chart...")
            categorical_cols = data.select_dtypes(include=['object']).columns
            print(f"Categorical columns: {list(categorical_cols)}")

            if len(categorical_cols) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-chart-bar me-2'></i>Bar chart için kategorik veri bulunamadı.</div>"

            # Use selected column or first categorical column
            col = selected_columns.get('x_column') if selected_columns and selected_columns.get('x_column') else \
            categorical_cols[0]
            value_counts = data[col].value_counts().head(10)
            print(f"Using column: {col}, unique values: {len(value_counts)}")

            # Analysis context based title
            title = f'{col} - Kategori Dağılımı'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'descriptive':
                    title = f'{col} - Tanımlayıcı İstatistik (Kategori Dağılımı)'
                elif analysis_type == 'comparison':
                    title = f'{col} - Karşılaştırmalı Analiz'

            # Create figure
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=title,
                color=value_counts.values,
                color_continuous_scale=['#1a1a2e', '#00FFFF'],
                labels={'x': col, 'y': 'Sayı'}
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                marker_line_color='#333366',
                marker_line_width=1,
                opacity=0.9
            )

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'bar_{col}',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id=f"bar-{col.replace(' ', '_')}",
                config=config
            )

            print(f"Bar chart HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Bar chart error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Bar chart hatası: {str(e)}</div>"

    def _create_pie_chart(self, data, analysis_context=None, selected_columns=None):
        """Create pie chart using Plotly"""
        try:
            print("Creating pie chart...")
            categorical_cols = data.select_dtypes(include=['object']).columns

            if len(categorical_cols) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-chart-pie me-2'></i>Pie chart için kategorik veri bulunamadı.</div>"

            # Use selected column or first categorical column
            col = selected_columns.get('x_column') if selected_columns and selected_columns.get('x_column') else \
            categorical_cols[0]
            value_counts = data[col].value_counts().head(8)
            print(f"Using column: {col}, unique values: {len(value_counts)}")

            # Analysis context based title
            title = f'{col} - Oransal Dağılım'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'descriptive':
                    title = f'{col} - Tanımlayıcı İstatistik (Oransal Dağılım)'

            # Create figure
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=title,
                color_discrete_sequence=self.neon_colors
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=12, color='#FFFFFF'),  # Beyaz text
                marker=dict(line=dict(color='#333366', width=2))
            )

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'pie_{col}',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id=f"pie-{col.replace(' ', '_')}",
                config=config
            )

            print(f"Pie chart HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Pie chart error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Pie chart hatası: {str(e)}</div>"

    def _create_box_plot(self, data, analysis_context=None, selected_columns=None):
        """Create box plot using Plotly"""
        try:
            print("Creating box plot...")
            numerical_cols = data.select_dtypes(include=[np.number]).columns

            if len(numerical_cols) == 0:
                return "<div class='alert alert-warning'><i class='fas fa-square me-2'></i>Box plot için sayısal veri bulunamadı.</div>"

            print(f"Using columns: {list(numerical_cols[:5])}")

            # Analysis context based title
            title = 'Sayısal Değişkenler - Box Plot Analizi'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'outlier':
                    title = 'Aykırı Değer Analizi - Box Plot'
                elif analysis_type == 'distribution':
                    title = 'Dağılım Analizi - Box Plot'

            # Create box plot for multiple numerical columns
            fig = go.Figure()

            for i, col in enumerate(numerical_cols[:5]):  # Max 5 columns
                fig.add_trace(go.Box(
                    y=data[col],
                    name=col,
                    marker_color=self.neon_colors[i % len(self.neon_colors)],
                    line=dict(color=self.neon_colors[i % len(self.neon_colors)], width=2)
                ))

            fig.update_layout(title=title)
            fig = self._apply_dark_theme(fig)

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'boxplot',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id="boxplot",
                config=config
            )

            print(f"Box plot HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Box plot error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Box plot hatası: {str(e)}</div>"

    def _create_heatmap(self, data, analysis_context=None, selected_columns=None):
        """Create heatmap using Plotly"""
        try:
            print("Creating heatmap...")
            numerical_cols = data.select_dtypes(include=[np.number]).columns

            if len(numerical_cols) < 2:
                return "<div class='alert alert-warning'><i class='fas fa-th me-2'></i>Heatmap için en az 2 sayısal sütun gerekli.</div>"

            correlation_matrix = data[numerical_cols].corr()
            print(f"Correlation matrix shape: {correlation_matrix.shape}")

            # Analysis context based title
            title = 'Korelasyon Heatmap - Değişkenler Arası İlişki'
            if analysis_context and analysis_context.get('analysis_type'):
                analysis_type = analysis_context['analysis_type']
                if analysis_type == 'correlation':
                    title = 'Korelasyon Analizi - Heatmap'

            # Create figure
            fig = px.imshow(
                correlation_matrix,
                text_auto=True,
                aspect="auto",
                title=title,
                color_continuous_scale='RdYlBu_r',
                zmin=-1,
                zmax=1
            )

            # Apply theme
            fig = self._apply_dark_theme(fig)
            fig.update_traces(
                texttemplate='%{text:.2f}',
                textfont=dict(color='#FFFFFF', size=10)  # Beyaz text
            )

            # Convert to HTML
            config = {
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'heatmap',
                    'height': 500,
                    'width': 700,
                    'scale': 1
                }
            }

            html = fig.to_html(
                include_plotlyjs='cdn',
                div_id="heatmap",
                config=config
            )

            print(f"Heatmap HTML generated successfully: {len(html)} chars")
            return html

        except Exception as e:
            print(f"Heatmap error: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<div class='alert alert-danger'>Heatmap hatası: {str(e)}</div>"

    def _create_correlation_matrix(self, data, analysis_context=None, selected_columns=None):
        """Create correlation matrix visualization"""
        return self._create_heatmap(data, analysis_context, selected_columns)
