from flask import Blueprint, render_template

about_page = Blueprint("about_page", __name__)


@about_page.route("/", endpoint="about")
def about_view():
    return render_template("about.html")
