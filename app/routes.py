from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app.model.user_dao import UserDao
from app.model.movie_dao import MovieDao
from app.model.movie import Movie
from app.model.user import User

userDAO = UserDao()
movieDAO = MovieDao()

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
  return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
  user = userDAO.find(request.form['username'])
  if user is None:
    return render_template('index.html', error="Inexistent user.")

  if user.password != request.form['password']:
    return render_template('index.html', error="Incorrect password.")

  login_user(user)
  flash('You were successfully logged in')
  return redirect(url_for('main.main'))


@bp.route('/main')
#@login_required
def main():
  return render_template('main.html')


@bp.route('/logout')
#@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))


@bp.route('/movie', methods=['GET', 'POST'])
#@login_required
def movie():
  if request.method == "GET":
    return render_template('movie.html')
  elif request.method == "POST":
    movie = Movie(None, request.form['moviename_field'],
                  int(request.form['year_field']))
    movieDAO.add(movie)
    return redirect(url_for('main.main'))
  else:
    return redirect(url_for('main.main'))


@bp.route('/del_movie', methods=['GET'])
#@login_required
def del_movie():
  iid = request.args.get('id')
  if iid:
    movieDAO.delete(iid)
    flash('Movie was removed!')
  return redirect(url_for('main.main'))


@bp.route('/movies')
#@login_required
def movies():
  movies = []
  for m in movieDAO.get_all():
    movies.append({"id": m.id, "name": m.name, "year": m.year})
  return render_template('movies.html', movies=movies)

@bp.route('/update_movie', methods=['GET', 'POST'])
#@login_required
def update_movie():
    if request.method == 'GET':
        # Se o método for GET, apenas renderiza o formulário de atualização
        return render_template('update.html')
    elif request.method == 'POST':
        # Processa a atualização do filme aqui
        movie_name = request.form['moviename_field']
        movie_year = request.form['year_field']
        # Você precisa de um campo escondido no formulário ou de algum método para determinar qual filme atualizar
        movie_id = request.form['movie_id']

        # Cria um objeto Movie com os dados do formulário
        movie = Movie(movie_id, movie_name, int(movie_year))

        # Atualiza o filme no banco de dados
        movieDAO.update(movie)

        # Redireciona para a página principal ou para onde você achar mais adequado
        flash('Movie updated successfully!')
        return redirect(url_for('main.main'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Validar os campos, incluindo se as senhas coincidem e se o usuário já existe
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
        if userDAO.find(username) is not None:
            return render_template('register.html', error="Username already exists.")

        # Criar novo usuário
        newUser = User(username, password)
        userDAO.add(newUser)
        # Redirecionar para a página de login ou onde preferir
        return redirect(url_for('main.index'))
    else:
        return render_template('register.html')