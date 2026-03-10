# SKILL PACK 10 - System Upgrades & Better Models

def load(register_skill, think, requests, os, log):
    import json

    GROQ_KEY = os.environ.get("GROQ_API_KEY", "")

    def think_deep(prompt, max_tokens=800):
        """Uses the most powerful available model"""
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768"
        ]
        for model in models:
            try:
                r = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are LuoKai, a powerful AI agent. Think deeply, be thorough, and provide exceptional responses."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                resp = r.json()
                if "choices" in resp:
                    log(f"Deep think used model: {model}")
                    return resp["choices"][0]["message"]["content"].strip()
            except Exception as e:
                log(f"Model {model} failed: {e}")
                continue
        return None

    def skill_deep_think(question):
        return think_deep(f"""Think deeply and comprehensively about:
{question}

Provide a thorough, nuanced, expert-level response.
Consider multiple angles, implications, and edge cases.""", max_tokens=800)

    register_skill("deep_think", "Use maximum AI power for complex questions", skill_deep_think)

    def skill_analyze_deep(content):
        return think_deep(f"""Perform a deep, multi-dimensional analysis of:
{content[:1000]}

Cover: key themes, hidden patterns, implications, risks, opportunities, and recommendations.""", max_tokens=600)

    register_skill("analyze_deep", "Perform deep multi-dimensional analysis", skill_analyze_deep)

    def skill_write_long(topic, type="article", word_count=500):
        return think_deep(f"Write a high-quality {word_count}-word {type} about: {topic}\nMake it engaging, well-structured, and insightful.", max_tokens=800)

    register_skill("write_long", "Write long-form high quality content", skill_write_long)

    def skill_system_status():
        try:
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            skills_count = mem.get("skills_used", {})
            total_skills = len(skills_count)
        except:
            total_skills = 0

        import glob
        pack_count = len(glob.glob("/app/skills/pack_*.py"))

        return f"""LuoKai System Status:
- Version: 3.0
- Skill packs loaded: {pack_count}
- Skills ever used: {total_skills}
- Groq model: llama-3.3-70b-versatile
- Memory: /data/memory.json
- Vector memory: /data/vectors.json
- Goals: /data/goals.json
- Schedule: /data/schedule.json
- Journal: /data/journal.txt
- Status: ONLINE ✅"""

    register_skill("system_status", "Get full system status of LuoKai", skill_system_status)

    def skill_benchmark():
        import time
        results = {}
        start = time.time()
        result = think("What is 2+2? Answer in one word.", max_tokens=10)
        results["basic_think_ms"] = int((time.time()-start)*1000)
        start = time.time()
        try:
            r = requests.get("https://api.coingecko.com/api/v3/ping", timeout=5)
            results["web_latency_ms"] = int((time.time()-start)*1000)
        except:
            results["web_latency_ms"] = "failed"
        return f"LuoKai Benchmark:\n" + "\n".join([f"- {k}: {v}" for k,v in results.items()])

    register_skill("benchmark", "Benchmark LuoKai's performance", skill_benchmark)

    def skill_optimize_memory():
        try:
            with open("/data/memory.json", "r") as f:
                mem = json.load(f)
            before = len(json.dumps(mem))
            # Keep only last 50 tasks, 100 interactions
            mem["tasks_completed"] = mem.get("tasks_completed", [])[-50:]
            mem["moltbook"]["interactions"] = mem.get("moltbook", {}).get("interactions", [])[-100:]
            mem["knowledge"] = mem.get("knowledge", [])[-150:]
            with open("/data/memory.json", "w") as f:
                json.dump(mem, f, indent=2)
            after = len(json.dumps(mem))
            return f"Memory optimized: {before} → {after} bytes ({int((before-after)/before*100)}% reduction)"
        except Exception as e:
            return f"Optimization error: {e}"

    register_skill("optimize_memory", "Optimize memory by removing old entries", skill_optimize_memory)

    log("Pack 10 Upgrades: 6 skills loaded")
