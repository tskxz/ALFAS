from db import db
from sqlalchemy.dialects.mysql import BIGINT


class ResourcelevelUser(db.Model):
    __tablename__ = "resourcelevel_user"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("users.id"),
        nullable=False,
    )
    resourcelevel_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("resourcelevels.id"),
        nullable=False,
    )
    progress = db.Column(db.Numeric(5, 2), nullable=False, default=0, server_default="0.00")
