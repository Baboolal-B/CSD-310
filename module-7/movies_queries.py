import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# Load secrets from .env file
secrets = dotenv_values(".env")

# Database config object
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]))
    cursor = db.cursor()

    # First Query - Select all fields from studio
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    # Second Query - Select all fields from genre
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    # Third Query - Movies with run time less than 2 hours
    print("\n-- DISPLAYING Short Film Names --")
    cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120")
    short_films = cursor.fetchall()
    for film in short_films:
        print("Film Name: {}".format(film[0]))

    # Fourth Query - Film names and directors grouped by director
    print("\n-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director")
    films_by_director = cursor.fetchall()
    for film in films_by_director:
        print("Director: {}\nFilm Name: {}\n".format(film[0], film[1]))

    input("\n\n  Press any key to end...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
