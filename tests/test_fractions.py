import copy
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from catalog import validate_catalog
from curriculum import COURSE_ASSESSMENTS, FRACTION_LESSONS, LESSONS, PRACTICE, SKILLS
from server import InvalidRequest, Store, grade


class FractionsTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store = Store(Path(directory.name) / "fractions.db")

    def submit(self, source, lid, q, **extra):
        return self.store.attempt({
            "source": source, "lesson_id": lid, "question_id": q["id"],
            "version": 1, "answer": q["answer"], "attempt_id": str(uuid4()), **extra,
        })

    def test_course_has_six_lessons_thirty_challenges_and_separate_banks(self):
        self.assertEqual(len(FRACTION_LESSONS), 6)
        self.assertEqual(sum(len(l["exercises"]) for l in FRACTION_LESSONS), 30)
        self.assertEqual(sum(len(PRACTICE[l["id"]]) for l in FRACTION_LESSONS), 24)
        self.assertEqual(len(COURSE_ASSESSMENTS["fractions"]), 12)
        self.assertEqual({l["skill"] for l in FRACTION_LESSONS}, {s["id"] for s in SKILLS[6:12]})
        for lesson in FRACTION_LESSONS:
            ids = [q["id"] for q in lesson["exercises"] + PRACTICE[lesson["id"]] +
                   [q for lid, q in COURSE_ASSESSMENTS["fractions"] if lid == lesson["id"]]]
            self.assertEqual(len(set(ids)), 11)
        course = next(c for c in self.store.state()["catalog"]["courses"] if c["id"] == "fractions")
        self.assertEqual(course["status"], "available")
        self.assertEqual(course["coverage"], "original-course")
        self.assertEqual(course["lesson_count"], 6)
        self.assertEqual(course["estimated_minutes"], 54)

    def test_numeric_answers_against_independent_arithmetic(self):
        expected = {
            "fp1": Fraction(3, 5), "fp4": 3, "fp5": Fraction(5, 4),
            "fe1": 2 * 4, "fe2": Fraction(6, 8), "fe4": 2, "fe5": Fraction(15, 20),
            "fa1": Fraction(2, 5) + Fraction(1, 5), "fa2": Fraction(1, 2) + Fraction(1, 3),
            "fa3": Fraction(3, 4) + Fraction(1, 2), "fa5": Fraction(2, 3) + Fraction(1, 6),
            "fs1": Fraction(5, 6) - Fraction(2, 6), "fs2": Fraction(3, 4) - Fraction(1, 6),
            "fs3": 1 - Fraction(3, 8), "fs4": Fraction(3, 2) - Fraction(3, 4),
            "fq1": Fraction(3, 4) * 20, "fq2": Fraction(2, 3) * 18,
            "fq3": Fraction(7, 2), "fq4": 18 / Fraction(3, 4), "fq5": 30 * (1 - Fraction(2, 5)),
            "pp1": Fraction(7, 10), "pp2": 2 * 6, "pp4": Fraction(8, 5),
            "pe1": 3 * 4, "pe2": Fraction(14, 21), "pe4": 6 * 4,
            "pa1": Fraction(3, 8) + Fraction(2, 8), "pa2": Fraction(2, 5) + Fraction(1, 2),
            "pa3": Fraction(5, 6) + Fraction(1, 3), "pa4": Fraction(1, 4) + Fraction(2, 3),
            "ps1": Fraction(7, 10) - Fraction(3, 10), "ps2": Fraction(5, 6) - Fraction(1, 4),
            "ps3": 2 - Fraction(3, 5), "ps4": Fraction(7, 8) - Fraction(1, 2),
            "pq1": Fraction(5, 6) * 24, "pq2": 14 / Fraction(2, 3),
            "pq3": Fraction(3, 5) * 25, "pq4": 9 * (1 - Fraction(1, 3)),
            "ap1": Fraction(9, 12), "ae1": 5 * 3, "ae2": Fraction(18, 30),
            "aa1": Fraction(1, 6) + Fraction(1, 4), "aa2": Fraction(4, 5) + Fraction(3, 10),
            "as1": Fraction(11, 12) - Fraction(1, 3), "as2": Fraction(5, 4) - Fraction(1, 2),
            "aq1": Fraction(3, 8) * 32, "aq2": 16 / Fraction(2, 5),
        }
        items = [q for l in FRACTION_LESSONS for q in l["exercises"]] + [
            q for l in FRACTION_LESSONS for q in PRACTICE[l["id"]]] + [
            q for _, q in COURSE_ASSESSMENTS["fractions"]]
        self.assertEqual({q["id"] for q in items if q["kind"] == "number"}, set(expected))
        for q in items:
            with self.subTest(question=q["id"]):
                if q["kind"] == "number":
                    self.assertEqual(Fraction(q["answer"]), expected[q["id"]])
                else:
                    self.assertIn(q["answer"], q["choices"])
                    self.assertEqual(len(set(q["choices"])), len(q["choices"]))
                self.assertTrue(grade(q["answer"], q["answer"], q["kind"]))
                self.assertTrue(q["hint"] and q["explanation"])

    def test_all_lessons_complete_course_and_master_six_new_skills(self):
        for lesson in FRACTION_LESSONS:
            for q in lesson["exercises"]:
                self.assertTrue(self.submit("lesson", lesson["id"], q)["correct"])
        state = self.store.state()
        course = next(c for c in state["catalog"]["courses"] if c["id"] == "fractions")
        self.assertEqual(course["completed_count"], 6)
        self.assertEqual([u["completed_count"] for u in course["units"]], [2, 3, 1])
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][6:12]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][:6] + state["mastery"][12:]))
        self.assertFalse(state["course_assessments"]["fractions"]["complete"])

    def test_practice_is_distinct_resumable_evidence_not_lesson_completion(self):
        lid = "fraction-addition"
        for q in PRACTICE[lid][:2]:
            self.submit("practice", lid, q)
        state = Store(self.store.path).state()
        self.assertEqual(state["practice"][lid]["passed"], ["pa1", "pa2"])
        self.assertEqual(state["passed"][lid], [])
        skill = next(s for s in state["mastery"] if s["id"] == "frac-addition")
        self.assertEqual(skill["independent"], 2)
        self.assertEqual(skill["status"], "mastered")
        self.submit("practice", lid, PRACTICE[lid][0])
        self.assertEqual(next(s for s in self.store.state()["mastery"] if s["id"] == "frac-addition")["independent"], 2)

    def test_practice_hints_and_retries_are_assisted(self):
        lid = "fraction-equivalence"
        q = PRACTICE[lid][0]
        self.submit("practice", lid, q, answer="0")
        self.assertTrue(self.submit("practice", lid, q)["assisted"])
        q = PRACTICE[lid][1]
        self.store.hint({"source": "practice", "lesson_id": lid, "version": 1, "question_id": q["id"]})
        self.assertTrue(self.submit("practice", lid, q)["assisted"])

    def test_assessment_saves_once_and_rejects_hints_and_cross_context(self):
        lid, q = COURSE_ASSESSMENTS["fractions"][0]
        payload = {"source": "course-assessment", "course_id": "fractions", "lesson_id": lid,
                   "question_id": q["id"], "version": 1, "answer": "0", "attempt_id": str(uuid4())}
        feedback = self.store.attempt(payload)
        self.assertFalse(feedback["correct"])
        self.assertIn("Answer saved", feedback["message"])
        self.assertEqual(self.store.attempt(payload), feedback)
        with self.assertRaisesRegex(InvalidRequest, "already saved"):
            self.store.attempt({**payload, "attempt_id": str(uuid4())})
        with self.assertRaisesRegex(InvalidRequest, "Hints"):
            self.store.hint(payload)
        for changes in [{"course_id": "everyday-foundations"}, {"lesson_id": "balance"},
                        {"source": "practice"}, {"source": "lesson"}, {"version": 2}]:
            with self.subTest(changes=changes), self.assertRaises(InvalidRequest):
                self.store.attempt({**payload, **changes, "attempt_id": str(uuid4())})
        state = self.store.state()
        self.assertEqual(state["course_assessments"]["fractions"]["answered"], ["ap1"])
        self.assertEqual(state["course_assessments"]["fractions"]["correct_count"], 0)
        self.assertEqual(state["passed"][lid], [])

    def test_invalid_assessment_input_is_not_recorded(self):
        lid, q = COURSE_ASSESSMENTS["fractions"][0]
        with self.assertRaises(InvalidRequest):
            self.submit("course-assessment", lid, q, course_id="fractions", answer="not a number")
        self.assertEqual(self.store.state()["course_assessments"]["fractions"]["answered"], [])

    def test_assessment_completion_and_score_survive_restart(self):
        for lid, q in COURSE_ASSESSMENTS["fractions"]:
            self.submit("course-assessment", lid, q, course_id="fractions")
        state = Store(self.store.path).state()
        check = state["course_assessments"]["fractions"]
        self.assertTrue(check["complete"])
        self.assertEqual(check["correct_count"], 12)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][6:12]))
        self.assertEqual(next(c for c in state["catalog"]["courses"] if c["id"] == "fractions")["completed_count"], 0)

    def test_lesson_versions_invalidate_only_their_practice_and_check_evidence(self):
        lid = "fraction-parts"
        self.submit("practice", lid, PRACTICE[lid][0])
        for lesson_id, q in COURSE_ASSESSMENTS["fractions"]:
            self.submit("course-assessment", lesson_id, q, course_id="fractions")
        content = self.store.author(lid)["lesson"]
        content["title"] = "A revised lesson on equal parts"
        self.store.save_lesson({"lesson_id": lid, "version": 1, "lesson": content})
        state = self.store.state()
        self.assertEqual(state["practice"][lid]["passed"], [])
        self.assertEqual(len(state["course_assessments"]["fractions"]["answered"]), 10)
        self.assertFalse(state["course_assessments"]["fractions"]["complete"])
        self.assertEqual(state["activity"]["attempts"], 13)
        lesson_id, q = COURSE_ASSESSMENTS["fractions"][0]
        self.submit("course-assessment", lesson_id, q, course_id="fractions", version=2)

    def test_old_database_seeds_only_missing_fraction_lessons(self):
        with self.store.connect() as db:
            for lesson in FRACTION_LESSONS:
                db.execute("DELETE FROM lessons WHERE id=?", (lesson["id"],))
        content = self.store.author("balance")["lesson"]
        content["title"] = "My existing lesson"
        self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": content})
        self.store.attempt({"source": "lesson", "lesson_id": "balance", "question_id": "b1",
                            "version": 2, "answer": "8", "attempt_id": str(uuid4())})
        reloaded = Store(self.store.path)
        self.assertEqual(reloaded.author("balance")["version"], 2)
        self.assertEqual(reloaded.author("balance")["lesson"]["title"], "My existing lesson")
        self.assertEqual(reloaded.state()["passed"]["balance"], ["b1"])
        self.assertEqual(len(reloaded.state()["lessons"]), 51)

    def test_public_banks_do_not_leak_answers_hints_or_explanations(self):
        state = self.store.state()
        for q in [q for bank in state["practice"].values() for q in bank["questions"]] + state["course_assessments"]["fractions"]["questions"]:
            self.assertFalse({"answer", "hint", "explanation"} & q.keys())

    def test_skill_prerequisite_cycles_are_rejected(self):
        skills = copy.deepcopy(SKILLS)
        skills[6]["prerequisites"] = [skills[7]["id"]]
        with self.assertRaisesRegex(ValueError, "Cyclic skill"):
            validate_catalog(LESSONS, skills)


if __name__ == "__main__":
    unittest.main()
