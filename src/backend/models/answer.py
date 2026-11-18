from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    answer = db.Column(db.Text, nullable=False)
    question_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("questions.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    correct = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    qastate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("qastates.id"),
        nullable=False,
    )
