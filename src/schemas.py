from pydantic import BaseModel, ConfigDict, Field


class SearchCoursesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=1)
    department_code: str | None = None


class CourseSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_code: str
    title: str
    credits: int


class SearchCoursesResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    results: list[CourseSummary]


class GetPrerequisitesInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_code: str = Field(..., min_length=2)


class PrerequisiteCourse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_code: str
    title: str


class PrerequisiteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_code: str
    prerequisites: list[PrerequisiteCourse]


class LookupInstructorInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instructor_name: str = Field(..., min_length=2)


class InstructorLookupResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    email: str | None = None
    department_name: str | None = None
    error: str | None = None


class PrerequisiteGraphInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    course_code: str = Field(..., min_length=2)


class GraphNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str


class GraphEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    target: str


class GraphResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nodes: list[GraphNode]
    edges: list[GraphEdge]
