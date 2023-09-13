from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    status = db.Column(db.String(100))




with app.app_context():
    db.create_all()




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        description = request.form['description']
        status = 'Incomplete'

        todo =Todo(description=description, status=status)
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')

    todos = db.session.execute(db.select(Todo)).scalars().all()
    return render_template('todos.html', todos=todos)




@app.route('/todos/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get(id)

    if request.method == 'POST':
        description = request.form['description']
        todo.description = description
        db.session.commit()
        return redirect('/todos')

    return render_template('edit.html', todo=todo)

@app.route('/todos/new', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        description = request.form['description']
        status = 'Incomplete'
        todo = Todo(description=description, status=status)
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')

    return render_template('add.html')



@app.route('/todos/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todos')


@app.route('/todos/mark-done/<int:id>', methods=['POST'])
def mark_done(id):
    todo = Todo.query.get(id)
    todo.status = 'Completed'
    db.session.commit()
    return redirect('/todos')


@app.route('/todos/mark-undone/<int:id>', methods=['POST'])
def mark_undone(id):
    todo = Todo.query.get(id)
    todo.status = 'Incomplete'
    db.session.commit()
    return redirect('/todos')



if __name__ == '__main__':
    app.run(debug=True)