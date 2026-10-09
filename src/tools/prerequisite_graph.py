from pydantic import TypeAdapter

from database import get_session
from schemas import GraphEdge, GraphNode, GraphResponse, PrerequisiteGraphInput
from tools.registry import ToolDefinition
from utils.graph_utils import build_prerequisite_graph


def get_prerequisite_graph(input: PrerequisiteGraphInput) -> GraphResponse:
    with get_session() as session:
        graph = build_prerequisite_graph(session, input.course_code)

    nodes = [GraphNode(id=node_id) for node_id in graph.nodes()]
    edges = [GraphEdge(source=edge[0], target=edge[1]) for edge in graph.edges()]
    return GraphResponse(nodes=nodes, edges=edges)


TOOL_DEFINITION = ToolDefinition(
    name="get_prerequisite_graph",
    description="Build a prerequisite graph for a course.",
    input_model=PrerequisiteGraphInput,
    output_schema=TypeAdapter(GraphResponse).json_schema(),
    handler=get_prerequisite_graph,
)
