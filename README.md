# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
================================================
             TODAY'S SCHEDULE
================================================
  00:00  Morning Walk          30 min  [high  ]  Buddy
  00:30  Feeding               15 min  [high  ]  Whiskers
  00:45  Grooming              45 min  [medium]  Buddy
================================================
  3 task(s) scheduled  |  90 / 120 min used
================================================
```
## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

### Sorting — `Scheduler.sort_by_time()`

Returns the current schedule sorted by `scheduled_time` in ascending order. Internally converts each time string to an integer minute offset via the shared `_to_minutes()` helper rather than sorting lexicographically — string comparison breaks for hour values beyond two digits. Tasks without a `scheduled_time` (unscheduled) sort to the end via a `float("inf")` sentinel.

### Filtering — `Scheduler.create_schedule()`

Filters and packs tasks using two passes:

1. **Completion filter** — any task with `is_complete=True` is excluded before scheduling begins.
2. **Budget filter** — tasks are sorted by `(priority, due_date)` and added greedily; a task is included only if `minutes_used + task.duration <= available_minutes`. Tasks that don't fit are skipped but remaining smaller tasks are still considered.

`Scheduler.detect_conflicts()` applies a third filter internally: only tasks that have a `scheduled_time` set are checked for overlaps — unscheduled tasks are excluded from conflict analysis.

### Conflict Detection — `Scheduler.detect_conflicts()`

Detects overlapping time intervals and returns a warning string for each conflict. Uses an **O(n log n) sort + O(n) adjacent-pair sweep** rather than an O(n²) all-pairs comparison:

1. Sort tasks by start time using `_to_minutes()`.
2. Walk adjacent pairs: if `start[i] + duration[i] > start[i+1]`, the two tasks overlap.

This is correct because if task A overlaps task C (non-adjacent after sorting), task B — which starts between A and C — must also overlap A, so no pair is ever missed by checking only neighbors.

### Recurring Tasks — `Pet.complete_task()`

When a task with `frequency="daily"` or `frequency="weekly"` is marked complete, `complete_task()` automatically queues a new copy of that task with:

- A fresh id drawn from `Pet._next_id` (an O(1) counter seeded at construction, incremented on each use — avoids an O(n) `max()` scan per completion).
- A `due_date` set to `today + 1 day` (daily) or `today + 7 days` (weekly).

One-time tasks (`frequency="once"`) are marked complete and not re-queued.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
