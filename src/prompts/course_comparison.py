from prompts.registry import PromptArgumentDefinition, PromptDefinition


def course_comparison_template(course_code_1: str, course_code_2: str) -> str:
    return (
        f"Create a detailed comparison between {course_code_1} and {course_code_2}.\n\n"
        "Include:\n"
        "- Title\n"
        "- Credits\n"
        "- Description\n"
        "- Prerequisites\n"
        "- Department\n"
        "- Instructor\n"
    )


PROMPT_DEFINITION = PromptDefinition(
    name="course_comparison_template",
    description="Compare two courses across core catalog details.",
    arguments=[
        PromptArgumentDefinition(
            name="course_code_1",
            description="First course code (e.g., CS201).",
            required=True,
        ),
        PromptArgumentDefinition(
            name="course_code_2",
            description="Second course code (e.g., CS301).",
            required=True,
        ),
    ],
    handler=course_comparison_template,
)
