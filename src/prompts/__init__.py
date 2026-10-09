from .course_comparison import PROMPT_DEFINITION as COURSE_COMPARISON
from .registry import PromptDefinition


def get_prompt_definitions() -> list[PromptDefinition]:
    return [COURSE_COMPARISON]
