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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
+========================================+
|  Daily Plan for Luna (Siamese)         |
|  Owner: Victor  |  Date: 2026-07-06    |
+========================================+

  #    TIME    TASK                   DURATION   PRIORITY
  --------------------------------------
  1    08:00  Feeding                10min      HIGH
  2    08:10  Grooming               20min      MEDIUM
  3    08:30  Enrichment Play        15min      LOW
  --------------------------------------
  Total:                            45min used  |  15min remaining
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

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority sorting | `Planner.sort_tasks()` | Orders tasks high → medium → low before filtering or slotting. |
| Time-based sorting | `Planner.sort_by_time()` | Sorts tasks by their `start_time` ("HH:MM") string. |
| Status / pet filtering | `Planner.filter_by(status, pet_name)` | Returns tasks matching a given `status` ("pending"/"complete") and/or pet name. |
| Budget filtering | `Planner.filter_tasks()` | Greedily keeps priority-sorted tasks that still fit within `available_minutes_per_day`; drops the rest. |
| Time-slot assignment | `Planner.assign_time_slots()` | Assigns sequential start times to filtered tasks based on cumulative duration. |
| Full plan generation | `Planner.generate_plan()` | Runs the sort → filter → assign-slots pipeline end to end. |
| Plan explanation | `Planner.explain_plan()` | Produces a human-readable summary of what was scheduled and what was dropped, and why. |
| Conflict handling | `Planner._time_range()`, `Planner.find_conflicts()`, `Planner.explain_conflicts()`, `Schedule.check_conflict()` | Detects overlapping `[start, start+duration)` ranges for tasks within one pet's schedule and across other pets' schedules; `Schedule.add_task()` also runs a lightweight same-schedule check and returns a warning string (rather than raising) when a new task overlaps an existing one. |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()`, `Schedule.complete_task()` | Completing a "daily" or "weekly" task automatically generates the next pending occurrence using `datetime.timedelta` (1 day or 1 week out) and adds it back onto the schedule. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
