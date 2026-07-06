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

## ✨ Features

- **Priority sorting** — orders tasks high → medium → low before filtering or slotting.
- **Time-based sorting** — orders tasks chronologically by their `start_time`.
- **Status / pet filtering** — pulls tasks matching a given status (pending/complete) and/or pet name.
- **Budget-aware filtering** — greedily keeps as many priority-sorted tasks as fit inside the day's available minutes, dropping the rest.
- **Automatic time-slot assignment** — assigns sequential start times to the filtered tasks based on cumulative duration.
- **Plan explanation** — generates a human-readable summary of what was scheduled, what was dropped, and why.
- **Conflict warnings** — detects overlapping task times (within one pet's schedule and across other pets' schedules) and surfaces a clear warning instead of silently double-booking.
- **Daily & weekly recurrence** — completing a recurring task automatically generates its next pending occurrence one day or one week out.

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

## 🎬 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) is organized into three sections:

- **Owner & Pet Setup** — enter the owner's name, daily time budget, and the pet's name/species/breed/age, then save to start a schedule.
- **Add a Task** — add tasks with a name, category, duration, priority, recurrence (daily/weekly/none), and optional start time. Newly added tasks appear in a live table sorted by time, with any scheduling conflicts flagged immediately.
- **Generate Schedule** — runs the full planning pipeline (sort by priority → filter by budget → assign time slots) and displays the resulting plan along with a plain-language explanation of what was scheduled, what was dropped, and any remaining conflicts.

### Example workflow

1. Enter owner and pet info (e.g., "Victor" and "Biscuit, Golden Retriever") and click **Save Owner & Pet**.
2. Add a task like "Morning Walk" (30min, high priority, start time 07:15).
3. Add a second task that overlaps an existing one — the app immediately shows a conflict warning.
4. Add a few more tasks with varying priorities and durations.
5. Click **Generate Schedule** to see the final time-slotted plan and its explanation.

### Key Scheduler behaviors shown

- **Sorting** — tasks are shown by start time in the task table, and by priority when the plan is generated.
- **Conflict warnings** — overlapping tasks (e.g., two tasks both starting at 08:00) trigger a warning naming both tasks and their times, both at the moment of conflict and in a persistent summary panel.
- **Budget filtering** — tasks that don't fit in the remaining daily budget are dropped from the generated plan and listed explicitly in the explanation.
- **Recurrence** — completing a daily or weekly task (via `Schedule.complete_task()`) automatically queues its next occurrence.

### Sample CLI output (`python main.py`)

`main.py` builds two pets' schedules from hardcoded sample tasks (added out of order on purpose) and prints the resulting plans, including a deliberate scheduling conflict:

```
Warning: 'Vet Call' (08:00) overlaps 'Feeding' (08:00) for Biscuit.

+===============================================+
|  Daily Plan for Biscuit (Golden Retriever)    |
|  Owner: Victor  |  Date: 2026-07-06           |
+===============================================+

  #    TIME    TASK                   DURATION   PRIORITY
  ---------------------------------------------
  1    08:00  Flea Medicine          5min       MEDIUM
  2    08:05  Feeding                10min      HIGH
  3    08:15  Morning Walk           30min      HIGH
  4    08:45  Vet Call               10min      MEDIUM
  ---------------------------------------------
  Total:                            55min used  |  65min remaining


+========================================+
|  Daily Plan for Luna (Siamese)         |
|  Owner: Victor  |  Date: 2026-07-06    |
+========================================+

  #    TIME    TASK                   DURATION   PRIORITY
  --------------------------------------
  1    08:00  Enrichment Play        15min      LOW
  2    08:15  Feeding                10min      HIGH
  3    08:25  Grooming               20min      MEDIUM
  --------------------------------------
  Total:                            45min used  |  15min remaining

========================================
  Biscuit: sorting & filtering demo
========================================

  Tasks sorted by start_time:
    07:15  Morning Walk           [high] status=complete
    08:00  Feeding                [high] status=complete
    08:00  Vet Call               [medium] status=pending
    12:30  Flea Medicine          [medium] status=pending

  Tasks filtered by status='pending':
    12:30  Flea Medicine          [medium] status=pending
    08:00  Vet Call               [medium] status=pending

  Tasks filtered by status='complete':
    08:00  Feeding                [high] status=complete
    07:15  Morning Walk           [high] status=complete
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
