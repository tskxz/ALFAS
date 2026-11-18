from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Resourcetype(db.Model):
    __tablename__ = "resourcetypes"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
