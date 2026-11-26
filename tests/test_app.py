import copy
from http.client import HTTPConnection
import json
from pathlib import Path
import tempfile
import threading
import unittest
from uuid import uuid4

from curriculum import DIAGNOSTIC
from server import InvalidRequest, Store, grade, make_server


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.directory.name) / "learnova.db")

    def tearDown(self):
        self.directory.cleanup()

    def submit(self, lesson_id, qid, response, **extra):
        return self.store.attempt({
            "source": "lesson", "lesson_id": lesson_id, "question_id": qid,
            "version": 1, "answer": response, "attempt_id": str(uuid4()), **extra,
        })

    def test_seed_and_public_questions_have_no_answer_keys(self):
        state = self.store.state()
        self.assertEqual(len(state["lessons"]), 50)
        self.assertEqual(len(state["diagnostic"]), 12)
        self.assertFalse(state["tutor"]["enabled"])
        for q in state["diagnostic"] + [
                q for lesson in state["lessons"] for q in lesson["exercises"]]:
            self.assertNotIn("answer", q)
            self.assertNotIn("hint", q)
            self.assertNotIn("explanation", q)
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"]))

    def test_numeric_equivalence_and_invalid_input(self):
        self.assertTrue(grade("0.5", "1/2", "number"))
        self.assertTrue(grade("4/6", "2/3", "number"))
        self.assertFalse(grade("-2", "2", "number"))
        for answer in ["0/0", "words", "2+2"]:
            with self.assertRaises(InvalidRequest):
                grade(answer, "2", "number")

    def test_wrong_answer_hint_and_retry_are_assisted(self):
        first = self.submit("balance", "b1", "4")
        self.assertFalse(first["correct"])
        second = self.submit("balance", "b1", "8")
        self.assertTrue(second["correct"])
        self.assertTrue(second["assisted"])
        self.store.hint({"source": "lesson", "lesson_id": "balance",
                         "question_id": "b2", "version": 1})
        hinted = self.submit("balance", "b2", "7")
        self.assertTrue(hinted["assisted"])
        mastery = self.store.state()["mastery"][2]
        self.assertEqual(mastery["independent"], 0)
        self.assertEqual(mastery["status"], "developing")

    def test_mastery_requires_distinct_unassisted_evidence(self):
        for _ in range(5):
            self.submit("balance", "b1", "8")
        self.assertEqual(self.store.state()["mastery"][2]["status"], "developing")
        self.assertEqual(self.store.state()["mastery"][2]["independent"], 1)
        self.submit("balance", "b2", "7")
        self.assertEqual(self.store.state()["mastery"][2]["status"], "mastered")

    def test_mastery_requires_accuracy_threshold(self):
        self.submit("balance", "b1", "8")
        self.submit("balance", "b2", "7")
        self.submit("balance", "b3", "100")
        self.assertEqual(self.store.state()["mastery"][2]["status"], "developing")
        self.assertEqual(self.store.state()["mastery"][2]["accuracy"], 67)

    def test_idempotency_and_conflicts(self):
        attempt_id = str(uuid4())
        self.submit("balance", "b1", "8", attempt_id=attempt_id)
        self.submit("balance", "b1", "8", attempt_id=attempt_id)
        self.assertEqual(self.store.state()["activity"]["attempts"], 1)
        with self.assertRaises(InvalidRequest):
            self.submit("balance", "b1", "9", attempt_id=attempt_id)
        self.assertEqual(self.store.state()["activity"]["attempts"], 1)

    def test_persistence_and_resume(self):
        self.store.save_profile({"name": "Explorer", "goal": "Stay curious", "minutes": 15})
        self.submit("balance", "b1", "8")
        reloaded = Store(self.store.path).state()
        self.assertEqual(reloaded["profile"]["name"], "Explorer")
        self.assertEqual(reloaded["passed"]["balance"], ["b1"])
        self.assertEqual(reloaded["activity"]["streak"], 1)

    def test_all_diagnostic_answers_establish_six_skills(self):
        for _, q in DIAGNOSTIC:
            self.store.attempt({"source": "diagnostic", "question_id": q["id"],
                                "version": 1, "answer": q["answer"],
                                "attempt_id": str(uuid4())})
        state = self.store.state()
        self.assertEqual(len(state["diagnostic_answered"]), 12)
        self.assertTrue(all(s["status"] == "mastered" for s in state["mastery"][:6]))
        self.assertTrue(all(s["status"] == "not-started" for s in state["mastery"][6:]))
        self.assertEqual(len(state["mastery"]), 50)
        self.assertTrue(all(not passed for passed in state["passed"].values()))

    def test_versioning_excludes_stale_evidence_and_checks_conflict(self):
        self.submit("balance", "b1", "8")
        self.submit("balance", "b2", "7")
        current = self.store.author("balance")
        lesson = copy.deepcopy(current["lesson"])
        lesson["title"] = "A freshly balanced idea"
        result = self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": lesson})
        self.assertEqual(result["version"], 2)
        state = self.store.state()
        self.assertEqual(state["passed"]["balance"], [])
        self.assertEqual(state["mastery"][2]["status"], "not-started")
        self.assertEqual(state["activity"]["attempts"], 2)
        with self.assertRaises(InvalidRequest):
            self.submit("balance", "b3", "5")
        with self.assertRaises(InvalidRequest):
            self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": lesson})

    def test_invalid_authoring_is_atomic(self):
        lesson = self.store.author("balance")["lesson"]
        lesson["exercises"][0]["answer"] = "not a number"
        with self.assertRaises(InvalidRequest):
            self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": lesson})
        self.assertEqual(self.store.author("balance")["version"], 1)
        self.assertEqual(self.store.author("balance")["lesson"]["exercises"][0]["answer"], "8")

    def test_immutable_metadata_rejected(self):
        lesson = self.store.author("balance")["lesson"]
        lesson["skill"] = "models"
        with self.assertRaises(InvalidRequest):
            self.store.save_lesson({"lesson_id": "balance", "version": 1, "lesson": lesson})

    def test_no_op_publish_preserves_progress(self):
        lesson = self.store.author("balance")["lesson"]
        self.assertEqual(self.store.save_lesson({
            "lesson_id": "balance", "version": 1, "lesson": lesson})["version"], 1)

    def test_input_validation_does_not_record_invalid_answers(self):
        for extra in [{"version": True}, {"question_id": "unknown"},
                      {"answer": "0/0"}, {"source": "unknown"},
                      {"attempt_id": "not-a-uuid"}]:
            with self.assertRaises(InvalidRequest):
                self.submit("balance", "b1", "8", **extra)
        with self.assertRaises(InvalidRequest):
            self.submit("fraction-sense", "f1", "not one of the choices")
        self.assertEqual(self.store.state()["activity"]["attempts"], 0)

    def test_profile_validation(self):
        for profile in [
            {"name": "", "goal": "Stay curious", "minutes": 10},
            {"name": "A", "goal": "Unsupported", "minutes": 10},
            {"name": "A", "goal": "Stay curious", "minutes": 100},
        ]:
            with self.assertRaises(InvalidRequest):
                self.store.save_profile(profile)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.server = make_server(0, Path(cls.directory.name) / "http.db")
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.directory.cleanup()

    def request(self, method, path, body=None, headers=None):
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        result = (response.status, dict(response.headers), response.read())
        connection.close()
        return result

    def post(self, path, payload, origin=True):
        headers = {"Content-Type": "application/json"}
        if origin:
            headers["Origin"] = f"http://127.0.0.1:{self.port}"
        return self.request("POST", path, json.dumps(payload), headers)

    def test_static_page_and_restricted_paths(self):
        status, headers, body = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Learnova", body)
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        for path in ["/server.py", "/data/learnova.db", "/../server.py", "/api/missing"]:
            self.assertEqual(self.request("GET", path)[0], 404)

    def test_cross_origin_and_host_rejected(self):
        self.assertEqual(self.post("/api/profile", {}, origin=False)[0], 403)
        self.assertEqual(self.request("POST", "/api/profile", "{}",
            {"Content-Type": "application/json", "Origin": "https://example.org"})[0], 403)
        self.assertEqual(self.request("GET", "/api/state", headers={"Host": "evil.example"})[0], 403)

    def test_json_validation(self):
        headers = {"Origin": f"http://127.0.0.1:{self.port}",
                   "Content-Type": "application/json"}
        self.assertEqual(self.request("POST", "/api/profile", "{", headers)[0], 400)
        self.assertEqual(self.post("/api/profile", [])[0], 400)
        self.assertEqual(self.post("/api/profile", {})[0], 400)

    def test_disabled_tutor_is_explicit(self):
        status, _, body = self.post("/api/tutor", {
            "source": "lesson", "lesson_id": "balance", "version": 1,
            "question_id": "b1", "message": "Can you help me reason through this?",
        })
        self.assertEqual(status, 503)
        self.assertEqual(json.loads(body)["code"], "TUTOR_NOT_CONFIGURED")

    def test_get_state_and_post_answer(self):
        status, _, body = self.request("GET", "/api/state")
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)["lessons"]), 50)
        self.assertEqual(json.loads(body)["catalog"]["summary"]["reference_course_count"], 64)
        status, _, body = self.post("/api/attempt", {
            "source": "lesson", "lesson_id": "balance", "version": 1,
            "question_id": "b1", "answer": "8", "attempt_id": str(uuid4()),
        })
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(body)["correct"])


if __name__ == "__main__":
    unittest.main()
