
from flask.json import jsonify
import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os
from psycopg2 import sql
from app.excepctions.anime_exceptions import UserNotFoundError


load_dotenv()

configs = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PWD') 
}

class Animes():
  def __init__(self, data: tuple):
      self.id, self.anime, self.released_date, self.seasons = data

  def save(self):
    return self.__dict__

  @staticmethod
  def checking_keys(**kwargs):
    available_keys = ["anime", "seasons", "released_date"]
    wrong_keys = []
    keys_kwargs = [i for i in kwargs.keys()]
    checking = [wrong_keys.append(i) for i in keys_kwargs if i not in available_keys]
    # for i in keys_kwargs:
    #     if i not in available_keys:
    #       wrong_keys.append(i)
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
      CREATE TABLE IF NOT EXISTS animes (
        id BIGSERIAL PRIMARY KEY,
        anime VARCHAR(100) NOT NULL UNIQUE,
        released_date DATE NOT NULL,
        seasons INTEGER NOT NULL
      )
    """)
    conn.commit()
    cur.close()
    conn.close()

  @staticmethod
  def insert_data_into_table(**kwargs):
    check_keys = Animes.checking_keys(**kwargs)
    if len(check_keys) == 0:
      conn = psycopg2.connect(**configs)
      cur = conn.cursor()
      data = {str(k):str(v).title() if k=='anime' else v for k,v in kwargs.items()}
      data_values = tuple(data.values())
      cur.execute("INSERT INTO animes(anime, released_date, seasons) VALUES (%s, %s, %s) RETURNING * ; ", (data_values) )
      result = cur.fetchone()
      data_processed = Animes(result).__dict__
      conn.commit()
      cur.close()
      conn.close()
      return data_processed
    else:
      return check_keys
    # nome do anime salvo com .title()
    # caso o anime ainda não exista retornar um dict com os dados do anime criado 201
    # se ele já exister um dict dizendo que o anime já existe no db 409
    # se as keys foram invalid, return a dict with the valid dicts and one with the invalid keys that were sent - 422


  @staticmethod
  def post_anime(**kwargs):
    try:
      Animes.create_table()
      return Animes.insert_data_into_table(**kwargs)


    except Exception as e:
      # Animes.create_db()
      # Animes.create_table()
      # Animes.insert_data_into_table(**kwargs)
      return str(e)

  @staticmethod
  def get_all_animes():
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()
    cur.execute("""
      SELECT * FROM animes
    """)
    getting_data = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()

    processed_data = [Animes(fetched_animes).__dict__ for fetched_animes in getting_data]
    
    return processed_data


  @staticmethod
  def get_specific_anime(anime_id):
   
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()
    cur.execute('SELECT * FROM animes WHERE id=(%s);', (anime_id, ))
    fetched_result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if not fetched_result:
      return {}
    return Animes(fetched_result).__dict__


  @staticmethod
  def delete(anime_id):
        
    conn = psycopg2.connect(**configs)
    cur = conn.cursor()

    cur.execute(""" DELETE FROM
                        animes
                    WHERE
                        id=(%s)
                    RETURNING *;""", (anime_id, ))

    getting_data = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not getting_data:
      return False
    return True
    
    # if it exist return nothing and 204
    # if it does not exist return a dict, 404

    
  @staticmethod
  def update_anime(id, **kwargs):
    check_keys = Animes.checking_keys(**kwargs)
    if len(check_keys) == 0:  
      conn = psycopg2.connect(**configs)
      cur = conn.cursor()

      columns = [sql.Identifier(key) for key in kwargs.keys()]
      values = [sql.Literal(value) for value in kwargs.values()]
      query = sql.SQL(
          """
              UPDATE
                  animes
              SET
                  ({columns}) = row({values})
              WHERE
                  id={id}
              RETURNING *
          """).format(id=sql.Literal(str(id)),
                      columns=sql.SQL(',').join(columns),
                      values=sql.SQL(',').join(values))
      
      cur.execute(query)
      fetch_result = cur.fetchone()
      conn.commit()
      cur.close()
      conn.close()

      if not fetch_result:
          return {}
      
      serialized_data = Animes(fetch_result).__dict__

      return serialized_data
    else:
      return check_keys, 422

  # def save(self):

  #     conn = psycopg2.connect(**configs)
  #     cur = conn.cursor()

  #     columns = [sql.Identifier(key) for key in self.__dict__.keys()]
  #     values = [sql.Literal(value) for value in self.__dict__.values()]

  #     query = sql.SQL(
  #         """
  #             INSERT INTO
  #                 animes (id, {columns})
  #             VALUES
  #                 (DEFAULT, {values})
  #             RETURNING *
  #         """).format(columns=sql.SQL(',').join(columns),
  #                     values=sql.SQL(',').join(values))

  #     print(query.as_string(cur))
      
  #     cur.execute(query)

  #     fetch_result = cur.fetchone()
    
  #     conn.commit()
  #     cur.close()
  #     conn.close()
      
  #     serialized_data = Animes(fetch_result).__dict__

  #     return serialized_data


  # if keys are invalid return a list with the valid_keys and a list with the invalid_keys in a dict, 422
  # if the id exists the key anime should be save with title() and return a dict with the updated data, 200
  # if the anime or table does not exist return an empty dict and 404