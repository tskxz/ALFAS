from db import db
from sqlalchemy.dialects.mysql import BIGINT


class ResourceUser(db.Model):
    __tablename__ = "resource_user"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    resource_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("resources.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    favorite = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    started_at = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    completed_at = db.Column(db.DateTime, nullable=True)
    certificate_code = db.Column(db.String(100), nullable=True, unique=True)
