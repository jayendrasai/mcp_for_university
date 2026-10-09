from database import get_session
from models import Course, Department, Instructor


def seed_database() -> None:
    with get_session() as session:
        if session.query(Department).first():
            return

        cs = Department(name="Computer Science", code="CS")
        math = Department(name="Mathematics", code="MATH")
        ee = Department(name="Electrical Engineering", code="EE")
        session.add_all([cs, math, ee])
        session.flush()

        instructors = [
            Instructor(
                name="Dr. Maya Reynolds",
                email="mreynolds@university.edu",
                office="CS-402",
                department=cs,
            ),
            Instructor(
                name="Prof. James Patel",
                email="jpatel@university.edu",
                office="CS-310",
                department=cs,
            ),
            Instructor(
                name="Dr. Elena Rossi",
                email="erossi@university.edu",
                office="MATH-210",
                department=math,
            ),
            Instructor(
                name="Prof. David Chen",
                email="dchen@university.edu",
                office="EE-115",
                department=ee,
            ),
            Instructor(
                name="Dr. Sara Alvarez",
                email="salvarez@university.edu",
                office="EE-220",
                department=ee,
            ),
        ]
        session.add_all(instructors)
        session.flush()

        courses = {
            "CS101": Course(
                course_code="CS101",
                title="Intro to Programming",
                description="Programming fundamentals in Python, including control flow, functions, and data structures.",
                credits=4,
                instructor=instructors[0],
                department=cs,
            ),
            "CS201": Course(
                course_code="CS201",
                title="Data Structures",
                description="Core data structures, algorithmic analysis, and implementation techniques.",
                credits=4,
                instructor=instructors[1],
                department=cs,
            ),
            "CS301": Course(
                course_code="CS301",
                title="Algorithms",
                description="Design and analysis of algorithms including sorting, graph algorithms, and optimization.",
                credits=4,
                instructor=instructors[1],
                department=cs,
            ),
            "CS315": Course(
                course_code="CS315",
                title="Operating Systems",
                description="Processes, scheduling, memory management, and file systems.",
                credits=4,
                instructor=instructors[0],
                department=cs,
            ),
            "CS330": Course(
                course_code="CS330",
                title="Database Systems",
                description="Relational modeling, SQL, indexing, and transaction management.",
                credits=3,
                instructor=instructors[0],
                department=cs,
            ),
            "MATH101": Course(
                course_code="MATH101",
                title="Calculus I",
                description="Limits, derivatives, and integrals with applications to engineering and science.",
                credits=4,
                instructor=instructors[2],
                department=math,
            ),
            "MATH201": Course(
                course_code="MATH201",
                title="Linear Algebra",
                description="Vector spaces, matrices, eigenvalues, and linear transformations.",
                credits=3,
                instructor=instructors[2],
                department=math,
            ),
            "MATH240": Course(
                course_code="MATH240",
                title="Discrete Mathematics",
                description="Logic, sets, combinatorics, graph theory, and proofs.",
                credits=3,
                instructor=instructors[2],
                department=math,
            ),
            "EE101": Course(
                course_code="EE101",
                title="Circuit Analysis",
                description="DC/AC circuit analysis, circuit laws, and basic components.",
                credits=4,
                instructor=instructors[3],
                department=ee,
            ),
            "EE201": Course(
                course_code="EE201",
                title="Signals and Systems",
                description="Signal representations, LTI systems, and frequency domain analysis.",
                credits=4,
                instructor=instructors[4],
                department=ee,
            ),
        }
        session.add_all(courses.values())
        session.flush()

        courses["CS201"].prerequisites.append(courses["CS101"])
        courses["CS301"].prerequisites.append(courses["CS201"])
        courses["CS315"].prerequisites.append(courses["CS201"])
        courses["CS330"].prerequisites.append(courses["CS201"])
        courses["MATH201"].prerequisites.append(courses["MATH101"])
        courses["MATH240"].prerequisites.append(courses["MATH101"])
        courses["EE201"].prerequisites.append(courses["EE101"])
