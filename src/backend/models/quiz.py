from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resource_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("resources.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    quiztype_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("quiztypes.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    qastate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("qastates.id"),
        nullable=False,
    )
