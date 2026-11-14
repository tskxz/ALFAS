from datetime import date, datetime
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    gender_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("genders.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    schoolyear_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("schoolyears.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    birth_date = db.Column(db.Date, nullable=False)
    parental_consent = db.Column(
        db.Boolean, nullable=False, default=False, server_default=db.false()
    )
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    img_url = db.Column(db.String(500), nullable=True, default=None)
    email_verified_at = db.Column(db.TIMESTAMP, nullable=True, default=None)
    password = db.Column(db.String(255), nullable=False)
    remember_token = db.Column(db.String(100), nullable=True, default=None)
    userstate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("userstates.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )