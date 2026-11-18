from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Gender(db.Model):
    __tablename__ = "genders"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    gender = db.Column(db.String(50), nullable=False)
