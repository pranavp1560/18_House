from app import app, db, Admin  # Replace 'your_app_file' with your main app file name

with app.app_context():
    admin = Admin(username='admin', password='admin123')
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user added successfully.")
