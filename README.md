# University Course Catalog MCP Server

## Project overview
This project is a production-ready MCP (Model Context Protocol) server for a university course catalog. It exposes catalog data via MCP tools, MCP resources, and MCP prompt templates on top of a FastAPI application.

## MCP explanation
MCP servers provide structured access to data and capabilities through tools, resources, and prompt templates. This server makes course data available to MCP clients so models can search courses, inspect prerequisites, and generate comparisons.

## Architecture
- FastAPI app with an embedded MCP low-level Server and SSE transport
- SQLite database with SQLAlchemy ORM models
- Seed data loaded automatically when the database is empty
- NetworkX used to build prerequisite graphs
- Dockerized runtime with a mounted data volume

## Setup steps (local)
1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --app-dir src --host 0.0.0.0 --port 8080`

## Docker usage
Start the full stack with:
```
docker-compose up --build
```

## MCP tools
### search_courses
Input:
```json
{
  "query": "data",
  "department_code": "CS"
}
```

### get_prerequisites
Input:
```json
{
  "course_code": "CS301"
}
```

### lookup_instructor
Input:
```json
{
  "instructor_name": "Reynolds"
}
```

### get_prerequisite_graph
Input:
```json
{
  "course_code": "CS301"
}
```

## MCP resources
- `course_descriptions`
- `department_directory`

## MCP prompt templates
- `course_comparison_template`

## Example natural language queries
- "Find introductory CS courses with 4 credits."
- "Show the prerequisite chain for CS301."
- "Who teaches Database Systems?"
- "Compare CS201 and CS301."

## API examples
Health check:
```
curl http://localhost:8080/health
```

## MCP transport endpoints
- SSE connect: `http://localhost:8080/sse`
- SSE message POST: `http://localhost:8080/messages`

## Testing instructions
- Run `docker-compose up --build` and confirm the health endpoint responds with status `ok`.
- Use the MCP Inspector to validate tools, resources, and prompt templates.

## MCP Inspector usage
1. Start the server locally or with Docker.
2. Open MCP Inspector and set the server URL to `http://localhost:8080/sse`.
3. Verify tools, resources, and prompts are visible.
