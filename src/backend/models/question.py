from db import db
from sqlalchemy.dialects.mysql import BIGINT, INTEGER


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("quizzes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    qastate_id = db.Column(
        INTEGER(unsigned=True),
        db.ForeignKey("qastates.id"),
        nullable=False,
    )
