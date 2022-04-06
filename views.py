from flask import request, render_template, redirect, url_for
from app import app
from forms import TodoForm
from models import todos_sqlite

@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm() 
    tasks = todos_sqlite.show()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit(): 
            todos_sqlite.create()
            task_id = todos_sqlite.add_task(form.data)
            return redirect(url_for("todos_list"))

    return render_template("todos.html", form=form, tasks=tasks, error=error)


@app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos_sqlite.get(todo_id)
    data_todo = {}
    data_todo['title'] = todo[0][1]
    data_todo['description'] = todo[0][2]
    data_todo['status'] = todo[0][3]
    form_todo = TodoForm(data=data_todo)
   
    if request.method == "POST":
        if request.form["btn"] == "Save":
            todos_sqlite.update(todo_id=todo_id, data=form_todo.data)
        if request.form["btn"] == "Delete":
            todos_sqlite.delete(todo_id)
        return redirect(url_for("todos_list"))

    return render_template("todo.html", form=form_todo, todo_id=todo_id)