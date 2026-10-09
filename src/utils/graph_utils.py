from typing import Set

import networkx as nx
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Course


def build_prerequisite_graph(session: Session, course_code: str) -> nx.DiGraph:
    graph = nx.DiGraph()
    visited: Set[str] = set()

    def visit(code: str) -> None:
        if code in visited:
            return
        visited.add(code)

        stmt = (
            select(Course)
            .options(selectinload(Course.prerequisites))
            .where(Course.course_code == code)
        )
        course = session.execute(stmt).scalar_one_or_none()
        if not course:
            return

        graph.add_node(course.course_code)
        for prereq in course.prerequisites:
            graph.add_node(prereq.course_code)
            graph.add_edge(prereq.course_code, course.course_code)
            visit(prereq.course_code)

    visit(course_code)
    return graph
