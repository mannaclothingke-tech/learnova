from fractions import Fraction
import math
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from curriculum import COURSE_ASSESSMENTS, GEOMETRY_LESSONS, PRACTICE, SKILLS
from server import Store, grade

COURSE = "coordinate-geometry"


def slope(p, q):
    return Fraction(q[1] - p[1], q[0] - p[0])


def dist(p, q):
    squared = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
    root = math.isqrt(squared)
    assert root * root == squared, "distance should be a whole number in these questions"
    return root


def mid(p, q, axis):
    return Fraction(p[axis] + q[axis], 2)


def polar_to_xy(r, cos, sin):
    return r * Fraction(cos), r * Fraction(sin)


class GeometryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "geometry.db")

    def submit(self, source, lesson_id, q, **extra):
        return self.store.attempt({
            "source": source, "lesson_id": lesson_id, "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()), **extra,
        })

    def test_one_merged_course_ordered_simple_to_complex(self):
        courses = self.store.state()["catalog"]["courses"]
        merged = [c for c in courses if c["id"] == COURSE]
        self.assertEqual(len(merged), 1)
        for retired in ["coordinates", "measurement", "geometric-thinking", "polar"]:
            self.assertNotIn(retired, {c["id"] for c in courses})
        course = merged[0]
        self.assertEqual(course["title"], "Geometry and coordinates")
        self.assertEqual(len(course["topics"]), 5)
        order = [lid for u in course["units"] for lid in u["lesson_ids"]]
        self.assertEqual(order, [
            "geom-measure", "geom-angles", "coord-points", "coord-grid", "coord-midpoint",
            "coord-distance", "coord-lines", "coord-shapes", "coord-polar"])
        self.assertEqual(order, [l["id"] for l in GEOMETRY_LESSONS])
        skills = {s["id"]: s for s in SKILLS}
        seen = set()
        for lesson in GEOMETRY_LESSONS:
            prerequisites = set(skills[lesson["skill"]]["prerequisites"])
            self.assertTrue(prerequisites <= seen, lesson["id"])
            seen.add(lesson["skill"])

    def test_catalog_is_ordered_by_stage_within_each_subject(self):
        courses = self.store.state()["catalog"]["courses"]
        subjects = [s["id"] for s in self.store.state()["catalog"]["subjects"]]
        keys = [(subjects.index(c["subject_id"]), c["stage"]) for c in courses]
        self.assertEqual(keys, sorted(keys))
        by_id = {c["id"]: c for c in courses}
        for course in courses:
            for prerequisite in course["prerequisites"]:
                self.assertLess(by_id[prerequisite]["stage"], course["stage"], course["id"])
        self.assertEqual(courses[0]["id"], "counting-numbers")
        self.assertEqual([c["id"] for c in courses if c["stage"] == 0 and c["subject_id"] == "math"][:1], ["counting-numbers"])

    def test_assessment_follows_lesson_order(self):
        order = [l["id"] for l in GEOMETRY_LESSONS]
        indexes = [order.index(lid) for lid, _ in COURSE_ASSESSMENTS[COURSE]]
        self.assertEqual(indexes, sorted(indexes))
        self.assertEqual(len(indexes), 18)

    def test_course_shape_and_unique_question_ids(self):
        self.assertEqual(len(GEOMETRY_LESSONS), 9)
        self.assertEqual(sum(len(l["exercises"]) for l in GEOMETRY_LESSONS), 45)
        self.assertEqual(sum(len(PRACTICE[l["id"]]) for l in GEOMETRY_LESSONS), 36)
        self.assertEqual({l["skill"] for l in GEOMETRY_LESSONS}, {s["id"] for s in SKILLS[24:33]})
        for lesson in GEOMETRY_LESSONS:
            ids = [q["id"] for q in lesson["exercises"] + PRACTICE[lesson["id"]] + [
                q for lid, q in COURSE_ASSESSMENTS[COURSE] if lid == lesson["id"]]]
            self.assertEqual(len(set(ids)), 11, lesson["id"])

    def test_numeric_answers_against_independent_geometry(self):
        expected = {
            "hm1": 2 * (8 + 5), "hm2": 8 * 5, "hm3": Fraction(10 * 6, 2), "hm4": 6 * 4 + 3 * 2,
            "ha1": 90 - 35, "ha2": 180 - 110, "ha3": 180 - (50 + 65), "ha4": (180 - 40) // 2,
            "ha5": 360 - (90 + 100 + 80),
            "op3": -3, "op4": -4, "op5": -1 + 4,
            "og1": 9 - 2, "og2": 4 - -2, "og3": 3 - -4, "og4": (6 - 1) * (4 - 1),
            "og5": 2 * ((4 - -2) + (3 - -1)),
            "om1": mid((2, 3), (8, 9), 0), "om2": mid((-4, 6), (2, -2), 1),
            "om3": 2 * 3 - 1, "om4": mid((-5, -1), (2, 4), 0),
            "od1": dist((0, 0), (3, 4)), "od2": dist((1, 2), (7, 10)), "od3": dist((-2, 1), (3, 13)),
            "od4": (5 - 0) ** 2 + (3 - 1) ** 2,
            "ol1": slope((1, 2), (3, 8)), "ol2": Fraction(2, 3), "ol3": Fraction(-1, 4),
            "ol4": Fraction(-5, 2),
            "os1": dist((0, 0), (4, 3)), "os2": dist((0, 0), (6, 8)), "os3": mid((0, 0), (4, 3), 0),
            "os5": Fraction(6 * 8, 2),
            "hp1": -7, "hp2": 5, "hp3": dist((0, 0), (6, 8)),
            "hp4": polar_to_xy(10, "0.6", "0.8")[1],
            "zm1": 2 * (9 + 3), "zm2": 7 * 7, "zm3": Fraction(8 * 5, 2), "zm4": 5 * 5 + 2 * 3,
            "za1": 90 - 62, "za2": 180 - 45, "za3": 180 - (30 + 90), "za4": 360 - (85 + 95 + 110),
            "qp3": 5, "qp4": 2 - 6,
            "qg1": 10 - 1, "qg2": 6 - -2, "qg3": -1 - -6, "qg4": 7 * 2,
            "qm1": mid((0, 4), (10, 8), 0), "qm2": mid((1, -3), (5, 9), 1), "qm3": 2 * -1 - 4,
            "qm4": mid((-7, 0), (2, 6), 0),
            "qd1": dist((0, 0), (6, 8)), "qd2": dist((2, 1), (5, 5)), "qd3": dist((-3, -2), (2, 10)),
            "qd4": (4 - 1) ** 2 + (4 - 2) ** 2,
            "ql1": slope((0, 1), (4, 9)), "ql2": Fraction(1, 3), "ql3": Fraction(-2, 5),
            "qs1": dist((0, 0), (5, 12)), "qs2": 3 + 4 + dist((0, 0), (3, 4)),
            "qs3": mid((0, 0), (6, 4), 1), "qs4": Fraction(10 * 6, 2),
            "zp1": 9, "zp2": -6, "zp3": dist((0, 0), (5, 12)), "zp4": polar_to_xy(20, "0.8", "0.6")[0],
            "wm1": 2 * (14 + 6), "wm2": Fraction(12 * 7, 2),
            "wa1": 180 - (72 + 58), "wa2": 180 // 3,
            "gp2": 2, "gg1": 2 - -5, "gg2": 2 * ((3 - -3) + (1 - -2)),
            "gm1": mid((3, -8), (9, 4), 1), "gm2": 2 * -2 - 4,
            "gd1": dist((0, 0), (5, 12)), "gd2": dist((-1, -1), (7, 5)),
            "gl1": Fraction(-5), "gs1": dist((0, 0), (8, 15)), "gs2": Fraction(9 * 4, 2),
            "wp1": dist((0, 0), (-8, 6)), "wp2": polar_to_xy(13, "5/13", "12/13")[0],
        }
        items = [q for l in GEOMETRY_LESSONS for q in l["exercises"]] + [
            q for l in GEOMETRY_LESSONS for q in PRACTICE[l["id"]]] + [
            q for _, q in COURSE_ASSESSMENTS[COURSE]]
        self.assertEqual({q["id"] for q in items if q["kind"] == "number"}, set(expected))
        for q in items:
            with self.subTest(question=q["id"]):
                if q["kind"] == "number":
                    self.assertEqual(Fraction(q["answer"]), Fraction(expected[q["id"]]))
                else:
                    self.assertIn(q["answer"], q["choices"])
                    self.assertEqual(len(set(q["choices"])), len(q["choices"]))
                self.assertTrue(grade(q["answer"], q["answer"], q["kind"]))
                self.assertTrue(q["hint"] and q["explanation"])

    def test_choice_answers_match_their_own_mathematics(self):
        lessons = {q["id"]: q for l in GEOMETRY_LESSONS for q in l["exercises"]}
        practice = {q["id"]: q for bank in PRACTICE.values() for q in bank}
        checks = {q["id"]: q for _, q in COURSE_ASSESSMENTS[COURSE]}
        # Points (x, y) after the moves named in each choice question.
        self.assertEqual(lessons["op1"]["answer"], "(3, -2)")
        self.assertEqual(practice["qp1"]["answer"], "(-4, 1)")

        def quadrant(x, y):
            return {(1, 1): "Quadrant I", (-1, 1): "Quadrant II",
                    (-1, -1): "Quadrant III", (1, -1): "Quadrant IV"}[(x > 0) - (x < 0), (y > 0) - (y < 0)]
        self.assertEqual(lessons["op2"]["answer"], quadrant(-4, 5))
        self.assertEqual(practice["qp2"]["answer"], quadrant(2, -6))
        self.assertEqual(checks["gp1"]["answer"], quadrant(-3, -7))
        # Perpendicular slope pairs multiply to -1; the other options do not.
        self.assertEqual(Fraction(3) * Fraction(-1, 3), -1)
        self.assertEqual([Fraction(2) * Fraction(1, 2), Fraction(2) * -2, Fraction(5) * 5], [1, -4, 25])
        self.assertEqual(lessons["ol5"]["answer"], "3 and -1/3")
        self.assertEqual(Fraction(3, 4) * Fraction(-4, 3), -1)
        self.assertEqual(checks["gl2"]["answer"], "3/4 and -4/3")
        # Only one pair of points in od5 is exactly 5 apart.
        pairs = {"(1, 1) and (4, 5)": ((1, 1), (4, 5)), "(1, 1) and (4, 4)": ((1, 1), (4, 4)),
                 "(0, 0) and (2, 4)": ((0, 0), (2, 4)), "(0, 0) and (4, 4)": ((0, 0), (4, 4))}
        five = [k for k, (p, q) in pairs.items() if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 == 25]
        self.assertEqual(five, [lessons["od5"]["answer"]])
        # Quadrilateral from os4 is a parallelogram but not a rectangle.
        a, b, c, d = (0, 0), (4, 1), (5, 4), (1, 3)
        vec = lambda p, q: (q[0] - p[0], q[1] - p[1])
        self.assertEqual(vec(a, b), vec(d, c))
        self.assertEqual(vec(a, d), vec(b, c))
        ab, ad = vec(a, b), vec(a, d)
        self.assertNotEqual(ab[0] * ad[0] + ab[1] * ad[1], 0)
        self.assertTrue(lessons["os4"]["answer"].startswith("Opposite sides AB and DC"))
        # Parallel line has the same slope; the other options differ.
        self.assertEqual(practice["ql4"]["answer"], "y = 3x - 7")
        self.assertEqual(lessons["hm5"]["answer"], "25 square cm")
        # (0, -4) lies 4 units from the origin directly below it: 270 degrees.
        self.assertEqual(lessons["hp5"]["answer"], "r = 4, angle 270 degrees")
        self.assertEqual(math.degrees(math.atan2(-4, 0)) % 360, 270)
        # Polar ratios in the questions form valid right triangles.
        for cos, sin in [("0.6", "0.8"), ("0.8", "0.6"), ("5/13", "12/13")]:
            self.assertEqual(Fraction(cos) ** 2 + Fraction(sin) ** 2, 1)

    def test_course_completion_mastery_and_check_flow(self):
        for lesson in GEOMETRY_LESSONS:
            for q in lesson["exercises"]:
                self.assertTrue(self.submit("lesson", lesson["id"], q)["correct"])
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == COURSE)
        self.assertEqual(course["completed_count"], 9)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][24:33]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][:24]))
        for lid, q in COURSE_ASSESSMENTS[COURSE]:
            self.assertTrue(self.submit("course-assessment", lid, q, course_id=COURSE)["correct"])
        check = Store(self.store.path).state()["course_assessments"][COURSE]
        self.assertTrue(check["complete"])
        self.assertEqual(check["correct_count"], 18)

    def test_practice_does_not_complete_lessons(self):
        lid = "geom-angles"
        for q in PRACTICE[lid][:2]:
            self.submit("practice", lid, q)
        state = self.store.state()
        self.assertEqual(state["practice"][lid]["passed"], ["za1", "za2"])
        self.assertEqual(state["passed"][lid], [])


if __name__ == "__main__":
    unittest.main()
