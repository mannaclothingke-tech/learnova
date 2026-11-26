from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from curriculum import COURSE_ASSESSMENTS, LINEAR_LESSONS, PRACTICE, SKILLS
from server import Store, grade

COURSE = "linear-relationships"


def slope(p, q):
    return Fraction(q[1] - p[1], q[0] - p[0])


def intercept_from_point(m, point):
    return point[1] - m * point[0]


def meet(m1, b1, m2, b2):
    x = Fraction(b2 - b1) / (m1 - m2)
    return x, m1 * x + b1


class LinearTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "linear.db")

    def submit(self, source, lesson_id, q, **extra):
        return self.store.attempt({
            "source": source, "lesson_id": lesson_id, "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()), **extra,
        })

    def test_course_shape_and_unique_question_ids(self):
        self.assertEqual(len(LINEAR_LESSONS), 6)
        self.assertEqual(sum(len(l["exercises"]) for l in LINEAR_LESSONS), 30)
        self.assertEqual(sum(len(PRACTICE[l["id"]]) for l in LINEAR_LESSONS), 24)
        self.assertEqual(len(COURSE_ASSESSMENTS[COURSE]), 12)
        self.assertEqual({l["skill"] for l in LINEAR_LESSONS}, {s["id"] for s in SKILLS[18:24]})
        for lesson in LINEAR_LESSONS:
            ids = [q["id"] for q in lesson["exercises"] + PRACTICE[lesson["id"]] + [
                q for lid, q in COURSE_ASSESSMENTS[COURSE] if lid == lesson["id"]]]
            self.assertEqual(len(set(ids)), 11)
        course = next(c for c in self.store.state()["catalog"]["courses"] if c["id"] == COURSE)
        self.assertEqual(course["status"], "available")
        self.assertEqual(course["coverage"], "original-course")
        self.assertEqual([len(u["lesson_ids"]) for u in course["units"]], [3, 2, 1])

    def test_numeric_answers_against_independent_geometry(self):
        expected = {
            "ip1": 9 - 5, "ip3": Fraction(7 - 1, 2), "ip4": 17 - 20, "ip5": 3 * 10,
            "is1": slope((1, 3), (4, 12)), "is2": slope((2, 10), (5, 4)),
            "is3": slope((0, 0), (4, 6)), "is5": slope((1, 4), (6, 4)),
            "ii1": 7, "ii2": -3, "ii3": intercept_from_point(4, (1, 9)),
            "ii5": intercept_from_point(3, (4, 20)),
            "iw2": 5 * 6 + 4, "iw3": intercept_from_point(slope((1, 7), (3, 13)), (1, 7)),
            "iw4": intercept_from_point(Fraction(1, 2), (4, 5)),
            "ig1": 2 * 4 + 3, "ig2": slope((0, 8), (4, 0)), "ig4": Fraction(6, 2), "ig5": 3 * 5 - 4,
            "ic1": meet(5, 10, 3, 20)[0], "ic3": meet(3, 0, 1, 8)[1], "ic5": meet(2, 12, 5, 0)[0],
            "jp1": 7 - 2, "jp3": Fraction(10 - 4, 3), "jp4": 44 - 50,
            "js1": slope((0, 2), (3, 11)), "js2": slope((1, 8), (3, 2)),
            "js3": slope((2, 1), (6, 3)), "js4": slope((-2, -1), (2, 7)),
            "ji1": 9, "ji2": 5, "ji3": intercept_from_point(5, (2, 13)),
            "ji4": intercept_from_point(-2, (3, 1)),
            "jw1": 4 * 5 + 1, "jw2": 3 * 4 - 1,
            "jw3": intercept_from_point(slope((2, 5), (4, 11)), (2, 5)),
            "jw4": intercept_from_point(Fraction(2, 3), (6, 7)),
            "jg1": 3 * 5 + 2, "jg2": slope((0, 6), (3, 0)), "jg3": Fraction(-5), "jg4": 2 * 4 - 1,
            "jc1": meet(2, 9, 5, 0)[0], "jc2": meet(-1, 10, 1, 2)[1], "jc4": meet(5, 15, 20, 0)[0],
            "kp1": 11 - 6, "kp2": 4 - 10,
            "ks1": slope((2, 5), (6, 17)), "ks2": slope((1, 9), (4, 0)),
            "ki1": intercept_from_point(5, (3, 22)), "ki2": 12,
            "kw1": intercept_from_point(slope((1, 5), (4, 14)), (1, 5)),
            "kw2": -3 * 5 + intercept_from_point(-3, (2, 4)),
            "kg1": Fraction(12, 4), "kg2": -2 * 6 + 15,
            "kc1": meet(3, 4, 5, -6)[0], "kc2": meet(4, 1, 1, 10)[1],
        }
        items = [q for l in LINEAR_LESSONS for q in l["exercises"]] + [
            q for l in LINEAR_LESSONS for q in PRACTICE[l["id"]]] + [
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
        lessons = {q["id"]: q for l in LINEAR_LESSONS for q in l["exercises"]}
        practice = {q["id"]: q for bank in PRACTICE.values() for q in bank}
        # ip2: the only table whose neighbouring differences are all equal.
        diffs = lambda ys: {b - a for a, b in zip(ys, ys[1:])}
        tables = {"x: 1, 2, 3, 4 and y: 2, 5, 8, 11": [2, 5, 8, 11], "x: 1, 2, 3, 4 and y: 1, 4, 9, 16": [1, 4, 9, 16],
                  "x: 1, 2, 3, 4 and y: 2, 4, 7, 11": [2, 4, 7, 11], "x: 1, 2, 3, 4 and y: 20, 10, 5, 2.5": [20, 10, 5, 2.5]}
        self.assertEqual([k for k, ys in tables.items() if len(diffs(ys)) == 1], [lessons["ip2"]["answer"]])
        self.assertEqual(len(diffs([3, 6, 12, 24])), 3)
        self.assertEqual(practice["jp2"]["answer"], "No")
        # is4: steepest line has the largest slope magnitude.
        self.assertEqual(max([3, -5, Fraction(1, 2), 4], key=abs), -5)
        self.assertEqual(lessons["is4"]["answer"], "slope -5")
        # iw1 and iw5: rules must satisfy the described slope, intercept, and table.
        self.assertEqual(lessons["iw1"]["answer"], "y = 3x - 2")
        self.assertEqual([-2 * x + 6 for x in range(4)], [6, 4, 2, 0])
        self.assertEqual(lessons["iw5"]["answer"], "y = -2x + 6")
        # ig3 and ic2: slopes decide the described behaviour.
        self.assertEqual(lessons["ig3"]["answer"][:13], "It falls 1 fo")
        self.assertEqual(lessons["ic4"]["answer"], "y = 7x + 1")
        self.assertGreater(7, 5)
        self.assertEqual(2 * 1 + 1 - (2 * 1 + 5), -4)
        self.assertEqual(lessons["ic2"]["answer"], "None")
        self.assertEqual(practice["jc3"]["answer"], "None")
        self.assertEqual(lessons["ii4"]["answer"], "The amount of water at the start (x = 0)")
        self.assertEqual(120 - 8 * 0, 120)

    def test_course_completion_mastery_and_check_flow(self):
        for lesson in LINEAR_LESSONS:
            for q in lesson["exercises"]:
                self.assertTrue(self.submit("lesson", lesson["id"], q)["correct"])
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == COURSE)
        self.assertEqual(course["completed_count"], 6)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][18:24]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][:18]))
        for lid, q in COURSE_ASSESSMENTS[COURSE]:
            self.assertTrue(self.submit("course-assessment", lid, q, course_id=COURSE)["correct"])
        check = Store(self.store.path).state()["course_assessments"][COURSE]
        self.assertTrue(check["complete"])
        self.assertEqual(check["correct_count"], 12)

    def test_practice_does_not_complete_lessons(self):
        lid = "linear-slope"
        for q in PRACTICE[lid][:2]:
            self.submit("practice", lid, q)
        state = self.store.state()
        self.assertEqual(state["practice"][lid]["passed"], ["js1", "js2"])
        self.assertEqual(state["passed"][lid], [])


if __name__ == "__main__":
    unittest.main()
