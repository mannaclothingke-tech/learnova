from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from curriculum import BEGINNER_LESSONS, COURSE_ASSESSMENTS, PRACTICE, SKILLS
from history import STORIES
from server import Store, grade

COURSES = {"counting-numbers": ["num-count", "num-place", "num-line"],
           "add-subtract": ["add-facts", "add-regroup", "sub-gap"],
           "multiply-divide": ["mul-groups", "mul-tables", "div-share"]}


class BeginnerPathTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "beginner.db")

    def submit(self, source, lesson_id, q, **extra):
        return self.store.attempt({
            "source": source, "lesson_id": lesson_id, "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()), **extra,
        })

    def test_path_comes_first_and_gates_later_courses(self):
        courses = self.store.state()["catalog"]["courses"]
        by_id = {c["id"]: c for c in courses}
        math = [c["id"] for c in courses if c["subject_id"] == "math"]
        self.assertEqual(math[0], "counting-numbers")
        self.assertLess(math.index("add-subtract"), math.index("multiply-divide"))
        for later in ["fractions", "signed-numbers", "everyday-foundations", "first-equations"]:
            self.assertLess(math.index("multiply-divide"), math.index(later), later)
        self.assertEqual(by_id["counting-numbers"]["prerequisites"], [])
        self.assertEqual(by_id["add-subtract"]["prerequisites"], ["counting-numbers"])
        self.assertEqual(by_id["multiply-divide"]["prerequisites"], ["add-subtract"])
        self.assertIn("multiply-divide", by_id["fractions"]["prerequisites"])
        self.assertIn("add-subtract", by_id["signed-numbers"]["prerequisites"])
        self.assertEqual(by_id["counting-numbers"]["level"], "Beginner")
        for cid, lessons in COURSES.items():
            course = by_id[cid]
            self.assertEqual(course["status"], "available")
            self.assertEqual([lid for u in course["units"] for lid in u["lesson_ids"]], lessons)

    def test_lessons_follow_skill_prerequisites(self):
        order = [lesson["skill"] for lesson in BEGINNER_LESSONS]
        skills = {s["id"]: s for s in SKILLS}
        seen = set()
        for skill in order:
            self.assertTrue(set(skills[skill]["prerequisites"]) <= seen, skill)
            seen.add(skill)
        self.assertEqual(len(BEGINNER_LESSONS), 9)

    def test_shape_and_unique_question_ids(self):
        for lesson in BEGINNER_LESSONS:
            self.assertEqual(len(lesson["exercises"]), 4)
            self.assertEqual(len(PRACTICE[lesson["id"]]), 4)
        for cid, lessons in COURSES.items():
            check = COURSE_ASSESSMENTS[cid]
            self.assertEqual([lid for lid, _ in check], [l for l in lessons for _ in range(2)])
            for lesson in [l for l in BEGINNER_LESSONS if l["id"] in lessons]:
                ids = [q["id"] for q in lesson["exercises"] + PRACTICE[lesson["id"]] + [
                    q for lid, q in check if lid == lesson["id"]]]
                self.assertEqual(len(set(ids)), 10, lesson["id"])

    def test_numeric_answers_against_independent_arithmetic(self):
        expected = {
            "nc1": 10 - 6, "nc2": 10 + 3, "nc3": 5 + 2,
            "np1": 47 // 10, "np2": (58 // 10) * 10, "np3": 3 * 10 + 6,
            "nl1": 25 + 5, "nl2": 4 * 3, "nl4": 90 + 10,
            "af1": 6 + 4, "af2": 8 + 5, "af3": 7 + 8,
            "ar1": 27 + 38, "ar2": (46 % 10 + 29 % 10) // 10, "ar3": 45 + 36, "ar4": 58 + 47,
            "sg1": 12 - 5, "sg2": 15 - 9, "sg3": 12 - 7, "sg4": 52 - 27,
            "mg1": 4 * 5, "mg2": 3 * 6, "mg3": 7 * 2,
            "mt1": 10 * 7, "mt2": 5 * 8, "mt3": 9 * 3, "mt4": 2 * 9,
            "ds1": 12 // 3, "ds2": 20 // 5, "ds3": 21 // 3, "ds4": 14 % 3,
            "tc1": 10 - 8, "tc2": 10 + 10, "tc3": 5 + 4, "tc4": 30 - 1,
            "tp1": 63 % 10, "tp2": 6 * 10, "tp3": 10 // 10, "tp4": (71 // 10) * 10,
            "tl1": 12 + 2, "tl2": 6 * 5, "tl4": 70 + 10,
            "ta1": 9 + 3, "ta2": 6 + 7, "ta3": 8 + 8, "ta4": 5 + 9,
            "tr1": 34 + 28, "tr2": 19 + 17, "tr3": 65 + 29, "tr4": 77 + 25,
            "ts1": 14 - 6, "ts2": 20 - 13, "ts3": 17 - 9, "ts4": 61 - 38,
            "tg1": 5 * 3, "tg2": 4 * 7, "tg3": 6 * 2, "tg4": 9 * 1,
            "tm1": 10 * 4, "tm2": 5 * 6, "tm3": 9 * 5, "tm4": 2 * 8,
            "td1": 15 // 5, "td2": 24 // 4, "td3": 48 // 8, "td4": 17 % 5,
            "vc1": 10 - 3, "vc2": 10 + 6, "vp1": 5 * 10 + 8, "vp2": (82 // 10) * 10, "vl1": 5 * 4,
            "vf1": 7 + 5, "vf2": 9 + 6, "vr1": 48 + 35, "vr2": 69 + 24, "vs1": 17 - 8, "vs2": 73 - 46,
            "vg1": 6 * 4, "vg2": 5 * 5, "vt1": 9 * 7, "vt2": 5 * 9, "vd1": 18 // 6, "vd2": 23 % 4,
        }
        items = [q for l in BEGINNER_LESSONS for q in l["exercises"] + PRACTICE[l["id"]]] + [
            q for cid in COURSES for _, q in COURSE_ASSESSMENTS[cid]]
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
        by_id = {q["id"]: q for l in BEGINNER_LESSONS for q in l["exercises"] + PRACTICE[l["id"]]}
        checks = {q["id"]: q for cid in COURSES for _, q in COURSE_ASSESSMENTS[cid]}
        self.assertEqual(by_id["np4"]["answer"], str(2 * 10 + 9))
        self.assertEqual(by_id["nc4"]["answer"], str(19 + 1))
        self.assertEqual(by_id["nl3"]["answer"], str(max(47, 39)))
        self.assertEqual(by_id["tl3"]["answer"], str(min(62, 26)))
        self.assertEqual(checks["vl2"]["answer"], str(max(81, 18)))
        self.assertEqual(5 + 9, 9 + 5)
        self.assertEqual(by_id["af4"]["answer"], "9 + 5")
        self.assertEqual(3 * 8, 8 * 3)
        self.assertEqual(by_id["mg4"]["answer"], "8 x 3")

    def test_explorer_logic_matches_arithmetic(self):
        for a in range(10, 100, 7):
            for b in range(10, 100, 9):
                ones = a % 10 + b % 10
                carry = 1 if ones >= 10 else 0
                self.assertEqual((a // 10 + b // 10 + carry) * 10 + ones % 10, a + b)
        for total in range(1, 31):
            for groups in range(1, 7):
                self.assertEqual((total // groups) * groups + total % groups, total)
        for r in range(1, 11):
            for c in range(1, 11):
                self.assertEqual(sum([c] * r), r * c)

    def test_stories_for_beginner_lessons_exist_and_are_complete(self):
        for lesson_id in ["num-count", "num-place", "add-regroup", "sub-gap", "mul-groups", "div-share"]:
            self.assertIn(lesson_id, STORIES)
            self.assertTrue(40 <= len(STORIES[lesson_id]["text"].split()) <= 110)

    def test_each_course_completes_and_masters_its_skills(self):
        for cid, lessons in COURSES.items():
            for lesson in [l for l in BEGINNER_LESSONS if l["id"] in lessons]:
                for q in lesson["exercises"]:
                    self.assertTrue(self.submit("lesson", lesson["id"], q)["correct"])
        state = self.store.state()
        for cid in COURSES:
            course = next(c for c in state["catalog"]["courses"] if c["id"] == cid)
            self.assertEqual(course["completed_count"], 3)
        new_skills = {l["skill"] for l in BEGINNER_LESSONS}
        for skill in state["mastery"]:
            self.assertEqual(skill["status"] == "mastered", skill["id"] in new_skills)

    def test_course_checks_save_once_and_score(self):
        for cid, lessons in COURSES.items():
            for lid, q in COURSE_ASSESSMENTS[cid]:
                self.assertTrue(self.submit("course-assessment", lid, q, course_id=cid)["correct"])
        state = self.store.state()
        for cid in COURSES:
            self.assertTrue(state["course_assessments"][cid]["complete"])
            self.assertEqual(state["course_assessments"][cid]["correct_count"], 6)


if __name__ == "__main__":
    unittest.main()
