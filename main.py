from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    todo: Mapped[str] = mapped_column()

@app.route('/', methods=['GET'])
def get_todo():
    todos = db.session.execute(db.select(Todo).order_by(Todo.todo)).scalars()
    return render_template('get.html', todos=todos)

@app.route('/submit',methods=['POST'])
def submit():
    todo = request.form['todo_input']
    with app.app_context():
        new_addition = Todo(todo=todo)
        db.session.add(new_addition)
        db.session.commit()
    
    return redirect('/')

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete(todo_id):
    print('hit')
    todo_to_delete = Todo.query.get(todo_id)
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return {'message': 'Todo deleted successfully'}, 200
    return redirect('/')






with app.app_context():
    db.create_all()

# with app.app_context():
#     new_task = Todo(id= 1, todo="test")

#     db.session.add(new_task)
#     db.session.commit()

app.run()