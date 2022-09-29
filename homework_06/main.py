from flask import Flask, render_template
from flask_migrate import Migrate
from os import getenv
# import config
from models import db
from views.users import users_app

app = Flask(__name__)

CONFIG_OBJECT = getenv("CONFIG", "DevelopmentConfig")
app.config.from_object(f"config.{CONFIG_OBJECT}")
# print(app.config)

db.app = app
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

app.register_blueprint(users_app, url_prefix="/users")


# with app.app_context():
#     db.create_all()


@app.route("/", endpoint="index_page")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
