from flask import Blueprint, render_template, request, url_for, redirect, flash

from models import db, User
from views.forms.users import CreateUserForm

users_app = Blueprint("users_app", __name__)


@users_app.route("/", endpoint="list")
def get_products():
    users = User.query.order_by(User.id).all()
    return render_template("users/list.html", users=users)


@users_app.route(
    "/<int:user_id>/confirm-delete/",
    methods=["GET", "POST"],
    endpoint="confirm-delete",
)
@users_app.route(
    "/<int:user_id>/",
    methods=["GET", "DELETE"],
    endpoint="details",
)
def get_user_by_id(user_id: int):

    user: User = User.query.get_or_404(
        user_id,
        f"User #{user_id} not found!",
    )

    confirm_delete = request.endpoint == "users_app.confirm-delete"
    if request.method == "GET":
        return render_template(
            "users/confirm-delete.html" if confirm_delete else "users/details.html",
            user=user,
        )

    db.session.delete(user)
    db.session.commit()

    flash(f"Deleted user {user.name}!", "warning")
    url = url_for("users_app.list")
    if confirm_delete:
        return redirect(url)

    return {"ok": True, "url": url}


@users_app.route("/add/", methods=["GET", "POST"], endpoint="add")
def add_user():
    form = CreateUserForm()

    if request.method == "GET":
        return render_template("users/add.html", form=form)

    if not form.validate_on_submit():
        return render_template("users/add.html", form=form), 400

    user_name = form.name.data
    is_new = form.is_new.data

    user = User(name=user_name, is_new=is_new)
    db.session.add(user)
    db.session.commit()

    flash(f"Successfully added user {user.name}!")
    url = url_for("users_app.details", user_id=user.id)
    return redirect(url)
