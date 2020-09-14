"""Import datetime, flask, SQLAlchemy, and SASS."""
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    """Todo database class."""

    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Return default repr value of Todo database class."""
        return '<Task %r>' % self.id

    def __str__(self):
        """Return default str value of Todo database class."""
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def home():
    """Home route."""
    if request.method == 'POST':
        todo_item = request.form['todo']
        new_todo = Todo(todo=todo_item)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except(ValueError, TypeError):
            return "There was an issue adding the to-do."
    elif request.method == 'GET':
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todos=todos)


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    """Delete todo route."""
    todo = Todo.query.get_or_404(todo_id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except(TypeError, ValueError):
        return "There was an issue deleting the to-do."


@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
def update(todo_id):
    """Update todo route."""
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.todo = request.form['todo']
        try:
            db.session.commit()
            return redirect('/')
        except(ValueError, TypeError):
            return "There was an issue updating the to-do."
    elif request.method == 'GET':
        return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)
