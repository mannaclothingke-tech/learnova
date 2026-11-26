"""Course catalog: subjects, courses, units, and prerequisites."""

from copy import deepcopy
from curriculum import COURSE_ASSESSMENTS, PRACTICE
from history import STORIES

REFERENCE = {"url": "https://brilliant.org/courses/", "checked_on": "2026-11-25",
             "scope": "Public Topics page; not a complete lesson-level inventory."}

SUBJECTS = [
    {"id": "math", "title": "Mathematics", "description": "From quantities to calculus."},
    {"id": "history", "title": "Math history", "description": "Why each idea was invented, and how people reasoned their way to it."},
    {"id": "logic", "title": "Logic and puzzles", "description": "Reason, deduce, and find patterns."},
    {"id": "computing", "title": "Computer science", "description": "Turn ideas into algorithms and code."},
    {"id": "technology", "title": "Technology", "description": "Explore the systems behind everyday tools."},
    {"id": "data", "title": "Data and probability", "description": "Understand evidence and uncertainty."},
    {"id": "science", "title": "Science", "description": "Test explanations of the physical world."},
]

# Rows contain Learnova ID/title, reference slug/title, original objective, prerequisites.
TOPICS = [
    ("Math Foundations", "math", [
        ("fractions", "Fractions as quantities", "math-fundamentals", "Fractions",
         "Represent, compare, and combine fractions using equal-part models.", ["multiply-divide"]),
        ("first-equations", "First steps with equations", "pre-algebra", "Solving Equations",
         "Use inverse operations to find an unknown and check the result.", ["fractions"]),
        ("signed-numbers", "Numbers on both sides of zero", "negative-numbers", "Negative Numbers",
         "Model signed arithmetic as movement along a number line.", ["add-subtract"]),
        ("coordinate-geometry", "Geometry and coordinates", "coordinate-plane", "Coordinate Plane",
         "Build geometry from simple to complex: measurement, angles, points, distance, slopes, shapes, and polar coordinates.", ["signed-numbers", "fractions"]),
        ("percents", "Think in hundredths", "percentages", "Percents",
         "Connect fractions, decimals, and percentages in comparison problems.", ["fractions"]),
        ("proportions", "Scale and proportion", "proportional-relationships", "Proportional Reasoning",
         "Distinguish proportional relationships and solve them using unit rates.", ["fractions"]),
    ]),
    ("Algebra Fundamentals", "math", [
        ("linear-equations", "Expressions and equality", "linear-expressions-and-equations", "Linear Equations",
         "Translate situations into expressions and solve linear equations.", ["first-equations"]),
        ("coordinate-geometry", "Geometry on a grid", "coordinate-geometry", "Coordinate Geometry",
         "Use coordinates to calculate distances and explain geometric relationships.", ["signed-numbers"]),
        ("linear-relationships", "Lines tell a story", "linear-functions", "Linear Relationships",
         "Connect tables, graphs, and equations through slope and intercept.", ["linear-equations", "coordinate-geometry"]),
        ("powers-roots", "Powers and roots", "exponents-and-radicals", "Exponents and Radicals",
         "Explain exponent rules and use roots to reverse powers.", ["signed-numbers"]),
        ("visual-algebra", "See algebra work", "systems-of-equations", "Visual Algebra",
         "Use diagrams and intersecting lines to explain simultaneous constraints.", ["linear-relationships"]),
    ]),
    ("Intermediate Algebra", "math", [
        ("functions", "Inputs, outputs, and functions", "introduction-to-functions", "Introduction to Functions",
         "Decide whether a relation is a function and interpret its domain and range.", ["linear-relationships"]),
        ("linear-systems", "Solve connected equations", "linear-systems", "Linear Systems",
         "Compare substitution, elimination, and graphical solutions to linear systems.", ["linear-equations"]),
        ("quadratics", "Explore quadratic patterns", "quadratics", "Quadratics",
         "Connect a parabola's roots and vertex to its equation.", ["functions", "powers-roots"]),
        ("transformations", "Move a graph", "transformations", "Coordinate Transformations",
         "Predict how translation, reflection, and scaling change a graph.", ["functions"]),
        ("exponentials", "Growth by multiplication", "exponential-functions", "Exponential Functions",
         "Distinguish additive growth from multiplicative growth using tables and graphs.", ["functions", "powers-roots"]),
    ]),
    ("Advanced Algebra", "math", [
        ("trigonometry", "Angles and periodic change", "trigonometric-functions", "Trigonometric Functions",
         "Connect unit-circle coordinates to sine, cosine, and periodic graphs.", ["functions", "coordinate-geometry"]),
        ("polynomials", "Build with polynomial terms", "polynomials", "Polynomials",
         "Relate polynomial factors, roots, and end behavior.", ["quadratics"]),
        ("curves", "Equations describe curves", "equations-and-curves", "Equations and Curves",
         "Connect geometric definitions of conic sections to their equations.", ["quadratics", "coordinate-geometry"]),
        ("logarithms", "Undo exponential growth", "logarithms", "Logarithms",
         "Interpret logarithms as inverse exponents and solve growth equations.", ["exponentials"]),
        ("coordinate-geometry", "Coordinates by angle and distance", "polar-coordinate-plane", "Polar Coordinate Plane",
         "Convert between Cartesian and polar descriptions of a point.", ["coordinate-geometry"]),
        ("complex", "Numbers beyond the real line", "complex-plane", "Complex Numbers",
         "Represent complex arithmetic as movement and rotation in a plane.", ["powers-roots", "coordinate-geometry"]),
    ]),
    ("Calculus", "math", [
        ("limits", "Approach a value", "limits", "Limits",
         "Reason about limiting values from graphs, tables, and expressions.", ["functions"]),
        ("derivatives", "Measure instantaneous change", "derivatives", "Derivatives",
         "Connect secant slopes to derivatives and interpret rates in context.", ["limits"]),
        ("integrals", "Add up continuous change", "integrals", "Integrals",
         "Connect accumulated quantities, area estimates, and antiderivatives.", ["derivatives"]),
        ("vectors", "Quantities with direction", "vectors", "Vectors",
         "Use components, vector addition, and dot products to model directed quantities.", ["coordinate-geometry"]),
        ("matrices", "Transform with matrices", "matrices", "Matrices",
         "Use matrix multiplication to describe transformations and linear systems.", ["vectors", "linear-systems"]),
    ]),
    ("Logical Reasoning", "logic", [
        ("deduction", "Build a sound deduction", "logic-deduction", "Logic",
         "Separate assumptions from conclusions and justify a deduction.", []),
        ("truth-puzzles", "Reason through conflicting claims", "grid-logic", "Truth and Lies",
         "Use consistency constraints to resolve statements and grid puzzles.", ["deduction"]),
        ("digital-logic", "From truth tables to circuits", "digital-circuits", "Digital Circuits",
         "Translate Boolean expressions into gates and verify their truth tables.", ["deduction"]),
        ("formal-logic", "Make reasoning precise", "logical-languages", "Reasoning with Logic",
         "Translate claims into propositions and test implication and equivalence.", ["deduction"]),
    ]),
    ("Everyday Math", "math", [
        ("everyday-statistics", "Read numbers critically", "basic-math", "Everyday Statistics",
         "Compare summaries and identify misleading numerical claims.", []),
        ("chance", "Make sense of chance", "winning-with-probability", "Probability and Chance",
         "Compare outcomes using sample spaces and expected value.", ["fractions"]),
        ("coordinate-geometry", "Measure the world", "geometry-fundamentals", "Geometry and Measurement",
         "Choose units and calculate lengths, areas, and volumes from models.", ["fractions"]),
        ("everyday-algebra", "Model everyday decisions", "using-variables", "Real-World Algebra",
         "Choose variables and build equations for costs, rates, and constraints.", ["linear-equations"]),
    ]),
    ("Mind-Bending Math", "logic", [
        ("puzzle-habits", "Develop a puzzle habit", "puzzles-100", "100 Days of Puzzles",
         "Compare multiple strategies and explain why a puzzle solution works.", []),
        ("strategy", "Plan a winning strategy", "strategic-puzzles-long-set", "Strategy Puzzles",
         "Use invariants and backward reasoning to analyze strategic choices.", ["deduction"]),
        ("math-puzzles", "Discover mathematical patterns", "foundation-puzzles-long-set", "Math Puzzles",
         "Test conjectures using patterns, counterexamples, and small cases.", []),
        ("infinity", "Reason about the infinite", "infinity", "Infinity",
         "Compare infinite sets through one-to-one correspondences.", ["deduction"]),
        ("number-theory", "Explore divisibility", "basic-number-theory", "Number Theory",
         "Use primes, factors, and modular arithmetic to explain integer patterns.", []),
        ("coordinate-geometry", "Find structure in shapes", "basic-2d-geometry", "Geometric Thinking",
         "Use symmetry and decomposition to justify geometric relationships.", ["fractions"]),
        ("bayes", "Update a belief with evidence", "knowledge-and-uncertainty", "Bayesian Probability",
         "Distinguish prior and posterior probabilities using conditional evidence.", ["probability"]),
        ("contest-math", "Solve unfamiliar math problems", "math-competition-fundamentals", "Contest Math",
         "Choose and justify counting, algebraic, and geometric problem-solving strategies.", ["linear-equations", "number-theory", "coordinate-geometry"]),
    ]),
    ("Programming & CS", "computing", [
        ("code-thinking", "Think in instructions", "thinking-in-code", "Thinking in Code",
         "Trace sequences, conditions, and loops to predict program behavior.", []),
        ("code-variables", "Store and change values", "creative-coding", "Programming with Variables",
         "Track program state and use variables to describe changing values.", ["code-thinking"]),
        ("code-functions", "Compose reusable instructions", "pixel-pusher", "Programming with Functions",
         "Design functions with clear inputs, outputs, and reusable behavior.", ["code-variables"]),
        ("algorithmic-thinking", "Choose an algorithm", "algorithms-greedy-dp", "Algorithmic Thinking",
         "Compare greedy choices with solutions that reuse subproblem results.", ["code-functions"]),
        ("cs-foundations", "Understand algorithmic efficiency", "computer-science-algorithms", "Computer Science Fundamentals",
         "Compare search and sorting strategies by correctness and work required.", ["code-functions"]),
        ("ai-systems", "Understand language models", "how-llms-work", "How AI Works",
         "Explain token prediction, training, and limitations without treating output as fact.", []),
        ("neural-networks", "Build intuition for neural networks", "intro-neural-networks", "Introduction to Neural Networks",
         "Trace weighted inputs, activations, and training error in a small network.", ["functions"]),
    ]),
    ("Python", "computing", [
        ("python-basics", "Express ideas in Python", "thinking-in-python", "Thinking in Python",
         "Trace Python expressions, conditions, and loops with simple values.", []),
        ("python-functions", "Design Python functions", "functions-in-python", "Functions in Python",
         "Write and test functions with explicit parameters and return values.", ["python-basics"]),
        ("python-recursion", "Solve a smaller version", "recursion-in-python", "Recursion in Python",
         "Identify base cases and trace recursive calls to termination.", ["python-functions"]),
        ("python-algorithms", "Implement and compare algorithms", "algorithms-in-python", "Algorithms in Python",
         "Implement search and sorting with tests and reason about their cost.", ["python-functions", "cs-foundations"]),
        ("python-objects", "Model with Python objects", "objects-in-python", "Object-Oriented Programming in Python",
         "Use classes to keep state and behavior together with clear responsibilities.", ["python-functions"]),
        ("python-data", "Choose a Python data structure", "data-structures-in-python", "Data Structures in Python",
         "Choose lists, dictionaries, and sets by their operations and constraints.", ["python-basics"]),
    ]),
    ("Technology", "technology", [
        ("ai-systems", "Understand language models", "how-llms-work", "How AI Works",
         "Explain token prediction, training, and limitations without treating output as fact.", []),
        ("digital-logic", "From truth tables to circuits", "digital-circuits", "Digital Circuits",
         "Translate Boolean expressions into gates and verify their truth tables.", ["deduction"]),
        ("computers", "Follow information through a computer", "how-computers-work", "How Technology Works",
         "Explain how representation, memory, and processors cooperate.", ["digital-logic"]),
        ("search", "Find and rank information", "search-fundamentals", "Search Engines",
         "Explain indexing and ranking with small information-retrieval models.", ["cs-foundations"]),
        ("distributed-ledgers", "Understand distributed ledgers", "cryptocurrency", "Cryptocurrency",
         "Explain hashing, signatures, and consensus, including their limitations.", ["computers"]),
        ("quantum", "Explore quantum information", "quantum-computing", "Quantum Computing",
         "Distinguish bits from qubits and interpret simple measurement probabilities.", ["vectors", "probability"]),
    ]),
    ("Data Analysis", "data", [
        ("data-visuals", "See patterns in data", "visual-exploration", "Exploring Data Visually",
         "Choose plots and identify patterns, outliers, and misleading scales.", []),
        ("probability", "Build a probability model", "probability-fundamentals", "Probability in Data",
         "Use events and conditional probability to model uncertain observations.", ["fractions"]),
        ("classification", "Group and classify observations", "clustering--classification", "Clustering & Classification",
         "Distinguish labeled prediction from grouping and evaluate simple models.", ["data-visuals"]),
        ("regression", "Explain variation with a model", "explaining-variation", "Regression",
         "Fit and interpret a linear model while examining residuals and confounding.", ["linear-relationships", "data-visuals"]),
        ("prediction", "Predict with uncertainty", "probabilistic-prediction", "Predicting with Probability",
         "Interpret model probabilities and test calibration against observations.", ["probability"]),
    ]),
    ("Science", "science", [
        ("scientific-thinking", "Test a scientific explanation", "puzzle-science", "Scientific Thinking",
         "Design a fair test and distinguish observations from causal explanations.", []),
        ("circuits", "Follow current and voltage", "circuits", "Circuits",
         "Use circuit models to relate current, voltage, and resistance.", ["proportions"]),
        ("digital-logic", "From truth tables to circuits", "digital-circuits", "Digital Circuits",
         "Translate Boolean expressions into gates and verify their truth tables.", ["deduction"]),
        ("science-puzzles", "Reason with physical models", "science-puzzles-long-set", "Science Puzzles",
         "Use simplified physical models and test their assumptions against evidence.", ["scientific-thinking"]),
        ("quantum", "Explore quantum information", "quantum-computing", "Quantum Computing",
         "Distinguish bits from qubits and interpret simple measurement probabilities.", ["vectors", "probability"]),
    ]),
]

RELATED_LESSONS = {
    "fractions": ["fraction-sense"],
    "first-equations": ["balance"],
    "linear-equations": ["expressions", "balance"],
    "linear-relationships": ["slope", "intercepts", "models"],
    "everyday-algebra": ["expressions", "models"],
}


def _ordered(courses):
    """Assign a difficulty stage from the prerequisite chain and order simple to complex."""
    by_id = {course["id"]: course for course in courses}
    stages = {}

    def stage(cid):
        if cid not in stages:
            parents = by_id[cid]["prerequisites"]
            stages[cid] = 1 + max(stage(p) for p in parents) if parents else 0
        return stages[cid]

    for course in courses:
        course["stage"] = stage(course["id"])
        course["level"] = ("Beginner" if course["stage"] <= 4 else
                           "Intermediate" if course["stage"] <= 7 else "Advanced")
    subject_order = {subject["id"]: i for i, subject in enumerate(SUBJECTS)}
    return sorted(courses, key=lambda c: (subject_order[c["subject_id"]], c["stage"]))


def _courses():
    courses = [{
        "id": "counting-numbers", "subject_id": "math",
        "title": "Counting and number sense",
        "prerequisites": [], "topics": ["Beginner path"], "reference": None,
        "related_lesson_ids": [],
        "units": [
            {"id": "counting-start", "title": "Seeing and counting numbers",
             "objectives": ["Count and see numbers to 20 using ten-frames.",
                            "Read tens and ones in two-digit numbers."],
             "lesson_ids": ["num-count", "num-place"]},
            {"id": "counting-line", "title": "The number line",
             "objectives": ["Skip count by 2s, 5s, and 10s, and compare numbers on a number line."],
             "lesson_ids": ["num-line"]},
        ],
    }, {
        "id": "add-subtract", "subject_id": "math",
        "title": "Adding and subtracting",
        "prerequisites": ["counting-numbers"], "topics": ["Beginner path"], "reference": None,
        "related_lesson_ids": [],
        "units": [
            {"id": "adding-start", "title": "Putting amounts together",
             "objectives": ["Add within 20 by making a ten.",
                            "Add two-digit numbers, carrying a ten when needed."],
             "lesson_ids": ["add-facts", "add-regroup"]},
            {"id": "subtracting-start", "title": "Taking away and finding the gap",
             "objectives": ["Subtract by taking away and by finding the gap, and check with adding."],
             "lesson_ids": ["sub-gap"]},
        ],
    }, {
        "id": "multiply-divide", "subject_id": "math",
        "title": "Multiplying and dividing",
        "prerequisites": ["add-subtract"], "topics": ["Beginner path"], "reference": None,
        "related_lesson_ids": [],
        "units": [
            {"id": "multiplying-start", "title": "Equal groups and patterns",
             "objectives": ["Multiply using equal groups and arrays.",
                            "Use patterns to learn the times tables."],
             "lesson_ids": ["mul-groups", "mul-tables"]},
            {"id": "dividing-start", "title": "Sharing and grouping",
             "objectives": ["Divide by sharing and grouping, and describe a remainder."],
             "lesson_ids": ["div-share"]},
        ],
    }, {
        "id": "everyday-foundations", "subject_id": "math",
        "title": "Foundations of everyday math",
        "prerequisites": ["multiply-divide"], "topics": ["Learnova starter course"], "reference": None,
        "related_lesson_ids": [],
        "units": [
            {"id": "quantities", "title": "Parts and quantities",
             "objectives": ["Represent fractions and combine equal-sized parts."],
             "lesson_ids": ["fraction-sense"]},
            {"id": "expressions-and-equations", "title": "Expressions and balance",
             "objectives": ["Translate quantities into expressions and preserve equality."],
             "lesson_ids": ["expressions", "balance"]},
            {"id": "linear-models", "title": "Lines and real-world models",
             "objectives": ["Interpret slope and intercept in a linear model."],
             "lesson_ids": ["slope", "intercepts", "models"]},
        ],
    }, {
        "id": "math-history", "subject_id": "history",
        "title": "How math was invented",
        "prerequisites": [], "topics": ["Math history"], "reference": None,
        "related_lesson_ids": [],
        "units": [
            {"id": "history-numbers", "title": "Counting and writing numbers",
             "objectives": ["Explain how matching and tallies led to number systems.",
                            "Compare additive systems with place value, and explain why zero matters."],
             "lesson_ids": ["history-counting", "history-symbols", "history-place-value"]},
            {"id": "history-calculating", "title": "Calculating, sharing, and owing",
             "objectives": ["Multiply by doubling and adding, and explain carrying.",
                            "Describe why fractions and negative numbers were needed."],
             "lesson_ids": ["history-arithmetic", "history-fractions", "history-negatives"]},
            {"id": "history-reasoning", "title": "Balancing, measuring, and proving",
             "objectives": ["Explain how restoring and balancing became algebra.",
                            "Trace geometry from land measuring to proof and coordinates."],
             "lesson_ids": ["history-algebra", "history-geometry"]},
        ],
    }]
    by_id = {}
    for topic, subject_id, rows in TOPICS:
        for cid, title, slug, reference_title, objective, prerequisites in rows:
            if cid in by_id:
                by_id[cid]["topics"].append(topic)
                continue
            course = {
                "id": cid, "subject_id": subject_id, "title": title,
                "prerequisites": prerequisites, "topics": [topic],
                "reference": {"title": reference_title,
                              "url": f"https://brilliant.org/courses/{slug}/"},
                "related_lesson_ids": RELATED_LESSONS.get(cid, []),
                "units": [{"id": f"{cid}-core", "title": "Core ideas",
                           "objectives": [objective], "lesson_ids": []}],
            }
            by_id[cid] = course
            courses.append(course)
    by_id["fractions"]["units"] = [
        {"id": "fractions-meaning", "title": "Wholes, parts, and equivalence",
         "objectives": ["Define equal parts and locate fractions on a number line.",
                        "Rename a fraction without changing its value."],
         "lesson_ids": ["fraction-parts", "fraction-equivalence"]},
        {"id": "fractions-operations", "title": "Compare, combine, and take away",
         "objectives": ["Compare fractions of the same whole.",
                        "Add and subtract using common denominators."],
         "lesson_ids": ["fraction-comparison", "fraction-addition", "fraction-subtraction"]},
        {"id": "fractions-amounts", "title": "Fractions in the world",
         "objectives": ["Find a fraction of a quantity and recover a whole from a known part."],
         "lesson_ids": ["fraction-quantities"]},
    ]
    by_id["first-equations"]["units"] = [
        {"id": "equations-one-step", "title": "Balance and undo",
         "objectives": ["Explain solutions as values that make an equation true.",
                        "Solve one-step equations using inverse operations."],
         "lesson_ids": ["equation-meaning", "equation-addsub", "equation-muldiv"]},
        {"id": "equations-multi-step", "title": "Multiple steps",
         "objectives": ["Solve two-step equations by undoing operations in reverse order.",
                        "Combine like terms, distribute, and gather unknowns on one side."],
         "lesson_ids": ["equation-two-step", "equation-multistep"]},
        {"id": "equations-in-context", "title": "Equations in context",
         "objectives": ["Define an unknown, model a situation, and judge the solution in context."],
         "lesson_ids": ["equation-stories"]},
    ]
    by_id["linear-relationships"]["units"] = [
        {"id": "linear-change", "title": "Change, slope, and starting values",
         "objectives": ["Recognize constant rate of change in tables.",
                        "Calculate slope from two points and interpret intercepts."],
         "lesson_ids": ["linear-patterns", "linear-slope", "linear-intercept"]},
        {"id": "linear-rules", "title": "Rules and graphs",
         "objectives": ["Write a linear rule from slope and intercept or two points.",
                        "Connect equations, intercepts, and points on a graph."],
         "lesson_ids": ["linear-writing", "linear-graphs"]},
        {"id": "linear-meeting-points", "title": "Comparing lines",
         "objectives": ["Find where two linear relationships meet and interpret the result."],
         "lesson_ids": ["linear-comparison"]},
    ]
    by_id["coordinate-geometry"]["units"] = [
        {"id": "shapes-and-measure", "title": "Shapes and measurement",
         "objectives": ["Calculate perimeter and area, including composite shapes.",
                        "Use angle relationships in lines, triangles, and quadrilaterals."],
         "lesson_ids": ["geom-measure", "geom-angles"]},
        {"id": "points-and-grids", "title": "Points, grids, and midpoints",
         "objectives": ["Locate, reflect, and move points on the coordinate plane.",
                        "Measure grid distances and find midpoints."],
         "lesson_ids": ["coord-points", "coord-grid", "coord-midpoint"]},
        {"id": "distance-slope-shapes", "title": "Distance, slope, and shapes",
         "objectives": ["Measure the distance between any two points.",
                        "Use slopes to identify parallel and perpendicular lines.",
                        "Justify properties of shapes using lengths, midpoints, and slopes."],
         "lesson_ids": ["coord-distance", "coord-lines", "coord-shapes"]},
        {"id": "angle-and-distance", "title": "Coordinates by angle and distance",
         "objectives": ["Describe a point by its distance from the origin and its angle.",
                        "Convert between polar and rectangular descriptions."],
         "lesson_ids": ["coord-polar"]},
    ]
    return _ordered(courses)


COURSES = _courses()


def validate_catalog(lessons, skills, courses=COURSES):
    """Fail startup for broken ownership, references, or prerequisite cycles."""
    subject_ids = {s["id"] for s in SUBJECTS}
    lesson_ids = {lesson["id"] for lesson in lessons}
    skill_ids = {skill["id"] for skill in skills}
    by_id = {course["id"]: course for course in courses}
    if len(by_id) != len(courses):
        raise ValueError("Duplicate course ID in curriculum catalog.")
    owned = []
    unit_ids = []
    for course in courses:
        if course["subject_id"] not in subject_ids or not course["units"]:
            raise ValueError(f"Invalid subject or missing units: {course['id']}")
        if any(cid not in by_id for cid in course["prerequisites"]):
            raise ValueError(f"Unknown prerequisite: {course['id']}")
        if not set(course["related_lesson_ids"]) <= lesson_ids:
            raise ValueError(f"Unknown related lesson: {course['id']}")
        for unit in course["units"]:
            unit_ids.append(unit["id"])
            if not unit["objectives"] or any(not o.strip() for o in unit["objectives"]):
                raise ValueError(f"Missing learning objectives: {unit['id']}")
            owned.extend(unit["lesson_ids"])
    if len(unit_ids) != len(set(unit_ids)):
        raise ValueError("Duplicate unit ID in curriculum catalog.")
    if len(owned) != len(set(owned)) or set(owned) != lesson_ids:
        raise ValueError("Every published lesson must belong to exactly one catalog unit.")
    if any(lesson["skill"] not in skill_ids for lesson in lessons):
        raise ValueError("Published lesson references an unknown skill.")
    for lesson_id, story in STORIES.items():
        if lesson_id not in lesson_ids:
            raise ValueError(f"Story references an unknown lesson: {lesson_id}")
        if not all(isinstance(story.get(key), str) and story[key].strip() for key in ("title", "text", "art")):
            raise ValueError(f"Story is incomplete: {lesson_id}")
    if len(skill_ids) != len(skills) or len(lesson_ids) != len(lessons):
        raise ValueError("Duplicate skill or lesson ID.")
    skill_map = {skill["id"]: skill for skill in skills}
    if any(not set(s["prerequisites"]) <= skill_ids for s in skills):
        raise ValueError("Unknown skill prerequisite.")
    skill_visiting, skill_visited = set(), set()

    def visit_skill(sid):
        if sid in skill_visiting:
            raise ValueError(f"Cyclic skill prerequisites: {sid}")
        if sid in skill_visited:
            return
        skill_visiting.add(sid)
        for prerequisite in skill_map[sid]["prerequisites"]:
            visit_skill(prerequisite)
        skill_visiting.remove(sid)
        skill_visited.add(sid)

    for sid in skill_ids:
        visit_skill(sid)
    questions = {l["id"]: {q["id"] for q in l["exercises"]} for l in lessons}
    for lid, items in PRACTICE.items():
        if lid not in lesson_ids or len({q["id"] for q in items}) != len(items):
            raise ValueError(f"Invalid practice bank: {lid}")
        if questions[lid] & {q["id"] for q in items}:
            raise ValueError(f"Practice and lesson question IDs overlap: {lid}")
        questions[lid].update(q["id"] for q in items)
    assessment_ids = set()
    for cid, items in COURSE_ASSESSMENTS.items():
        if cid not in by_id:
            raise ValueError(f"Unknown assessment course: {cid}")
        course_lessons = {lid for unit in by_id[cid]["units"] for lid in unit["lesson_ids"]}
        for lid, q in items:
            if lid not in course_lessons or q["id"] in questions[lid] or q["id"] in assessment_ids:
                raise ValueError(f"Invalid assessment question: {q['id']}")
            assessment_ids.add(q["id"])
            questions[lid].add(q["id"])
    visiting, visited = set(), set()

    def visit(cid):
        if cid in visiting:
            raise ValueError(f"Cyclic course prerequisites: {cid}")
        if cid in visited:
            return
        visiting.add(cid)
        for prerequisite in by_id[cid]["prerequisites"]:
            visit(prerequisite)
        visiting.remove(cid)
        visited.add(cid)

    for cid in by_id:
        visit(cid)


def catalog_state(lessons, passed):
    catalog = {"reference": dict(REFERENCE), "subjects": deepcopy(SUBJECTS),
               "courses": deepcopy(COURSES)}
    by_id = {lesson["id"]: lesson for lesson in lessons}
    for course in catalog["courses"]:
        for unit in course["units"]:
            ids = unit["lesson_ids"]
            unit["status"] = "available" if ids else "planned"
            unit["lesson_count"] = len(ids)
            unit["completed_count"] = sum(
                all(q["id"] in passed[lid] for q in by_id[lid]["exercises"]) for lid in ids)
        course["lesson_count"] = sum(u["lesson_count"] for u in course["units"])
        course["completed_count"] = sum(u["completed_count"] for u in course["units"])
        course["status"] = ("available" if all(u["status"] == "available" for u in course["units"])
                            else "in-progress" if course["lesson_count"] else "planned")
        course["estimated_minutes"] = sum(by_id[lid]["duration"]
                                          for u in course["units"] for lid in u["lesson_ids"])
        course["coverage"] = ("original-course" if course["reference"] and course["lesson_count"]
                              else "partial" if course["related_lesson_ids"]
                              else "not-authored" if course["reference"] else "original")
    catalog["summary"] = {
        "subject_count": len(SUBJECTS), "course_count": len(catalog["courses"]),
        "available_course_count": sum(c["status"] == "available" for c in catalog["courses"]),
        "published_lesson_count": len(lessons),
        "reference_course_count": sum(c["reference"] is not None for c in catalog["courses"]),
        "partial_reference_count": sum(c["coverage"] == "partial" for c in catalog["courses"]),
        "topic_count": len(TOPICS),
    }
    return catalog
