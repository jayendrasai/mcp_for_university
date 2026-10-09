from pydantic import TypeAdapter
from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from database import get_session
from models import Course, Department
from schemas import CourseSummary, SearchCoursesInput, SearchCoursesResponse
from tools.registry import ToolDefinition


def search_courses(input: SearchCoursesInput) -> SearchCoursesResponse:
    query_text = f"%{input.query.strip()}%"
    with get_session() as session:
        stmt = select(Course).options(joinedload(Course.department))
        if input.department_code:
            stmt = stmt.join(Department).where(Department.code == input.department_code)
        stmt = stmt.where(
            or_(
                Course.title.ilike(query_text),
                Course.description.ilike(query_text),
            )
        )
        courses = session.execute(stmt).scalars().all()

    results = [
        CourseSummary(
            course_code=course.course_code,
            title=course.title,
            credits=course.credits,
        )
        for course in courses
    ]
    return SearchCoursesResponse(results=results)


TOOL_DEFINITION = ToolDefinition(
    name="search_courses",
    description="Search courses by keyword and optional department code.",
    input_model=SearchCoursesInput,
    output_schema=TypeAdapter(SearchCoursesResponse).json_schema(),
    handler=search_courses,
)
