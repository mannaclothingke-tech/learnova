from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from curriculum import COURSE_ASSESSMENTS, EQUATION_LESSONS, PRACTICE, SKILLS
from server import Store, grade


def linear(a1, b1, a2=0, b2=0):
    """Solve a1*x + b1 = a2*x + b2 without using the authored answer."""
    return Fraction(b2 - b1) / (a1 - a2)


class EquationsTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "equations.db")

    def submit(self, source, lesson_id, q, **extra):
        return self.store.attempt({
            "source": source, "lesson_id": lesson_id, "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()), **extra,
        })

    def test_course_shape_and_unique_question_ids(self):
        self.assertEqual(len(EQUATION_LESSONS), 6)
        self.assertEqual(sum(len(l["exercises"]) for l in EQUATION_LESSONS), 30)
        self.assertEqual(sum(len(PRACTICE[l["id"]]) for l in EQUATION_LESSONS), 24)
        self.assertEqual(len(COURSE_ASSESSMENTS["first-equations"]), 12)
        self.assertEqual({l["skill"] for l in EQUATION_LESSONS}, {s["id"] for s in SKILLS[12:18]})
        for lesson in EQUATION_LESSONS:
            ids = [q["id"] for q in lesson["exercises"] + PRACTICE[lesson["id"]] + [
                q for lid, q in COURSE_ASSESSMENTS["first-equations"] if lid == lesson["id"]]]
            self.assertEqual(len(set(ids)), 11)
        course = next(c for c in self.store.state()["catalog"]["courses"] if c["id"] == "first-equations")
        self.assertEqual(course["status"], "available")
        self.assertEqual(course["coverage"], "original-course")
        self.assertEqual([len(u["lesson_ids"]) for u in course["units"]], [3, 2, 1])
        self.assertEqual(course["estimated_minutes"], sum(l["duration"] for l in EQUATION_LESSONS))

    def test_numeric_answers_against_independent_algebra(self):
        expected = {
            "lb3": 12 - 5, "lb5": 3 * 5 - 2,
            "la1": linear(1, 12, 0, 20), "la2": linear(1, -7, 0, 5), "la3": linear(1, 9, 0, 4),
            "la4": linear(1, 6, 0, 15), "la5": Fraction(3, 4) + Fraction(1, 2),
            "lm1": linear(4, 0, 0, 28), "lm2": 5 * 6, "lm3": linear(-3, 0, 0, 12),
            "lm4": linear(2, 0, 0, 7), "lm5": 9 / Fraction(3, 4),
            "lt1": linear(2, 3, 0, 13), "lt2": linear(3, -4, 0, 11), "lt3": 2 * (6 - 1),
            "lt4": linear(-4, 5, 0, -7),
            "lc1": linear(5, 0, 0, 35), "lc2": linear(2, 6, 0, 14), "lc3": linear(5, 0, 2, 12),
            "lc4": linear(4, 1, 1, 10), "lc5": linear(3, -6, 2, 1),
            "ls1": linear(2, 4, 0, 18), "ls2": linear(3, 12, 1, 30), "ls4": linear(3, 3, 0, 51),
            "rb3": 20 - 8, "rb4": 4 * 3 + 1,
            "ra1": linear(1, 5, 0, 17), "ra2": linear(1, -9, 0, 3), "ra3": linear(1, 11, 0, 2),
            "ra4": Fraction(5, 6) - Fraction(1, 3),
            "rm1": linear(6, 0, 0, 42), "rm2": 3 * 8, "rm3": linear(-5, 0, 0, 20),
            "rm4": 10 / Fraction(2, 3),
            "rt1": linear(3, 2, 0, 20), "rt2": linear(5, -7, 0, 18), "rt3": 3 * (4 + 2),
            "rt4": linear(-2, 10, 0, 4),
            "rc1": linear(7, 0, 0, 21), "rc2": linear(3, 6, 0, 21), "rc3": linear(6, 0, 4, 10),
            "rc4": linear(5, -3, 2, 9),
            "rs1": linear(2, 5, 0, 21), "rs2": linear(-4, 40, 0, 12), "rs3": linear(4, 30, 6, 18),
            "rs4": linear(4, 3, 0, 31),
            "xa1": linear(1, 14, 0, 30), "xa2": linear(1, -8, 0, -3), "xm1": linear(9, 0, 0, 54),
            "xm2": 7 * -2, "xt1": linear(4, 5, 0, 29), "xt2": linear(-3, 7, 0, -2),
            "xc1": linear(7, 0, 0, 56), "xc2": linear(4, -4, 3, 5), "xs1": linear(5, 12, 0, 52),
            "xs2": linear(3, 3, 0, 78) + 2,
        }
        items = [q for l in EQUATION_LESSONS for q in l["exercises"]] + [
            q for l in EQUATION_LESSONS for q in PRACTICE[l["id"]]] + [
            q for _, q in COURSE_ASSESSMENTS["first-equations"]]
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
        by_id = {q["id"]: q for l in EQUATION_LESSONS for q in l["exercises"]}
        self.assertEqual(by_id["lb1"]["answer"], "7")
        self.assertEqual(int(by_id["lb1"]["answer"]) + 3, 10)
        self.assertNotEqual(2 * 4 + 1, 10)
        self.assertEqual(by_id["lb2"]["answer"], "No")
        self.assertEqual(3 * 15 + 0, 45)
        self.assertEqual(by_id["ls3"]["answer"], "3g + 15 = 36")
        self.assertEqual(linear(3, 15, 0, 36), 7)
        practice = {q["id"]: q for bank in PRACTICE.values() for q in bank}
        self.assertEqual(practice["rb1"]["answer"], "13")
        self.assertEqual(13 - 4, 9)
        self.assertEqual(practice["rb2"]["answer"], "Yes")
        self.assertEqual(5 * 3 - 2, 13)
        checks = {q["id"]: q for _, q in COURSE_ASSESSMENTS["first-equations"]}
        self.assertEqual(checks["xb1"]["answer"], "9")
        self.assertEqual(2 * 9, 18)
        self.assertEqual(checks["xb2"]["answer"], "No")
        self.assertNotEqual(5 + 7, 11)

    def test_course_completion_mastery_and_check_flow(self):
        for lesson in EQUATION_LESSONS:
            for q in lesson["exercises"]:
                self.assertTrue(self.submit("lesson", lesson["id"], q)["correct"])
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == "first-equations")
        self.assertEqual(course["completed_count"], 6)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][12:18]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][:12] + state["mastery"][18:]))
        for lid, q in COURSE_ASSESSMENTS["first-equations"]:
            self.assertTrue(self.submit("course-assessment", lid, q, course_id="first-equations")["correct"])
        check = Store(self.store.path).state()["course_assessments"]["first-equations"]
        self.assertTrue(check["complete"])
        self.assertEqual(check["correct_count"], 12)

    def test_practice_does_not_complete_lessons(self):
        lid = "equation-two-step"
        for q in PRACTICE[lid][:2]:
            self.submit("practice", lid, q)
        state = self.store.state()
        self.assertEqual(state["practice"][lid]["passed"], ["rt1", "rt2"])
        self.assertEqual(state["passed"][lid], [])
        self.assertEqual(next(s for s in state["mastery"] if s["id"] == "eq-twostep")["status"], "mastered")


if __name__ == "__main__":
    unittest.main()
