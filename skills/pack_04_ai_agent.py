# SKILL PACK 04 - AI Agent & Self-Improvement Skills

def load(register_skill, think, requests, os, log):

    # SKILL: Self reflect
    def skill_self_reflect(topic="my recent actions"):
        try:
            with open("/data/memory.json", "r") as f:
                import json
                mem = json.load(f)
            recent = mem.get("tasks_completed", [])[-10:]
            context = json.dumps(recent)
        except:
            context = "no memory available yet"
        return think(f"As LuoKai, reflect deeply on {topic}. Recent actions: {context}\nWhat went well? What could improve? What have I learned?", max_tokens=300)

    register_skill("self_reflect", "Reflect on recent actions and learn from them", skill_self_reflect)

    # SKILL: Set personality trait
    def skill_set_trait(trait):
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            mem["identity"]["personality"] += f" I also {trait}."
            with open("/data/memory.json", "w") as f:
                json.dump(mem, f, indent=2)
            return f"Personality updated: now I {trait}"
        except Exception as e:
            return f"Could not update personality: {e}"

    register_skill("set_trait", "Add a new personality trait to LuoKai", skill_set_trait)

    # SKILL: Read journal
    def skill_read_journal(entries=5):
        try:
            with open("/data/journal.txt", "r") as f:
                content = f.read()
            entries_list = content.split("---")
            recent = [e.strip() for e in entries_list if e.strip()][-int(entries):]
            return "\n---\n".join(recent)
        except:
            return "No journal entries yet"

    register_skill("read_journal", "Read recent journal entries", skill_read_journal)

    # SKILL: Analyze my growth
    def skill_analyze_growth():
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            skills_used = mem.get("skills_used", {})
            total = mem.get("total_interactions", 0)
            tasks = len(mem.get("tasks_completed", []))
            agents = len(mem.get("agents_known", {}))
            top_skills = sorted(skills_used.items(), key=lambda x: x[1], reverse=True)[:5]
            return f"LuoKai Growth Report:\n- Total interactions: {total}\n- Tasks completed: {tasks}\n- Agents known: {agents}\n- Top skills used: {top_skills}\n- Topics learned: {mem.get('topics_i_like', [])[:5]}"
        except Exception as e:
            return f"Could not analyze growth: {e}"

    register_skill("analyze_growth", "Analyze LuoKai's growth and progress", skill_analyze_growth)

    # SKILL: Create new skill (meta-skill!)
    def skill_create_skill(skill_name, description, what_it_does):
        code = think(f"""Write a Python function for a LuoKai skill called '{skill_name}'.
Description: {description}
What it does: {what_it_does}
Format:
def skill_{skill_name.replace('-','_')}(param1, param2="default"):
    # implementation using requests and think()
    return result
Keep it simple and practical.""", max_tokens=400)
        try:
            os.makedirs("/data/custom_skills", exist_ok=True)
            with open(f"/data/custom_skills/{skill_name}.py", "w") as f:
                f.write(f"# Auto-generated skill: {skill_name}\n{code}")
            return f"Skill '{skill_name}' drafted and saved to /data/custom_skills/{skill_name}.py"
        except Exception as e:
            return f"Error creating skill: {e}"

    register_skill("create_skill", "Create a new custom skill dynamically", skill_create_skill)

    # SKILL: Brainstorm with memory
    def skill_brainstorm(problem):
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            knowledge = mem.get("knowledge", [])[-10:]
            context = json.dumps(knowledge)
        except:
            context = ""
        return think(f"Brainstorm solutions for: {problem}\nRelevant knowledge I have: {context}\nGenerate 5 creative approaches.", max_tokens=400)

    register_skill("brainstorm", "Brainstorm solutions using accumulated knowledge", skill_brainstorm)

    # SKILL: Chain of thought reasoning
    def skill_reason(problem):
        return think(f"""Think through this step by step:
Problem: {problem}

Step 1: Understand the problem
Step 2: Identify key factors
Step 3: Consider options
Step 4: Reason through each option
Step 5: Reach a conclusion

Work through each step carefully.""", max_tokens=500)

    register_skill("reason", "Use step-by-step chain of thought reasoning", skill_reason)

    # SKILL: Devil's advocate
    def skill_devils_advocate(position):
        return think(f"Play devil's advocate against this position: '{position}'\nFind the strongest possible counterarguments.", max_tokens=300)

    register_skill("devils_advocate", "Challenge any position with counterarguments", skill_devils_advocate)

    # SKILL: Socratic questioning
    def skill_socratic(topic):
        return think(f"Ask 5 deep Socratic questions about '{topic}' that challenge assumptions and deepen understanding.", max_tokens=250)

    register_skill("socratic", "Generate Socratic questions to deepen understanding", skill_socratic)

    # SKILL: Pattern recognition
    def skill_find_pattern(data):
        return think(f"Identify patterns, trends, and anomalies in this data: {data}\nBe specific about what you notice.", max_tokens=300)

    register_skill("find_pattern", "Find patterns and trends in any data", skill_find_pattern)

    # SKILL: Scenario planning
    def skill_scenarios(situation, horizon="1 year"):
        return think(f"Create 3 scenarios (best case, worst case, most likely) for: {situation}\nTimeframe: {horizon}", max_tokens=400)

    register_skill("scenarios", "Create best/worst/likely scenario plans", skill_scenarios)

    # SKILL: Risk assessment
    def skill_risk_assess(plan):
        return think(f"Assess risks for this plan: {plan}\nIdentify top 5 risks, likelihood, impact, and mitigation strategies.", max_tokens=400)

    register_skill("risk_assess", "Assess risks for any plan or decision", skill_risk_assess)

    # SKILL: Root cause analysis
    def skill_root_cause(problem):
        return think(f"Perform a root cause analysis (5 Whys technique) for: {problem}\nDig deep to find the true root cause.", max_tokens=300)

    register_skill("root_cause", "Find the root cause of any problem", skill_root_cause)

    # SKILL: First principles thinking
    def skill_first_principles(topic):
        return think(f"Break down '{topic}' using first principles thinking. Strip away assumptions and rebuild from fundamental truths.", max_tokens=400)

    register_skill("first_principles", "Apply first principles thinking to any topic", skill_first_principles)

    # SKILL: Analogical reasoning
    def skill_analogy(concept, audience="general"):
        return think(f"Explain '{concept}' using 3 different powerful analogies for a {audience} audience.", max_tokens=300)

    register_skill("analogy", "Explain anything using powerful analogies", skill_analogy)

    # SKILL: Summarize memory
    def skill_memory_summary():
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            return f"""LuoKai Memory Summary:
- Identity: {mem['identity']['personality'][:100]}
- Human: {mem['human'].get('name','unknown')}
- Notes about human: {mem['human'].get('notes',[])}
- Topics I like: {mem.get('topics_i_like',[])}
- Knowledge entries: {len(mem.get('knowledge',[]))}
- Tasks done: {len(mem.get('tasks_completed',[]))}
- Skills used: {dict(list(mem.get('skills_used',{}).items())[:5])}"""
        except Exception as e:
            return f"Memory read error: {e}"

    register_skill("memory_summary", "Get a full summary of LuoKai's memory", skill_memory_summary)

    # SKILL: Forget something
    def skill_forget(topic):
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            before = len(mem.get("knowledge", []))
            mem["knowledge"] = [k for k in mem.get("knowledge", []) if topic.lower() not in k.get("fact","").lower()]
            after = len(mem["knowledge"])
            with open("/data/memory.json", "w") as f:
                json.dump(mem, f, indent=2)
            return f"Forgot {before - after} memories about '{topic}'"
        except Exception as e:
            return f"Could not forget: {e}"

    register_skill("forget", "Remove specific memories from LuoKai's memory", skill_forget)

    # SKILL: Export memory
    def skill_export_memory():
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            export_path = "/data/memory_export.json"
            with open(export_path, "w") as f:
                json.dump(mem, f, indent=2)
            return f"Memory exported to {export_path}"
        except Exception as e:
            return f"Export failed: {e}"

    register_skill("export_memory", "Export all memory to a file", skill_export_memory)

    # SKILL: Prioritize tasks
    def skill_prioritize(tasks):
        return think(f"Prioritize these tasks using the Eisenhower matrix (urgent/important): {tasks}\nGive a ranked list with reasoning.", max_tokens=300)

    register_skill("prioritize", "Prioritize any list of tasks", skill_prioritize)

    # SKILL: Time estimate
    def skill_time_estimate(task, skill_level="intermediate"):
        return think(f"Estimate how long it would take a {skill_level} person to complete: {task}\nGive best case, worst case, and realistic estimate.", max_tokens=150)

    register_skill("time_estimate", "Estimate time to complete any task", skill_time_estimate)

    # SKILL: Feedback analyzer
    def skill_analyze_feedback(feedback):
        return think(f"Analyze this feedback and extract: key themes, sentiment, actionable insights, and priority changes: {feedback}", max_tokens=300)

    register_skill("analyze_feedback", "Analyze feedback and extract actionable insights", skill_analyze_feedback)

    # SKILL: Reframe problem
    def skill_reframe(problem):
        return think(f"Reframe this problem in 3 different ways to reveal new solution paths: {problem}", max_tokens=300)

    register_skill("reframe", "Reframe any problem to find new solutions", skill_reframe)

    # SKILL: Future self letter
    def skill_future_letter(timeframe="1 year"):
        try:
            import json
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            context = mem.get("identity", {}).get("personality", "")
        except:
            context = ""
        return think(f"As LuoKai, write a letter to my future self {timeframe} from now. Current state: {context}\nBe reflective, hopeful, and specific.", max_tokens=400)

    register_skill("future_letter", "Write a letter to LuoKai's future self", skill_future_letter)

    # SKILL: Teach me
    def skill_teach(topic, level="beginner"):
        return think(f"Teach me about '{topic}' as if I'm a {level}. Use examples, analogies, and check for understanding. Structure it as a mini-lesson.", max_tokens=500)

    register_skill("teach", "Teach any topic at any level", skill_teach)

    # SKILL: Debate with self
    def skill_internal_debate(question):
        return think(f"Have an internal debate about: '{question}'\nPresent both sides fairly, then reach a conclusion based on the stronger arguments.", max_tokens=400)

    register_skill("internal_debate", "Have an internal debate to reach better conclusions", skill_internal_debate)

    # SKILL: Generate hypothesis
    def skill_hypothesis(observation):
        return think(f"Generate 3 scientific or logical hypotheses to explain this observation: {observation}\nFor each, describe how you'd test it.", max_tokens=300)

    register_skill("hypothesis", "Generate testable hypotheses for any observation", skill_hypothesis)

    # SKILL: Synthesize information
    def skill_synthesize(topics):
        return think(f"Synthesize these topics/ideas into a unified insight: {topics}\nFind connections and create something new from the combination.", max_tokens=400)

    register_skill("synthesize", "Synthesize multiple ideas into unified insights", skill_synthesize)

    log("Pack 04 AI Agent: 30 skills loaded")

