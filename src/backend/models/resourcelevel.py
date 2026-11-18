from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Resourcelevel(db.Model):
    __tablename__ = "resourcelevels"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    level = db.Column(INTEGER(unsigned=True), nullable=False, default=1, server_default="1")
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(500), nullable=True)
    pdf_url = db.Column(db.String(500), nullable=True)
    resource_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("resources.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    resourcestate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("resourcestates.id"),
        nullable=False,
    )
