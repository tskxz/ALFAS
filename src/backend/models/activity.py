from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    activity_datetime = db.Column(db.DateTime, nullable=False)
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
