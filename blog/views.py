from flask import render_template


from . import app
from .database import session, Entry

from flask import request, redirect, url_for


PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>/?limit=10")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    
    try:
        PAGINATE_BY = int(request.args.get('limit', 10))
    except:
        PAGINATE_BY = 10
    
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html",
        entries=entries, 
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages, 
        limit=PAGINATE_BY
    )

from flask_login import login_required, current_user

@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")


@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/<id>")
#click to get to this route
# query the single entry
def entry(id):
    entry = session.query(Entry).filter(Entry.id == id).first()
    return render_template("view_entry.html", entry=entry)

@app.route("/entry/<id>/edit", methods=["GET", "POST"])
def edit_entry_get(id):
    
    if request.method=="GET":
        entry = session.query(Entry).filter(Entry.id == id).one()
        return render_template("edit_entry.html", entry=entry)
    
    elif request.method=="POST":
        #edit_entry_post(id)
        entry = session.query(Entry).filter(Entry.id==id).one()
        entry.title = request.form.get("title", entry.title)
        entry.content = request.form.get("content", entry.content)
        session.add(entry)
        session.commit()
        return redirect(url_for('entries'))
        
@app.route("/entry/<id>/delete", methods=["GET", "POST"])
def open_options(id):
    
    if request.method=="GET":
        entry = session.query(Entry).filter(Entry.id==id).one()
        return render_template("delete_entry.html", entry=entry)
    
    elif request.method=="POST":
        entry = session.query(Entry).filter(Entry.id==id).one()
        session.delete(entry)
        session.commit()
        return redirect(url_for("entries"))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

from flask import flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from .database import User

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

# style="color:black; color:hover:black;
