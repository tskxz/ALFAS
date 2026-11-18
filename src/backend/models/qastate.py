from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Qastate(db.Model):
    __tablename__ = "qastates"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    state = db.Column(db.String(50), nullable=False)
