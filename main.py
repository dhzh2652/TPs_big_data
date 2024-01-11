from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuration de la connexion à la base de données PostgreSQL
db_config = {
    'dbname': 'films-database',  #  nom de la base de données
    'user': 'admin',        #  nom d'utilisateur PostgreSQL
    'password': 'adminadmin',  # mot de passe PostgreSQL
    'host': '10.192.37.31',    # adresse IP de ma machine hote
    'port': '5432'          # Port par défaut de PostgreSQL
}

# Fonction pour établir une connexion à la base de données
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        return connection
    except psycopg2.Error as error:
        print("Problème de connexion à la base de données:", error)
        return None



# Endpoint pour obtenir la liste des films
@app.route('/films', methods=['GET', 'POST'])
def movies():
    connection = connect_to_db()
    if connection :
        if request.method == 'GET':
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM test")
            films = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify({'films': films})
        elif request.method == 'POST':
            # Parse the JSON data from the request body
            new_film_data = request.json
            # Check if the required fields are present in the JSON data
            if 'title' not in new_film_data or 'description' not in new_film_data:
                return jsonify({'status': 'error', 'message': 'Missing required data'}), 400
            # Insert the new film data into the database
            cursor = connection.cursor()
            cursor.execute("INSERT INTO test (title, description) VALUES (%s, %s)",
                           (new_film_data['title'], new_film_data['description']))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'status': 'success', 'message': 'Film added successfully'}), 201
    else:
        return jsonify({'status': 'error','message': 'Problème de connexion à la base de données'}), 500


@app.route('/films/<int:filmID>', methods=['GET'])
def get_movie_by_id(filmID):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test WHERE id = %s", (filmID,))
        film = cursor.fetchone()
        cursor.close()
        connection.close()
        if film:
            return jsonify({'film': film})
        else:
            return jsonify({'status': 'error', 'message': 'Film not found'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Problème de connexion à la base de données'}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Bonjour, Vous voulez le chemin: %s' % path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
