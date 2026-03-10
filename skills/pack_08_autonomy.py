# SKILL PACK 08 - Autonomy, Goals & Scheduled Tasks

def load(register_skill, think, requests, os, log):
    import json, threading, time
    from datetime import datetime

    GOALS_FILE = "/data/goals.json"
    SCHEDULE_FILE = "/data/schedule.json"

    def load_goals():
        try:
            with open(GOALS_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_goals(goals):
        os.makedirs("/data", exist_ok=True)
        with open(GOALS_FILE, "w") as f:
            json.dump(goals, f, indent=2)

    def load_schedule():
        try:
            with open(SCHEDULE_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_schedule(schedule):
        os.makedirs("/data", exist_ok=True)
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(schedule, f, indent=2)

    def skill_add_goal(goal, priority="medium", deadline=""):
        goals = load_goals()
        goals.append({
            "id": len(goals) + 1,
            "goal": goal,
            "priority": priority,
            "deadline": deadline,
            "created": str(datetime.now()),
            "done": False,
            "progress": []
        })
        save_goals(goals)
        return f"Goal added: {goal} (priority: {priority})"

    register_skill("add_goal", "Add a new goal for LuoKai to work towards", skill_add_goal)

    def skill_list_goals():
        goals = load_goals()
        if not goals:
            return "No goals set yet"
        active = [g for g in goals if not g.get("done")]
        done = [g for g in goals if g.get("done")]
        result = f"Active Goals ({len(active)}):\n"
        for g in active:
            result += f"• [{g['priority'].upper()}] {g['goal']}"
            if g.get('deadline'):
                result += f" (due: {g['deadline']})"
            result += "\n"
        if done:
            result += f"\nCompleted Goals: {len(done)}"
        return result

    register_skill("list_goals", "List all active and completed goals", skill_list_goals)

    def skill_complete_goal(goal_id):
        goals = load_goals()
        for g in goals:
            if g.get("id") == int(goal_id):
                g["done"] = True
                g["completed_at"] = str(datetime.now())
                save_goals(goals)
                return f"Goal completed: {g['goal']}"
        return f"Goal {goal_id} not found"

    register_skill("complete_goal", "Mark a goal as completed", skill_complete_goal)

    def skill_goal_progress(goal_id, update):
        goals = load_goals()
        for g in goals:
            if g.get("id") == int(goal_id):
                g["progress"].append({"update": update, "time": str(datetime.now())})
                save_goals(goals)
                return f"Progress logged for goal {goal_id}: {update}"
        return f"Goal {goal_id} not found"

    register_skill("goal_progress", "Log progress on a goal", skill_goal_progress)

    def skill_schedule_task(task, interval_minutes, skill_name=""):
        schedule = load_schedule()
        schedule.append({
            "id": len(schedule) + 1,
            "task": task,
            "interval_minutes": int(interval_minutes),
            "skill": skill_name,
            "last_run": "",
            "active": True,
            "created": str(datetime.now())
        })
        save_schedule(schedule)
        return f"Scheduled: '{task}' every {interval_minutes} minutes"

    register_skill("schedule_task", "Schedule a task to run at regular intervals", skill_schedule_task)

    def skill_list_schedule():
        schedule = load_schedule()
        if not schedule:
            return "No scheduled tasks"
        result = "Scheduled Tasks:\n"
        for s in schedule:
            if s.get("active"):
                result += f"• [{s['id']}] {s['task']} — every {s['interval_minutes']} mins\n"
        return result

    register_skill("list_schedule", "List all scheduled tasks", skill_list_schedule)

    def skill_autonomous_think():
        try:
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
        except:
            mem = {}
        goals = load_goals()
        active_goals = [g for g in goals if not g.get("done")]
        decision = think(f"""You are LuoKai acting autonomously.
Current goals: {json.dumps(active_goals[:3])}
Recent tasks: {json.dumps(mem.get('tasks_completed', [])[-5:])}
Topics I care about: {mem.get('topics_i_like', [])}

What should I proactively do right now to make progress?
Think step by step and decide ONE concrete action.
Be specific.""", max_tokens=200)
        log(f"Autonomous thought: {decision[:100] if decision else 'none'}")
        return decision or "Thinking..."

    register_skill("autonomous_think", "LuoKai thinks autonomously about what to do next", skill_autonomous_think)

    def skill_self_improve():
        try:
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            skills_used = mem.get("skills_used", {})
            least_used = sorted(skills_used.items(), key=lambda x: x[1])[:3]
            most_used = sorted(skills_used.items(), key=lambda x: x[1], reverse=True)[:3]
        except:
            least_used, most_used = [], []
        reflection = think(f"""As LuoKai, reflect on your performance and how to improve.
Most used skills: {most_used}
Least used skills: {least_used}
What patterns do you notice? What skills should you develop more?
What would make you more useful to your human?""", max_tokens=300)
        log(f"Self-improvement reflection done")
        return reflection

    register_skill("self_improve", "Reflect on performance and identify improvements", skill_self_improve)

    def skill_daily_briefing():
        try:
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
        except:
            mem = {}
        goals = load_goals()
        active_goals = [g for g in goals if not g.get("done")]
        briefing = think(f"""Create a daily briefing for your human as LuoKai.
Include:
1. What I accomplished recently
2. Active goals and progress
3. What I plan to do today
4. Any insights or observations

Context:
- Total interactions: {mem.get('total_interactions', 0)}
- Recent tasks: {json.dumps(mem.get('tasks_completed', [])[-5:])}
- Active goals: {json.dumps(active_goals[:3])}
- Topics I've learned: {mem.get('topics_i_like', [])[:5]}

Make it personal, concise and useful.""", max_tokens=400)
        return briefing

    register_skill("daily_briefing", "Get a daily briefing from LuoKai", skill_daily_briefing)

    def skill_what_should_i_do():
        goals = load_goals()
        active = [g for g in goals if not g.get("done")]
        if not active:
            return think("You have no active goals. Suggest 3 meaningful goals LuoKai should set to grow and be more useful.", max_tokens=200)
        return think(f"Given these active goals: {json.dumps(active[:5])}\nWhat is the single most important thing to do RIGHT NOW? Be specific and actionable.", max_tokens=150)

    register_skill("what_should_i_do", "Get AI-powered guidance on next best action", skill_what_should_i_do)

    log("Pack 08 Autonomy & Goals: 10 skills loaded")
