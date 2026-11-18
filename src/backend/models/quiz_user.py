from db import db
from sqlalchemy.dialects.mysql import BIGINT


class QuizUser(db.Model):
    __tablename__ = "quiz_user"

    id = db.Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    grade = db.Column(db.Numeric(5, 2), nullable=False)
    grade_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    quiz_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey("quizzes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
