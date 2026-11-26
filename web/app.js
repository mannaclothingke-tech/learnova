"use strict";

const $ = (selector, root = document) => root.querySelector(selector);
const esc = (value) => String(value).replace(/[&<>"']/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
let state;
let session = null;
let studio = null;
let busy = false;
let toastTimer;
let routeSequence = 0;
const iconPaths = {
  home: '<path d="m3 10 9-7 9 7v10H3z"/><path d="M9 20v-7h6v7"/>',
  learn: '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M8 7h8M8 11h8M8 15h4"/>',
  practice: '<path d="m13 2-9 12h7l-1 8 10-12h-7z"/>',
  progress: '<path d="M4 20V10M12 20V4M20 20v-7"/>',
  studio: '<path d="m4 16 12-12 4 4L8 20H4zM13 7l4 4"/>',
  arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
};
function icon(name, cls = "") {
  return `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${iconPaths[name] || iconPaths.learn}</svg>`;
}

async function api(path, payload) {
  const response = await fetch(path, payload === undefined ? { cache: "no-store" } : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || `Request failed (${response.status}).`);
  return result;
}
function toast(message) {
  const element = $("#toast");
  clearTimeout(toastTimer);
  element.textContent = message;
  element.hidden = false;
  toastTimer = setTimeout(() => { element.hidden = true; }, 6000);
}
function completed(lesson) {
  return lesson.exercises.every(q => state.passed[lesson.id].includes(q.id));
}
function recommended(course) {
  const lessons = course ? courseLessons(course) :
    state.catalog.courses.filter(c => c.subject_id === "math" && c.lesson_count).flatMap(courseLessons);
  return lessons.find(lesson => state.mastery.find(s => s.id === lesson.skill).status !== "mastered") || lessons[0];
}
function masteryCount() {
  return state.mastery.filter(s => s.status === "mastered").length;
}
function courseLessons(course) {
  return course.units.flatMap(unit => unit.lesson_ids.map(id => state.lessons.find(l => l.id === id)));
}
function lessonPlacement(id) {
  for (const course of state.catalog.courses) {
    const unit = course.units.find(u => u.lesson_ids.includes(id));
    if (unit) return { course, unit };
  }
  throw new Error(`Lesson ${id} has no curriculum placement.`);
}
function stepName(lesson) {
  return state.mastery.find(s => s.id === lesson.skill)?.name || lesson.title;
}
function miniArt(kind, color = "violet") {
  if (kind === "fraction") return `<svg class="lesson-art ${color}" viewBox="0 0 160 110" aria-hidden="true"><circle cx="80" cy="55" r="36" class="art-light"/><path d="M80 19a36 36 0 0 1 0 72z" class="art-dark"/><path d="M80 19v72M44 55h72" class="art-stroke"/></svg>`;
  if (kind === "expression") return `<svg class="lesson-art ${color}" viewBox="0 0 160 110" aria-hidden="true"><rect x="22" y="35" width="32" height="40" rx="8" class="art-dark"/><rect x="61" y="35" width="32" height="40" rx="8" class="art-dark"/><circle cx="120" cy="55" r="17" class="art-light"/><text x="38" y="61">x</text><text x="77" y="61">x</text><text x="120" y="61">2</text></svg>`;
  if (kind === "balance") return `<svg class="lesson-art ${color}" viewBox="0 0 160 110" aria-hidden="true"><path d="M80 25v61M58 89h44M28 35h104M43 35 25 63h36zM117 35 99 63h36z" class="art-stroke"/><circle cx="80" cy="35" r="7" class="art-dark"/></svg>`;
  return `<svg class="lesson-art ${color}" viewBox="0 0 160 110" aria-hidden="true"><path d="M30 20v70h106M30 66h106M30 42h106M56 20v70M82 20v70M108 20v70" class="art-grid"/><path d="m35 78 94-52" class="art-line"/><circle cx="78" cy="54" r="6" class="art-dark"/></svg>`;
}
function heroArt() {
  return `<svg class="hero-art" viewBox="0 0 380 280" role="img" aria-label="An illustration of a rising line and mathematical building blocks">
    <defs><pattern id="hero-grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0v32" fill="none" stroke="#617364" stroke-opacity=".25"/></pattern></defs>
    <rect x="40" y="15" width="290" height="245" rx="24" fill="url(#hero-grid)"/>
    <path d="M66 219h239M91 242V38" stroke="#87968a" stroke-width="1.5"/>
    <path d="m66 224 225-151" fill="none" stroke="#d8f36a" stroke-width="4"/>
    <path d="M151 167h76v-49" fill="none" stroke="#d8f36a" stroke-width="1.5" stroke-dasharray="5 5"/>
    <circle cx="151" cy="167" r="7" fill="#d8f36a"/><circle cx="227" cy="116" r="7" fill="#d8f36a"/>
    <text x="185" y="190" fill="#c1cbbd" font-size="13">run</text><text x="239" y="147" fill="#c1cbbd" font-size="13">rise</text>
    <g transform="rotate(-8 110 65)"><rect x="43" y="37" width="121" height="48" rx="14" fill="#ece7ff"/><text x="104" y="68" text-anchor="middle" fill="#46376a" font-size="22" font-family="Georgia">y = mx + b</text></g>
    <g transform="rotate(9 295 216)"><rect x="261" y="180" width="68" height="68" rx="18" fill="#d8f36a"/><path d="m277 216 10 10 26-29" fill="none" stroke="#2c3d2b" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>
    <path d="m310 38 4 10 10 4-10 4-4 10-4-10-10-4 10-4z" fill="#d8f36a"/>
  </svg>`;
}

function updateShell(page) {
  const nav = [["home", "Overview"], ["learn", "Explore lessons"], ["practice", "Practice"],
    ["progress", "Your progress"], ["studio", "Content studio"]];
  $("#nav").innerHTML = nav.map(([id, name]) => `<a href="#${id}" aria-label="${name}" class="nav-link ${page === id ? "active" : ""}" ${page === id ? 'aria-current="page"' : ""}>${icon(id)}<span>${name}</span>${id === "studio" ? '<span class="nav-tag">LOCAL</span>' : ""}</a>`).join("");
  $("#breadcrumb").innerHTML = `Your learning space <span>/</span> ${esc(nav.find(n => n[0] === page)?.[1] || "Lesson")}`;
  const name = state.profile?.name || "Your workspace";
  $("#profile-name").textContent = name;
  $("#avatar").textContent = name.slice(0, 1).toUpperCase();
  $("#goal-chip").textContent = `${state.profile?.minutes || 10} min / day`;
}
function heading(kicker, title, subtitle, trailing = "") {
  return `<div class="page-heading"><div><div class="eyebrow">${kicker}</div><h1>${title}</h1><p>${subtitle}</p></div>${trailing}</div>`;
}
function card(lesson, index) {
  const done = completed(lesson);
  const started = state.passed[lesson.id].length;
  return `<a class="lesson-card" href="#lesson/${lesson.id}">
    <div class="card-art ${lesson.color}">${miniArt(lesson.icon, lesson.color)}<span class="card-number">${String(index + 1).padStart(2, "0")}</span>${done ? `<span class="done-badge">${icon("check")} Completed</span>` : ""}</div>
    <div class="card-body"><span class="eyebrow small">${esc(stepName(lesson))}</span><h3>${esc(lesson.title)}</h3><p>${esc(lesson.subtitle)}</p><div class="card-meta"><span>${icon("clock")} ${lesson.duration} min</span><span>${started ? `${started}/${lesson.exercises.length} solved` : `${lesson.exercises.length} challenges`} ${icon("arrow")}</span></div></div>
  </a>`;
}
function home() {
  const next = recommended();
  const name = state.profile?.name;
  const done = state.lessons.filter(completed).length;
  const pathCourse = lessonPlacement(next.id).course;
  const pathLessons = courseLessons(pathCourse);
  const pathDone = pathLessons.filter(completed).length;
  const pathStart = Math.max(0, pathLessons.findIndex(l => l.id === next.id));
  const recent = [];
  for (let offset = 6; offset >= 0; offset--) {
    const date = new Date();
    date.setUTCDate(date.getUTCDate() - offset);
    const iso = date.toISOString().slice(0, 10);
    recent.push(`<div class="day"><span>${date.toLocaleDateString("en", { weekday: "narrow", timeZone: "UTC" })}</span><span class="day-circle ${state.activity.days.includes(iso) ? "done" : ""} ${offset === 0 ? "today" : ""}">${state.activity.days.includes(iso) ? icon("check") : date.getUTCDate()}</span></div>`);
  }
  return `${heading("LET'S KEEP YOUR CURIOSITY GOING", name ? `Welcome back, ${esc(name)} <span class="wave">&#10038;</span>` : 'Your next "aha" starts here.', "Build understanding, one small discovery at a time.",
    `<a class="text-link" href="#progress">View your progress ${icon("arrow")}</a>`)}
    <div class="dashboard-grid"><section class="hero"><div class="hero-copy"><span class="pill">LEARN BY DOING</span><h2>Make the next<br>idea <em>click.</em></h2><p>Not just the answer. The understanding.<br>Explore the math hiding in everyday things.</p><a class="button lime" href="#lesson/${next.id}">${state.activity.attempts ? "Continue your path" : "Start exploring"} ${icon("arrow")}</a><span class="hero-foot">${icon("clock")} One lesson. A fresh perspective.</span></div>${heroArt()}</section>
    <section class="week-card"><div class="section-label">YOUR LEARNING RHYTHM <span>&#10038;</span></div><div class="streak-value">${state.activity.streak}<span>day${state.activity.streak === 1 ? "" : "s"} of momentum</span></div><p>Consistency starts with showing up.</p><div class="week-days">${recent.join("")}</div><hr><div class="daily-goal">${icon("clock")}<span>Daily intention<strong>${state.profile?.minutes || 10} minutes of curiosity</strong></span><button class="icon-button" data-action="profile" aria-label="Edit daily intention">${icon("studio")}</button></div></section></div>
    <section class="stats-row"><div>${icon("learn")}<span><strong>${done}<small> / ${state.lessons.length}</small></strong>Lessons completed</span></div><div>${icon("check")}<span><strong>${masteryCount()}<small> / ${state.mastery.length}</small></strong>Skills mastered</span></div><div>${icon("practice")}<span><strong>${state.activity.attempts}</strong>Answers explored</span></div><div><span class="tiny-spark">&#10038;</span><span><strong>A little every day</strong>Progress, not perfection</span></div></section>
    <div class="section-heading"><div><span class="eyebrow">YOUR GUIDED PATH</span><h2>From little pieces to big ideas</h2></div><a class="text-link" href="#learn">Explore all lessons ${icon("arrow")}</a></div>
    <a class="path-banner" href="#course/${pathCourse.id}"><span class="path-icon">${icon("learn")}</span><div><strong>${esc(pathCourse.title)}</strong><p>${pathCourse.units.length} units &middot; ${pathLessons.length} lessons &middot; ${esc(pathCourse.level)}</p></div><div class="path-progress"><span>${pathDone} of ${pathLessons.length} complete</span><progress value="${pathDone}" max="${pathLessons.length}" aria-label="Course completion"></progress></div></a>
    <div class="cards-grid">${pathLessons.slice(pathStart, pathStart + 3).map((lesson, i) => card(lesson, pathStart + i)).join("")}</div>
    <section class="assessment-banner"><div class="assessment-symbol">?</div><div><span class="eyebrow">FIND YOUR STARTING POINT</span><h3>Already know a little? Let's find out.</h3><p>A 12-question starting check maps these six skills. No timer. No pressure.</p></div><a class="button secondary" href="#assessment">${state.diagnostic_answered.length === 12 ? "See your results" : "Check my skills"} ${icon("arrow")}</a></section>`;
}
function courseStatus(course) {
  return { available: "Available", "in-progress": "Partly available", planned: "Planned" }[course.status];
}
function courseCard(course) {
  return `<a class="catalog-card" href="#course/${course.id}"><div class="catalog-card-top"><span class="eyebrow small">${esc(state.catalog.subjects.find(s => s.id === course.subject_id).title)}</span><span class="status ${course.status}">${courseStatus(course)}</span></div><h3>${esc(course.title)}</h3><p>${esc(course.units[0].objectives[0])}</p><div class="card-meta"><span>${course.units.length} ${course.units.length === 1 ? "unit" : "units"} &middot; ${course.lesson_count} published lessons</span>${icon("arrow")}</div>${course.lesson_count ? `<p class="course-completion">${course.completed_count} / ${course.lesson_count} lessons complete</p>` : '<p class="course-completion">Outline only &middot; not yet playable</p>'}</a>`;
}
function learn(subjectId) {
  if (subjectId && !state.catalog.subjects.some(s => s.id === subjectId)) return notFound();
  const courses = state.catalog.courses.filter(c => !subjectId || c.subject_id === subjectId);
  const summary = state.catalog.summary;
  return `${heading("A PATH, NOT A PLAYLIST", "A whole world to understand.", `${summary.subject_count} subjects. ${summary.course_count} course outlines. ${summary.published_lesson_count} published lessons.`,
    '<a class="text-link" href="#curriculum">View coverage map ' + icon("arrow") + '</a>')}
    <div class="notice">${icon("learn")}<p>Playable courses contain full lessons, practice, and a course check. Planned courses show learning objectives only; no lessons or assessments are implied. <a class="text-link" href="#curriculum">Open the roadmap ${icon("arrow")}</a></p></div>
    <nav class="subject-filters" aria-label="Filter courses by subject"><a href="#learn" ${!subjectId ? 'aria-current="page"' : ""}>All subjects</a>${state.catalog.subjects.map(s => `<a href="#learn/${s.id}" ${subjectId === s.id ? 'aria-current="page"' : ""}>${esc(s.title)}</a>`).join("")}</nav>
    <div class="catalog-grid">${courses.map(courseCard).join("")}</div>`;
}
function unitBlock(course, unit) {
  return `<section class="unit-block"><div class="section-heading"><h2><a href="#unit/${unit.id}">${esc(unit.title)}</a></h2><span class="status ${unit.status}">${unit.status === "available" ? `${unit.completed_count} / ${unit.lesson_count} complete` : "Planned"}</span></div><ul class="objective-list">${unit.objectives.map(o => `<li>${esc(o)}</li>`).join("")}</ul>${unit.lesson_ids.length ? `<div class="cards-grid">${unit.lesson_ids.map((id, i) => card(state.lessons.find(l => l.id === id), i)).join("")}</div>` : '<p class="outline-note">Lessons and challenges have not been authored for this unit.</p>'}</section>`;
}
function courseView(id) {
  const course = state.catalog.courses.find(c => c.id === id);
  if (!course) return notFound();
  const subject = state.catalog.subjects.find(s => s.id === course.subject_id);
  return `<a class="text-link" href="#learn/${subject.id}">&larr; ${esc(subject.title)}</a>
    ${heading(esc(subject.title.toUpperCase()), esc(course.title), `${course.units.length} units · ${course.lesson_count} published lessons · ${courseStatus(course)}`)}
    ${course.prerequisites.length ? `<section class="notice"><div><strong>Suggested prerequisites</strong><div class="prerequisite-links">${course.prerequisites.map(cid => `<a class="text-link" href="#course/${cid}">${esc(state.catalog.courses.find(c => c.id === cid).title)} ${icon("arrow")}</a>`).join("")}</div><p>These are Learnova's proposed course prerequisites, not access restrictions. Planned prerequisites are not yet playable.</p></div></section>` : ""}
    ${course.status !== "available" ? '<div class="notice warning"><p>This course is an outline. Teaching content, interactive activities, practice, and assessments still need authoring and review.</p></div>' : ""}
    ${state.course_assessments[id] ? `<section class="course-actions"><a class="button primary" href="#lesson/${(courseLessons(course).find(l => !completed(l)) || courseLessons(course)[0]).id}">${course.completed_count ? "Continue or revisit lessons" : "Start the course"} ${icon("arrow")}</a><a class="button secondary" href="#course-check/${id}">${state.course_assessments[id].complete ? "View course check results" : state.course_assessments[id].answered.length ? "Resume course check" : "Take the course check"}</a><p>${courseLessons(course).reduce((count, l) => count + l.exercises.length, 0)} lesson challenges &middot; ${courseLessons(course).reduce((count, l) => count + (state.practice[l.id]?.questions.length || 0), 0)} separate practice questions &middot; ${state.course_assessments[id].questions.length} assessment questions. No timer.</p></section>` : ""}
    ${course.units.map(u => unitBlock(course, u)).join("")}
    ${course.related_lesson_ids.length ? `<section class="unit-block"><h2>Try related starter lessons</h2><p>These introduce some concepts; they do not replace or complete this course's own lessons.</p><div class="cards-grid">${course.related_lesson_ids.map((lid, i) => card(state.lessons.find(l => l.id === lid), i)).join("")}</div></section>` : ""}
    `;
}
function unitView(id) {
  const course = state.catalog.courses.find(c => c.units.some(u => u.id === id));
  if (!course) return notFound();
  const unit = course.units.find(u => u.id === id);
  return `<a class="text-link" href="#course/${course.id}">&larr; ${esc(course.title)}</a>${heading("COURSE UNIT", esc(unit.title), `${esc(course.title)} · ${unit.status === "available" ? "Available" : "Outline only"}`)}${unitBlock(course, unit)}`;
}
function curriculumView() {
  const summary = state.catalog.summary;
  return `${heading("COURSE ROADMAP", "Our coverage map.", "Every course in the catalog, and where it stands today.")}
    <section class="notice"><p>${summary.course_count} courses across ${summary.subject_count} subjects and ${summary.topic_count} topic groups. Courses marked Planned have objectives only and are not yet playable.</p></section>
    <div class="course-intro"><div><h2>${summary.published_lesson_count} lessons live. A much bigger roadmap.</h2><p>${summary.available_course_count} courses are playable now. ${summary.partial_reference_count} more have introductory lessons.</p></div></div>
    ${state.catalog.subjects.map(subject => `<section class="coverage-section"><h2>${esc(subject.title)}</h2><div class="coverage-table-wrap"><table class="coverage-table"><caption>${esc(subject.description)}</caption><thead><tr><th scope="col">Course</th><th scope="col">Topic group</th><th scope="col">Status</th></tr></thead><tbody>${state.catalog.courses.filter(c => c.subject_id === subject.id).map(c => `<tr><td><a href="#course/${c.id}">${esc(c.title)}</a></td><td>${esc(c.topics.join(" · "))}</td><td>${c.status === "available" ? "Playable" : c.coverage === "partial" ? "Introductory lessons only" : "Planned"}</td></tr>`).join("")}</tbody></table></div></section>`).join("")}
    <a class="button primary" href="#learn">Explore Learnova courses ${icon("arrow")}</a>`;
}
function practice() {
  const next = recommended();
  return `${heading("TURN UNDERSTANDING INTO CONFIDENCE", "A little practice goes a long way.", "Revisit the skills that need attention, at your own pace.")}
    <section class="practice-hero"><span class="practice-star">&#10038;</span><div><span class="eyebrow">RECOMMENDED FOR YOU</span><h2>${esc(next.title)}</h2><p>${masteryCount() === state.mastery.length ? "Keep your foundations fresh with a review." : "Your earliest skill without enough independent evidence. Start here to strengthen your foundation."}</p><a class="button primary" href="#review/${next.id}">Practice this skill ${icon("arrow")}</a></div>${miniArt(next.icon, next.color)}</section>
    <div class="section-heading"><h2>Choose a skill to revisit</h2><span class="muted">Authored challenges, immediate feedback</span></div>
    <div class="practice-list">${state.lessons.map((lesson, i) => `<a href="#review/${lesson.id}" class="practice-item"><span class="number-badge">${i + 1}</span><div><strong>${esc(stepName(lesson))}</strong><p>${esc(lessonPlacement(lesson.id).course.title)} &middot; ${esc(lesson.subtitle)}</p></div><span class="status ${state.mastery.find(s => s.id === lesson.skill).status}">${statusLabel(state.mastery.find(s => s.id === lesson.skill).status)}</span>${icon("arrow")}</a>`).join("")}</div>
    <div class="notice">${icon("check")}<p>The fractions, equations, linear relationships, and geometry courses have four separate review questions per skill. Starter-course review repeats its lesson questions. These are fixed authored sets, not generated questions. Repeating a question never adds new independent mastery evidence. Hints and retries are recorded.</p></div>`;
}
function statusLabel(status) {
  return { mastered: "Mastered", developing: "Developing", "not-started": "Not started" }[status];
}
function progressView() {
  return `${heading("EVIDENCE, NOT GUESSWORK", "See your understanding grow.", "Your skills, your learning history, and a clearer next step.")}
    <div class="progress-summary"><section class="mastery-overview"><div class="mastery-ring"><strong>${masteryCount()}<small>/ ${state.mastery.length}</small></strong></div><div><span class="eyebrow">YOUR FOUNDATION</span><h2>Skills with independent evidence</h2><p>A skill is mastered after at least two different, unassisted correct answers and 80% accuracy across its last ten attempts. Planned courses do not add skills or mastery evidence.</p></div></section><section class="summary-note"><span>&#10038;</span><h3>Mistakes are useful.</h3><p>A retry tells us you kept going. It counts as progress, but not as an independent demonstration of mastery.</p></section></div>
    <div class="section-heading"><h2>Your skill map</h2><span class="muted">Published courses only. Prerequisites are shown below each skill.</span></div>
    ${state.catalog.courses.filter(c => c.lesson_count).map(course => `<section class="course-skill-map"><h3><a href="#course/${course.id}">${esc(course.title)}</a></h3><div class="skill-map">${courseLessons(course).map((lesson, i) => { const skill = state.mastery.find(s => s.id === lesson.skill); return `<a class="skill-row" href="#lesson/${lesson.id}"><span class="skill-node ${skill.status}">${skill.status === "mastered" ? icon("check") : i + 1}</span><div class="skill-info"><strong>${esc(skill.name)}</strong><small>${skill.prerequisites.length ? `Builds on ${esc(skill.prerequisites.map(id => state.mastery.find(s => s.id === id).name).join(", "))}` : "Your starting foundation"}</small></div><div class="skill-evidence"><strong>${skill.independent} independent answers</strong><small>${skill.attempts ? `${skill.accuracy}% recent accuracy · ${skill.attempts} attempts` : "No answers recorded yet"}</small></div><span class="status ${skill.status}">${statusLabel(skill.status)}</span>${icon("arrow")}</a>`; }).join("")}</div></section>`).join("")}
    <div class="notice">${icon("clock")}<p>${state.activity.attempts} recorded attempts across ${state.activity.days.length} active days. Activity dates use UTC. Everything is stored in this local workspace, not synced to an account.</p></div>`;
}
function graph(slope = 2, intercept = 1) {
  const x = n => 200 + n * 25;
  const y = n => 150 - n * 25;
  const lines = Array.from({ length: 15 }, (_, i) => i - 7).map(n =>
    `<path d="M${x(n)} 0v300" class="graph-grid"/>`).join("") +
    Array.from({ length: 11 }, (_, i) => i - 5).map(n =>
      `<path d="M0 ${y(n)}h400" class="graph-grid"/>`).join("");
  return `<svg viewBox="0 0 400 300" id="math-graph" role="img" aria-label="Graph of y equals ${slope} x plus ${intercept}">
    <defs><clipPath id="plot-clip"><rect width="400" height="300"/></clipPath></defs>
    ${lines}<path d="M0 150h400M200 0v300" class="graph-axis"/>
    <g class="graph-labels"><text x="381" y="143">x</text><text x="209" y="16">y</text><text x="208" y="166">0</text><text x="247" y="166">2</text><text x="307" y="166">4</text><text x="209" y="103">2</text><text x="209" y="53">4</text></g>
    <path id="graph-line" d="M0 ${y(slope * -8 + intercept)} L400 ${y(slope * 8 + intercept)}" clip-path="url(#plot-clip)" class="graph-plot"/>
    <circle id="graph-point" cx="200" cy="${y(intercept)}" r="6" class="graph-point"/>
  </svg>`;
}
function fractionValue(numerator, denominator) {
  let a = numerator, b = denominator;
  while (b) [a, b] = [b, a % b];
  return denominator / a === 1 ? String(numerator / a) : `${numerator / a}/${denominator / a}`;
}
function fractionModel(numerator, denominator, whole) {
  const bars = (n, d, y) => [0, 1].map(w => Array.from({ length: d }, (_, i) => `<rect x="${20 + w * 200 + i * 180 / d}" y="${y}" width="${180 / d}" height="32" fill="${w * d + i < n ? "#8e7bbd" : "#f7f8f2"}" stroke="#b7adc9" stroke-width="1"/>`).join("")).join("");
  const ticks = Array.from({length: 2 * denominator + 1}, (_, i) => `<path d="M${20 + i * 380 / (2 * denominator)} 150v${i % denominator ? 6 : 12}" stroke="#75866a"/>`).join("");
  return `<svg viewBox="0 0 420 190" role="img" aria-label="${numerator}/${denominator}, equivalent to ${2 * numerator}/${2 * denominator}, shown on equal whole bars and a number line from zero to two"><text x="20" y="16">${numerator}/${denominator}</text>${bars(numerator, denominator, 24)}<text x="20" y="78">${2 * numerator}/${2 * denominator}</text>${bars(2 * numerator, 2 * denominator, 86)}<path d="M20 150h380" stroke="#75866a"/>${ticks}<circle cx="${20 + numerator / denominator * 190}" cy="150" r="6" fill="#526f36"/><text x="16" y="182">0</text><text x="206" y="182">1</text><text x="395" y="182">2</text></svg><p class="fraction-equality" aria-live="polite">${numerator}/${denominator} = ${2 * numerator}/${2 * denominator} = ${fractionValue(numerator, denominator)}</p><p class="fraction-amount">${numerator}/${denominator} of ${whole} = ${fractionValue(numerator * whole, denominator)}</p>`;
}
function fractionExplorer() {
  const { numerator, denominator, whole } = session.explorer;
  return `<div class="interactive-canvas fraction-explorer"><div class="canvas-header"><span>EXPLORE EQUAL PARTS</span><span class="canvas-badge">INTERACTIVE</span></div><p class="canvas-caption">Each bar is one whole. The second row splits every piece in two.<br>The point shows the same amount on a number line.</p><div id="fraction-model">${fractionModel(numerator, denominator, whole)}</div><div class="fraction-controls"><label>Equal parts per whole <output id="fraction-denominator-output">${denominator}</output><input id="fraction-denominator" aria-label="Equal parts per whole" type="range" min="2" max="12" value="${denominator}"></label><label>Selected parts (up to two wholes) <output id="fraction-numerator-output">${numerator}</output><input id="fraction-numerator" aria-label="Selected parts" type="range" min="0" max="${2 * denominator}" value="${numerator}"></label><label>Whole amount <output id="fraction-whole-output">${whole}</output><input id="fraction-whole" aria-label="Whole amount" type="range" min="2" max="48" value="${whole}"></label></div><p class="canvas-caption">Changing the partition can change the selected quantity. Read both counts.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function xTerm(a) {
  return a === 1 ? "x" : `${a}x`;
}
function equationModel(a, b, x) {
  const c = a * x + b;
  const left = b ? `${xTerm(a)} + ${b}` : xTerm(a);
  const steps = [`Start: ${left} = ${c}`];
  if (b) steps.push(`Subtract ${b} from both sides: ${xTerm(a)} = ${c - b}`);
  if (a !== 1) steps.push(`Divide both sides by ${a}: x = ${x}`);
  steps.push(`Check: ${a} \u00d7 ${x}${b ? ` + ${b}` : ""} = ${c}`);
  return `<svg viewBox="0 0 420 150" role="img" aria-label="A balanced scale with ${left} on the left and ${c} on the right"><path d="M210 36v84M170 124h80" fill="none" stroke="#75866a" stroke-width="3"/><path d="M50 36h320" fill="none" stroke="#75866a" stroke-width="3"/><path d="M50 36l-34 52h68zM370 36l-34 52h68z" fill="#e0eee1" stroke="#75866a" stroke-width="2"/><text x="50" y="112" text-anchor="middle">${left}</text><text x="370" y="112" text-anchor="middle">${c}</text><text x="210" y="28" text-anchor="middle">=</text></svg><ol class="equation-steps" aria-live="polite">${steps.map(step => `<li>${step}</li>`).join("")}</ol>`;
}
function equationExplorer() {
  const { a, b, x } = session.equation;
  return `<div class="interactive-canvas equation-explorer"><div class="canvas-header"><span>EXPLORE THE BALANCE</span><span class="canvas-badge">INTERACTIVE</span></div><p class="canvas-caption">Choose the pieces of an equation. The solution is built in, so each step keeps both sides equal.</p><div id="equation-model">${equationModel(a, b, x)}</div><div class="fraction-controls"><label>Multiplier of x <output id="equation-a-output">${a}</output><input id="equation-a" aria-label="Multiplier of x" type="range" min="1" max="6" value="${a}"></label><label>Number added <output id="equation-b-output">${b}</output><input id="equation-b" aria-label="Number added" type="range" min="0" max="9" value="${b}"></label><label>Solution <output id="equation-x-output">${x}</output><input id="equation-x" aria-label="Solution" type="range" min="1" max="9" value="${x}"></label></div><p class="canvas-caption">This explorer does not submit answers or award mastery.</p></div>`;
}
function lineEquation(m, b) {
  const term = m === 0 ? "" : m === 1 ? "x" : m === -1 ? "-x" : `${m}x`;
  if (!term) return `y = ${b}`;
  return `y = ${term}${b === 0 ? "" : ` ${b < 0 ? "-" : "+"} ${Math.abs(b)}`}`;
}
function lineModel(m, b) {
  const value = v => Number.isInteger(v) ? String(v) : v.toFixed(1);
  const xs = [0, 1, 2, 3, 4];
  return `<div class="graph-wrap">${graph(m, b)}</div><div class="graph-equation" aria-live="polite">${lineEquation(m, b)}</div><table class="values-table"><caption>Table of values</caption><thead><tr><th scope="row">x</th>${xs.map(x => `<td>${x}</td>`).join("")}</tr></thead><tbody><tr><th scope="row">y</th>${xs.map(x => `<td>${value(m * x + b)}</td>`).join("")}</tr></tbody></table><p class="canvas-caption">Each 1-unit step right changes y by ${value(m)}. The line crosses the y-axis at ${b}.</p>`;
}
function lineExplorer() {
  const { m, b } = session.line;
  return `<div class="interactive-canvas line-explorer"><div class="canvas-header"><span>EXPLORE THE LINE</span><span class="canvas-badge">INTERACTIVE</span></div><div id="line-model">${lineModel(m, b)}</div><div class="fraction-controls"><label>Slope <output id="line-m-output">${m}</output><input id="line-m" aria-label="Slope" type="range" min="-3" max="3" step="0.5" value="${m}"></label><label>Y-intercept <output id="line-b-output">${b}</output><input id="line-b" aria-label="Y-intercept" type="range" min="-4" max="4" step="1" value="${b}"></label></div><p class="canvas-caption">Watch the table and graph change together.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function slopeText(dy, dx) {
  if (dx === 0) return dy === 0 ? "undefined (same point)" : "undefined (vertical line)";
  if (dy === 0) return "0";
  const divisor = ((a, b) => { while (b) [a, b] = [b, a % b]; return a; })(Math.abs(dy), Math.abs(dx));
  let num = dy / divisor, den = dx / divisor;
  if (den < 0) { num = -num; den = -den; }
  return den === 1 ? String(num) : `${num}/${den}`;
}
function planeGrid() {
  const sx = v => 200 + v * 30, sy = v => 200 - v * 30;
  const lines = Array.from({ length: 13 }, (_, i) => i - 6).map(n => `<path d="M${sx(n)} 20v360M20 ${sy(n)}h360" class="graph-grid"/>`).join("");
  const labels = [-6, -4, -2, 2, 4, 6].map(n => `<text x="${sx(n)}" y="216" font-size="11" text-anchor="middle" fill="#7a8a70">${n}</text><text x="186" y="${sy(n) + 4}" font-size="11" text-anchor="end" fill="#7a8a70">${n}</text>`).join("");
  return `${lines}<path d="M20 200h360M200 20v360" class="graph-axis"/>${labels}`;
}
function planeModel({ x1, y1, x2, y2 }) {
  const sx = v => 200 + v * 30, sy = v => 200 - v * 30;
  const fmt = v => Number.isInteger(v) ? String(v) : v.toFixed(1);
  const dx = x2 - x1, dy = y2 - y1, squared = dx * dx + dy * dy, root = Math.sqrt(squared);
  const distance = squared === 0 ? "0" : Number.isInteger(root) ? String(root) : `\u221a${squared} \u2248 ${root.toFixed(2)}`;
  const guide = `<path d="M${sx(x1)} ${sy(y1)}H${sx(x2)}V${sy(y2)}" fill="none" stroke="#c9bfee" stroke-width="3" stroke-dasharray="6 5"/>`;
  return `<svg viewBox="0 0 400 400" role="img" aria-label="Coordinate plane with point A at (${x1}, ${y1}) and point B at (${x2}, ${y2})">${planeGrid()}${guide}<path d="M${sx(x1)} ${sy(y1)}L${sx(x2)} ${sy(y2)}" class="graph-plot"/><circle cx="${sx(x1)}" cy="${sy(y1)}" r="7" class="graph-point"/><circle cx="${sx(x2)}" cy="${sy(y2)}" r="7" fill="#8e7bbd"/><text x="${sx(x1) + 10}" y="${sy(y1) - 10}" font-size="16" font-weight="700" fill="#3f5a35">A</text><text x="${sx(x2) + 10}" y="${sy(y2) - 10}" font-size="16" font-weight="700" fill="#5d4a8a">B</text></svg><ul class="plane-facts" aria-live="polite"><li>A = (${x1}, ${y1}) and B = (${x2}, ${y2})</li><li>Across: ${dx}. Up or down: ${dy}. (The dashed purple path.)</li><li>Distance AB: ${distance}</li><li>Midpoint: (${fmt((x1 + x2) / 2)}, ${fmt((y1 + y2) / 2)})</li><li>Slope: ${slopeText(dy, dx)}</li></ul>`;
}
function sliderRow(prefix, name, label, value, min, max, step = 1) {
  return `<label>${label} <output id="${prefix}-${name}-output">${value}</output><input id="${prefix}-${name}" aria-label="${label}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
}
function planeExplorer() {
  const p = session.plane;
  return `<div class="interactive-canvas plane-explorer"><div class="canvas-header"><span>EXPLORE THE PLANE</span><span class="canvas-badge">INTERACTIVE</span></div><div id="plane-model">${planeModel(p)}</div><div class="fraction-controls">${sliderRow("plane", "x1", "Point A: across", p.x1, -6, 6)}${sliderRow("plane", "y1", "Point A: up or down", p.y1, -6, 6)}${sliderRow("plane", "x2", "Point B: across", p.x2, -6, 6)}${sliderRow("plane", "y2", "Point B: up or down", p.y2, -6, 6)}</div><p class="canvas-caption">Move the points and watch the distance, midpoint, and slope change.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function shapeModel(w, h) {
  const unit = 24, x0 = 60, y0 = 20;
  const cells = Array.from({ length: w * h }, (_, i) => `<rect x="${x0 + (i % w) * unit}" y="${y0 + Math.floor(i / w) * unit}" width="${unit}" height="${unit}" fill="${(i % w + Math.floor(i / w)) % 2 ? "#f8efcf" : "#f1e3a5"}" stroke="#d8c97b" stroke-width="1"/>`).join("");
  const W = w * unit, H = h * unit;
  return `<svg viewBox="0 0 400 280" role="img" aria-label="A rectangle ${w} squares wide and ${h} squares tall, with area ${w * h} and perimeter ${2 * (w + h)}">${cells}<path d="M${x0} ${y0 + H}L${x0 + W} ${y0 + H}L${x0} ${y0}Z" fill="#8e7bbd" fill-opacity=".28" stroke="#6a5599" stroke-width="2" stroke-dasharray="6 5"/><rect x="${x0}" y="${y0}" width="${W}" height="${H}" fill="none" stroke="#3f7a3a" stroke-width="4"/><text x="${x0 + W / 2}" y="${y0 + H + 22}" text-anchor="middle" font-size="14" fill="#3f5a35">${w}</text><text x="${x0 - 12}" y="${y0 + H / 2 + 5}" text-anchor="end" font-size="14" fill="#3f5a35">${h}</text></svg><ul class="plane-facts" aria-live="polite"><li>Perimeter, the green edge: ${w} + ${h} + ${w} + ${h} = ${2 * (w + h)}</li><li>Area, the squares inside: ${w} \u00d7 ${h} = ${w * h}</li><li>The purple triangle covers half: ${w * h / 2}</li></ul>`;
}
function shapeExplorer() {
  const s = session.shape;
  return `<div class="interactive-canvas shape-explorer"><div class="canvas-header"><span>COUNT THE SQUARES</span><span class="canvas-badge">INTERACTIVE</span></div><div id="shape-model">${shapeModel(s.w, s.h)}</div><div class="fraction-controls">${sliderRow("shape", "w", "Squares across", s.w, 1, 10)}${sliderRow("shape", "h", "Squares up", s.h, 1, 10)}</div><p class="canvas-caption">Make the rectangle wider or taller and watch both numbers.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function angleModel(a) {
  const ox = 110, oy = 210, len = 200, rad = a * Math.PI / 180;
  const ex = ox + len * Math.cos(rad), ey = oy - len * Math.sin(rad);
  const arc = a === 0 ? "" : `<path d="M${ox + 56} ${oy}A56 56 0 0 0 ${(ox + 56 * Math.cos(rad)).toFixed(1)} ${(oy - 56 * Math.sin(rad)).toFixed(1)}" fill="none" stroke="#c97a3d" stroke-width="5" stroke-linecap="round"/>`;
  const square = a === 90 ? `<path d="M${ox + 22} ${oy}V${oy - 22}H${ox}" fill="none" stroke="#3f7a3a" stroke-width="3"/>` : "";
  const kind = a === 0 ? "no turn" : a < 90 ? "acute: smaller than a square corner" : a === 90 ? "right angle: a square corner" : a < 180 ? "obtuse: wider than a square corner" : "straight line";
  return `<svg viewBox="0 0 400 250" role="img" aria-label="An angle of ${a} degrees between two rays"><path d="M${ox} ${oy}H${ox + len}" stroke="#75866a" stroke-width="5" stroke-linecap="round"/><path d="M${ox} ${oy}L${ex.toFixed(1)} ${ey.toFixed(1)}" stroke="#6a5599" stroke-width="5" stroke-linecap="round"/>${arc}${square}<circle cx="${ox}" cy="${oy}" r="7" fill="#3f5a35"/><text x="${ox + 70}" y="${oy - 14}" font-size="20" font-weight="700" fill="#c97a3d">${a}\u00b0</text></svg><ul class="plane-facts" aria-live="polite"><li>This angle is ${kind}.</li><li>${a <= 90 ? `Its complement is ${90 - a}\u00b0 (together they make a square corner).` : "It is bigger than a square corner, so it has no complement."}</li><li>Its supplement is ${180 - a}\u00b0 (together they make a straight line).</li></ul>`;
}
function angleExplorer() {
  return `<div class="interactive-canvas angle-explorer"><div class="canvas-header"><span>TURN THE RAY</span><span class="canvas-badge">INTERACTIVE</span></div><div id="angle-model">${angleModel(session.angle.a)}</div><div class="fraction-controls">${sliderRow("angle", "a", "Angle in degrees", session.angle.a, 0, 180, 5)}</div><p class="canvas-caption">Try 90 for a square corner and 180 for a straight line.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function polarModel(r, a) {
  const sx = v => 200 + v * 30, sy = v => 200 - v * 30;
  const rad = a * Math.PI / 180, clean = v => { const n = Math.round(v * 100) / 100; return Object.is(n, -0) ? 0 : n; };
  const x = clean(r * Math.cos(rad)), y = clean(r * Math.sin(rad));
  const R = 36, large = a > 180 ? 1 : 0;
  const arc = a === 0 || a === 360 ? "" : `<path d="M${200 + R} 200A${R} ${R} 0 ${large} 0 ${(200 + R * Math.cos(rad)).toFixed(1)} ${(200 - R * Math.sin(rad)).toFixed(1)}" fill="none" stroke="#c97a3d" stroke-width="4" stroke-linecap="round"/>`;
  const rings = [1, 2, 3, 4, 5, 6].map(n => `<circle cx="200" cy="200" r="${n * 30}" fill="none" stroke="#d6e2c9" stroke-width="1"/>`).join("");
  return `<svg viewBox="0 0 400 400" role="img" aria-label="A point ${r} units from the origin at an angle of ${a} degrees, at about (${x}, ${y})">${planeGrid()}${rings}${arc}<path d="M200 200L${sx(x)} ${sy(y)}" stroke="#6a5599" stroke-width="4" stroke-linecap="round"/><circle cx="${sx(x)}" cy="${sy(y)}" r="8" class="graph-point"/><circle cx="200" cy="200" r="5" fill="#3f5a35"/></svg><ul class="plane-facts" aria-live="polite"><li>Distance and angle: (r, \u03b8) = (${r}, ${a}\u00b0)</li><li>Right and up: (x, y) \u2248 (${x}, ${y})</li><li>Check: x\u00b2 + y\u00b2 \u2248 ${clean(x * x + y * y)}, and r\u00b2 = ${r * r}</li></ul>`;
}
function polarExplorer() {
  const p = session.polar;
  return `<div class="interactive-canvas polar-explorer"><div class="canvas-header"><span>DISTANCE AND DIRECTION</span><span class="canvas-badge">INTERACTIVE</span></div><div id="polar-model">${polarModel(p.r, p.a)}</div><div class="fraction-controls">${sliderRow("polar", "r", "Distance from the origin", p.r, 1, 6)}${sliderRow("polar", "a", "Angle in degrees", p.a, 0, 345, 15)}</div><p class="canvas-caption">Rings show each step of distance. Turn the angle to swing the point around.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function storyArt(kind) {
  const art = {
    pie: () => miniArt("fraction", "violet"),
    scales: () => miniArt("balance", "mint"),
    grid: () => miniArt("graph", "blue"),
    river: () => `<svg class="lesson-art blue" viewBox="0 0 160 110" aria-hidden="true"><path d="M8 62C38 38 62 86 92 62S138 48 152 60" fill="none" class="art-stroke"/><path d="M8 74C38 50 62 98 92 74S138 60 152 72" fill="none" class="art-stroke" opacity=".5"/><rect x="18" y="80" width="46" height="22" rx="4" class="art-light"/><rect x="92" y="10" width="50" height="26" rx="4" class="art-dark"/><path d="M92 23h50M117 10v26" class="art-grid"/></svg>`,
    circle: () => `<svg class="lesson-art yellow" viewBox="0 0 160 110" aria-hidden="true"><circle cx="80" cy="55" r="40" class="art-light"/><path d="M80 55V15A40 40 0 0 1 120 55Z" class="art-dark"/><path d="M80 15v80M40 55h80M52 27l56 56M108 27L52 83" class="art-grid"/><circle cx="80" cy="55" r="4" class="art-stroke"/></svg>`,
    rope: () => `<svg class="lesson-art peach" viewBox="0 0 160 110" aria-hidden="true"><path d="M30 92V32L110 92Z" fill="none" class="art-stroke"/><path d="M30 80h12V92" fill="none" class="art-grid"/><circle cx="30" cy="32" r="5" class="art-dark"/><circle cx="30" cy="92" r="5" class="art-dark"/><circle cx="110" cy="92" r="5" class="art-dark"/><circle cx="30" cy="62" r="3.5" class="art-light"/><circle cx="70" cy="62" r="3.5" class="art-light"/><circle cx="70" cy="92" r="3.5" class="art-light"/></svg>`,
    tally: () => `<svg class="lesson-art yellow" viewBox="0 0 160 110" aria-hidden="true"><path d="M26 24v54M42 24v54M58 24v54M74 24v54M18 66L84 36" fill="none" class="art-stroke"/><path d="M100 24v54M116 24v54M132 24v54" fill="none" class="art-stroke"/><ellipse cx="40" cy="96" rx="10" ry="6" class="art-light"/><ellipse cx="64" cy="98" rx="9" ry="5" class="art-dark"/><ellipse cx="86" cy="96" rx="10" ry="6" class="art-light"/></svg>`,
    hands: () => `<svg class="lesson-art mint" viewBox="0 0 160 110" aria-hidden="true">${[0, 1, 2, 3, 4].map(i => `<rect x="${24 + i * 12}" y="${22 - (i === 2 ? 6 : i % 4 === 0 ? 0 : 3)}" width="9" height="${i === 0 || i === 4 ? 34 : 42}" rx="4.5" class="art-dark"/>`).join("")}${[0, 1, 2, 3, 4].map(i => `<rect x="${88 + i * 12}" y="${22 - (i === 2 ? 6 : i % 4 === 0 ? 0 : 3)}" width="9" height="${i === 0 || i === 4 ? 34 : 42}" rx="4.5" class="art-dark"/>`).join("")}<rect x="22" y="62" width="62" height="34" rx="12" class="art-light"/><rect x="86" y="62" width="62" height="34" rx="12" class="art-light"/></svg>`,
    abacus: () => `<svg class="lesson-art violet" viewBox="0 0 160 110" aria-hidden="true"><rect x="22" y="14" width="116" height="82" rx="8" fill="none" class="art-stroke"/>${[0, 1, 2].map(i => `<path d="M${54 + i * 34} 14v82" class="art-stroke"/>${Array.from({ length: [4, 6, 3][i] }, (_, k) => `<circle cx="${54 + i * 34}" cy="${26 + k * 13}" r="6" class="${k % 2 ? "art-light" : "art-dark"}"/>`).join("")}`).join("")}</svg>`,
    coins: () => `<svg class="lesson-art yellow" viewBox="0 0 160 110" aria-hidden="true"><circle cx="50" cy="62" r="26" class="art-dark"/><circle cx="50" cy="62" r="18" class="art-light"/><circle cx="104" cy="52" r="22" class="art-light"/><circle cx="104" cy="52" r="14" class="art-dark"/><circle cx="116" cy="84" r="14" class="art-dark"/></svg>`,
    baskets: () => `<svg class="lesson-art peach" viewBox="0 0 160 110" aria-hidden="true">${[0, 1, 2].map(i => `<path d="M${14 + i * 48} 52h38c0 24-8 40-19 40s-19-16-19-40z" class="art-dark"/>${[0, 1, 2, 3].map(k => `<circle cx="${23 + i * 48 + (k % 2) * 20}" cy="${40 + Math.floor(k / 2) * -10 + 8}" r="6" class="art-light"/>`).join("")}`).join("")}</svg>`,
    share: () => `<svg class="lesson-art blue" viewBox="0 0 160 110" aria-hidden="true">${[0, 1, 2].map(i => `<rect x="${12 + i * 50}" y="30" width="42" height="50" rx="8" class="art-light"/>${[0, 1, 2, 3].map(k => `<circle cx="${23 + i * 50 + (k % 2) * 18}" cy="${46 + Math.floor(k / 2) * 18}" r="6" class="art-dark"/>`).join("")}`).join("")}</svg>`,
  };
  return (art[kind] || art.pie)();
}
function storyCard(lessonId) {
  const story = state.stories?.[lessonId];
  if (!story) return "";
  return `<aside class="story-card" aria-label="Math history"><div class="story-art">${storyArt(story.art)}</div><div><span class="eyebrow">WHY PEOPLE NEEDED THIS</span><h3>${esc(story.title)}</h3><p>${esc(story.text)}</p></div></aside>`;
}
function numberSystemsModel(n) {
  const h = Math.floor(n / 100), t = Math.floor(n / 10) % 10, u = n % 10;
  const additive = h + t + u, digits = String(n).length;
  const rows = [["Tally strokes", n, "#c9bfee", `${n} strokes`], ["Repeated symbols", additive, "#bed8b5", `${additive} symbols`], ["Place value", digits, "#edc3a3", `${digits} digit${digits === 1 ? "" : "s"}`]];
  const bars = rows.map(([label, value, color, text], i) => `<text x="12" y="${28 + i * 46}" font-size="13" fill="#54664b">${label}</text><rect x="12" y="${34 + i * 46}" width="${Math.max(6, 300 * value / n)}" height="16" rx="5" fill="${color}"/><text x="${Math.max(6, 300 * value / n) + 20}" y="${47 + i * 46}" font-size="13" font-weight="700" fill="#3f5a35">${text}</text>`).join("");
  return `<svg viewBox="0 0 400 150" role="img" aria-label="To write ${n}: ${n} tally strokes, ${additive} repeated symbols, or ${digits} digits using place value">${bars}</svg><ul class="plane-facts" aria-live="polite"><li>The number ${n} has ${h} hundred${h === 1 ? "" : "s"}, ${t} ten${t === 1 ? "" : "s"}, and ${u} one${u === 1 ? "" : "s"}.</li><li>Tally strokes: ${n}. In bundles of 5, that is ${Math.floor(n / 5)} bundle${Math.floor(n / 5) === 1 ? "" : "s"} and ${n % 5} left over.</li><li>Repeated symbols (${h} + ${t} + ${u}): ${additive}.</li><li>Place value: ${digits} digit${digits === 1 ? "" : "s"}, with a zero holding any empty place.</li></ul>`;
}
function numberSystemsExplorer() {
  return `<div class="interactive-canvas nsys-explorer"><div class="canvas-header"><span>THREE WAYS TO WRITE A NUMBER</span><span class="canvas-badge">INTERACTIVE</span></div><div id="nsys-model">${numberSystemsModel(session.nsys.n)}</div><div class="fraction-controls">${sliderRow("nsys", "n", "The number", session.nsys.n, 1, 999)}</div><p class="canvas-caption">Slide to a big number and see how much shorter place value is.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function doublingModel(a, b) {
  const rows = [];
  for (let p = 1; p <= a; p *= 2) rows.push(p);
  let remaining = a;
  const chosen = new Set();
  for (const p of [...rows].reverse()) if (p <= remaining) { chosen.add(p); remaining -= p; }
  const picked = rows.filter(p => chosen.has(p));
  const table = rows.map(p => `<tr class="${chosen.has(p) ? "picked" : ""}"><td>${p}</td><td>${p * b}</td><td>${chosen.has(p) ? "\u2713 add" : ""}</td></tr>`).join("");
  return `<table class="doubling-table"><caption>Doubling ${b}</caption><thead><tr><th scope="col">Rows</th><th scope="col">Amount</th><th scope="col">Use?</th></tr></thead><tbody>${table}</tbody></table><ul class="plane-facts" aria-live="polite"><li>${a} = ${picked.join(" + ")}</li><li>${picked.map(p => p * b).join(" + ")} = ${a * b}</li><li>So ${a} \u00d7 ${b} = ${a * b}</li></ul>`;
}
function doublingExplorer() {
  const d = session.dbl;
  return `<div class="interactive-canvas dbl-explorer"><div class="canvas-header"><span>MULTIPLY BY DOUBLING</span><span class="canvas-badge">INTERACTIVE</span></div><div id="dbl-model">${doublingModel(d.a, d.b)}</div><div class="fraction-controls">${sliderRow("dbl", "a", "Multiply by", d.a, 1, 20)}${sliderRow("dbl", "b", "The amount", d.b, 1, 20)}</div><p class="canvas-caption">The ticked rows are the doublings that add up to the first number.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function ledgerModel(owned, owed) {
  const net = owned - owed, x = v => 200 + v * 18;
  const ticks = Array.from({ length: 21 }, (_, i) => i - 10).map(v => `<path d="M${x(v)} 62v${v % 5 === 0 ? 14 : 8}" stroke="#75866a"/>${v % 5 === 0 ? `<text x="${x(v)}" y="98" font-size="12" text-anchor="middle" fill="#54664b">${v}</text>` : ""}`).join("");
  const color = net < 0 ? "#c97a3d" : "#3f7a3a";
  return `<svg viewBox="0 0 400 130" role="img" aria-label="You have ${owned} coins and owe ${owed} coins, so your net total is ${net}"><path d="M20 62h360" stroke="#75866a" stroke-width="3"/>${ticks}<path d="M${x(0)} 62L${x(net)} 62" stroke="${color}" stroke-width="6" stroke-linecap="round"/><circle cx="${x(net)}" cy="62" r="9" fill="${color}"/><text x="${x(net)}" y="40" font-size="16" font-weight="700" text-anchor="middle" fill="${color}">${net}</text></svg><ul class="plane-facts" aria-live="polite"><li>You have ${owned} coin${owned === 1 ? "" : "s"} and owe ${owed} coin${owed === 1 ? "" : "s"}.</li><li>Net total: ${owned} - ${owed} = ${net}${net < 0 ? ` (you are ${-net} short)` : ""}</li></ul>`;
}
function ledgerExplorer() {
  const l = session.ledger;
  return `<div class="interactive-canvas ledger-explorer"><div class="canvas-header"><span>OWING AND OWNING</span><span class="canvas-badge">INTERACTIVE</span></div><div id="ledger-model">${ledgerModel(l.owned, l.owed)}</div><div class="fraction-controls">${sliderRow("ledger", "owned", "Coins you have", l.owned, 0, 10)}${sliderRow("ledger", "owed", "Coins you owe", l.owed, 0, 10)}</div><p class="canvas-caption">Owing more than you have pushes the total below zero.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function tenFrame(x, y, count, color) {
  const cell = 28, spots = Array.from({ length: 10 }, (_, i) => {
    const cx = x + (i % 5) * cell + cell / 2, cy = y + Math.floor(i / 5) * cell + cell / 2;
    return `<rect x="${x + (i % 5) * cell}" y="${y + Math.floor(i / 5) * cell}" width="${cell}" height="${cell}" fill="#fffdf4" stroke="#b9ad84" stroke-width="2"/>${i < count ? `<circle cx="${cx}" cy="${cy}" r="10" fill="${color}"/>` : ""}`;
  });
  return spots.join("");
}
function tenFrameModel(a, b) {
  const total = a + b;
  const makeTen = a < 10 && b > 0 && total > 10;
  const move = 10 - a;
  const lines = [`${a} + ${b} = ${total}`,
    `First tray: ${a} dot${a === 1 ? "" : "s"}, ${10 - a} empty. Second tray: ${b} dot${b === 1 ? "" : "s"}, ${10 - b} empty.`];
  if (makeTen) lines.push(`Make ten: move ${move} from the second tray to fill the first. That leaves ${b - move}, so ${a} + ${b} = 10 + ${b - move} = ${total}.`);
  else if (total === 10) lines.push("The two trays together make exactly 10.");
  else lines.push(`Together the trays hold ${total}.`);
  return `<svg viewBox="0 0 400 130" role="img" aria-label="Two ten-frames: ${a} dots in the first and ${b} dots in the second, ${total} in all"><rect x="20" y="20" width="160" height="88" rx="8" fill="none"/>${tenFrame(30, 24, a, "#8e7bbd")}${tenFrame(220, 24, b, "#e0894a")}<text x="100" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#5d4a8a">${a}</text><text x="290" y="122" text-anchor="middle" font-size="14" font-weight="700" fill="#b5642a">${b}</text></svg><ul class="plane-facts" aria-live="polite">${lines.map(line => `<li>${line}</li>`).join("")}</ul>`;
}
function tenFrameExplorer() {
  const t = session.tf;
  return `<div class="interactive-canvas tf-explorer"><div class="canvas-header"><span>FILL THE TEN-FRAMES</span><span class="canvas-badge">INTERACTIVE</span></div><div id="tf-model">${tenFrameModel(t.a, t.b)}</div><div class="fraction-controls">${sliderRow("tf", "a", "Purple dots", t.a, 0, 10)}${sliderRow("tf", "b", "Orange dots", t.b, 0, 10)}</div><p class="canvas-caption">A full row is 5 and a full tray is 10. Try 8 and 5 to see make-ten.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function blocksModel(n) {
  const tens = Math.floor(n / 10), ones = n % 10;
  const rods = Array.from({ length: tens }, (_, i) => `<rect x="${16 + i * 30}" y="14" width="22" height="112" rx="4" fill="#bed8b5" stroke="#5d8361" stroke-width="2"/>${Array.from({ length: 9 }, (_, k) => `<path d="M${16 + i * 30} ${14 + (k + 1) * 11.2}h22" stroke="#5d8361" stroke-width="1"/>`).join("")}`).join("");
  const cubes = Array.from({ length: ones }, (_, j) => `<rect x="${300 + (j % 3) * 30}" y="${22 + Math.floor(j / 3) * 30}" width="24" height="24" rx="4" fill="#f4c27a" stroke="#b5642a" stroke-width="2"/>`).join("");
  return `<svg viewBox="0 0 400 140" role="img" aria-label="${n} shown as ${tens} tens rods and ${ones} ones cubes">${rods}${cubes}<text x="290" y="132" text-anchor="end" font-size="12" fill="#54664b">${tens} ten${tens === 1 ? "" : "s"}</text><text x="392" y="132" text-anchor="end" font-size="12" fill="#54664b">${ones} one${ones === 1 ? "" : "s"}</text></svg><ul class="plane-facts" aria-live="polite"><li>${n} = ${tens} ten${tens === 1 ? "" : "s"} and ${ones} one${ones === 1 ? "" : "s"}</li><li>${tens > 0 ? `The ${tens} is worth ${tens * 10}` : "There are no tens, so the tens place is empty"}, and the ${ones} is worth ${ones}.</li><li>${ones === 9 ? "One more cube makes 10 cubes. Trade them for 1 rod!" : "Ten cubes can always be traded for one rod."}</li></ul>`;
}
function blocksExplorer() {
  return `<div class="interactive-canvas blocks-explorer"><div class="canvas-header"><span>RODS AND CUBES</span><span class="canvas-badge">INTERACTIVE</span></div><div id="blocks-model">${blocksModel(session.blocks.n)}</div><div class="fraction-controls">${sliderRow("blocks", "n", "The number", session.blocks.n, 0, 99)}</div><p class="canvas-caption">Slide past 9, 19, and 29 and watch cubes turn into a rod.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function hopsModel(step, hops) {
  const end = step * hops, max = end <= 20 ? 20 : end <= 50 ? 50 : 100, ux = 360 / max, x = v => 20 + v * ux;
  const points = Array.from({ length: hops + 1 }, (_, i) => i * step);
  const arcs = points.slice(1).map((p, i) => `<path d="M${x(points[i])} 70Q${(x(points[i]) + x(p)) / 2} 14 ${x(p)} 70" fill="none" stroke="#7299c5" stroke-width="3" stroke-linecap="round"/>`).join("");
  const labelEvery = max / 10;
  const ticks = Array.from({ length: 11 }, (_, i) => i * labelEvery).map(v => `<path d="M${x(v)} 70v10" stroke="#75866a"/><text x="${x(v)}" y="96" font-size="11" text-anchor="middle" fill="#7a8a70">${v}</text>`).join("");
  const dots = points.map(p => `<circle cx="${x(p)}" cy="70" r="6" fill="${p === end ? "#e0894a" : "#7299c5"}"/>`).join("");
  return `<svg viewBox="0 0 400 110" role="img" aria-label="${hops} hops of ${step} on a number line, landing on ${end}"><path d="M20 70h360" stroke="#75866a" stroke-width="3"/>${ticks}${arcs}${dots}</svg><ul class="plane-facts" aria-live="polite"><li>Landing spots: ${points.join(", ")}</li><li>${hops} hop${hops === 1 ? "" : "s"} of ${step} lands on ${end}.</li><li>${hops} \u00d7 ${step} = ${end}</li></ul>`;
}
function hopsExplorer() {
  const h = session.hops;
  return `<div class="interactive-canvas hops-explorer"><div class="canvas-header"><span>HOP ALONG THE LINE</span><span class="canvas-badge">INTERACTIVE</span></div><div id="hops-model">${hopsModel(h.step, h.hops)}</div><div class="fraction-controls">${sliderRow("hops", "step", "Size of each hop", h.step, 1, 10)}${sliderRow("hops", "hops", "Number of hops", h.hops, 0, 10)}</div><p class="canvas-caption">Try hops of 2, 5, and 10. Notice where you land.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function regroupModel(a, b) {
  const ones = a % 10 + b % 10, carry = ones >= 10 ? 1 : 0, tens = Math.floor(a / 10) + Math.floor(b / 10) + carry, total = a + b;
  const digits = String(total).padStart(3, " ").split("");
  const col = [150, 190, 230];
  const carryMark = carry ? `<text x="190" y="38" font-size="24" font-weight="700" fill="#e0894a" text-anchor="middle">1</text>` : "";
  return `<svg viewBox="0 0 400 200" role="img" aria-label="${a} plus ${b} equals ${total}">${carryMark}<g font-size="38" font-family="Consolas, monospace" fill="#3f5a35" text-anchor="middle"><text x="190" y="82">${Math.floor(a / 10)}</text><text x="230" y="82">${a % 10}</text><text x="110" y="124" fill="#7299c5">+</text><text x="190" y="124">${Math.floor(b / 10)}</text><text x="230" y="124">${b % 10}</text>${digits.map((d, i) => d === " " ? "" : `<text x="${col[i]}" y="182" fill="#5d4a8a">${d}</text>`).join("")}</g><path d="M100 138h160" stroke="#3f5a35" stroke-width="3"/></svg><ul class="plane-facts" aria-live="polite"><li>Ones: ${a % 10} + ${b % 10} = ${ones}${carry ? `. That is 1 ten and ${ones - 10} ones, so write ${ones - 10} and carry 1 ten.` : ". No ten to carry."}</li><li>Tens: ${Math.floor(a / 10)} + ${Math.floor(b / 10)}${carry ? " + 1 (carried)" : ""} = ${tens}</li><li>${a} + ${b} = ${total}</li></ul>`;
}
function regroupExplorer() {
  const r = session.regroup;
  return `<div class="interactive-canvas regroup-explorer"><div class="canvas-header"><span>ADD AND CARRY</span><span class="canvas-badge">INTERACTIVE</span></div><div id="regroup-model">${regroupModel(r.a, r.b)}</div><div class="fraction-controls">${sliderRow("regroup", "a", "First number", r.a, 10, 99)}${sliderRow("regroup", "b", "Second number", r.b, 10, 99)}</div><p class="canvas-caption">The orange 1 shows a ten being carried. When does it appear?<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function gapModel(a, b) {
  const big = Math.max(a, b), small = Math.min(a, b), gap = big - small, u = 16;
  const bar = (v, y, color, label) => `<rect x="30" y="${y}" width="${v * u}" height="30" rx="6" fill="${color}"/><text x="${30 + v * u + 8}" y="${y + 20}" font-size="14" font-weight="700" fill="#3f5a35">${label} ${v}</text>`;
  return `<svg viewBox="0 0 400 130" role="img" aria-label="Two towers of ${a} and ${b} blocks with a gap of ${gap}">${bar(a, 16, "#bcd0ea", "A")}${bar(b, 70, "#f4c27a", "B")}${gap ? `<rect x="${30 + small * u}" y="${a >= b ? 70 : 16}" width="${gap * u}" height="30" rx="6" fill="none" stroke="#3f7a3a" stroke-width="3" stroke-dasharray="6 5"/>` : ""}</svg><ul class="plane-facts" aria-live="polite"><li>The gap: ${big} - ${small} = ${gap}</li><li>Check by adding: ${small} + ${gap} = ${big}</li><li>Fact family: ${small} + ${gap} = ${big}, ${gap} + ${small} = ${big}, ${big} - ${small} = ${gap}, ${big} - ${gap} = ${small}</li></ul>`;
}
function gapExplorer() {
  const g = session.gap;
  return `<div class="interactive-canvas gap-explorer"><div class="canvas-header"><span>FIND THE GAP</span><span class="canvas-badge">INTERACTIVE</span></div><div id="gap-model">${gapModel(g.a, g.b)}</div><div class="fraction-controls">${sliderRow("gap", "a", "Tower A", g.a, 0, 20)}${sliderRow("gap", "b", "Tower B", g.b, 0, 20)}</div><p class="canvas-caption">The dashed green part is the gap. Adding it back gives the taller tower.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function arrayModel(r, c) {
  const gap = 26, x0 = 30, y0 = 24;
  const dots = Array.from({ length: r * c }, (_, i) => `<circle cx="${x0 + (i % c) * gap}" cy="${y0 + Math.floor(i / c) * gap}" r="10" fill="${Math.floor(i / c) % 2 ? "#7eac87" : "#8e7bbd"}"/>`).join("");
  return `<svg viewBox="0 0 330 ${y0 + r * gap}" role="img" aria-label="An array of ${r} rows with ${c} dots in each row, ${r * c} dots in all">${dots}</svg><ul class="plane-facts" aria-live="polite"><li>${r} row${r === 1 ? "" : "s"} of ${c}: ${Array(r).fill(c).join(" + ")} = ${r * c}</li><li>${r} \u00d7 ${c} = ${r * c}</li><li>Turned on its side: ${c} \u00d7 ${r} = ${r * c}</li></ul>`;
}
function arrayExplorer() {
  const a = session.array;
  return `<div class="interactive-canvas array-explorer"><div class="canvas-header"><span>BUILD AN ARRAY</span><span class="canvas-badge">INTERACTIVE</span></div><div id="array-model">${arrayModel(a.r, a.c)}</div><div class="fraction-controls">${sliderRow("array", "r", "Rows", a.r, 1, 10)}${sliderRow("array", "c", "Dots in each row", a.c, 1, 10)}</div><p class="canvas-caption">Swap the two sliders. The total stays the same.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function sharingModel(total, groups) {
  const each = Math.floor(total / groups), rem = total % groups;
  const boxes = Array.from({ length: groups }, (_, g) => {
    const bx = 15 + (g % 3) * 128, by = 10 + Math.floor(g / 3) * 92;
    const dots = Array.from({ length: each }, (_, k) => `<circle cx="${bx + 14 + (k % 7) * 14}" cy="${by + 18 + Math.floor(k / 7) * 14}" r="5.5" fill="#8e7bbd"/>`).join("");
    return `<rect x="${bx}" y="${by}" width="116" height="80" rx="10" fill="#f4f1fb" stroke="#c9bfee" stroke-width="2"/>${dots}`;
  }).join("");
  const leftover = Array.from({ length: rem }, (_, k) => `<circle cx="${22 + k * 14}" cy="${groups > 3 ? 214 : 122}" r="5.5" fill="#e0894a"/>`).join("");
  return `<svg viewBox="0 0 400 ${groups > 3 ? 232 : 140}" role="img" aria-label="${total} shared among ${groups} groups gives ${each} each with ${rem} left over">${boxes}${leftover}</svg><ul class="plane-facts" aria-live="polite"><li>${total} \u00f7 ${groups} = ${each}${rem ? `, with ${rem} left over (orange)` : ", with none left over"}</li><li>Each group gets ${each}.</li><li>Check: ${each} \u00d7 ${groups}${rem ? ` + ${rem}` : ""} = ${total}</li></ul>`;
}
function sharingExplorer() {
  const s = session.share;
  return `<div class="interactive-canvas share-explorer"><div class="canvas-header"><span>SHARE EQUALLY</span><span class="canvas-badge">INTERACTIVE</span></div><div id="share-model">${sharingModel(s.total, s.groups)}</div><div class="fraction-controls">${sliderRow("share", "total", "Things to share", s.total, 1, 30)}${sliderRow("share", "groups", "Number of groups", s.groups, 1, 6)}</div><p class="canvas-caption">Orange dots are left over when the sharing cannot be exactly equal.<br>This explorer does not submit answers or award mastery.</p></div>`;
}
function visual(lesson) {
  if (lesson.visual === "tenframe-explorer") return tenFrameExplorer();
  if (lesson.visual === "blocks-explorer") return blocksExplorer();
  if (lesson.visual === "hops-explorer") return hopsExplorer();
  if (lesson.visual === "regroup-explorer") return regroupExplorer();
  if (lesson.visual === "gap-explorer") return gapExplorer();
  if (lesson.visual === "array-explorer") return arrayExplorer();
  if (lesson.visual === "sharing-explorer") return sharingExplorer();
  if (lesson.visual === "number-systems-explorer") return numberSystemsExplorer();
  if (lesson.visual === "doubling-explorer") return doublingExplorer();
  if (lesson.visual === "ledger-explorer") return ledgerExplorer();
  if (lesson.visual === "plane-explorer") return planeExplorer();
  if (lesson.visual === "shape-explorer") return shapeExplorer();
  if (lesson.visual === "angle-explorer") return angleExplorer();
  if (lesson.visual === "polar-explorer") return polarExplorer();
  if (lesson.visual === "line-explorer") return lineExplorer();
  if (lesson.visual === "equation-explorer") return equationExplorer();
  if (lesson.visual === "fraction-explorer") return fractionExplorer();
  if (lesson.visual === "graph") return `<div class="interactive-canvas"><div class="canvas-header"><span>${icon("practice")} EXPLORE THE LINE</span><span class="canvas-badge">INTERACTIVE</span></div><div class="graph-wrap">${graph()}</div><div class="graph-equation" id="graph-equation">y = 2x + 1</div><div class="canvas-controls"><label>Slope <output id="slope-output">2</output><input id="slope-control" type="range" min="-3" max="3" step="0.5" value="2" aria-label="Slope"></label><label>Starting value <output id="intercept-output">1</output><input id="intercept-control" type="range" min="-4" max="4" step="1" value="1" aria-label="Starting value"></label></div><p class="canvas-caption">Move a slider. What changes? What stays the same?<br>This exploratory canvas does not submit an answer.</p></div>`;
  if (lesson.visual === "fraction") return `<div class="concept-visual fraction-visual"><div class="fraction-blocks"><span></span><span></span><span class="empty"></span><span class="empty"></span></div><strong>2 of 4 equal parts</strong><span>Same amount. Two ways to describe it.</span><div class="formula">2/4 <span>=</span> 1/2</div></div>`;
  if (lesson.visual === "balance") return `<div class="concept-visual">${miniArt("balance", "mint")}<div class="formula">2x + 4 = 12</div><span>Subtract 4 from both sides.</span><div class="formula small-formula">2x = 8 <span>&rarr;</span> x = 4</div></div>`;
  return `<div class="concept-visual">${miniArt("expression", "peach")}<div class="formula">3x + 2</div><span>Three notebooks. One pen. One expression.</span></div>`;
}
function lessonQuestions(mode, lesson) {
  return mode === "review" && state.practice[lesson.id] ? state.practice[lesson.id].questions : lesson.exercises;
}
function getSession(mode, lesson) {
  const questions = mode === "assessment" ? state.diagnostic : lessonQuestions(mode, lesson);
  const key = `${mode}/${lesson?.id || "diagnostic"}/${lesson?.version || 1}`;
  if (session?.key !== key) {
    let index = mode === "assessment" ? state.diagnostic.findIndex(q => !state.diagnostic_answered.includes(q.id)) :
      mode === "review" ? state.practice[lesson.id] ? questions.findIndex(q => !state.practice[lesson.id].passed.includes(q.id)) : 0 :
      questions.findIndex(q => !state.passed[lesson.id].includes(q.id));
    if (index === -1) index = mode === "review" ? 0 : questions.length;
    session = { key, index, intro: mode === "lesson" && index < questions.length,
      feedback: null, hint: null, answer: "", error: null, attemptId: null,
      explorer: { numerator: 1, denominator: 4, whole: 12 }, equation: { a: 2, b: 3, x: 4 }, line: { m: 2, b: 1 }, plane: { x1: -2, y1: 1, x2: 4, y2: 5 }, shape: { w: 4, h: 3 }, angle: { a: 60 }, polar: { r: 5, a: 45 }, nsys: { n: 243 }, dbl: { a: 13, b: 12 }, ledger: { owned: 3, owed: 5 }, tf: { a: 8, b: 5 }, blocks: { n: 34 }, hops: { step: 5, hops: 4 }, regroup: { a: 27, b: 38 }, gap: { a: 15, b: 9 }, array: { r: 3, c: 4 }, share: { total: 14, groups: 3 } };
  }
  return session;
}
function tutorPanel() {
  return `<aside class="tutor-panel"><div class="tutor-title"><span class="tutor-face">&#10038;</span><div><strong>Your learning companion</strong><small>AI integration &middot; not configured</small></div></div><div class="tutor-disabled">${icon("lock")}<span>AI tutoring is currently off</span></div><p>The tutor connection is ready for a provider integration. No AI responses are generated in this version.</p><div class="authored-help"><span class="eyebrow">HELP YOU CAN USE NOW</span><h3>A nudge, not a shortcut.</h3><p>Each lesson has carefully written hints. Using one is recorded so your mastery reflects what you can do independently.</p><div class="help-tip"><span>&#10038;</span>Ask yourself: what do I know, and what am I trying to find?</div></div><div class="tutor-input"><span>Configure a provider to ask the tutor</span>${icon("arrow")}</div><small class="privacy-note">No message or learner data is sent to an AI service.</small></aside>`;
}
function exerciseView(question, mode, total) {
  const s = session;
  const correct = s.feedback?.correct;
  const isAssessment = ["assessment", "course-check"].includes(mode);
  return `<div class="exercise-card"><div class="exercise-header"><span class="eyebrow">${mode === "assessment" ? "STARTING CHECK" : mode === "course-check" ? "COURSE CHECK" : "YOUR TURN"}</span><span>${s.index + 1} / ${total}</span></div>
    <h2 id="question-heading">${esc(question.prompt)}</h2>
    <form id="answer-form"><div class="${question.kind === "choice" ? "answer-choices" : "number-answer"}">${question.kind === "choice" ?
      question.choices.map((choice, i) => `<label class="choice ${s.answer === choice ? "selected" : ""}"><input type="radio" name="answer" value="${esc(choice)}" required ${s.answer === choice ? "checked" : ""} ${s.feedback ? "disabled" : ""}><span class="choice-letter">${String.fromCharCode(65 + i)}</span><span>${esc(choice)}</span></label>`).join("") :
      `<label for="answer-input">Your answer</label><input id="answer-input" name="answer" value="${esc(s.answer)}" placeholder="Enter a number or fraction" required maxlength="100" autocomplete="off" ${s.feedback ? "disabled" : ""}><small>Use a number or fraction, for example -2, 0.5, or 1/2.</small>`}</div>
      ${s.error ? `<p class="form-error" role="alert">${esc(s.error)}</p>` : ""}
      ${s.hint ? `<div class="hint-box"><span class="eyebrow">AUTHORED LESSON HINT</span><p>${esc(s.hint)}</p></div>` : ""}
      ${s.feedback ? `<div class="answer-feedback ${correct ? "correct" : "incorrect"}" role="status"><strong>${correct ? "That's it. The idea is clicking." : "Not quite. Keep exploring."}</strong><p>${esc(s.feedback.message)}</p>${correct && s.feedback.assisted ? "<small>Saved as assisted progress, not independent mastery evidence.</small>" : ""}</div>` : ""}
      <div class="exercise-actions">${s.feedback ? (correct || isAssessment ?
        `<button class="button primary" type="button" data-action="next" ${busy ? "disabled" : ""}>${s.index + 1 === total ? "See my results" : "Next question"} ${icon("arrow")}</button>` :
        `<button class="button primary" type="button" data-action="retry">Try again ${icon("arrow")}</button>`) :
        `<button class="button primary" type="submit" ${busy ? "disabled" : ""}>${busy ? "Saving..." : "Check my answer"} ${icon("arrow")}</button>`}
        ${!isAssessment && !correct ? `<button class="button quiet" type="button" data-action="hint" ${busy || s.hint ? "disabled" : ""}>${s.hint ? "Hint opened" : "I'd like a hint"}</button>` : ""}
      </div>
    </form></div>`;
}
function finishView(mode, lesson) {
  const assessment = mode === "assessment";
  const course = assessment ? state.catalog.courses[0] : lessonPlacement(lesson.id).course;
  const nextLesson = courseLessons(course).find(l => !completed(l));
  const next = nextLesson || recommended(course);
  const starterSkills = new Set(state.diagnostic.map(q => q.skill));
  const diagnosticMastered = state.mastery.filter(s => starterSkills.has(s.id) && s.status === "mastered").length;
  const mastered = !assessment && state.mastery.find(s => s.id === lesson.skill).status === "mastered";
  return `<section class="finish-card"><div class="finish-symbol">${icon("check")}</div><span class="eyebrow">${assessment ? "YOUR STARTING POINT IS MAPPED" : "ONE MORE IDEA TO BUILD ON"}</span><h1>${assessment ? "A clearer place to begin." : mode === "review" ? "Practice set complete." : "Look what you figured out."}</h1><p>${assessment ? `${diagnosticMastered} of ${starterSkills.size} starter skills currently have enough independent evidence. This check does not assess the separate fractions course.` : `${mode === "review" ? "Your review questions are finished." : `${esc(lesson.title)} is complete.`} ${mastered ? "You have enough independent evidence for this skill." : "Keep practising: completion and independent mastery are different milestones."}`}</p>${!assessment ? `<blockquote>${esc(lesson.takeaway)}</blockquote>` : ""}<div class="finish-actions"><a class="button primary" href="#${nextLesson ? "lesson" : "review"}/${next.id}">${nextLesson ? "Continue this course" : "Practise this course"} ${icon("arrow")}</a><a class="button secondary" href="#course/${course.id}">Back to course</a></div>${state.course_assessments[course.id] ? `<a class="text-link" href="#course-check/${course.id}">Check your course understanding ${icon("arrow")}</a>` : '<a class="text-link" href="#progress">View skill map</a>'}</section>`;
}
function lessonView(mode, id) {
  const lesson = state.lessons.find(l => l.id === id);
  if (!lesson) return notFound();
  const placement = lessonPlacement(id);
  getSession(mode, lesson);
  const questions = lessonQuestions(mode, lesson);
  const passed = mode === "review" && state.practice[id] ? state.practice[id].passed : state.passed[id];
  if (session.index >= questions.length) return finishView(mode, lesson);
  const question = questions[session.index];
  return `<div class="lesson-navigation"><a href="#course/${placement.course.id}" class="text-link">&larr; Course</a><a href="#unit/${placement.unit.id}" class="text-link">${esc(placement.unit.title)}</a><span>${lesson.duration} min</span><span class="pill outline">${mode === "review" ? "REVIEW" : "GUIDED LESSON"}</span></div>
    <div class="lesson-title"><span class="eyebrow">${esc(placement.course.title.toUpperCase())}</span><h1>${esc(lesson.title)}</h1><p>${esc(lesson.subtitle)}</p></div>
    <div class="lesson-layout"><section><div class="lesson-stepper">${mode === "lesson" ? `<span class="${session.intro ? "current" : "done"}">Explore</span>` : ""}${questions.map((q, i) => `<span class="${!session.intro && session.index === i ? "current" : passed.includes(q.id) ? "done" : ""}">Challenge ${i + 1}</span>`).join("")}</div>
    ${session.intro ? `${storyCard(lesson.id)}<div class="explanation-card"><span class="eyebrow">FIRST, THE IDEA</span><h2>${esc(lesson.formula)}</h2><p>${esc(lesson.intro)}</p>${visual(lesson)}<div class="takeaway"><span>&#10038;</span><p>${esc(lesson.takeaway)}</p></div><button class="button primary" data-action="begin">Let's try it ${icon("arrow")}</button></div>` :
      `${exerciseView(question, mode, questions.length)}${["graph", "fraction-explorer", "equation-explorer", "line-explorer", "plane-explorer", "shape-explorer", "angle-explorer", "polar-explorer", "number-systems-explorer", "doubling-explorer", "ledger-explorer", "tenframe-explorer", "blocks-explorer", "hops-explorer", "regroup-explorer", "gap-explorer", "array-explorer", "sharing-explorer"].includes(lesson.visual) ? `<details class="canvas-details"><summary>Open the ${({ graph: "graph", "fraction-explorer": "fraction", "equation-explorer": "equation", "line-explorer": "line", "plane-explorer": "plane", "shape-explorer": "shape", "angle-explorer": "angle", "polar-explorer": "polar", "number-systems-explorer": "number", "doubling-explorer": "doubling", "ledger-explorer": "owing and owning", "tenframe-explorer": "ten-frame", "blocks-explorer": "blocks", "hops-explorer": "number line", "regroup-explorer": "carrying", "gap-explorer": "gap", "array-explorer": "array", "sharing-explorer": "sharing" })[lesson.visual]} explorer</summary>${visual(lesson)}</details>` : ""}`}
    </section>${tutorPanel()}</div>`;
}
function assessment() {
  getSession("assessment");
  if (session.index >= state.diagnostic.length) return finishView("assessment");
  const q = state.diagnostic[session.index];
  return `${heading("FIND YOUR STARTING POINT", "Let's see what already clicks.", "12 questions, two per skill. This first version uses a fixed starting check, not an adaptive diagnostic.")}
    <div class="assessment-layout"><div><progress class="assessment-progress" value="${session.index}" max="12" aria-label="Assessment progress"></progress>${exerciseView(q, "assessment", 12)}</div><aside class="assessment-guide"><span>&#10038;</span><h3>No pressure.<br>Just a starting point.</h3><p>Try each question on your own. We use your answers to recommend the earliest skill that needs attention.</p><p>No hints here, and no timer. Your submitted answers are saved automatically.</p><a class="text-link" href="#home">Pause and return home &rarr;</a></aside></div>`;
}
function courseCheck(id) {
  const check = state.course_assessments[id];
  const course = state.catalog.courses.find(c => c.id === id);
  if (!check || !course) return notFound();
  const skills = [...new Set(courseLessons(course).map(l => l.skill))].map(sid => state.mastery.find(s => s.id === sid));
  const key = `course-check/${id}/${check.questions.map(q => q.version).join("-")}`;
  if (session?.key !== key) {
    let index = check.questions.findIndex(q => !check.answered.includes(q.id));
    if (index === -1) index = check.questions.length;
    session = {key, index, feedback: null, hint: null, answer: "", error: null, attemptId: null};
  }
  if (session.index >= check.questions.length) {
    const next = recommended(course);
    return `<section class="finish-card"><span class="eyebrow">${esc(course.title.toUpperCase())} &middot; COURSE CHECK</span><h1>Your course check results.</h1><p>${check.correct_count} / ${check.questions.length} correct (${Math.round(check.correct_count / check.questions.length * 100)}%). ${skills.filter(s => s.status === "mastered").length} / ${skills.length} course skills have enough independent evidence across lessons, practice, and this check.</p><p>This fixed check saves one answer per question and lesson version. It does not mark lessons complete or offer retakes of the same questions.</p><ul class="check-skill-results">${skills.map(s => `<li>${esc(s.name)} <span class="status ${s.status}">${statusLabel(s.status)}</span></li>`).join("")}</ul><div class="finish-actions"><a class="button primary" href="#review/${next.id}">Practise a course skill ${icon("arrow")}</a><a class="button secondary" href="#course/${id}">Back to course</a></div></section>`;
  }
  return `${heading("CHECK YOUR UNDERSTANDING", `${esc(course.title)}: course check`, `${check.questions.length} questions across ${skills.length} skills. No hints, retries, timer, or AI.`)}<div class="assessment-layout"><section><progress class="assessment-progress" value="${check.answered.length}" max="${check.questions.length}" aria-label="Course check progress"></progress>${exerciseView(check.questions[session.index], "course-check", check.questions.length)}</section><aside class="assessment-guide"><h3>A check, not a race.</h3><p>Each valid answer is saved once, including mistakes. Invalid input is not recorded. Return later to resume at the first unanswered question.</p><p>Scores and lesson completion are separate. Your existing mastery rule still requires distinct independent answers and 80% recent accuracy.</p><a class="text-link" href="#course/${id}">Pause and return to course</a></aside></div>`;
}
function studioView() {
  return `${heading("BEHIND EVERY AHA, A WELL-CRAFTED LESSON", "Your content workshop.", "Preview and publish edits to the curriculum. Local access only.")}
    <div class="notice warning">${icon("studio")}<p>Publishing creates a new lesson version. Old attempts remain in history but no longer count toward the revised lesson or its mastery evidence. The lesson IDs, skill graph, visual type, and exercise IDs are fixed in this editor.</p></div>
    <div class="studio-layout"><aside class="studio-list">${state.lessons.map(l => `<button class="studio-item ${studio?.lesson.id === l.id ? "selected" : ""}" data-action="edit-lesson" data-id="${l.id}"><strong>${esc(l.title)}</strong><small>${esc(lessonPlacement(l.id).unit.title)} &middot; Version ${l.version} &middot; ${l.exercises.length} challenges</small>${icon("arrow")}</button>`).join("")}</aside><section class="studio-editor">${studio ? `<div class="editor-header"><div><span class="eyebrow">PUBLISHED VERSION ${studio.version}</span><h2>${esc(studio.lesson.title)}</h2></div><span class="pill outline">JSON EDITOR</span></div><p>Edit teaching text, prompts, answers, explanations, hints, and choice options. Unsupported metadata changes are rejected.</p><form id="studio-form"><label for="lesson-json">Lesson content</label><textarea id="lesson-json" name="content" spellcheck="false" rows="24" required>${esc(JSON.stringify(studio.lesson, null, 2))}</textarea><p class="form-error" id="studio-error" role="alert"></p><div class="editor-actions"><button class="button primary" type="submit">Validate &amp; publish ${icon("check")}</button><a href="#lesson/${studio.lesson.id}" class="button secondary">Preview published lesson</a></div></form>` : `<div class="empty-editor">${icon("studio")}<h2>Choose a lesson to shape.</h2><p>Select a lesson on the left to open its content.</p></div>`}</section></div>`;
}
function notFound() {
  return `<div class="finish-card"><h1>This path isn't here.</h1><p>The requested page or lesson does not exist.</p><a class="button primary" href="#home">Return home ${icon("arrow")}</a></div>`;
}
function render() {
  if (!state) return;
  const [rawPage, id] = location.hash.slice(1).split("/");
  const page = rawPage || "home";
  updateShell(["lesson", "review", "assessment", "course-check", "course", "unit", "curriculum"].includes(page) ? "learn" : page);
  const views = { home, learn, practice, progress: progressView, studio: studioView, assessment,
    course: courseView, unit: unitView, curriculum: curriculumView, "course-check": courseCheck };
  const html = page === "lesson" || page === "review" ? lessonView(page, id) : views[page] ? views[page](id) : notFound();
  $("#main").innerHTML = html;
  document.title = `${page === "lesson" || page === "review" ? state.lessons.find(l => l.id === id)?.title || "Lesson" : ({ home: "Overview", learn: "Explore", practice: "Practice", progress: "Progress", studio: "Content studio", assessment: "Starting check", "course-check": "Course check", course: state.catalog.courses.find(c => c.id === id)?.title, unit: "Course unit", curriculum: "Coverage map" }[page] || "Not found")} - Learnova`;
}
async function refresh() {
  state = await api("/api/state");
}
function currentContext() {
  const [mode, id] = location.hash.slice(1).split("/");
  if (mode === "assessment") return { source: "diagnostic", version: 1, question_id: state.diagnostic[session.index].id };
  if (mode === "course-check") {
    const q = state.course_assessments[id].questions[session.index];
    return { source: "course-assessment", course_id: id, lesson_id: q.lesson_id,
      version: q.version, question_id: q.id };
  }
  const lesson = state.lessons.find(l => l.id === id);
  return { source: mode === "review" && state.practice[id] ? "practice" : "lesson",
    lesson_id: lesson.id, version: lesson.version, question_id: lessonQuestions(mode, lesson)[session.index].id };
}
function showProfile() {
  const form = $("#profile-form");
  form.elements.name.value = state.profile?.name || "";
  form.elements.goal.value = state.profile?.goal || "Build foundations";
  form.elements.minutes.value = state.profile?.minutes || 10;
  $("#profile-error").textContent = "";
  $("#profile-dialog").showModal();
}

document.addEventListener("click", async event => {
  const button = event.target.closest("[data-action]");
  if (!button || busy) return;
  const action = button.dataset.action;
  if (action === "profile") { showProfile(); return; }
  if (action === "begin") { session.intro = false; render(); $("#question-heading")?.scrollIntoView({ block: "center" }); return; }
  if (action === "retry") { session.feedback = null; session.answer = ""; session.attemptId = null; render(); return; }
  if (action === "next") {
    session.index++;
    session.feedback = null; session.hint = null; session.error = null; session.answer = ""; session.attemptId = null;
    render(); $("#main").focus(); return;
  }
  if (action === "hint") {
    const target = session;
    const context = currentContext();
    busy = true;
    try { target.hint = (await api("/api/hint", context)).hint; }
    catch (error) { target.error = error.message; }
    finally { busy = false; render(); }
  }
  if (action === "edit-lesson") {
    busy = true;
    button.disabled = true;
    try { studio = await api(`/api/author/${encodeURIComponent(button.dataset.id)}`); render(); }
    catch (error) { toast(error.message); }
    finally { busy = false; button.disabled = false; }
  }
});
document.addEventListener("submit", async event => {
  if (event.target.id === "answer-form") {
    event.preventDefault();
    if (busy || session.feedback) return;
    session.answer = String(new FormData(event.target).get("answer") || "").trim();
    if (!session.answer) { session.error = "Enter or select an answer first."; render(); return; }
    session.error = null;
    session.attemptId ||= crypto.randomUUID();
    const target = session;
    const context = currentContext();
    busy = true; render();
    try {
      target.feedback = await api("/api/attempt", { ...context, answer: target.answer, attempt_id: target.attemptId });
      await refresh();
    } catch (error) {
      target.error = error.message;
      // A completed request can safely be retried using the same idempotency key.
    } finally { busy = false; render(); }
  } else if (event.target.id === "profile-form") {
    event.preventDefault();
    const form = event.target;
    const submit = $('button[type="submit"]', form);
    submit.disabled = true;
    try {
      await api("/api/profile", { name: form.elements.name.value, goal: form.elements.goal.value,
        minutes: Number(form.elements.minutes.value) });
      await refresh(); $("#profile-dialog").close(); render(); toast("Your learning profile is saved.");
    } catch (error) { $("#profile-error").textContent = error.message; }
    finally { submit.disabled = false; }
  } else if (event.target.id === "studio-form") {
    event.preventDefault();
    const button = $('button[type="submit"]', event.target);
    button.disabled = true;
    try {
      let lesson;
      try { lesson = JSON.parse($("#lesson-json").value); }
      catch (error) { throw new Error(`Invalid lesson JSON: ${error.message}`); }
      const result = await api("/api/author", { lesson_id: studio.lesson.id, version: studio.version, lesson });
      studio = await api(`/api/author/${studio.lesson.id}`);
      await refresh(); render(); toast(result.message);
    } catch (error) { $("#studio-error").textContent = error.message; }
    finally { button.disabled = false; }
  }
});
document.addEventListener("input", event => {
  if (event.target.name === "answer" && session) {
    const value = event.target.value;
    if (session.answer !== value) session.attemptId = null;
    session.answer = value;
    if (event.target.type === "radio") {
      document.querySelectorAll(".choice").forEach(el => el.classList.toggle("selected", $("input", el).checked));
    }
  }
  if (["fraction-numerator", "fraction-denominator", "fraction-whole"].includes(event.target.id)) {
    const field = event.target.id.replace("fraction-", "");
    session.explorer[field] = Number(event.target.value);
    const model = session.explorer;
    model.numerator = Math.min(model.numerator, 2 * model.denominator);
    $("#fraction-numerator").max = String(2 * model.denominator);
    $("#fraction-numerator").value = String(model.numerator);
    for (const name of ["numerator", "denominator", "whole"]) $(`#fraction-${name}-output`).textContent = model[name];
    $("#fraction-model").innerHTML = fractionModel(model.numerator, model.denominator, model.whole);
    return;
  }
  const explorerIds = { "plane-": ["x1", "y1", "x2", "y2"], "shape-": ["w", "h"], "angle-": ["a"], "polar-": ["r", "a"], "nsys-": ["n"], "dbl-": ["a", "b"], "ledger-": ["owned", "owed"], "tf-": ["a", "b"], "blocks-": ["n"], "hops-": ["step", "hops"], "regroup-": ["a", "b"], "gap-": ["a", "b"], "array-": ["r", "c"], "share-": ["total", "groups"] };
  for (const [prefix, names] of Object.entries(explorerIds)) {
    if (!event.target.id.startsWith(prefix) || !names.includes(event.target.id.slice(prefix.length))) continue;
    const key = prefix.slice(0, -1), model = session[key];
    model[event.target.id.slice(prefix.length)] = Number(event.target.value);
    for (const name of names) $(`#${key}-${name}-output`).textContent = model[name];
    const render = { plane: () => planeModel(model), shape: () => shapeModel(model.w, model.h), angle: () => angleModel(model.a), polar: () => polarModel(model.r, model.a), nsys: () => numberSystemsModel(model.n), dbl: () => doublingModel(model.a, model.b), ledger: () => ledgerModel(model.owned, model.owed), tf: () => tenFrameModel(model.a, model.b), blocks: () => blocksModel(model.n), hops: () => hopsModel(model.step, model.hops), regroup: () => regroupModel(model.a, model.b), gap: () => gapModel(model.a, model.b), array: () => arrayModel(model.r, model.c), share: () => sharingModel(model.total, model.groups) };
    $(`#${key}-model`).innerHTML = render[key]();
    return;
  }
  if (["line-m", "line-b"].includes(event.target.id)) {
    session.line[event.target.id.replace("line-", "")] = Number(event.target.value);
    $("#line-m-output").textContent = session.line.m;
    $("#line-b-output").textContent = session.line.b;
    $("#line-model").innerHTML = lineModel(session.line.m, session.line.b);
    return;
  }
  if (["equation-a", "equation-b", "equation-x"].includes(event.target.id)) {
    session.equation[event.target.id.replace("equation-", "")] = Number(event.target.value);
    for (const name of ["a", "b", "x"]) $(`#equation-${name}-output`).textContent = session.equation[name];
    $("#equation-model").innerHTML = equationModel(session.equation.a, session.equation.b, session.equation.x);
    return;
  }
  if (!["slope-control", "intercept-control"].includes(event.target.id)) return;
  const slope = Number($("#slope-control").value);
  const intercept = Number($("#intercept-control").value);
  $("#slope-output").textContent = slope;
  $("#intercept-output").textContent = intercept;
  $("#graph-equation").textContent = `y = ${slope}x ${intercept < 0 ? "-" : "+"} ${Math.abs(intercept)}`;
  $("#graph-line").setAttribute("d", `M0 ${150 - (slope * -8 + intercept) * 25} L400 ${150 - (slope * 8 + intercept) * 25}`);
  $("#graph-point").setAttribute("cy", String(150 - intercept * 25));
  $("#math-graph").setAttribute("aria-label", `Graph of y equals ${slope} x plus ${intercept}`);
});
$("#profile-button").addEventListener("click", () => { if (state) showProfile(); });
$("#goal-chip").addEventListener("click", () => { if (state) showProfile(); });
$("#close-profile").addEventListener("click", () => $("#profile-dialog").close());
async function navigate() {
  const sequence = ++routeSequence;
  try {
    await refresh();
    if (sequence !== routeSequence) return;
    session = null;
    render();
    window.scrollTo({ top: 0, behavior: "instant" });
    $("#main").focus({ preventScroll: true });
  } catch (error) {
    $("#main").innerHTML = `<div class="finish-card"><h1>We couldn't open your workspace.</h1><p role="alert">${esc(error.message)}</p><p>Check that the Learnova server is running, then reload this page.</p><button class="button primary" data-action="reload">Try again</button></div>`;
  }
}
document.addEventListener("click", event => {
  if (event.target.closest('[data-action="reload"]')) navigate();
});
window.addEventListener("hashchange", navigate);
navigate();
