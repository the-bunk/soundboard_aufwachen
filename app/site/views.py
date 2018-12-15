from flask import Blueprint, render_template
from app.models import Board, Sound
from app import db

mod_site = Blueprint('site', __name__, template_folder='site_templates', static_folder='site_static')


@mod_site.before_app_first_request
def init_my_blueprint():
    # board = Board(name="beste")
    # db.session.add(board)
    # sound = Sound(name="45€", description="Riesenrad gefahren und schön Puffjes gegessen", soundfile='sounds/45_uebern_schnitt.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)

    # sound = Sound(name="AKK ausländisch 1", description="", soundfile='sounds/akk_ndhs_1.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)
    # sound = Sound(name="AKK ausländisch 2", description="", soundfile='sounds/akk_ndhs_2.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)
    # sound = Sound(name="AKK ausländisch 3", description="japan?", soundfile='sounds/akk_ndhs_3.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)

    # sound = Sound(name="Zunichte gerammelt", description="deutsches Reich und Europa", soundfile='sounds/zunichte_gerammelt.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)

    # sound = Sound(name="Toller Nachmittag", description="Gottkanzler Schulz", soundfile='sounds/schulz_toller_nachmittag.ogg')
    # db.session.add(sound)
    # board.sounds.append(sound)

    # db.session.commit()
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
