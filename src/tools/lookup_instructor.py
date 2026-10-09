from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import get_session
from models import Instructor
from schemas import InstructorLookupResult, LookupInstructorInput
from tools.registry import ToolDefinition


def lookup_instructor(input: LookupInstructorInput) -> InstructorLookupResult:
    name_query = f"%{input.instructor_name.strip()}%"
    with get_session() as session:
        stmt = (
            select(Instructor)
            .options(joinedload(Instructor.department))
            .where(Instructor.name.ilike(name_query))
        )
        instructor = session.execute(stmt).scalar_one_or_none()
        if not instructor:
            return InstructorLookupResult(error="Instructor not found")

        return InstructorLookupResult(
            name=instructor.name,
            email=instructor.email,
            department_name=instructor.department.name,
        )


TOOL_DEFINITION = ToolDefinition(
    name="lookup_instructor",
    description="Find instructor contact and department details by name.",
    input_model=LookupInstructorInput,
    output_schema=TypeAdapter(InstructorLookupResult).json_schema(),
    handler=lookup_instructor,
)
