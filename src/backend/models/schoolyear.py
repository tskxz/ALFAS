from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Schoolyear(db.Model):
    __tablename__ = "schoolyears"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    schoolyear = db.Column(db.String(50), nullable=False)
