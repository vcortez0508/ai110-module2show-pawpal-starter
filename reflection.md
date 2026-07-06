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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
