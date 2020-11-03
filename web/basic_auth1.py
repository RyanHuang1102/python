from flask import Flask, request, redirect, Response, jsonify
from functools import wraps

from flasgger import Swagger

def requires_basic_auth(f):
    """Decorator to require HTTP Basic Auth for your endpoint."""

    def check_auth(username, password):
        return username == "admin" and password == "admin"

    def authenticate():
        return Response(
            "Authentication required.", 401,
            {"WWW-Authenticate": "Basic realm='Login Required'"},
        )

    @wraps(f)
    def decorated(*args, **kwargs):
        # NOTE: This example will require Basic Auth only when you run the
        # app directly. For unit tests, we can't block it from getting the
        # Swagger specs so we just allow it to go thru without auth.
        # The following two lines of code wouldn't be needed in a normal
        # production environment.
        if __name__ != "__main__":
            return f(*args, **kwargs)

        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Swagger Basic Auth App",
    "uiversion": 2,
}
swag = Swagger(app,
    decorators=[ requires_basic_auth ],
    template={
        "swagger": "2.0",
        "info": {
            "title": "Swagger Basic Auth App",
            "version": "1.0",
        },
        "consumes": [
            "application/json",
        ],
        "produces": [
            "application/json",
        ],
    },
)

@app.route("/echo/<name>", methods=["GET", "POST"])
def echo(name):
    """
    Echo back the name and any posted parameters.
    ---
    tags:
      - echo
    parameters:
      - in: path
        name: name
        type: string
        required: true
      - in: body
        name: body
        description: JSON parameters.
        schema:
          properties:
            first_name:
              type: string
              description: First name.
              example: Alice
            last_name:
              type: string
              description: Last name.
              example: Smith
            dob:
              type: string
              format: date
              description: Date of birth.
              example: 1990-01-01
            comment:
              type: string
              description: Something arbitrary.
              example: Hello world
    responses:
      200:
        description: OK.
    """
    data = {
        "url_name": name,
        "json": request.json,
    }
    return jsonify(data)

@app.route("/")
def index():
    return redirect("/apidocs")

if __name__ == "__main__":
    app.run(host='10.19.5.212',debug=True)
