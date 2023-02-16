import json
import requests
from flask import Flask, render_template

app = Flask(__name__)


def refresh_authenticate():
    print("refresh du token")
    url_auth = "http://127.0.0.1:8000/api/authenticate"
    auth = requests.get(url_auth)

    # importation du json depuis l'api
    json_generated = auth.json()

    # création du json et ecriture du json importé
    with open("token.json", "w") as file:
        json.dump(json_generated, file)

    # lecture du json
    with open('token.json') as files:
        data = json.load(files)
        tokens = data["tokens"]
        print("token reçu :", tokens)

    url_token = f"http://127.0.0.1:5000/api/stage/token"
    headers = {
        "tokens": f"{tokens}"
    }
    url_tokens = requests.get(url_token, headers=headers)

    # importation du json depuis l'api
    json_generated = url_tokens.json()

    # création du json et ecriture du json importé
    with open("api.json", "w") as file:
        json.dump(json_generated, file)

    # lecture du json
    with open('api.json') as mon_fichier:
        data = json.load(mon_fichier)
        hello_world = data["valeur1"]
    print("authentification réussi")

    @app.route('/')
    def refreshed():
        return render_template('index.html', json_api=hello_world)


# noinspection PyBroadException
try:
    # lecture du json
    print("tentative de connexion")
    with open('token.json') as mon_fichier:
        data = json.load(mon_fichier)
        tokens = data["tokens"]
    url_token = f"http://127.0.0.1:5000/api/stage/token"
    headers = {
        "tokens": f"{tokens}"
    }
    url_tokens = requests.get(url_token, headers=headers)

    # importation du json depuis l'api
    json_generated = url_tokens.json()

except Exception:
    try:
        print("création d'un nouveau token")
        print("authentification en cour ")
        url_auth = "http://127.0.0.1:8000/api/authenticate"
        auth = requests.get(url_auth)

        # importation du json depuis l'api
        json_generated = auth.json()

        # création du json et ecriture du json importé
        with open("token.json", "w") as file:
            json.dump(json_generated, file)

        # lecture du json
        with open('token.json') as files:
            data = json.load(files)
            tokens = data["tokens"]
            print("token reçu :", tokens)

        url_token = "http://127.0.0.1:8000/api/stage/token"
        headers = {
            "tokens": f"{tokens}"
        }
        url_tokens = requests.get(url_token, headers=headers)

        # importation du json depuis l'api
        json_generated = url_tokens.json()

    except requests.exceptions.ConnectionError:
        print("Connexion à l'api impossible")
        exit()

# création du json et ecriture du json importé
with open("api.json", "w") as file:
    json.dump(json_generated, file)

# lecture du json
with open('api.json') as mon_fichier:
    data = json.load(mon_fichier)
    hello_world = data["valeur1"]
    token_checked = data["tokens"]

if token_checked == 'invalid':
    print("refresh")
    refresh_authenticate()

else:

    @app.route('/')
    def home():
        return render_template('index.html', json_api=hello_world)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
