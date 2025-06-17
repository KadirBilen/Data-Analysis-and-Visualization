from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from werkzeug.utils import secure_filename
import pandas as pd
from utils.data_processor import DataProcessor
from utils.visualizer import Visualizer
from utils.analysis_engine import AnalysisEngine
import json
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_session_data():
    """Clear previous analysis data from session"""
    keys_to_clear = ['data', 'filename', 'analysis_results', 'numerical_cols', 'categorical_cols']
    for key in keys_to_clear:
        session.pop(key, None)


@app.route('/')
def index():
    # Clear session when returning to home page
    clear_session_data()
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Clear previous session data
        clear_session_data()

        # Check if file was uploaded
        if 'file' not in request.files:
            flash('Dosya seçilmedi')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Dosya seçilmedi')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the uploaded file
            try:
                print(f"=== PROCESSING FILE: {filename} ===")
                processor = DataProcessor()
                data = processor.load_data(filepath)

                print(f"✅ Data loaded successfully!")
                print(f"📊 Shape: {data.shape}")
                print(f"📋 Columns: {list(data.columns)}")
                print(f"🔢 Data types: {data.dtypes.to_dict()}")

                # Get column information
                numerical_cols = list(data.select_dtypes(include=['number']).columns)
                categorical_cols = list(data.select_dtypes(include=['object']).columns)

                print(f"🔢 Numerical columns: {numerical_cols}")
                print(f"📝 Categorical columns: {categorical_cols}")

                # Store data in session with proper encoding
                data_json = data.to_json(orient='records', force_ascii=False, date_format='iso')

                # Store everything in session
                session['data'] = data_json
                session['filename'] = filename
                session['data_source'] = 'file'
                session['numerical_cols'] = numerical_cols
                session['categorical_cols'] = categorical_cols

                print(f"💾 Session data stored:")
                print(f"   - Data length: {len(data_json)}")
                print(f"   - Numerical cols: {len(numerical_cols)}")
                print(f"   - Categorical cols: {len(categorical_cols)}")
                print(f"   - Session keys: {list(session.keys())}")

                # Clean up uploaded file
                try:
                    os.remove(filepath)
                    print(f"🗑️ Cleaned up uploaded file: {filepath}")
                except:
                    pass

                # Redirect to analysis selection
                return redirect(url_for('select_analysis'))

            except Exception as e:
                print(f"❌ FILE PROCESSING ERROR:")
                print(f"   Error: {str(e)}")
                traceback.print_exc()
                flash(f'Dosya işlenirken hata oluştu: {str(e)}')
                return redirect(request.url)
        else:
            flash('Geçersiz dosya formatı. CSV, Excel veya JSON dosyası yükleyin.')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/select_analysis')
def select_analysis():
    print(f"=== SELECT ANALYSIS ROUTE ===")
    print(f"Session keys: {list(session.keys())}")
    print(f"Has data: {'data' in session}")
    print(f"Has columns: {'numerical_cols' in session and 'categorical_cols' in session}")

    if 'data' not in session:
        print("❌ No data in session - redirecting to upload")
        flash('Önce veri yüklemeniz gerekiyor')
        return redirect(url_for('upload_file'))

    try:
        # Get available analyses
        analysis_engine = AnalysisEngine()
        available_analyses = analysis_engine.get_available_analyses()

        # Get data info for preview
        data_json = session['data']
        numerical_cols = session.get('numerical_cols', [])
        categorical_cols = session.get('categorical_cols', [])

        print(f"📊 Loading data from session - Length: {len(data_json)}")

        data = pd.DataFrame(json.loads(data_json))
        print(f"✅ Data loaded successfully: {data.shape}")

        # If columns not in session, recalculate
        if not numerical_cols and not categorical_cols:
            print("🔄 Recalculating column types...")
            numerical_cols = list(data.select_dtypes(include=['number']).columns)
            categorical_cols = list(data.select_dtypes(include=['object']).columns)
            session['numerical_cols'] = numerical_cols
            session['categorical_cols'] = categorical_cols

        data_info = {
            'rows': len(data),
            'columns': len(data.columns),
            'numerical_cols': numerical_cols,
            'categorical_cols': categorical_cols
        }

        print(f"📋 Data info: {data_info}")

        return render_template('select_analysis.html',
                               available_analyses=available_analyses,
                               data_info=data_info,
                               filename=session.get('filename', 'Bilinmeyen'))

    except Exception as e:
        print(f"❌ SELECT ANALYSIS ERROR:")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        flash(f'Veri yüklenirken hata oluştu: {str(e)}')
        return redirect(url_for('upload_file'))


@app.route('/perform_analysis', methods=['POST'])
def perform_analysis():
    if 'data' not in session:
        flash('Önce veri yüklemeniz gerekiyor')
        return redirect(url_for('upload_file'))

    try:
        # Get selected analyses
        selected_analyses = request.form.getlist('analyses')

        if not selected_analyses:
            flash('En az bir analiz türü seçmelisiniz')
            return redirect(url_for('select_analysis'))

        # Load data
        data = pd.DataFrame(json.loads(session['data']))
        print(f"=== PERFORMING ANALYSIS ===")
        print(f"📊 Data shape: {data.shape}")
        print(f"🔍 Selected analyses: {selected_analyses}")

        # Perform basic analysis
        processor = DataProcessor()
        basic_analysis = processor.analyze_data(data)

        # Perform selected analyses
        analysis_engine = AnalysisEngine()
        detailed_analyses = analysis_engine.perform_analysis(data, selected_analyses)

        # Convert DataFrame to JSON for client-side storage
        data_json = data.to_json(orient='records', force_ascii=False)

        # Get column information
        numerical_cols = session.get('numerical_cols', list(data.select_dtypes(include=['number']).columns))
        categorical_cols = session.get('categorical_cols', list(data.select_dtypes(include=['object']).columns))

        print(f"📋 Columns for template:")
        print(f"   - Numerical: {numerical_cols}")
        print(f"   - Categorical: {categorical_cols}")

        return render_template('analysis_results.html',
                               basic_analysis=basic_analysis,
                               detailed_analyses=detailed_analyses,
                               filename=session.get('filename', 'Bilinmeyen'),
                               data_preview=data.head(10).to_html(classes='table table-striped'),
                               data_json=data_json,
                               selected_analyses=selected_analyses,
                               numerical_cols=numerical_cols,
                               categorical_cols=categorical_cols)

    except Exception as e:
        print(f"❌ ANALYSIS ERROR:")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        flash(f'Analiz gerçekleştirilirken hata oluştu: {str(e)}')
        return redirect(url_for('select_analysis'))


@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        # Get data and chart type from POST request
        request_data = request.get_json()
        chart_type = request_data.get('chart_type')
        data_json = request_data.get('data')
        analysis_context = request_data.get('analysis_context', {})
        selected_columns = request_data.get('selected_columns', {})

        print(f"=== VISUALIZATION REQUEST ===")
        print(f"📊 Chart type: {chart_type}")
        print(f"📋 Data records: {len(data_json) if data_json else 0}")
        print(f"🔍 Analysis context: {analysis_context}")
        print(f"📝 Selected columns: {selected_columns}")

        if not data_json:
            return jsonify({'error': 'Veri bulunamadı. Lütfen önce veri yükleyin.'}), 400

        if not chart_type:
            return jsonify({'error': 'Grafik türü belirtilmedi.'}), 400

        # Convert JSON back to DataFrame
        data = pd.DataFrame(data_json)
        print(f"✅ DataFrame created: {data.shape}")
        print(f"📋 Columns: {list(data.columns)}")

        # Create visualizer and generate chart
        visualizer = Visualizer()
        chart_html = visualizer.create_chart(chart_type, data, analysis_context, selected_columns)

        print(f"✅ Chart HTML generated: {len(chart_html)} characters")

        return jsonify({'chart_html': chart_html})

    except Exception as e:
        print(f"❌ VISUALIZATION ERROR:")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Grafik oluşturulurken hata: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
