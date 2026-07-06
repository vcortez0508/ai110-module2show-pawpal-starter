# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    My original UML design was not very straightforward. I included a few unnecessary classes that could be merged into other classes.
- What classes did you include, and what responsibilities did you assign to each?
    During the first UML design I had:
    * Owner - Holds descriptive data about the customer (Pet owner).
    * Pet - Holds descriptive data about the pet (who is the care for?).
    * Task - Holds everything about a single care activity — what it is, how long it takes, how important it is, and how often it recurs.
    * Schedule - Hold all the inputs the planner needs and acts as the data container for a planning session — the owner's constraints, the pet, the task list, and the date
    * Planner - It reads the Schedule, sorts tasks by priority, filters out tasks that won't fit in the time budget, assigns start times, and explains its reasoning.


**b. Design changes**

- Did your design change during implementation?

    Yes.

- If yes, describe at least one change and why you made it.

    **Change 1 — Removed the `Owner` class**

    The original design had a standalone Owner class. During review I realized  Owner had no methods and was only ever accessed through Schedule. Keeping it as a separate class added an unnecessary layer of indirection, so its attributes were folded directly into Schedule. This simplified the design from 5 classes to 4 without losing any information.

    **Change 2 — Typed `tasks` as `list[Task]`**

    The initial skeleton defined `tasks` as a plain untyped `list`. During review this was identified as a potential bottleneck. Nothing would prevent invalid data from being added to the task list silently. Changing it to `list[Task]` makes the contract explicit and catches type mismatches early.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    Priority, Time budget, overlap and how recurrent a task is
- How did you decide which constraints mattered most?
    I prioritized constraints in the order they'd actually cause harm if ignored: priority first, because a missed high-priority task (like medicine) has real consequences while a skipped low-priority one (like extra playtime) doesn't. Time budget second, since it's the hard limiting resource — there's no point planning tasks that can't physically fit in the day. Overlap/conflict checking came third as a safety net once the core plan existed, to catch cases where two tasks land at the same time. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    One of the tradeoffs scheduler makes is within our "find_conflicts" algo. It currently has a good balance of performance and readability but could definitely be optimized for much better performance. With help of the chat agent, it was decided to keep as-is rather than optimizing for performance.
- Why is that tradeoff reasonable for this scenario?
    Because of the scale of the application. It will most likely only handle a handful of daily tasks and isn't worth the added complexity. Readability was prioritized over an uneccesa
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

I built a 15-test suite (`tests/test_pawpal.py`) covering three main areas plus edge cases. **Sorting correctness**: verified `sort_by_time()` returns tasks in chronological order, and that untimed tasks are placed consistently. **Recurring logic**: confirmed that marking a daily task complete generates a new pending task due the next day, weekly tasks advance by 7 days, non-recurring tasks return `None`, and that completed recurring tasks are correctly re-added to the schedule. **Conflict detection**: verified that overlapping and identical start times are flagged with a warning, that back-to-back tasks (no actual overlap) are correctly *not* flagged, and that untimed tasks never trigger false conflicts. I also tested edge cases like an empty schedule (no tasks, full budget) and a task whose duration exactly fills the remaining time budget. These were important because sorting, recurrence, and conflict detection are the core logic the whole scheduler depends on — a silent bug in any of them would produce a plan that looks correct but is subtly wrong (e.g., double-booked pets or recurring tasks silently disappearing).

**b. Confidence**

I'm fairly confident in the core logic since all 15 tests pass and cover both normal and boundary behavior. I'd still want to test a couple of trickier edge cases with more time: tasks with malformed or non-zero-padded `start_time` strings (e.g. `"9:00"` vs `"09:00"`), and how `remove_task`/`filter_tasks` behave when two distinct tasks have identical field values (since `Task` uses value equality, this could cause the wrong task to be removed or filtered).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
