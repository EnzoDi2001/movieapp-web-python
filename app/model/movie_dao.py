from app.model.movie import Movie
from app.model.database import Database


class MovieDao:

  def get_all(self):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, year FROM movie;")
    movies = []
    for row in cursor.fetchall():
      movies.append(Movie(row[0], row[1], row[2]))

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return movies

  def add(self, movie):
    conn = Database.get_connection()
    cursor = conn.cursor()
    new_movie = (
        movie.name,
        movie.year,
    )
    cursor.execute("INSERT INTO movie (name, year) VALUES (?, ?);", new_movie)

    # Commit the changes to the database
    conn.commit()
    # Close the cursor and connection
    cursor.close()
    conn.close()

  def delete(self, iid):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movie WHERE id=?;", (iid, ))

    # Commit the changes to the database
    conn.commit()
    # Close the cursor and connection
    cursor.close()
    conn.close()

  def update(self, movie):
    """
    Atualiza os dados de um filme existente no banco de dados.
    :param movie: um objeto Movie contendo as novas informações e o id do filme a ser atualizado.
    """
    # Obter conexão com o banco de dados
    conn = Database.get_connection()
    cursor = conn.cursor()

    # Preparar os dados do filme para atualização
    updated_movie = (movie.name, movie.year, movie.id)

    # Executar a consulta de atualização
    cursor.execute("UPDATE movie SET name = ?, year = ? WHERE id = ?;", updated_movie)

    # Efetuar as mudanças no banco de dados
    conn.commit()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()