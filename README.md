# Learnova

An interactive-mathematics learning app with courses, lessons, practice, and
course checks. It runs locally on your machine.

## Run on Windows

Python 3.12 is sufficient. There are no third-party runtime dependencies.

```powershell
Set-Location C:\Users\cwahome\dev\learnova
python server.py
```

Open **http://127.0.0.1:8000**. Stop with Ctrl+C. To choose another port:

```powershell
python server.py --port 8001
```

## Included

- Responsive overview, course library, practice, and skill-map screens.
- A warm, illustrated visual design: soft gradient backgrounds, a lesson-specific
  illustration on every lesson card, lesson header, and playable course card,
  tactile answer choices, styled sliders, and a small celebration on correct
  answers. Motion respects the reduced-motion setting. The home hero has floating
  math symbols, the sidebar shows live lesson progress, and finishing a lesson
  shows a confetti burst (plus a banner when a whole course is complete).
  All styling uses external
  CSS and SVG attributes, because the local server's Content Security Policy
  blocks inline `style` attributes.
- Seven subject areas, 69 courses, and subject/course/unit navigation. Courses
  are ordered from simple to complex within each subject, using each course's
  prerequisite chain to assign a Beginner, Intermediate, or Advanced level.
- A roadmap page listing every course by subject and topic group.
- A beginner path for people starting with no foundation, taught in this order:
  "Counting and number sense" (three lessons), "Adding and subtracting" (three
  lessons), and "Multiplying and dividing" (four lessons, ending with a word
  problems lesson on choosing the operation). Fractions and negative numbers now
  depend on it, and the home screen's Start button points at the first lesson you
  have not yet mastered, beginning with counting. Each lesson has a hands-on
  explorer (ten-frames, tens-and-ones blocks, number-line hops, carrying, a gap
  between towers, dot arrays, sharing, and a story-type picker), 4 lesson
  challenges, 4 practice questions, and a course check with two questions per
  lesson.
- Nine playable courses: the beginner path above, the six-lesson starter
  course, fractions, equations ("First steps with equations"), linear
  relationships ("Lines tell a story"), a combined geometry course ("Geometry and
  coordinates", nine lessons from perimeter and angles through slopes, shapes,
  and polar coordinates), and a math history course ("How math was invented").
  The other 60 courses are outlines with objectives and proposed prerequisites,
  not playable courses.
- Math history in two forms. Story cards ("Why people needed this") open
  sixteen lessons with a short account and illustration. They are display-only:
  not graded, and they never affect progress. The history course follows the
  chain of needs from counting to geometry in eight low-stakes lessons, with no
  graded course check. History text is written in hedged language where
  scholars disagree and should be fact-checked against reputable sources before
  release.
- Editable local learner profile and daily intention.
- Fifty-one lessons, 225 lesson challenges, hints, and explanations.
- The fractions course covers equal parts, equivalence, comparison, addition,
  subtraction, and fractions of quantities. It includes 30 lesson challenges,
  24 separate authored practice questions, and a twelve-question course check.
- The equations course covers equality and solutions, inverse operations,
  two-step equations, combining and distributing terms, and equations in
  context. It has the same structure: 30 lesson challenges, 24 separate
  practice questions, and a twelve-question course check.
- Interactive fraction bars, equivalent partitions, a 0-to-2 number line, and
  a whole-amount control, plus an equation balance explorer that shows each
  inverse-operation step. Explorer changes do not submit answers or award mastery.
- Exploratory graph canvas with slope and intercept controls.
- Twelve-question starting assessment with resumable submitted progress.
- Separate resumable course assessments for fractions and equations: one valid
  answer per question and current lesson version, no hints or retries. Invalid
  input is not recorded. The results report correctness and course skill
  mastery, not a certificate or automatic lesson completion.
- SQLite-backed attempts, lesson completion, activity dates, and mastery.
- Mastery requires two distinct unassisted correct answers and at least 80%
  accuracy over the skill's last ten attempts. Retries following mistakes and
  hinted questions are assisted. Repeating questions adds no distinct evidence.
- Course recommendations select the earliest skill without mastery in the
  prerequisite chain. The starting diagnostic itself is fixed, not adaptive.
- Local JSON content editor with validation, optimistic concurrency, and
  versioned publishing. Changed lesson versions invalidate their prior-version
  completion and mastery evidence without deleting history.
- Explicit AI-disabled UI and an integration endpoint that returns HTTP 503
  with `TUTOR_NOT_CONFIGURED`. Hints are authored content, not simulated AI.

Lesson progress resumes at the first unsolved challenge. Fractions practice
resumes at its first unsolved review question; finishing all four allows reviewing
the same set again without new distinct mastery evidence. Starter-course review
still repeats its lesson questions. Neither course generates unlimited practice.
Both assessments resume at their first unanswered question.

Numeric answers accept equivalent fractions and decimals. They test quantity,
not whether a particular notation is in lowest terms. Mixed-number answers must
be entered as improper fractions or decimals (for example, `3/2` or `1.5`).

## Local-only boundary

This is a **single-user development MVP**, not a production subscription service.
The server binds only to `127.0.0.1`. Write requests require the app's local
origin and JSON content type, and the Host header is checked. The editor has no
role-based authentication because the entire app is restricted to this local
workspace. Do not expose it through a public tunnel or change its bind address.

Data is stored in `data\learnova.db`, which is ignored by Git. Copy that file
while the server is stopped to back it up. Profile names need not be real names.
No analytics, hosted fonts, trackers, or external AI requests are used.

Activity days use UTC. Daily minutes are an intention, not measured study time.
No payment or billing screens pretend that a transaction has occurred.

## AI integration contract

`POST /api/tutor` accepts a JSON object with:

```json
{
  "source": "lesson",
  "lesson_id": "balance",
  "version": 1,
  "question_id": "b1",
  "message": "Help me understand the next step."
}
```

The current route validates lesson context and the message, then explicitly
returns 503; it is an integration boundary, **not an implemented provider**.
Provider-specific authentication, streaming, context assembly, validated canvas
actions, usage budgets, consent, and tutor-quality evaluations are still needed.
Configure secrets locally only when that implementation is added; never put
keys in browser JavaScript or commit them.

## Validation

```powershell
python -m unittest discover -s tests -v
python -m compileall -q server.py curriculum.py catalog.py tests
```

Tests use temporary databases, not your learner data. They cover answer checking,
invalid input, assisted evidence, accuracy thresholds, distinct-question mastery,
idempotency, persistence, assessment outcomes, content versioning, write origins,
restricted paths, and the explicit disabled-tutor response.
Catalog tests also check inventory counts, deduplication, unique lesson ownership,
course prerequisite cycles, honest availability, completion, and preservation of
edited lesson versions and saved progress. Fractions tests independently check
arithmetic answers, course completion, distinct practice evidence, assisted
answers, fixed assessment scoring, resume, and old-database seeding.

When shell loopback sockets are unavailable, the data-layer tests can run without
HTTP connections:

```powershell
$env:PYTHONPATH = "tests"
python -m unittest test_app.StoreTests test_catalog.CatalogTests test_fractions.FractionsTests test_equations.EquationsTests test_linear.LinearTests test_geometry.GeometryTests test_history.HistoryTests test_beginner.BeginnerPathTests -v
```

This does not replace the HTTP tests, which still need an environment with
permitted loopback socket connections.

## Curriculum authoring and expansion

`catalog.py` is the source-controlled curriculum map: subjects contain courses,
courses contain ordered units, and units reference stable lesson IDs. Each
published lesson belongs to exactly one unit. Related starter lessons are
cross-references, not course completion evidence. Course prerequisites are
proposed by Learnova and may cross subjects; they do not lock access.

`curriculum.py` contains published lessons, skills, separate `PRACTICE` banks,
`COURSE_ASSESSMENTS`, and the fixed twelve-question starter diagnostic.
The starter diagnostic measures only its six original skills. The fractions
course check measures its six separate skills. Neither assesses the whole catalog.
The local JSON editor edits existing published lessons only. It does not yet
create courses, units, skills, or new lessons.

To expand a course:

1. Refine its original unit objectives and course prerequisites in `catalog.py`.
2. Author and review original lessons/challenges in `curriculum.py`, with stable
   IDs, skills, hints, explanations, and supported activity types.
3. Add published lesson IDs to their owning units. Startup validates ownership,
   course references, and acyclic prerequisites. Availability and completion are
   derived from actual published lessons; empty units remain planned.
4. Add tests for answers, progression, and interaction behavior. Extend the
   diagnostic deliberately rather than implying that existing questions measure
   new skills. New graph/geometry/coding activity types need implementation.
5. Keep the roadmap current as courses move from outline to playable.

Adding the catalog does not rewrite existing SQLite lesson content, change lesson
versions, or reset progress. Re-running the server inserts only missing lesson
seeds. As before, updates to existing persisted lessons use the versioned editor.
Practice and course-assessment attempts use their own question IDs and sources.
They can provide independent skill evidence but never mark lesson challenges
complete. Changing an associated lesson version invalidates its old practice
and course-check evidence while retaining history; unchanged lessons' assessment
answers remain saved. The JSON editor does not edit these source-controlled banks.
Changes to existing bank questions require deliberate version invalidation of
their associated lessons, or new question IDs for genuinely new questions.

The playable courses have automated arithmetic and interaction checks
(answers are verified against independent calculations), but still need
independent educator/learner review before production, and the history text
needs a fact-check. Learnova is meant for people who are struggling with math or
starting with no foundation, so the beginner path now comes first. The next
content milestone is to test it with real beginners, then extend it with more
hands-on lessons (for example, comparing and rounding, money and time, and
word problems) before fractions.

## Before production

Implement authenticated accounts and editor roles, deployable backend/storage,
AI provider integration and evaluations, fresh/adaptive question selection,
subscription entitlements and verified payment webhooks, account deletion and
retention controls, backups, observability, and applicable learner/child privacy
requirements. Homework uploads, voice, coding execution, family seats, and
classroom management are not implemented in this first version.

Python's built-in HTTP server is used for local development, not production.
