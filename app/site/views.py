import os
import sys
from flask import Blueprint, render_template, request, current_app, flash
from werkzeug.utils import secure_filename
from app import db
from app.core import remove_html
from app.models import Board, Sound

mod_site = Blueprint('site', __name__, template_folder='templates', static_folder='static/site')


@mod_site.before_app_first_request
def init_my_blueprint():
    if not Board.query.filter_by(name="beste").first():
        # BOARDS
        beste = Board(name="beste")
        db.session.add(beste)
        tilo = Board(name="Tilo")
        db.session.add(tilo)
        stefan = Board(name="Stefan")
        db.session.add(stefan)
        jingles = Board(name="Jingles")
        db.session.add(jingles)
        alle = Board(name="alle")
        db.session.add(alle)

        # SOUNDS
        sound = Sound(name="45€", description="Riesenrad gefahren und schön Puffjes gegessen", soundfile='sounds/45_uebern_schnitt.ogg', enabled=True)
        db.session.add(sound)
        beste.sounds.append(sound)
        alle.sounds.append(sound)

        sound = Sound(name="AKK ndhs 1", description="", soundfile='sounds/akk_ndhs_1.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="AKK ndhs 2", description="", soundfile='sounds/akk_ndhs_2.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="AKK ndhs 3", description="japan?", soundfile='sounds/akk_ndhs_3.ogg', enabled=True)
        db.session.add(sound)
        beste.sounds.append(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Zunichte gerammelt", description="deutsches Reich und Europa", soundfile='sounds/zunichte_gerammelt.ogg', enabled=True)
        db.session.add(sound)
        beste.sounds.append(sound)
        alle.sounds.append(sound)

        sound = Sound(name="Toller Nachmittag", description="Gottkanzler Schulz", soundfile='sounds/schulz_toller_nachmittag.ogg', enabled=True)
        db.session.add(sound)

        sound = Sound(name="Jingle Tyler", description="Was ist der größte gemeinsame Tyler", soundfile='sounds/gemeinsamer_tyler.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        jingles.sounds.append(sound)
        tilo.sounds.append(sound)

        sound = Sound(name="Jingle Hans-Jessen-Show", description="instrumental", soundfile='sounds/hans_jessen_show.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        jingles.sounds.append(sound)
        tilo.sounds.append(sound)

        sound = Sound(name="Joint rauchen", description="", soundfile='sounds/fdp_alte_joint_geraucht.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Demokrat Hoeneß", description="", soundfile='sounds/grosser_demokrat.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        beste.sounds.append(sound)
        
        sound = Sound(name="Herzlichen Dank und Deutschland alles Gute", description="", soundfile='sounds/herzlichen_dank_deutschland_alles_gute.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        beste.sounds.append(sound)
        
        sound = Sound(name="Herzlichen Dank", description="", soundfile='sounds/herzlichen_dank.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Entschuldigung", description="Andrea Nahles", soundfile='sounds/nahles_entschuldigung.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        beste.sounds.append(sound)
        
        sound = Sound(name="Klasse!", description="Marin Schulz", soundfile='sounds/schulz_klasse.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Tschüss zusammen", description="Marin Schulz", soundfile='sounds/schulz_tschuess_zusammen.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Tagesschau und Tagesthemen informieren Sie", description="", soundfile='sounds/tagesschau_und_tagesthemen.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        
        sound = Sound(name="Wir kümmern uns", description="", soundfile='sounds/wir_kuemmern_uns.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        beste.sounds.append(sound)
        
        sound = Sound(name="Wolf soll im Wald bleiben", description="", soundfile='sounds/wolf_bleibt_im_wald.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)
        beste.sounds.append(sound)
        
        sound = Sound(name="You are on your own", description="", soundfile='sounds/you_are_on_your_own.ogg', enabled=True)
        db.session.add(sound)
        alle.sounds.append(sound)

        db.session.commit()
    
    print("init done")



@mod_site.route('/')
def home():
    boards = Board.query.all()
    board = Board.query.filter_by(name="beste").first()
    return render_template('site/index.html', board=board, boards=boards)


@mod_site.route('/board/<board>')
def board(board):
    boards = Board.query.all()
    board = Board.query.filter_by(id=board).first()
    return render_template('site/index.html', board=board, boards=boards)


@mod_site.route('/create_board')
def create_board():
    boards = Board.query.all()
    return render_template('site/create_board.html', board=None, boards=boards)


@mod_site.route('/soundspende/submit', methods=["POST"])
def soundspende_submit():
    name = remove_html(request.form['name'])
    description = remove_html(request.form['description'])
    soundfile = request.files['soundfile']

    # save file
    filename = secure_filename(soundfile.filename)
    db_filename = "sounds/" + filename
    filename = os.path.join(current_app.config['SOUNDS_DIR'], filename)
    soundfile.save(filename)

    # add to database
    new_sound = Sound(name=name, description=description, soundfile=db_filename)
    db.session.add(new_sound)
    db.session.commit()

    flash('Soundfile übertragen, dankeschön.', 'success')
    return "1"
