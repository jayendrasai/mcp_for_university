from sqlalchemy import select

from database import get_session
from models import Department
from resources.registry import ResourceDefinition


def department_directory() -> str:
    with get_session() as session:
        departments = (
            session.execute(select(Department).order_by(Department.code))
            .scalars()
            .all()
        )

    lines = [f"{dept.name} ({dept.code})" for dept in departments]
    return "\n".join(lines)


RESOURCE_DEFINITION = ResourceDefinition(
    uri="catalog://department-directory",
    name="department_directory",
    description="Directory of academic departments.",
    mime_type="text/plain",
    read=department_directory,
)
