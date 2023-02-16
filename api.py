import datetime
import hashlib
import sqlite3
import jwt
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = 'secretkey!'


@app.route("/api/stage/", methods=['GET', 'POST'])
def api():
    if request.method == "GET":
        if 'tokens' in session:

            # génération de hello world + confirmation de la validité du token
            api1 = {
                "title": "stage_copernic",
                "valeur1": "HELLO WORLD",
                "tokens": "valid"
            }

            return jsonify(api1)
        else:
            return 'please authenticate you'
    else:
        return 'error'


@app.route("/api/stage/token", methods=['GET', 'POST'])
def tokens():
    token_get = request.headers.get('tokens')

    try:
        jwt.decode(token_get, app.secret_key, algorithms=["HS256"])
        token_used = hashlib.sha256(token_get.encode()).hexdigest()
        connn = sqlite3.connect("userdata.db")
        cur = connn.cursor()
        username = token_used
        password = token_used
        # vérification du token
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        if cur.fetchall():
            session['tokens'] = token_get
            return api()
        else:
            return authenticate()
    except jwt.exceptions.ExpiredSignatureError:
        expired_cookie = {
            "title": "stage_copernic",
            "tokens": "invalid",
            "valeur1": "invalid"
        }
        return jsonify(expired_cookie)
    except Exception as error:
        return f'{error}'


@app.route("/api/authenticate", methods=['GET', 'POST'])
def authenticate():
    if request.method == "GET":
        if 'tokens' in session:
            return api()
        else:
            # creation du token et de la session
            tokenss = jwt.encode(
                {"passw": 'nottoken', 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                app.secret_key, algorithm="HS256")

            hashage = hashlib.sha256(tokenss.encode()).hexdigest()
            session['tokens'] = tokenss

            # enregistrement du token dans la base de donné hashé
            connec = sqlite3.connect("userdata.db")
            cur = connec.cursor()
            cur.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
            id INTEGRER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
            username = hashage
            password = hashage
            cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, password))
            connec.commit()

            token_json = {
                "title": "stage_copernic",
                "tokens": f"{tokenss}"
            }

            return jsonify(token_json)
    else:
        return 'error 401'


if __name__ == "__main__":
    app.run(port=8000)
