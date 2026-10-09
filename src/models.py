from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


prerequisites_table = Table(
    "prerequisites",
    Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("prerequisite_id", ForeignKey("courses.id"), primary_key=True),
)


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    instructors: Mapped[list["Instructor"]] = relationship(
        "Instructor", back_populates="department"
    )
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="department")


class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False)
    office: Mapped[str] = mapped_column(String(100), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)

    department: Mapped["Department"] = relationship(
        "Department", back_populates="instructors"
    )
    courses: Mapped[list["Course"]] = relationship("Course", back_populates="instructor")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False)
    instructor_id: Mapped[int] = mapped_column(ForeignKey("instructors.id"), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)

    instructor: Mapped["Instructor"] = relationship(
        "Instructor", back_populates="courses"
    )
    department: Mapped["Department"] = relationship(
        "Department", back_populates="courses"
    )
    prerequisites: Mapped[list["Course"]] = relationship(
        "Course",
        secondary=prerequisites_table,
        primaryjoin=id == prerequisites_table.c.course_id,
        secondaryjoin=id == prerequisites_table.c.prerequisite_id,
        backref="dependents",
    )
