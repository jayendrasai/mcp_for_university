from .course_descriptions import RESOURCE_DEFINITION as COURSE_DESCRIPTIONS
from .department_directory import RESOURCE_DEFINITION as DEPARTMENT_DIRECTORY
from .registry import ResourceDefinition


def get_resource_definitions() -> list[ResourceDefinition]:
    return [COURSE_DESCRIPTIONS, DEPARTMENT_DIRECTORY]
