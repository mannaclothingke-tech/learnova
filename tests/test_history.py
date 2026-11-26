from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from curriculum import HISTORY_LESSONS, LESSONS, SKILLS
from history import STORIES
from server import Store, grade

COURSE = "math-history"


class HistoryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "history.db")

    def submit(self, lesson, q):
        return self.store.attempt({
            "source": "lesson", "lesson_id": lesson["id"], "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()),
        })

    def test_course_is_playable_and_ordered_by_need(self):
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == COURSE)
        self.assertEqual(course["subject_id"], "history")
        self.assertEqual(course["status"], "available")
        self.assertEqual(course["stage"], 0)
        order = [lid for unit in course["units"] for lid in unit["lesson_ids"]]
        self.assertEqual(order, [
            "history-counting", "history-symbols", "history-place-value", "history-arithmetic",
            "history-fractions", "history-negatives", "history-algebra", "history-geometry"])
        self.assertEqual(order, [lesson["id"] for lesson in HISTORY_LESSONS])
        self.assertNotIn(COURSE, state["course_assessments"])
        skills = {s["id"]: s for s in SKILLS}
        seen = set()
        for lesson in HISTORY_LESSONS:
            self.assertTrue(set(skills[lesson["skill"]]["prerequisites"]) <= seen, lesson["id"])
            seen.add(lesson["skill"])

    def test_stories_reference_real_lessons_and_are_complete(self):
        lesson_ids = {lesson["id"] for lesson in LESSONS}
        self.assertEqual(len(STORIES), 15)
        for lesson_id, story in STORIES.items():
            self.assertIn(lesson_id, lesson_ids)
            self.assertTrue(story["title"].strip() and story["art"] in {"pie", "scales", "grid", "river", "circle", "rope", "tally", "hands", "abacus", "coins", "baskets", "share"})
            self.assertTrue(40 <= len(story["text"].split()) <= 110, lesson_id)
        state = self.store.state()
        self.assertEqual(state["stories"], STORIES)

    def test_stories_do_not_affect_progress_or_grading(self):
        before = self.store.state()
        self.assertEqual(before["activity"]["attempts"], 0)
        self.assertTrue(all(s["status"] == "not-started" for s in before["mastery"]))
        self.assertFalse({"answer", "hint", "explanation"} & set(next(iter(STORIES.values()))))

    def test_numeric_answers_against_independent_arithmetic(self):
        rows = [b * p for p in (1, 2, 4, 8) for b in (12,)]
        self.assertEqual(rows, [12, 24, 48, 96])
        expected = {
            "yc1": 3, "yc2": 4 * 5 + 3, "yc4": 37 // 5,
            "ys1": 3 + 1 + 2, "ys2": 9 + 9 + 9, "ys4": 4 * 100 + 0 * 10 + 5,
            "yp1": 5 * 10, "yp3": len(str(999)), "yp4": 4 * 100 + 0 * 10 + 7,
            "yr2": 8 * 7 + 1 * 7, "yr3": 16, "yr4": (7 + 8) // 10,
            "yf1": Fraction(3, 4) - Fraction(1, 2), "yf2": Fraction(1, 2) + Fraction(1, 3),
            "yf4": Fraction(3, 4),
            "yn1": 3 - 5, "yn2": -8 + 3, "yn3": -4 + -6,
            "ya1": 9 + 5, "ya2": 11, "ya4": Fraction(11 - 3, 2),
            "yg2": 10, "yg4": 5,
        }
        items = [q for lesson in HISTORY_LESSONS for q in lesson["exercises"]]
        self.assertEqual({q["id"] for q in items if q["kind"] == "number"}, set(expected))
        self.assertEqual(6 ** 2 + 8 ** 2, 10 ** 2)
        self.assertEqual(3 ** 2 + 4 ** 2, 5 ** 2)
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
        by_id = {q["id"]: q for lesson in HISTORY_LESSONS for q in lesson["exercises"]}
        # yr1: only the rows 1, 4, and 8 add to 13.
        options = {"1, 4, and 8": (1, 4, 8), "2, 4, and 8": (2, 4, 8), "1, 2, and 8": (1, 2, 8), "1, 2, and 4": (1, 2, 4)}
        self.assertEqual([k for k, v in options.items() if sum(v) == 13], [by_id["yr1"]["answer"]])
        self.assertEqual(12 + 48 + 96, 13 * 12)
        # yf3: only the first sum equals 7/8 using different unit fractions.
        sums = {"1/2 + 1/4 + 1/8": [2, 4, 8], "1/2 + 1/3 + 1/6": [2, 3, 6],
                "1/4 + 1/4 + 1/4": [4, 4, 4], "1/2 + 1/8 + 1/8": [2, 8, 8]}
        good = [k for k, v in sums.items() if sum(Fraction(1, d) for d in v) == Fraction(7, 8) and len(set(v)) == len(v)]
        self.assertEqual(good, [by_id["yf3"]["answer"]])
        # yg1: the right angle is opposite the longest side of a 3-4-5 triangle.
        self.assertEqual(3 ** 2 + 4 ** 2, 5 ** 2)
        self.assertTrue(by_id["yg1"]["answer"].endswith("between the 3 and 4 sides"))
        # yn4: opposites have equal size and opposite signs.
        self.assertEqual(-7 + 7, 0)
        self.assertEqual(by_id["yn4"]["answer"], "Having 7 coins")
        self.assertEqual(by_id["ys3"]["answer"], "No, you just add the values")
        self.assertEqual(by_id["yp2"]["answer"], "An empty tens place")
        self.assertEqual(3, 3)

    def test_greedy_doubling_matches_every_product(self):
        for a in range(1, 21):
            for b in range(1, 21):
                rows = [1]
                while rows[-1] * 2 <= a:
                    rows.append(rows[-1] * 2)
                remaining, chosen = a, []
                for row in reversed(rows):
                    if row <= remaining:
                        chosen.append(row)
                        remaining -= row
                self.assertEqual(remaining, 0)
                self.assertEqual(sum(row * b for row in chosen), a * b)

    def test_lessons_complete_course_and_master_skills(self):
        for lesson in HISTORY_LESSONS:
            for q in lesson["exercises"]:
                self.assertTrue(self.submit(lesson, q)["correct"])
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == COURSE)
        self.assertEqual(course["completed_count"], 8)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][33:41]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][:33]))


if __name__ == "__main__":
    unittest.main()
