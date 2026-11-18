from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Content(db.Model):
    __tablename__ = "contents"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(500), nullable=True)
    healtharea_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("healthareas.id"),
        nullable=False,
    )
    resourcestate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("resourcestates.id"),
        nullable=False,
    )
    contenttype_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("contenttypes.id"),
        nullable=False,
    )
