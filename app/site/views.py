from flask import Blueprint, render_template
from app.models import Board, Sound
from app import db

mod_site = Blueprint('site', __name__, template_folder='site_templates', static_folder='site_static')


@mod_site.before_app_first_request
def init_my_blueprint():
    print("init done")



@mod_site.route('/')
def home():
    boards = Board.query.all()
    board = Board.query.filter_by(name="beste").first()
    return render_template('index.html', board=board, boards=boards)


@mod_site.route('/board/<board>')
def board(board):
    boards = Board.query.all()
    board = Board.query.filter_by(id=board).first()
    return render_template('index.html', board=board, boards=boards)


@mod_site.route('/create_board')
def create_board():
    boards = Board.query.all()
    return render_template('create_board.html', board=None, boards=boards)
