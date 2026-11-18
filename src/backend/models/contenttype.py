from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Contenttype(db.Model):
    __tablename__ = "contenttypes"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)
