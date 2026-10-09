from .get_prerequisites import TOOL_DEFINITION as GET_PREREQUISITES
from .lookup_instructor import TOOL_DEFINITION as LOOKUP_INSTRUCTOR
from .prerequisite_graph import TOOL_DEFINITION as PREREQUISITE_GRAPH
from .registry import ToolDefinition
from .search_courses import TOOL_DEFINITION as SEARCH_COURSES


def get_tool_definitions() -> list[ToolDefinition]:
    return [
        SEARCH_COURSES,
        GET_PREREQUISITES,
        LOOKUP_INSTRUCTOR,
        PREREQUISITE_GRAPH,
    ]
