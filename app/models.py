from flask_security import current_user
from sqlalchemy import Table, Column, Integer, ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.core import db

Base = db.Model

sounds_boards = Table('sounds_boards', Base.metadata,
    Column('sound_id', Integer, ForeignKey('sound.id')),
    Column('board_id', Integer, ForeignKey('board.id'))
)


sounds_tags = Table('sounds_tags', Base.metadata,
    Column('sound_id', Integer, ForeignKey('sound.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Sound(Base):
    __tablename__ = 'sound'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(500))
    icon = Column(String(500))
    soundfile = Column(String(500))
    count = Column(BigInteger, default=0)
    enabled = Column(Boolean, default=False)
    hidden = Column(Boolean, default=False)
    boards = relationship(
        "Board",
        secondary=sounds_boards,
        back_populates="sounds")
    tags = relationship(
        "Tag",
        secondary=sounds_tags,
        back_populates="sounds")

    def get_all():
        # if current_user.has_role("spezial") geht nicht
        sounds = None
        for r in current_user.roles:
            if str(r.name) == "spezial":
                sounds = Sound.query.all()
                break
        if not sounds:
            sounds = Sound.query.filter_by(enabled=True).all()
        return sounds

    def get_charts():
        sounds = Sound.query.filter(Sound.enabled == True, Sound.hidden == False, Sound.count > 10).order_by(Sound.count.desc()).limit(24)
        return sounds

    def get_sound(index):
        sound = None
        for r in current_user.roles:
            if str(r.name) == "spezial":
                sound = Sound.query.filter_by(id=index).first()
                break
        if not sound:
            sound = Sound.query.filter(Sound.enabled==True, Sound.id==index).first()
        return sound

    def get_sounds(sounds_list):
        sounds = None
        for r in current_user.roles:
            if str(r.name) == "spezial":
                sounds = Sound.query.filter(Sound.id.in_(sounds_list)).all()
                break
        if not sounds:
            sounds = Sound.query.filter(Sound.id.in_(sounds_list), Sound.enabled == True).all()
        return sounds



class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(500))
    icon = Column(String(500))
    sounds = relationship(
        "Sound",
        secondary=sounds_boards,
        back_populates="boards")


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag = Column(String(80), unique=True, nullable=False)
    tag_lower = Column(String(80), unique=True, nullable=False)
    sounds = relationship(
        "Sound",
        secondary=sounds_tags,
        back_populates="tags")
