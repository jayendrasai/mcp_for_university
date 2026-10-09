from sqlalchemy import select

from database import get_session
from models import Course
from resources.registry import ResourceDefinition


def course_descriptions() -> str:
    with get_session() as session:
        courses = (
            session.execute(select(Course).order_by(Course.course_code))
            .scalars()
            .all()
        )

    lines = [
        f"[{course.course_code}] {course.title}: {course.description}"
        for course in courses
    ]
    return "\n".join(lines)


RESOURCE_DEFINITION = ResourceDefinition(
    uri="catalog://course-descriptions",
    name="course_descriptions",
    description="List of course descriptions.",
    mime_type="text/plain",
    read=course_descriptions,
)
