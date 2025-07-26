from flask import Flask, render_template, jsonify
from model import db, Notification
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notifications.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Add sample notifications if DB is empty
    if Notification.query.count() == 0:
        db.session.add_all([
            Notification(title="New Comment", message="Someone commented on your post."),
            Notification(title="New Like", message="Your photo got a new like."),
            Notification(title="Reminder", message="Don't forget the meeting at 5 PM."),
        ])
        db.session.commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/notifications')
def notifications():
    unread_count = Notification.query.filter_by(is_read=False).count()
    notifications = Notification.query.order_by(Notification.id.desc()).all()
    return jsonify({
        "unread_count": unread_count,
        "notifications": [n.to_dict() for n in notifications]
    })

if __name__ == '__main__':
    app.run(debug=True)
