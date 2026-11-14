from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class News(db.Model):
    __tablename__ = "news"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(150), nullable=False)
    news_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    img_url = db.Column(db.String(500), nullable=True)
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
