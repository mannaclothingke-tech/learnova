import copy
import json
from pathlib import Path
import tempfile
import unittest
from uuid import uuid4

from catalog import COURSES, TOPICS, validate_catalog
from curriculum import LESSONS, SKILLS
from server import Store


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.store = Store(Path(self.directory.name) / "catalog.db")

    def test_public_inventory_counts_and_deduplication(self):
        catalog = self.store.state()["catalog"]
        self.assertEqual(catalog["summary"], {
            "subject_count": 7, "course_count": 69, "available_course_count": 9,
            "published_lesson_count": 51, "reference_course_count": 64,
            "partial_reference_count": 2, "topic_count": 13,
        })
        self.assertEqual(sum(len(rows) for _, _, rows in TOPICS), 72)
        references = [c["reference"]["url"] for c in catalog["courses"] if c["reference"]]
        self.assertEqual(len(set(references)), 64)
        digital = next(c for c in catalog["courses"] if c["id"] == "digital-logic")
        self.assertEqual(digital["topics"], ["Logical Reasoning", "Technology", "Science"])

    def test_each_published_lesson_has_one_unit_owner(self):
        validate_catalog(LESSONS, SKILLS)
        catalog = self.store.state()["catalog"]
        ids = [lid for c in catalog["courses"] for u in c["units"] for lid in u["lesson_ids"]]
        self.assertCountEqual(ids, [l["id"] for l in LESSONS])
        self.assertEqual(len(set(ids)), len(ids))
        starter = next(c for c in catalog["courses"] if c["id"] == "everyday-foundations")
        self.assertEqual(starter["estimated_minutes"], sum(l["duration"] for l in LESSONS[:6]))
        self.assertEqual(len(ids), 51)
        self.assertEqual(starter["status"], "available")
        self.assertEqual(len(starter["units"]), 3)

    def test_outlines_do_not_pretend_to_be_playable(self):
        state = self.store.state()
        playable = {"everyday-foundations", "fractions", "first-equations", "linear-relationships", "coordinate-geometry", "math-history",
                    "counting-numbers", "add-subtract", "multiply-divide"}
        for course in [c for c in state["catalog"]["courses"] if c["id"] not in playable]:
            self.assertEqual(course["status"], "planned")
            self.assertEqual(course["lesson_count"], 0)
            self.assertEqual(course["completed_count"], 0)
            self.assertEqual(course["estimated_minutes"], 0)
            for unit in course["units"]:
                self.assertEqual(unit["status"], "planned")
                self.assertEqual(unit["lesson_ids"], [])
                self.assertTrue(unit["objectives"])
        self.assertEqual(len(state["mastery"]), 51)
        self.assertEqual(len(state["diagnostic"]), 12)

    def test_existing_database_content_and_evidence_are_not_migrated(self):
        current = self.store.author("balance")
        current["lesson"]["title"] = "My edited balance lesson"
        self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": current["lesson"]})
        self.store.attempt({"source": "lesson", "lesson_id": "balance", "question_id": "b1",
                            "version": 2, "answer": "8", "attempt_id": str(uuid4())})
        before = self.store.state()
        after = Store(self.store.path).state()
        for key in ["lessons", "mastery", "passed", "activity", "diagnostic_answered"]:
            self.assertEqual(before[key], after[key])
        self.assertEqual(self.store.author("balance")["version"], 2)

    def test_course_completion_uses_all_questions_in_current_version(self):
        for q in LESSONS[0]["exercises"]:
            self.store.attempt({"source": "lesson", "lesson_id": "fraction-sense",
                                "question_id": q["id"], "version": 1, "answer": q["answer"],
                                "attempt_id": str(uuid4())})
        starter = lambda: next(c for c in self.store.state()["catalog"]["courses"] if c["id"] == "everyday-foundations")
        self.assertEqual(starter()["completed_count"], 1)
        self.assertEqual(starter()["units"][0]["completed_count"], 1)
        content = self.store.author("fraction-sense")["lesson"]
        content["title"] = "New fraction lesson"
        self.store.save_lesson({"lesson_id": "fraction-sense", "version": 1, "lesson": content})
        self.assertEqual(starter()["completed_count"], 0)

    def test_public_catalog_is_serializable_and_has_no_answer_keys(self):
        catalog = self.store.state()["catalog"]
        serialized = json.dumps(catalog)
        self.assertNotIn('"answer":', serialized)
        self.assertNotIn('"hint":', serialized)
        next(c for c in catalog["courses"] if c["id"] == "everyday-foundations")["units"][0]["lesson_ids"].clear()
        fresh = next(c for c in self.store.state()["catalog"]["courses"] if c["id"] == "everyday-foundations")
        self.assertEqual(fresh["lesson_count"], 6)

    def test_invalid_catalog_references_fail_explicitly(self):
        mutations = [
            lambda c: c.append(copy.deepcopy(c[0])),
            lambda c: c[0].update(subject_id="missing"),
            lambda c: c[0].update(prerequisites=["missing"]),
            lambda c: c[0].update(related_lesson_ids=["missing"]),
            lambda c: c[0]["units"][0].update(objectives=[]),
            lambda c: c[0]["units"][0]["lesson_ids"].append("missing"),
            lambda c: c[0]["units"][0]["lesson_ids"].append("balance"),
            lambda c: c[0]["units"][0]["lesson_ids"].clear(),
            lambda c: c[1]["units"][0].update(id=c[0]["units"][0]["id"]),
            lambda c: c[0].update(prerequisites=[c[0]["id"]]),
            lambda c: c[0].update(units=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                courses = copy.deepcopy(COURSES)
                mutate(courses)
                with self.assertRaises(ValueError):
                    validate_catalog(LESSONS, SKILLS, courses)

    def test_indirect_prerequisite_cycles_are_rejected(self):
        courses = copy.deepcopy(COURSES)
        courses[0]["prerequisites"] = [courses[1]["id"]]
        courses[1]["prerequisites"] = [courses[0]["id"]]
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            validate_catalog(LESSONS, SKILLS, courses)


if __name__ == "__main__":
    unittest.main()
