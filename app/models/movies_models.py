import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os
from psycopg2 import sql

load_dotenv()

configs = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PWD') 
}


class Movies():
    def __init__(self, data: tuple):
        self.id, self.movie, self.released_date, self.rating = data

    @staticmethod
    def checking_keys(**kwargs):
        available_keys = ["movie", "rating", "released_date"]
        wrong_keys = []
        keys_kwargs = [i for i in kwargs.keys()]
        checking = [wrong_keys.append(i) for i in keys_kwargs if i not in available_keys]
        if len(wrong_keys) == 0:
            return wrong_keys
        return {'available_keys': available_keys, 'wrong_keys': wrong_keys}

    @staticmethod
    def create_db():
        conn = connect(
          dbname = os.environ.get('DB_CREATE_DB'),
          user = os.environ.get('DB_USER'),
          host = os.environ.get('DB_HOST'),
          password = os.environ.get('DB_PWD')
        )

        DB_NAME = os.environ.get('DB_NAME')
        autocommit = ISOLATION_LEVEL_AUTOCOMMIT
        conn.set_isolation_level(autocommit)
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE ' + str(DB_NAME))
        conn.close()

    @staticmethod
    def create_table():
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        cur.execute("""
          CREATE TABLE IF NOT EXISTS movies (
            id BIGSERIAL PRIMARY KEY,
            movie VARCHAR(100) NOT NULL UNIQUE,
            released_date DATE NOT NULL,
            rating INTEGER NOT NULL
          )
        """)
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def insert_data_into_table(**kwargs):
        check_keys = Movies.checking_keys(**kwargs)
        if len(check_keys) == 0:
            conn = psycopg2.connect(**configs)
            cur = conn.cursor()
            data = {str(k):str(v).title() if k=='movie' else v for k,v in kwargs.items()}
            data_values = tuple(data.values())
            cur.execute("INSERT INTO movies(movie, released_date, rating) VALUES (%s, %s, %s) RETURNING * ; ", (data_values) )
            result = cur.fetchone()
            data_processed = Movies(result).__dict__
            data_processed['released_date'] = str(data_processed['released_date'])
            conn.commit()
            cur.close()
            conn.close()
                
            return data_processed
        else:
            return check_keys

    @staticmethod
    def post_movie(**kwargs):
        try:     
            Movies.create_table()
            return Movies.insert_data_into_table(**kwargs)
        except psycopg2.OperationalError:
            Movies.create_db()
            Movies.create_table()
            return Movies.insert_data_into_table(**kwargs)
      
    @staticmethod
    def get_all_movies():
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        cur.execute("""
          SELECT * FROM movies
        """)
        getting_data = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        processed_data = [Movies(fetched_movies).__dict__ for fetched_movies in getting_data]    
        return processed_data

    @staticmethod
    def get_specific_movie(movie_id):   
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        cur.execute('SELECT * FROM movies WHERE id=(%s);', (movie_id, ))
        fetched_result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return Movies(fetched_result).__dict__

    @staticmethod
    def delete(movie_id):
        conn = psycopg2.connect(**configs)
        cur = conn.cursor()
        cur.execute(""" DELETE FROM
                            movies
                        WHERE
                            id=(%s)
                        RETURNING *;""", (movie_id, ))
        getting_data = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        serialized_data = Movies(getting_data).__dict__
        serialized_data['released_date'] = str(serialized_data['released_date'])
        return serialized_data

    @staticmethod
    def update_movie(id, **kwargs):
        check_keys = Movies.checking_keys(**kwargs)
        if len(check_keys) == 0:  
            data = {str(k):str(v).title() if k=='movie' else v for k,v in kwargs.items()}
            data_values = tuple(data.values())
            conn = psycopg2.connect(**configs)
            cur = conn.cursor()
            columns = [sql.Identifier(key) for key in kwargs.keys()]
            values = [sql.Literal(value) for value in data_values]
            query = sql.SQL("""
                    UPDATE
                        movies
                    SET
                        ({columns}) = row({values})
                    WHERE
                        id={id}
                    RETURNING *
                """).format(id=sql.Literal(str(id)),
                            columns=sql.SQL(',').join(columns),
                            values=sql.SQL(',').join(values))
            cur.execute(query)
            updated_movie = cur.fetchone()
            conn.commit()
            cur.close()
            conn.close()

            if not updated_movie:
                return {"error": "Not found"}, 404
            serialized_data = Movies(updated_movie).__dict__
            serialized_data['released_date'] = str(serialized_data['released_date'])
            return serialized_data
        else:
          return check_keys, 422
