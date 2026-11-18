from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Userstate(db.Model):
    __tablename__ = "userstates"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    state = db.Column(db.String(50), nullable=False)
