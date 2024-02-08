from app.model.user import User
from app.model.database import Database


class UserDao:

  def find(self, login):
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM user WHERE name = ?;",
                   (login, ))
    row = cursor.fetchone()
    if row:
      user = User(row[0], row[1])
    else:
      user = None

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return user

  def add(self, user):
    """
    Adiciona um novo usuário ao banco de dados.
    :param user: Um objeto User contendo o nome de usuário e a senha.
    """
    conn = Database.get_connection()
    cursor = conn.cursor()
    # Certifique-se de que o hash da senha seja feito antes de chamar este método,
    # ou faça aqui se preferir.
    cursor.execute("INSERT INTO user (name, password) VALUES (?, ?);", (user.name, user.password))

    # Commit as mudanças para o banco de dados
    conn.commit()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()