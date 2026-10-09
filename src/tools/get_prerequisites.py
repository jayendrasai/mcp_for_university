from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_session
from models import Course
from schemas import GetPrerequisitesInput, PrerequisiteCourse, PrerequisiteResponse
from tools.registry import ToolDefinition


def get_prerequisites(input: GetPrerequisitesInput) -> PrerequisiteResponse:
    with get_session() as session:
        stmt = (
            select(Course)
            .options(selectinload(Course.prerequisites))
            .where(Course.course_code == input.course_code)
        )
        course = session.execute(stmt).scalar_one_or_none()
        if not course:
            return PrerequisiteResponse(course_code=input.course_code, prerequisites=[])

        prereqs = sorted(course.prerequisites, key=lambda item: item.course_code)
        return PrerequisiteResponse(
            course_code=course.course_code,
            prerequisites=[
                PrerequisiteCourse(course_code=pr.course_code, title=pr.title)
                for pr in prereqs
            ],
        )


TOOL_DEFINITION = ToolDefinition(
    name="get_prerequisites",
    description="Get direct prerequisites for a course.",
    input_model=GetPrerequisitesInput,
    output_schema=TypeAdapter(PrerequisiteResponse).json_schema(),
    handler=get_prerequisites,
)
