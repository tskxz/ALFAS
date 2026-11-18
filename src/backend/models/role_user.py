from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class RoleUser(db.Model):
    __tablename__ = "role_user"

    role_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
