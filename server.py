"""Single-user, loopback-only Learnova development server."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from fractions import Fraction
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import mimetypes
from pathlib import Path
import sqlite3
from urllib.parse import urlsplit
from uuid import UUID

from curriculum import COURSE_ASSESSMENTS, DIAGNOSTIC, LESSONS, PRACTICE, SKILLS
from history import STORIES
from catalog import catalog_state, validate_catalog

ROOT = Path(__file__).resolve().parent
LOG = logging.getLogger("learnova")
MAX_BODY = 128 * 1024


class InvalidRequest(ValueError):
    pass


def text(value, name, maximum=200, allow_empty=False):
    if not isinstance(value, str) or len(value.strip()) > maximum:
        raise InvalidRequest(f"{name} must be text of at most {maximum} characters.")
    value = value.strip()
    if not value and not allow_empty:
        raise InvalidRequest(f"{name} is required.")
    return value


def grade(answer, expected, kind):
    if kind == "choice":
        return answer == expected
    try:
        supplied = Fraction(answer)
    except (ValueError, ZeroDivisionError):
        raise InvalidRequest("Enter a number or fraction, such as 0.5 or 1/2.") from None
    return supplied == Fraction(expected)


def public_question(item):
    return {key: value for key, value in item.items()
            if key not in {"answer", "explanation", "hint"}}


class Store:
    def __init__(self, path):
        validate_catalog(LESSONS, SKILLS)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS lessons (
                    id TEXT PRIMARY KEY, content TEXT NOT NULL, version INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY, source TEXT NOT NULL, lesson_id TEXT NOT NULL,
                    version INTEGER NOT NULL, question_id TEXT NOT NULL, skill TEXT NOT NULL,
                    answer TEXT NOT NULL, correct INTEGER NOT NULL,
                    assisted INTEGER NOT NULL, created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS hints (
                    lesson_id TEXT NOT NULL, version INTEGER NOT NULL,
                    question_id TEXT NOT NULL,
                    PRIMARY KEY (lesson_id, version, question_id)
                );
            """)
            for lesson in LESSONS:
                db.execute("INSERT OR IGNORE INTO lessons VALUES (?, ?, 1)",
                           (lesson["id"], json.dumps(lesson)))

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def lesson(self, lesson_id, db=None):
        if db is None:
            with self.connect() as connection:
                return self.lesson(lesson_id, connection)
        row = db.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,)).fetchone()
        if row is None:
            raise InvalidRequest("That lesson does not exist.")
        return json.loads(row["content"]), row["version"]

    def question(self, payload, db):
        source = payload.get("source")
        qid = text(payload.get("question_id"), "Question ID")
        version = payload.get("version")
        if type(version) is not int:
            raise InvalidRequest("Version must be an integer.")
        if source == "diagnostic":
            if version != 1:
                raise InvalidRequest("This assessment version is no longer available.")
            for skill, item in DIAGNOSTIC:
                if item["id"] == qid:
                    return "diagnostic", 1, skill, item
            raise InvalidRequest("That assessment question does not exist.")
        if source not in {"lesson", "practice", "course-assessment"}:
            raise InvalidRequest("Choose a lesson, practice, or assessment source.")
        lesson_id = text(payload.get("lesson_id"), "Lesson ID")
        lesson, current = self.lesson(lesson_id, db)
        if version != current:
            raise InvalidRequest("This lesson was updated. Reload it before continuing.")
        items = lesson["exercises"]
        if source == "practice":
            items = PRACTICE.get(lesson_id, [])
        elif source == "course-assessment":
            course_id = text(payload.get("course_id"), "Course ID")
            items = [q for lid, q in COURSE_ASSESSMENTS.get(course_id, []) if lid == lesson_id]
        for item in items:
            if item["id"] == qid:
                return lesson_id, current, lesson["skill"], item
        raise InvalidRequest("That question does not belong to this lesson.")

    def attempt(self, payload):
        attempt_id = text(payload.get("attempt_id"), "Attempt ID")
        try:
            UUID(attempt_id)
        except ValueError:
            raise InvalidRequest("Attempt ID must be a UUID.") from None
        answer = text(payload.get("answer"), "Answer", 100)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            lesson_id, version, skill, item = self.question(payload, db)
            previous = db.execute("SELECT * FROM attempts WHERE id = ?",
                                  (attempt_id,)).fetchone()
            if previous:
                if (previous["answer"], previous["lesson_id"], previous["question_id"],
                    previous["version"], previous["source"]) != (
                        answer, lesson_id, item["id"], version, payload["source"]):
                    raise InvalidRequest("Attempt ID was already used for another answer.")
                return self.feedback(bool(previous["correct"]), bool(previous["assisted"]), item,
                                     payload["source"] == "course-assessment")
            if payload["source"] == "course-assessment" and db.execute(
                "SELECT 1 FROM attempts WHERE source=? AND lesson_id=? AND version=? AND question_id=?",
                (payload["source"], lesson_id, version, item["id"])).fetchone():
                raise InvalidRequest("This assessment answer is already saved. Resume the assessment.")
            if item["kind"] == "choice" and answer not in item["choices"]:
                raise InvalidRequest("Select one of the available answer choices.")
            correct = grade(answer, item["answer"], item["kind"])
            assisted = bool(db.execute(
                "SELECT 1 FROM hints WHERE lesson_id=? AND version=? AND question_id=?",
                (lesson_id, version, item["id"])).fetchone())
            assisted = assisted or bool(db.execute(
                "SELECT 1 FROM attempts WHERE lesson_id=? AND version=? AND question_id=? "
                "AND correct=0", (lesson_id, version, item["id"])).fetchone())
            db.execute("INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (attempt_id, payload["source"], lesson_id, version, item["id"],
                        skill, answer, int(correct), int(assisted),
                        datetime.now(timezone.utc).isoformat()))
        return self.feedback(correct, assisted, item, payload["source"] == "course-assessment")

    @staticmethod
    def feedback(correct, assisted, item, assessment=False):
        return {
            "correct": correct, "assisted": assisted,
            "message": item["explanation"] if correct else
                       "Answer saved. Continue the check, then review the recommended lessons." if assessment else
                       "Not quite yet. Try a different approach, or open the lesson hint.",
        }

    def hint(self, payload):
        with self.connect() as db:
            lesson_id, version, _, item = self.question(payload, db)
            if payload.get("source") in {"diagnostic", "course-assessment"}:
                raise InvalidRequest("Hints are not available during an assessment.")
            db.execute("INSERT OR IGNORE INTO hints VALUES (?, ?, ?)",
                       (lesson_id, version, item["id"]))
        return {"hint": item["hint"]}

    def state(self):
        with self.connect() as db:
            lessons = []
            versions = {}
            for row in db.execute("SELECT * FROM lessons ORDER BY rowid"):
                lesson = json.loads(row["content"])
                versions[lesson["id"]] = row["version"]
                lesson["version"] = row["version"]
                lesson["exercises"] = [public_question(q) for q in lesson["exercises"]]
                lessons.append(lesson)
            attempts = [dict(row) for row in db.execute("SELECT * FROM attempts ORDER BY rowid")]
            profile_row = db.execute("SELECT value FROM settings WHERE key='profile'").fetchone()
        valid = [a for a in attempts if a["version"] == (
            1 if a["source"] == "diagnostic" else versions.get(a["lesson_id"]))]
        mastery = []
        for skill in SKILLS:
            evidence = [a for a in valid if a["skill"] == skill["id"]]
            independent = {(a["source"], a["lesson_id"], a["question_id"])
                           for a in evidence if a["correct"] and not a["assisted"]}
            recent = evidence[-10:]
            accuracy = sum(a["correct"] for a in recent) / len(recent) if recent else 0
            mastered = len(independent) >= 2 and accuracy >= 0.8
            mastery.append({**skill, "status": "mastered" if mastered else
                            ("developing" if evidence else "not-started"),
                            "independent": len(independent),
                            "accuracy": round(accuracy * 100), "attempts": len(evidence)})
        passed = {}
        for lesson in lessons:
            passed[lesson["id"]] = list(dict.fromkeys(a["question_id"] for a in valid
                if a["source"] == "lesson" and a["lesson_id"] == lesson["id"] and a["correct"]))
        practice = {lid: {
            "questions": [public_question(q) for q in items],
            "passed": list(dict.fromkeys(a["question_id"] for a in valid
                                        if a["source"] == "practice" and a["lesson_id"] == lid and a["correct"])),
        } for lid, items in PRACTICE.items()}
        by_id = {lesson["id"]: lesson for lesson in lessons}
        assessments = {}
        for cid, items in COURSE_ASSESSMENTS.items():
            questions = [{"lesson_id": lid, "version": versions[lid], "skill": by_id[lid]["skill"],
                          **public_question(q)} for lid, q in items]
            ids = {q["id"] for q in questions}
            results = [a for a in valid if a["source"] == "course-assessment" and a["question_id"] in ids]
            assessments[cid] = {
                "questions": questions, "answered": [a["question_id"] for a in results],
                "correct_count": sum(a["correct"] for a in results),
                "complete": len(results) == len(questions),
            }
        diagnostic_ids = list(dict.fromkeys(a["question_id"] for a in valid
                                           if a["source"] == "diagnostic"))
        days = sorted({a["created_at"][:10] for a in attempts})
        today = datetime.now(timezone.utc).date()
        streak = 0
        from datetime import timedelta
        cursor = today if today.isoformat() in days else today - timedelta(days=1)
        while cursor.isoformat() in days:
            streak += 1
            cursor -= timedelta(days=1)
        return {
            "profile": json.loads(profile_row["value"]) if profile_row else None,
            "lessons": lessons, "mastery": mastery, "passed": passed,
            "catalog": catalog_state(lessons, passed),
            "practice": practice, "course_assessments": assessments, "stories": STORIES,
            "diagnostic": [{"skill": skill, **public_question(q)} for skill, q in DIAGNOSTIC],
            "diagnostic_answered": diagnostic_ids,
            "activity": {"days": days, "streak": streak, "attempts": len(attempts)},
            "tutor": {"enabled": False, "reason": "No AI provider is configured. "
                      "Lesson hints are available; they are authored content, not AI."},
        }

    def save_profile(self, payload):
        name = text(payload.get("name"), "Display name", 40)
        goal = payload.get("goal")
        minutes = payload.get("minutes")
        if goal not in {"Build foundations", "Prepare for tests", "Stay curious"}:
            raise InvalidRequest("Choose a supported learning goal.")
        if type(minutes) is not int or minutes not in {5, 10, 15, 20}:
            raise InvalidRequest("Choose a daily goal of 5, 10, 15, or 20 minutes.")
        profile = {"name": name, "goal": goal, "minutes": minutes}
        with self.connect() as db:
            db.execute("INSERT INTO settings VALUES ('profile', ?) "
                       "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       (json.dumps(profile),))
        return {"profile": profile}

    def author(self, lesson_id):
        lesson, version = self.lesson(lesson_id)
        return {"lesson": lesson, "version": version}

    def save_lesson(self, payload):
        lesson_id = text(payload.get("lesson_id"), "Lesson ID")
        content = payload.get("lesson")
        if not isinstance(content, dict):
            raise InvalidRequest("Lesson content must be an object.")
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            original, version = self.lesson(lesson_id, db)
            if type(payload.get("version")) is not int or payload.get("version") != version:
                raise InvalidRequest("Another edit changed this lesson. Reload before saving.")
            if set(content) != set(original):
                raise InvalidRequest("Keep the existing lesson fields.")
            for field in {"id", "skill", "duration", "color", "icon", "visual"}:
                if content.get(field) != original[field]:
                    raise InvalidRequest(f"{field} cannot be changed in the local editor.")
            updated = dict(original)
            for field, maximum in [("title", 80), ("subtitle", 140), ("intro", 3000),
                                   ("takeaway", 300), ("formula", 150)]:
                updated[field] = text(content.get(field), field.capitalize(), maximum)
            exercises = content.get("exercises")
            if not isinstance(exercises, list) or len(exercises) != len(original["exercises"]):
                raise InvalidRequest("Keep the existing exercises in this local editor.")
            clean = []
            for old, new in zip(original["exercises"], exercises):
                if not isinstance(new, dict) or new.get("id") != old["id"]:
                    raise InvalidRequest("Exercise IDs and order must remain unchanged.")
                if set(new) != set(old) or new.get("kind") != old["kind"]:
                    raise InvalidRequest("Keep each exercise's fields and answer type.")
                q = {"id": old["id"], "kind": old["kind"]}
                for field, limit in [("prompt", 600), ("answer", 100),
                                     ("explanation", 1000), ("hint", 600)]:
                    q[field] = text(new.get(field), field.capitalize(), limit)
                if q["kind"] == "choice":
                    choices = new.get("choices")
                    if not isinstance(choices, list) or not 2 <= len(choices) <= 6:
                        raise InvalidRequest("Choice questions need 2 to 6 choices.")
                    q["choices"] = [text(c, "Choice", 100) for c in choices]
                    if len(set(q["choices"])) != len(q["choices"]):
                        raise InvalidRequest("Choices must be unique.")
                    if q["answer"] not in q["choices"]:
                        raise InvalidRequest("The correct answer must be one of the choices.")
                else:
                    grade(q["answer"], q["answer"], "number")
                clean.append(q)
            updated["exercises"] = clean
            if updated == original:
                return {"version": version, "message": "No content changes to publish."}
            db.execute("UPDATE lessons SET content=?, version=? WHERE id=?",
                       (json.dumps(updated), version + 1, lesson_id))
        return {"version": version + 1, "message": "Published. Previous-version progress "
                "is retained in history, but no longer counts toward this lesson."}


class Handler(BaseHTTPRequestHandler):
    server_version = "Learnova/0.1"

    def log_message(self, fmt, *args):
        LOG.info(fmt, *args)

    def respond(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def valid_host(self):
        port = self.server.server_address[1]
        return self.headers.get("Host") in {f"localhost:{port}", f"127.0.0.1:{port}"}

    def do_GET(self):
        if not self.valid_host():
            self.respond(HTTPStatus.FORBIDDEN, {"error": "Use the localhost app address."})
            return
        path = urlsplit(self.path).path
        try:
            if path == "/api/state":
                self.respond(200, self.server.store.state())
            elif path.startswith("/api/author/"):
                self.respond(200, self.server.store.author(path.removeprefix("/api/author/")))
            elif path.startswith("/api/"):
                self.respond(404, {"error": "Endpoint not found."})
            else:
                names = {"/": "index.html", "/app.js": "app.js", "/styles.css": "styles.css"}
                if path not in names:
                    self.respond(404, {"error": "Page not found."})
                    return
                file = ROOT / "web" / names[path]
                body = file.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type",
                                 f"{mimetypes.guess_type(file.name)[0]}; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-cache")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("Content-Security-Policy", "default-src 'self'; "
                                 "script-src 'self'; style-src 'self'; img-src 'self' data:; "
                                 "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; "
                                 "form-action 'self'")
                self.end_headers()
                self.wfile.write(body)
        except InvalidRequest as exc:
            self.respond(400, {"error": str(exc)})
        except (sqlite3.Error, OSError):
            LOG.exception("Could not serve request")
            self.respond(500, {"error": "Could not load data. Check the server log and retry."})

    def do_POST(self):
        port = self.server.server_address[1]
        origins = {f"http://localhost:{port}", f"http://127.0.0.1:{port}"}
        if not self.valid_host() or self.headers.get("Origin") not in origins:
            self.respond(403, {"error": "Requests must come from the local Learnova app."})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.respond(415, {"error": "Use application/json."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                self.respond(413, {"error": "Request is empty or exceeds 128 KB."})
                return
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise InvalidRequest("Request must be a JSON object.")
            path = urlsplit(self.path).path
            actions = {"/api/profile": self.server.store.save_profile,
                       "/api/attempt": self.server.store.attempt,
                       "/api/hint": self.server.store.hint,
                       "/api/author": self.server.store.save_lesson}
            if path == "/api/tutor":
                with self.server.store.connect() as db:
                    self.server.store.question(payload, db)
                text(payload.get("message"), "Message", 2000)
                self.respond(503, {"error": "AI tutoring is disabled: no provider is configured. "
                                  "Use the authored lesson hints instead.",
                                  "code": "TUTOR_NOT_CONFIGURED"})
            elif path in actions:
                self.respond(200, actions[path](payload))
            else:
                self.respond(404, {"error": "Endpoint not found."})
        except (InvalidRequest, ValueError) as exc:
            self.respond(400, {"error": str(exc)})
        except (sqlite3.Error, OSError):
            LOG.exception("Could not save request")
            self.respond(500, {"error": "Could not save your work. Check the server log and retry."})


def make_server(port=8000, database=None):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.store = Store(database or ROOT / "data" / "learnova.db")
    return server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    with make_server(args.port) as server:
        print(f"Learnova ready at http://127.0.0.1:{server.server_address[1]}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nLearnova stopped.", flush=True)
