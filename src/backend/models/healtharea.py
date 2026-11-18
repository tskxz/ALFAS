from db import db
from sqlalchemy.dialects.mysql import INTEGER


class Healtharea(db.Model):
    __tablename__ = "healthareas"

    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(255), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    resourcestate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("resourcestates.id"),
        nullable=False,
    )
