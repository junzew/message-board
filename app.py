from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Message %r>' % self.id


@app.route('/messages', methods=['POST'])
def create_message():
    msg_content = request.form['content']
    new_msg = Message(content=msg_content)
    try:
        db.session.add(new_msg)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'There was an issue adding your message'


@app.route('/messages/<int:id>', methods=['POST', 'GET'])
def update_message(id):
    msg = Message.query.get_or_404(id)
    if request.method == 'POST':
        msg.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'There was an issue updating your msg'
    elif request.method == 'GET':
        return render_template("update.html", msg=msg)


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_todo(id):
    msg_to_delete = Message.query.get_or_404(id)
    try:
        db.session.delete(msg_to_delete)
        db.session.commit()

        return redirect('/', code=303)
    except Exception:
        return 'There was a problem deleting that msg'


@app.route('/', methods=['GET'])
def home():
    messages = Message.query.order_by(Message.date_created).all()[::-1]
    return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)


"""
from app import db
db.create_all()
"""
