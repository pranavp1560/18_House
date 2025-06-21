# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from flask_mysqldb import MySQL
# from werkzeug.utils import secure_filename
# import os
# import requests
# from functools import wraps

# app = Flask(__name__)
# app.secret_key = 'ganesh_secret'
# app.config['UPLOAD_FOLDER'] = 'static/uploads/gallery/'
# app.config['EVENT_UPLOAD_FOLDER'] = 'static/uploads/events'

# # MySQL Config
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'ganesh_mandal'

# mysql = MySQL(app)

# # Decorator for login-required pages
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('admin_logged_in'):
#             return redirect('/admin')
#         return f(*args, **kwargs)
#     return decorated_function

# @app.route('/')
# def homepage():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM events ORDER BY event_date DESC")
#     events = cur.fetchall()
#     cur.execute("SELECT * FROM gallery ORDER BY id DESC LIMIT 3")
#     gallery = cur.fetchall()
#     cur.close()
#     return render_template('index.html', events=events, gallery=gallery)

# @app.route('/admin', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         cur = mysql.connection.cursor()
#         cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
#         admin = cur.fetchone()
#         cur.close()

#         if admin:
#             session['admin_logged_in'] = True
#             return redirect('/dashboard')
#         else:
#             flash('Invalid credentials')
#     return render_template('admin_login.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/admin')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('admin_dashboard.html')

# @app.route('/events', methods=['GET', 'POST'])
# @login_required
# def manage_events():
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         event_date = request.form['event_date']
#         image = request.files['image']
#         filename = secure_filename(image.filename) if image else None
#         if image:
#             image.save(os.path.join(app.config['EVENT_UPLOAD_FOLDER'], filename))
#         cur.execute("INSERT INTO events (title, description, event_date, image_filename) VALUES (%s, %s, %s, %s)",
#                     (title, description, event_date, filename))
#         mysql.connection.commit()
#     cur.execute("SELECT * FROM events ORDER BY event_date DESC")
#     events = cur.fetchall()
#     cur.close()
#     return render_template('events_manage.html', events=events)

# @app.route('/view_events')
# def view_events():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM events ORDER BY event_date DESC")
#     events = cur.fetchall()
#     cur.close()
#     return render_template('view_events.html', events=events)

# @app.route('/delete_event/<int:event_id>')
# @login_required
# def delete_event(event_id):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM events WHERE id=%s", (event_id,))
#     mysql.connection.commit()
#     cur.close()
#     return redirect('/events')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/gallery', methods=['GET', 'POST'])
# @login_required
# def manage_gallery():
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         caption = request.form['caption']
#         file = request.files['image']
#         if file:
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             cur.execute("INSERT INTO gallery (filename, caption) VALUES (%s, %s)", (filename, caption))
#             mysql.connection.commit()
#     cur.execute("SELECT * FROM gallery ORDER BY id DESC")
#     gallery = cur.fetchall()
#     cur.close()
#     return render_template('gallery_manage.html', gallery=gallery)

# @app.route('/galleryview')
# def view_gallery():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM gallery ORDER BY id DESC")
#     images = cur.fetchall()
#     cur.close()
#     return render_template("view_gallery.html", gallery=images)

# @app.route('/delete_image/<int:image_id>')
# @login_required
# def delete_image(image_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT filename FROM gallery WHERE id=%s", (image_id,))
#     image = cur.fetchone()
#     if image:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], image[0])
#         if os.path.exists(filepath):
#             os.remove(filepath)
#         cur.execute("DELETE FROM gallery WHERE id=%s", (image_id,))
#         mysql.connection.commit()
#     cur.close()
#     return redirect('/gallery')

# @app.route('/vargani')
# @login_required
# def vargani_entry():
#     return render_template('vargani.html')

# @app.route('/submit_vargani', methods=['POST'])
# @login_required
# def submit_vargani():
#     name = request.form['name']
#     amount = request.form['amount']
#     contact = request.form['contact']

#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO vargani (name, amount, contact) VALUES (%s, %s, %s)", (name, amount, contact))
#     mysql.connection.commit()
#     cur.close()

#     try:
#         url = "https://www.fast2sms.com/dev/bulkV2"
#         payload = {
#             "sender_id": "FSTSMS",
#             "message": f"🙏 Thank you {name}! Your Vargani ₹{amount} has been received. - 18 HOUSE Mandal",
#             "language": "english",
#             "route": "v3",
#             "numbers": contact
#         }
#         headers = {
#             'authorization': "J87PtlregKofFyQRVuGOUjqW3CSZb4LimpxEv9wn6cIDNAHX1zNEdfug1DvXmZaRYr9WIhikOjtJMSAK",
#             'Content-Type': "application/json"
#         }
#         response = requests.post(url, json=payload, headers=headers)
#         print(response.json())
#     except Exception as e:
#         print("SMS sending failed:", e)

#     return redirect('/vargani_list')

# @app.route('/vargani_list')
# @login_required
# def vargani_list():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM vargani ORDER BY amount DESC")
#     vargani_data = cur.fetchall()
#     cur.execute("SELECT SUM(amount) FROM vargani")
#     total = cur.fetchone()[0] or 0
#     cur.close()
#     return render_template('vargani_list.html', vargani=vargani_data, total=total)

# @app.route('/delete_vargani/<int:id>')
# @login_required
# def delete_vargani(id):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM vargani WHERE id = %s", (id,))
#     mysql.connection.commit()
#     cur.close()
#     return redirect('/vargani_list')

# @app.route('/delete_all_vargani')
# def delete_all_vargani():
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM vargani")
#     mysql.connection.commit()
#     cur.close()
#     return redirect('/vargani_list')


# @app.route('/edit_vargani/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_vargani(id):
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         name = request.form['name']
#         amount = request.form['amount']
#         contact = request.form['contact']
#         cur.execute("UPDATE vargani SET name=%s, amount=%s, contact=%s WHERE id=%s", (name, amount, contact, id))
#         mysql.connection.commit()
#         cur.close()
#         return redirect('/vargani_list')
#     cur.execute("SELECT * FROM vargani WHERE id=%s", (id,))
#     vargani_entry = cur.fetchone()
#     cur.close()
#     return render_template('edit_vargani.html', vargani=vargani_entry)

# @app.route('/expense', methods=['GET', 'POST'])
# @login_required
# def manage_expense():
#     cur = mysql.connection.cursor()
#     if request.method == 'POST':
#         title = request.form['title']
#         amount = int(request.form['amount'])
#         description = request.form['description']
#         cur.execute("INSERT INTO expense (title, amount, description) VALUES (%s, %s, %s)",
#                     (title, amount, description))
#         mysql.connection.commit()
#     cur.execute("SELECT * FROM expense ORDER BY created_at DESC")
#     expenses = cur.fetchall()
#     cur.execute("SELECT SUM(amount) FROM expense")
#     total_expense = cur.fetchone()[0] or 0
#     cur.execute("SELECT SUM(amount) FROM vargani")
#     total_vargani = cur.fetchone()[0] or 0
#     remaining = total_vargani - total_expense
#     cur.close()
#     return render_template('expense.html', expenses=expenses, total_expense=total_expense, remaining=remaining, total_vargani=total_vargani)

# @app.route('/delete_expense/<int:expense_id>')
# @login_required
# def delete_expense(expense_id):
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM expense WHERE id = %s", (expense_id,))
#     mysql.connection.commit()
#     cur.close()
#     return redirect('/expense')

# if __name__ == '__main__':
#     app.run(debug=True)


# This version uses SQLAlchemy instead of Flask-MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from functools import wraps
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  


app = Flask(__name__)
app.secret_key = 'ganesh_secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads/gallery/'
app.config['EVENT_UPLOAD_FOLDER'] = 'static/uploads/events'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ganesh_mandal.db'  # change to your MySQL URI if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== MODELS ==========
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    event_date = db.Column(db.String(20))
    image_filename = db.Column(db.String(200))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    caption = db.Column(db.String(200))

class Vargani(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    contact = db.Column(db.String(15))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    amount = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ========== DECORATORS ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES ==========
@app.route('/')
def homepage():
    events = Event.query.order_by(Event.event_date.desc()).all()
    gallery = Gallery.query.order_by(Gallery.id.desc()).limit(3).all()
    return render_template('index.html', events=events, gallery=gallery)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if admin:
            session['admin_logged_in'] = True
            return redirect('/dashboard')
        flash('Invalid credentials')
    return render_template('admin_login.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    if request.method == 'POST':
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['EVENT_UPLOAD_FOLDER'], filename))
        new_event = Event(
            title=request.form['title'],
            description=request.form['description'],
            event_date=request.form['event_date'],
            image_filename=filename
        )
        db.session.add(new_event)
        db.session.commit()
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('events_manage.html', events=events)

@app.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect('/events')

@app.route('/view_events')
def view_events():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('view_events.html', events=events)

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def manage_gallery():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_image = Gallery(filename=filename, caption=request.form['caption'])
        db.session.add(new_image)
        db.session.commit()
    gallery = Gallery.query.order_by(Gallery.id.desc()).all()
    return render_template('gallery_manage.html', gallery=gallery)

@app.route('/galleryview')
def view_gallery():
    gallery = Gallery.query.order_by(Gallery.id.desc()).all()
    return render_template('view_gallery.html', gallery=gallery)

@app.route('/delete_image/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Gallery.query.get(image_id)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    db.session.delete(image)
    db.session.commit()
    return redirect('/gallery')

@app.route('/vargani')
@login_required
def vargani_entry():
    return render_template('vargani.html')

@app.route('/submit_vargani', methods=['POST'])
@login_required
def submit_vargani():
    name = request.form['name']
    amount = request.form['amount']
    contact = request.form['contact']

    new_vargani = Vargani(
        name=name,
        amount=amount,
        contact=contact
    )
    db.session.add(new_vargani)
    db.session.commit()

    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = {
            "sender_id": "FSTSMS",
            "message": f"🙏 Thank you {name}! Your Vargani ₹{amount} has been received. - 18 HOUSE Mandal",
            "language": "english",
            "route": "v3",
            "numbers": contact
        }
        headers = {
            'authorization': os.getenv("FAST2SMS_API_KEY"),
            'Content-Type': "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
    except Exception as e:
        print("SMS sending failed:", e)

    return redirect('/vargani_list')


@app.route('/vargani_list')
@login_required
def vargani_list():
    data = Vargani.query.order_by(Vargani.amount.desc()).all()
    total = db.session.query(db.func.sum(Vargani.amount)).scalar() or 0
    return render_template('vargani_list.html', vargani=data, total=total)

@app.route('/delete_vargani/<int:id>')
@login_required
def delete_vargani(id):
    entry = db.session.get(Vargani, id)
    db.session.delete(entry)
    db.session.commit()
    return redirect('/vargani_list')

@app.route('/delete_all_vargani')
@login_required
def delete_all_vargani():
    db.session.query(Vargani).delete()
    db.session.commit()
    return redirect('/vargani_list')

@app.route('/edit_vargani/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vargani(id):
    entry = Vargani.query.get(id)
    if request.method == 'POST':
        entry.name = request.form['name']
        entry.amount = request.form['amount']
        entry.contact = request.form['contact']
        db.session.commit()
        return redirect('/vargani_list')
    return render_template('edit_vargani.html', vargani=entry)

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def manage_expense():
    if request.method == 'POST':
        new_expense = Expense(
            title=request.form['title'],
            amount=int(request.form['amount']),
            description=request.form['description']
        )
        db.session.add(new_expense)
        db.session.commit()

    expenses = Expense.query.order_by(Expense.created_at.desc()).all()
    total_expense = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    total_vargani = db.session.query(db.func.sum(Vargani.amount)).scalar() or 0
    remaining = total_vargani - total_expense

    return render_template('expense.html', expenses=expenses, total_expense=total_expense, total_vargani=total_vargani, remaining=remaining)

@app.route('/delete_expense/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expense')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
