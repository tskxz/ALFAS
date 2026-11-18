from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    healtharea_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("healthareas.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    resourcetype_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("resourcetypes.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    resourcestate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("resourcestates.id"),
        nullable=False,
    )
    img_url = db.Column(db.String(500), nullable=True)
    badge_url = db.Column(db.String(500), nullable=True)
