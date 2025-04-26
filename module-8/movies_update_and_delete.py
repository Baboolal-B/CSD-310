import mysql.connector
from mysql.connector import errorcode

# Function to display film records
def show_films(cursor, title):
    cursor.execute("""
        SELECT film_name AS Name, film_director AS Director, 
               genre_name AS Genre, studio_name AS 'Studio Name'
        FROM film 
        INNER JOIN genre ON film.genre_id = genre.genre_id 
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """)
    
    films = cursor.fetchall()

    print("\n -- {} --".format(title))

    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre: {}\nStudio Name: {}\n".format(
            film[0], film[1], film[2], film[3]
        ))

# Connect to the database and perform operations
try:
    db = mysql.connector.connect(
        user="movies_user",         
        password="new_password",     
        host="localhost",             
        database="movies",            
    )

    cursor = db.cursor()

    # Display original films (unchanged)
    show_films(cursor, "DISPLAYING FILMS")

    # Insert Transformers One only if it doesn't already exist
    cursor.execute("""
        SELECT COUNT(*) FROM film WHERE film_name = 'Transformers One'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO film (
                film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id
            ) VALUES (
                'Transformers One', '2024-09-13', 120, 'Josh Cooley', 1, 1
            )
        """)
        db.commit()

    # Show films after insert
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update the genre of Alien to Horror (assuming genre_id = 3 for Horror)
    cursor.execute("""
        UPDATE film
        SET genre_id = 3
        WHERE film_name = 'Alien'
    """)
    db.commit()

    # Show films after update
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

    # Delete Gladiator from the film table
    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)
    db.commit()

    # Show films after deletion
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        db.close()
