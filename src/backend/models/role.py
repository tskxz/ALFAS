from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
