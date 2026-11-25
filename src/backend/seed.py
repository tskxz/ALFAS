from datetime import date, datetime, timedelta

from werkzeug.security import generate_password_hash

from db import db
from models import (
    User,
    Role,
    RoleUser,
    Gender,
    Schoolyear,
    Userstate,
    Healtharea,
    Resourcetype,
    Resourcestate,
    Resource,
    Resourcelevel,
    Quiz,
    Question,
    Answer,
    QuizUser,
    Quiztype,
    Qastate,
    ResourceUser,
    ResourcelevelUser,
    Activity,
    Content,
    Contenttype,
    News,
)

from app import app


def seed_database():
    print("Starting database seed...")

    # =========================
    # ROLES
    # =========================
    roles = ["Administrator", "Content Manager", "Registado"]

    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            db.session.add(Role(name=role_name))

    # =========================
    # GENDERS
    # =========================
    genders = ["Feminino", "Masculino", "Outro"]

    for gender_name in genders:
        if not Gender.query.filter_by(gender=gender_name).first():
            db.session.add(Gender(gender=gender_name))

    # =========================
    # SCHOOL YEARS
    # =========================
    schoolyears = [
        "1.º ano",
        "2.º ano",
        "3.º ano",
        "4.º ano",
        "5.º ano",
        "6.º ano",
        "7.º ano",
        "8.º ano",
        "9.º ano",
        "10.º ano",
        "11.º ano",
        "12.º ano",
        "Licenciatura",
        "Mestrado",
        "CTeSP",
    ]

    for schoolyear_name in schoolyears:
        if not Schoolyear.query.filter_by(schoolyear=schoolyear_name).first():
            db.session.add(Schoolyear(schoolyear=schoolyear_name))

    # =========================
    # USER STATES
    # =========================
    userstates = ["Ativo", "Pendente", "Inativo"]

    for state_name in userstates:
        if not Userstate.query.filter_by(state=state_name).first():
            db.session.add(Userstate(state=state_name))

    # =========================
    # RESOURCE STATES
    # =========================
    resourcestates = ["Publicado", "Rascunho", "Arquivado"]

    for state_name in resourcestates:
        if not Resourcestate.query.filter_by(state=state_name).first():
            db.session.add(Resourcestate(state=state_name))

    # =========================
    # RESOURCE TYPES
    # =========================
    resourcetypes = ["Workshop", "Webinar", "Artigo", "Vídeo", "Curso"]

    for type_name in resourcetypes:
        if not Resourcetype.query.filter_by(type=type_name).first():
            db.session.add(Resourcetype(type=type_name))

    # =========================
    # QUIZ TYPES
    # =========================
    quiztypes = ["Diagnóstico", "Avaliação", "Final"]

    for type_name in quiztypes:
        if not Quiztype.query.filter_by(type=type_name).first():
            db.session.add(Quiztype(type=type_name))

    # =========================
    # QA STATES
    # =========================
    qastates = ["Publicado", "Rascunho"]

    for state_name in qastates:
        if not Qastate.query.filter_by(state=state_name).first():
            db.session.add(Qastate(state=state_name))

    # =========================
    # CONTENT TYPES
    # =========================
    contenttypes = ["Artigo", "Vídeo", "Infográfico", "PDF"]

    for type_name in contenttypes:
        if not Contenttype.query.filter_by(type=type_name).first():
            db.session.add(Contenttype(type=type_name))

    db.session.commit()

    print("Base data inserted successfully!")

    print("Seed completed!")


if __name__ == "__main__":
    with app.app_context():
        seed_database()