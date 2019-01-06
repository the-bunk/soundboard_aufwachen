import json
import os
import sys
import uuid
from flask import Blueprint, render_template, request, current_app, flash, make_response, redirect, Markup
from flask_security import login_required, roles_accepted
from werkzeug.utils import secure_filename
from app import db
from app.core import remove_html
from app.models import Board, Sound, Tag

mod_site = Blueprint('site', __name__, template_folder='templates', static_folder='static/site')





def get_userboards():
    userboards = []
    for c in request.cookies.items():
        if "board" in c[0]:
            cdata = json.loads(c[1])
            userboards.append(cdata)
    return userboards






@mod_site.before_app_first_request
def init_my_blueprint():
    def str2filename(mystr):
        return mystr.lower().replace(" ","_")

    if not Board.query.first():
    # if False:
        # BOARDS
        beste = Board(name="beste")
        db.session.add(beste)
        jingles = Board(name="Jingles")
        db.session.add(jingles)

        # SOUNDS
        los = [
                ["1 prozent club", "1", ""],
                ["45 uebern schnitt riesenrad gegessen", "", ""],
                ["akk compilation", "", ""],
                ["aufwachen quizshow blank", "1", ""],
                ["big time", "2", ""],
                ["billig ist nicht die antwort", "", ""],
                ["das ist gut fuer unser land", "2", ""],
                ["das kann nicht sein so", "2", ""],
                ["deutsche hymne aegypten", "2", ""],
                ["deutsche hymne amthor", "2", ""],
                ["find ich nicht gut", "2", ""],
                ["for the many not the few", "1", ""],
                ["fuer deutschland 1", "", ""],
                ["fuer deutschland compilation", "", ""],
                ["immer nachdenken", "2", ""],
                ["jobsegen", "1", ""],
                ["kein kuesschen", "2", ""],
                ["kohleausstieg nicht verkraften", "", ""],
                ["landwirte gesellschaft", "", ""],
                ["macron am firmament", "2", ""],
                ["merz alles dummes zeug", "", ""],
                ["merz heuschrecke", "", ""],
                ["nahles gebet", "2", ""],
                ["nahles gut fuer deutschland", "", ""],
                ["neustart fuer cdu deutschland", "", ""],
                ["nichts ist for free", "2", ""],
                ["planung in planung", "2", ""],
                ["radarschirm", "2", ""],
                ["richtig und wichtig 1", "", ""],
                ["sauberer diesel 1", "2", ""],
                ["sauberer diesel 2", "", ""],
                ["schulz gebet", "2", ""],
                ["seehofer raus", "", ""],
                ["nee ich kann nicht meckern", "", ""],
                ["terrorziege", "", ""],
                ["springend klingt die Muenze", "", ""],
                ["wer den Mund spitzt", "", "lindner_pfeift.ogg"],
                ["Die Verantwortung der Autohersteller", "", "verantwortung_der_autohersteller.ogg"],
                ["radikal krass cool", "", ""],
                ["Geburtstagswünsche von Seehofer", "", "seehofer_geburtstag.ogg"],
                ["der Verlierer ist die SPD", "", ""],
                ["wenn wir 15% haben dann stimmt was nicht", "", "nahles_15_prozent.ogg"],
                ["Junge du hast nichts kapiert", "", "steinmeier_nichts_kapiert.ogg"],
                ["Hört zu!", "", "steinmeier_hoert_zu.ogg"],
                ["gute Botschaft fuer unser Land", "", ""],
                ["I said: King we're protecting you!", "2", "trump_protecting_the_king.ogg"],
                ["Greta 1", "", "greta_1.ogg"],
                ["Greta 2", "", "greta_2.ogg"],
                ["ja", "", ""],
                ["Wirtschaftsmotor", "", "wirtschaftsmotor_ziehen.ogg"],
                ["die Furche weiterziehen", "", "schulz_furche.ogg"],
                ["Deutschland oder unser Land", "", "merkel_unser_land.ogg"],
                ["Geburtstagswünsche von Merkel", "", "merkel_geburtstag.ogg"],
                ["Feuer!", "", "feuer.ogg"],
                ["Waffenexportpolitik", "", ""],
                ["Danke Angela Merkel", "", ""],
                ["traurig", "2", ""],
                ["Arbeit Geißel der Menschheit", "", "arbeit_geissel_der_menschheit.ogg"],
                ["45€", "2", '45_uebern_schnitt.ogg'],
                ["AKK ndhs 1", "", 'akk_ndhs_1.ogg'],
                ["AKK ndhs 2", "", 'akk_ndhs_2.ogg'],
                ["AKK ndhs 3", "", 'akk_ndhs_3.ogg'],
                ["Zunichte gerammelt", "2", 'zunichte_gerammelt.ogg'],
                ["Toller Nachmittag", "2", 'schulz_toller_nachmittag.ogg'],
                ["Jingle Tyler", "1", 'gemeinsamer_tyler.ogg'],
                ["Jingle Hans-Jessen-Show", "1", 'hans_jessen_show.ogg'],
                ["Joint rauchen", "", 'fdp_alte_joint_geraucht.ogg'],
                ["Demokrat Hoeneß", "2", 'grosser_demokrat.ogg'],
                ["Herzlichen Dank und Deutschland alles Gute", "", 'herzlichen_dank_deutschland_alles_gute.ogg'],
                ["Herzlichen Dank", "", 'herzlichen_dank.ogg'],
                ["Entschuldigung", "2", 'nahles_entschuldigung.ogg'],
                ["Klasse!", "2", 'schulz_klasse.ogg'],
                ["Tschüss zusammen", "", 'schulz_tschuess_zusammen.ogg'],
                ["Tagesschau und Tagesthemen informieren Sie", "", 'tagesschau_und_tagesthemen.ogg'],
                ["Wir kümmern uns", "2", 'wir_kuemmern_uns.ogg'],
                ["Wolf soll im Wald bleiben", "", 'wolf_bleibt_im_wald.ogg'],
                ["You are on your own", "", 'you_are_on_your_own.ogg'],
                ["wolf1", "", ""]
                ]

        for s in los:
            if s[2] == "":
                s[2] = "{}.ogg".format(str2filename(s[0]))
            sound = Sound(name=s[0], soundfile="sounds/{}".format(s[2]), enabled=True)
            db.session.add(sound)
            if s[1] == "1":
                jingles.sounds.append(sound)
            elif s[1] == "2":
                beste.sounds.append(sound)
            db.session.commit()


        db.session.commit()
    
    print("site done")


@mod_site.before_request
def mod_site_before_request():
    # check Datenschutzcookie
    datenschutz = request.cookies.get('Datenschutz')
    if not datenschutz:
        flash(Markup('Information zum <a href="/datenschutz">Datenschutz</a>. <a href="#" onclick="datenschutzAccepted(); return false;">nicht mehr anzeigen</a>'), 'info')


@mod_site.route('/')
def home():
    # userboards = get_userboards()
    # boards = Board.query.all()
    # sounds = Sound.get_charts()
       
    # return render_template('site/charts.html', boards=boards, userboards=userboards, sounds=sounds, selected="charts")
    return redirect('/beste')


@mod_site.route('/datenschutz')
def datenschutz():
    # lade cookies, das ganze besser mit js clientseitig
    cookies = request.cookies.items()
    click_count = request.cookies.get('ClickCount')
    if click_count != 'false':
        click_count = 'true'
    # else:
    #     click_count = 'false'
    # click_count = 
    return render_template('site/datenschutz.html', click_count=click_count)


@mod_site.route('/datenschutz/accepted', methods=["GET"])
def datenschutz_accepted():
    ret = make_response(redirect("/"))
    ret.set_cookie('Datenschutz', "false")
    return ret


@mod_site.route('/click_count/<state>', methods=["GET"])
def click_count_set(state):
    ret = make_response(redirect("/datenschutz"))
    ret.set_cookie('ClickCount', state)
    return ret


@mod_site.route('/beste')
def charts():
    userboards = get_userboards()
    boards = Board.query.all()
    sounds = Sound.get_charts()
    return render_template('site/charts.html', boards=boards, userboards=userboards, sounds=sounds, selected="charts")


@mod_site.route('/spezial')
@login_required
@roles_accepted('spezial')
def spezial():
    userboards = get_userboards()
    boards = Board.query.all()
    board = Board.query.filter_by(name="spezial").first()
    return render_template('site/spezial.html', board=board, userboards=userboards, boards=boards)


@mod_site.route('/board/<board>')
def board(board):
    userboards = get_userboards()
    boards = Board.query.all()
    board = Board.query.filter_by(id=board).first()
    return render_template('site/index.html', board=board, userboards=userboards, boards=boards)


@mod_site.route('/userboard/<userboard>')
def userboard(userboard):
    sound=None
    userboards = get_userboards()
    for c in request.cookies.items():
        if c[0] == userboard:
            cdata = json.loads(c[1])
            selected = cdata['id']
            sounds = Sound.get_sounds(cdata['sounds'])
            break
    
    boards = Board.query.all()
    return render_template('site/userboard.html', sounds=sounds, boards=boards, userboards=userboards, selected=selected)


@mod_site.route('/search')
def search():
    userboards = get_userboards()
    boards = Board.query.all()
    sounds = Sound.get_all()
    return render_template('site/search_sound.html', sounds=sounds, boards=boards, userboards=userboards, selected="search")


@mod_site.route('/modal/soundspende', methods=["GET"])
def soundspende():
    tags = Tag.query.all()
    return render_template('site/includes/_modal_soundspende.html', tags=tags)


@mod_site.route('/modal/boards', methods=["GET"])
def boards():
    userboards = get_userboards()
    sounds = Sound.get_all()
    return render_template('site/includes/_modal_boards.html', sounds=sounds, userboards=userboards)


@mod_site.route('/userboard/submit', methods=["POST"])
def userboard_submit():
    data = request.get_json()
    name = data["name"]
    sounds = data["sounds"]

    # check if sounds are valid 
    print("sounds: {}".format(sounds))

    # neues board erstellen
    if not name:
        flash('Kein Name.', 'danger')

    flash('Board erstellt.', 'success')

    userboard_id = str(uuid.uuid4())
    userboard = { "name": str(name), "id": userboard_id, "sounds": sounds}
    ret = make_response(redirect("/"))
    ret.set_cookie('board{}'.format(userboard_id), json.dumps(userboard))
    return ret


@mod_site.route('/userboard/delete/<board_id>')
def userboard_delete(board_id):
    flash('Board gelöscht.', 'success')

    # ret = make_response(render_template('site/charts.html', boards=boards, userboards=userboards, sounds=sounds, selected="charts"))
    ret = make_response(redirect("/"))
    ret.set_cookie('board{}'.format(board_id), '', expires=0)
    return ret


@mod_site.route('/soundspende/submit', methods=["POST"])
def soundspende_submit():
    try:
        name = remove_html(request.form['name'])
        description = remove_html(request.form['description'])
        soundfile = request.files['soundfile']
        tags_str = request.form['tags'].split(',')
        tags_id = request.form['tags_id']
    except:
        flash('Fehlerhafte Daten.', 'danger')
        return "3"

    if not soundfile:
        flash('Keine Datei übertragen.', 'danger')
        return "2"
    if Sound.query.filter_by(name=name).first():
        flash('Dieser Name existiert bereits.', 'danger')
        return "1"

    # tags sammeln
    tags = []
    for t in tags_str:
        t = t.strip()
        if t.replace(" ","") == "":
            continue
        tag = Tag.query.filter_by(tag=t).first()
        if not tag:
            tag = Tag(tag=t, tag_lower=t.lower())
            db.session.add(tag)
            db.session.commit()
        tags.append(tag)
    for t in tags_id:
        tag = Tag.query.filter_by(id=t).first()
        if tag:
            tags.append(tag)

    # save file
    filename = secure_filename(soundfile.filename)
    db_filename = "sounds/" + filename
    filename = os.path.join(current_app.config['SOUNDS_DIR'], filename)
    soundfile.save(filename)

    # add to database
    new_sound = Sound(name=name, description=description, soundfile=db_filename)
    db.session.add(new_sound)
    db.session.commit()
    for t in tags:
        new_sound.tags.append(t)

    db.session.commit()

    flash('Soundfile übertragen, dankeschön.', 'success')
    return "0"


@mod_site.route('/board/submit', methods=["POST"])
def board_submit():
    data = request.get_json()
    name = data["name"]
    sounds = data["sounds"]

    # neues board erstellen
    if not name:
        flash('Kein Name.', 'danger')
        return "/admin/boards"

    # gibt es schon ein board mit diesem namen?
    # TODO
    if board:
        flash('Dieser Name existiert bereits.', 'danger')
        return "/admin/boards"

    # cookie für board erstellen
    # TODO
    # name
    # sounds
    for s in sounds:
        pass

    flash('Board erstellt.', 'success')

    return "/"


@mod_site.route('/clicked/<audio_id>', methods=["GET"])
def clicked_audio(audio_id):
    try:
        sound = Sound.query.filter_by(id=audio_id).first()
        sound.count += 1
        db.session.commit()
    except:
        # logger.debug("sound clicked count error")
        pass
    return "0"
