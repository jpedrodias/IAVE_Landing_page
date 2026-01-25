# -*- coding: utf-8 -*-
# IAVE - Landing page (flaskapp).
import os, functools, datetime

from flask import Flask, request, make_response, render_template, redirect, url_for, session, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# ========================= C O N F I G =========================
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///myapp.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASKAPP_SECRET_KEY', 'mysecret')
app.config['SESSION_TYPE'] = 'filesystem'

try:
    app.config['DEBUG'] = bool(int(os.getenv('FLASKAPP_DEBUG', 0)))
except:
    app.config['DEBUG'] = False

app.config['REDIRECT_URL'] = os.getenv('FLASKAPP_REDIRECT_URL', 'https://provas.iave.pt')
app.config['REDIRECT_WAIT'] = os.getenv('FLASKAPP_REDIRECT_WAIT', 10)
app.config['DOWNLOAD_FOLDER'] = os.getenv('FLASKAPP_DOWNLOAD_FOLDER', 'download')
app.config['TITLE'] = os.getenv('FLASKAPP_TITLE', 'IAVE Offline')
app.config['DB_RESET_PIN'] = os.getenv('FLASKAPP_DB_RESET_PIN', '1234')

if app.config['DEBUG']:
    print(app.config)

db = SQLAlchemy()
db.init_app(app)

# ========================= M O D E L S =========================
class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(256), nullable=False)
#end class Record


# ========================= F U N C T I O N S =========================
def no_cache(view):
    @functools.wraps(view)
    def no_cache_wrapper(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return no_cache_wrapper
#end def no_cache


def require_login(view):
    @functools.wraps(view)
    def require_login_wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return require_login_wrapper
#end def require_login


# ========================= V I E W S =========================
@app.route('/')
@no_cache
def homepage():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    record = Record(ip_address=ip_address, user_agent=user_agent)
    db.session.add(record)
    db.session.commit()
    return render_template('index.html',
        redirect=app.config.get('REDIRECT_URL'),
        wait=app.config.get('REDIRECT_WAIT'),
        ip_address=ip_address,
        user_agent=user_agent,
        title=app.config.get('TITLE', ''),
    )
#end def homepage


@app.route('/login', methods=['GET', 'POST'])
@no_cache
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['DB_RESET_PIN']:
            session['logged_in'] = True
            return redirect(url_for('view_records'))
        else:
            return render_template('login.html', error='Invalid password', title=app.config.get('TITLE', ''))
    return render_template('login.html')
#end def login


@app.route('/logout')
@no_cache
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('homepage'))
#end def logout


@app.route('/download/')
@app.route('/download/<path:filename>')
@no_cache
def download(filename=None):
    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])

    if not filename:
        extensoes = {'win': ['.exe'], 'macos': ['.dmg'], 'linux': ['.AppImage']}
        ficheiros = {'win': [], 'macos': [], 'linux': []}

        for file in os.listdir(app.config['DOWNLOAD_FOLDER']):
            for plataforma in extensoes:
                for ext in extensoes.get(plataforma):
                    if file.endswith(ext):
                        ficheiros[plataforma].append(file)
                        break
        
        return render_template('download.html', ficheiros=ficheiros, title=app.config.get('TITLE', ''), do_not_show_menu=True)

    return send_from_directory(directory=app.config['DOWNLOAD_FOLDER'], path=filename, as_attachment=True)
#end def download


@app.route('/export/<path:filename>')
@no_cache
@require_login
def export(filename):
    if filename.endswith('.csv'):
        from user_agents import parse

        # Generate CSV file from database records
        query = Record.query.order_by(Record.timestamp.desc()).all()
        data = []
        for record in query:
            agent= parse(record.user_agent)

            data.append({
                'id': record.id,
                'timestamp': record.timestamp,
                'ip_address': record.ip_address,
                'user_agent': record.user_agent,
                'os': agent.os.family,
                'os_version': agent.os.version_string,
                'device': agent.device.family,
                'device_brand': agent.device.brand,
                'device_model': agent.device.model,
                'browser': agent.browser.family,
                'browser_version': agent.browser.version_string,
            })

        if not data:
            return "No records found", 404
        
        from io import StringIO, BytesIO
        import csv
        output_text  = StringIO()
        writer = csv.DictWriter(output_text, fieldnames=data[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(data)
        output_text.seek(0)
        output = BytesIO(output_text.read().encode('utf-8'))
        output.seek(0)
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )    
    return redirect(url_for('download'))
#end def export


@app.route('/reset_database', methods=['POST'])
@no_cache
@require_login
def reset_database():
    pin = request.form.get('pin')
    hardcoded_pin = app.config['DB_RESET_PIN']  # PIN hardcoded para confirmação

    if pin == hardcoded_pin:
        try:
            db.drop_all()
            db.create_all()
            #return "Database reset successfully!", 200 
        except Exception as e:
            return f"Error resetting database: {str(e)}", 500
    else:
        return "Invalid PIN. Database reset aborted.", 403

    return redirect(url_for('view_records'))
#end def reset_database


@app.route('/view/<int:page>')
@app.route('/view/')
@require_login
@no_cache
def view_records(page=1):
    PAGE_SIZE = 10
    slice_i = (page - 1) * PAGE_SIZE
    slice_f = page * PAGE_SIZE

    total_records = Record.query.count()
    query = Record.query.order_by(Record.timestamp.desc()).slice(slice_i, slice_f).all()

    pagination = {
        'next': page + 1 if total_records > page * PAGE_SIZE else None,
        'prev': page - 1 if page > 1 else None ,
        'curr': page,
        'pages': (total_records // PAGE_SIZE) + 1,
        'records': total_records
    }

    return render_template('view.html', pagination=pagination, records=query, title='Registos')
#end def view_records


@app.route('/view/stats/')
@require_login
@no_cache
def view_records_stats():
    from collections import Counter
    from user_agents import parse

    # Consultar todos os registros
    query = Record.query.order_by(Record.timestamp.desc()).all()

    # Contar os sistemas operativos
    os_counts = Counter()
    for record in query:
        agent = parse(record.user_agent)
        os_name = agent.os.family
        os_counts[os_name] += 1

    # Contar os sistemas operativos (sem duplicados por IP)
    unique_devices = {}
    for record in query:
        agent = parse(record.user_agent)
        os_name = agent.os.family
        if record.ip_address not in unique_devices:
            unique_devices[record.ip_address] = os_name

    unique_os_counts = Counter(unique_devices.values())

    #Preparar os dados para exibição
    total_devices = sum(os_counts.values())
    total_unique_devices = sum(unique_os_counts.values())
    
    stats = [
        {
            'os': os_name,
            'count': count,
            'unique_count': unique_os_counts.get(os_name, 0),
            'percentage': (count / total_devices) * 100 if total_devices > 0 else 0,
            'unique_percentage': (unique_os_counts.get(os_name, 0) / total_unique_devices) * 100 if total_unique_devices > 0 else 0
        }
        for os_name, count in os_counts.items()
    ]

    # Ordenar por número de dispositivos (opcional)
    stats.sort(key=lambda x: x['count'], reverse=True)

    return render_template('view_stats.html', title='Estatisticas', stats=stats)
#end def view_records_stats


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        print('Creating database tables...')
        db.create_all()
    
    print('DEBUG?', app.config.get('DEBUG'))
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
#end if __name__ == '__main__'
#end flaskapp/app.py