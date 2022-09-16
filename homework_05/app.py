from flask import Flask, request, render_template
from views.about_page import about_page

app = Flask(__name__)
app.register_blueprint(about_page, url_prefix="/about")


@app.route("/", endpoint="home_page")
def hello_world():
    return render_template("index.html")


@app.route("/<name>/")
def hello_view(name: str = None):
    if name is None:
        name = request.args.get("name", "")
    name = name.strip()
    if not name:
        name = "World"
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(debug=True)
