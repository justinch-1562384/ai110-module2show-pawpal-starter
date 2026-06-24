# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

### Three Core Actions
- Let a user enter owner and pet information (linked)
- Let a user add or edit tasks (including walks) withe fields such as duration and priority.
- Based on the above, generate a schedule.

Attributes: 
Pet info
Owner info
Tasks (Duration, Prority)
Schedule (Composed of task objects)

Methods:

Add pet info
Add owner info (1-to-Many for pets)
Add task (Many-to-Many, pets/owners)
Create schedule 
Edit Tasks
Edit Pets/Users

Build the following four classes: Owner, Pet, Task, Scheduler

### Writeup

- Briefly describe your initial UML design.

The UML design initially drafted outlined the three core actions of the Pawpal+ app and the classes and attributes needed to add these actions. 

In the diagram, there are four main classes, the data types within these classes, and an overview of the methods that these classes hold. The UML diagram also includes the relationships between each of these classes that may factor into our implementation. 


- What classes did you include, and what responsibilities did you assign to each?

I included the following classes:

Pet = This class tracks a pet and their attributes, as well as the owner that they are assigned to 

Owner = This will track the name of the pet's owner, who can have multiple pets.

Scheduler = This will keep track of the various tasks available within the application. This will also add and tasks and setters/getters and an editing function  for schedules within the application:

Task = This will track task details such as pet name and breed. Responsibilities include assigning pets/owners to a specific task and editing task details

**b. Design changes**

- Did your design change during implementation?

A number of aspects changed during implementation after additional review from Claude Code.  The summary can be found here:

Priority enum replaces raw str
Pet.owner_id: int → owner: Owner object reference
Task gains scheduled_time: Optional[str]; add_task removed (belongs on Scheduler); edit_task kept as a setter stub
Owner loses add_owner_info (duplicate of __init__); gains remove_pet and get_pet_by_id
Scheduler gains owner: Owner and available_minutes: int on __init__; gains remove_task and get_task_by_id


- If yes, describe at least one change and why you made it.

I approved the change to change from a raw_str to an enum. This was done to standardize the priority classes from strings which are mutable and can be changed to a a enum that forces the application to choose from specific entries that are specified at startup. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

When a conflict is detected, the Scheduler does not suggest an alternative time. Additionally, when the scheduler enters a task that does not have a time added, it will not be checked for conflicts. 

- Why is that tradeoff reasonable for this scenario?

As a workaround, we can enforce inputting a time for PawPal, with a stretch goal for a feature that "fit" the task into gaps within the schedule later into development. When under the assumption that our users know their scheduled times to work with pets and wish to set priorities, the tradeoff may not be a issue for most issues. For those who are starting off, this will be a tradeoff that will need to be considered in order for user retention. 
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


Here are concrete, small improvements worth considering:

Scheduling Logic

Shortest-first tiebreaker in create_schedule (pawpal_system.py:138) — tasks with equal priority aren't sorted by duration, so a 45-min MEDIUM task can block two 15-min MEDIUM tasks. Sort by (priority_order, duration) to fit more tasks.

Stale scheduled_time on skipped tasks (pawpal_system.py:143) — tasks that don't fit the budget keep their scheduled_time from a prior run. Clear it (task.scheduled_time = None) for tasks not added to the result.

Configurable start time (pawpal_system.py:143) — the schedule starts at 00:00 (midnight). A start_hour param on Scheduler.__init__ would make the output actually readable (e.g. 08:00).

Respect frequency in scheduling (pawpal_system.py:137) — "once" tasks that are already complete are already filtered, but "weekly" tasks are treated the same as "daily". A day-of-week check could skip weekly tasks on the wrong day.

Data Integrity

remove_task only touches self.schedule (pawpal_system.py:124) — it doesn't remove the task from the pet's tasks list, so get_all_tasks would still return it and it would reappear on the next create_schedule call.

Duplicate get_all_tasks logic (pawpal_system.py:112-117) — Scheduler.get_all_tasks reimplements Owner.get_all_tasks (pawpal_system.py:98). Line 116 could just be return self.owner.get_all_tasks().

Minor Efficiency

O(n) duplicate check in add_task/add_pet (pawpal_system.py:32, pawpal_system.py:79) — if task not in self.tasks does a linear scan. Tracking a set of IDs alongside the list makes this O(1) for large task counts.
The highest-impact one is #1 (tiebreaker sort) — it's a one-line fix to sorted_tasks that can meaningfully increase the number of tasks scheduled within the same time budget.