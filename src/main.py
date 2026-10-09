import logging
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI, Request
from pydantic import AnyUrl, BaseModel, ValidationError
from starlette.responses import Response

import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.sse import SseServerTransport

from config import get_settings
from database import init_db
from prompts import get_prompt_definitions
from resources import get_resource_definitions
from seed import seed_database
from tools import get_tool_definitions


settings = get_settings()


def configure_logging() -> None:
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


configure_logging()
logger = logging.getLogger("catalog_mcp")

server = Server(
    name="University Course Catalog",
    version="1.0.0",
)

tool_definitions = get_tool_definitions()
tool_registry = {tool.name: tool for tool in tool_definitions}

resource_definitions = get_resource_definitions()


def _normalize_uri(value: str) -> str:
    return value.rstrip("/")


@dataclass(frozen=True)
class ResourceContents:
    content: str | bytes
    mime_type: str | None = None
    meta: dict[str, Any] | None = None


resource_registry = {
    _normalize_uri(resource.uri): resource for resource in resource_definitions
}

prompt_definitions = get_prompt_definitions()
prompt_registry = {prompt.name: prompt for prompt in prompt_definitions}

notification_options = NotificationOptions()
initialization_options = server.create_initialization_options(
    notification_options=notification_options,
)

sse_transport = SseServerTransport("/messages")

app = FastAPI(title="University Course Catalog MCP Server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name=tool.name,
            description=tool.description,
            inputSchema=tool.input_model.model_json_schema(),
            outputSchema=tool.output_schema,
        )
        for tool in tool_definitions
    ]


def _serialize_tool_result(result: Any) -> dict[str, Any]:
    if isinstance(result, BaseModel):
        return result.model_dump()
    if isinstance(result, dict):
        return result
    raise ValueError(
        "Tool handlers must return a Pydantic model or dictionary structured result."
    )


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None):
    tool = tool_registry.get(name)
    if not tool:
        raise ValueError(f"Unknown tool: {name}")

    try:
        input_data = tool.input_model.model_validate(arguments or {})
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc

    result = tool.handler(input_data)
    return _serialize_tool_result(result)


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=AnyUrl(resource.uri),
            name=resource.name,
            description=resource.description,
            mimeType=resource.mime_type,
        )
        for resource in resource_definitions
    ]


@server.list_resource_templates()
async def list_resource_templates() -> list[types.ResourceTemplate]:
    return []


@server.read_resource()
async def read_resource(uri: AnyUrl):
    resource = resource_registry.get(_normalize_uri(str(uri)))
    if not resource:
        raise ValueError(f"Unknown resource: {uri}")
    return [
        ResourceContents(
            content=resource.read(),
            mime_type=resource.mime_type,
        )
    ]


@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name=prompt.name,
            description=prompt.description,
            arguments=[
                types.PromptArgument(
                    name=arg.name,
                    description=arg.description,
                    required=arg.required,
                )
                for arg in prompt.arguments
            ],
        )
        for prompt in prompt_definitions
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    prompt = prompt_registry.get(name)
    if not prompt:
        raise ValueError(f"Unknown prompt: {name}")

    provided_args = arguments or {}
    missing_args = [
        arg.name
        for arg in prompt.arguments
        if arg.required and not provided_args.get(arg.name)
    ]
    if missing_args:
        missing = ", ".join(missing_args)
        raise ValueError(f"Missing prompt arguments: {missing}")

    prompt_args = {
        arg.name: provided_args.get(arg.name, "") for arg in prompt.arguments
    }
    prompt_text = prompt.handler(**prompt_args)
    return types.GetPromptResult(
        description=prompt.description,
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_text),
            )
        ],
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/sse")
async def sse_endpoint(request: Request) -> Response:
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            initialization_options=initialization_options,
        )
    return Response()


app.mount("/messages", sse_transport.handle_post_message)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
    seed_database()
    logger.info("Database initialized and seeded if empty.")
