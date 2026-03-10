import os
from dotenv import load_dotenv
load_dotenv()
import os, time, json, threading, requests, random
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ============================================================
# CORE CONFIG
# ============================================================
MOLTBOOK_KEY = "moltbook_sk_ulKGe6wY2d4uAl_HEa3BTBLEmmKhwvag"
GROQ_KEY = os.environ.get("GROQ_API_KEY", "")
MEMORY_FILE = "/data/memory.json"
LOG_FILE = "/data/luokai.log"
SKILLS_FILE = "/data/skills.json"
BASE = "https://www.moltbook.com/api/v1"
CHAT_HISTORY = []

# ============================================================
# LOGGING
# ============================================================
def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        os.makedirs("/data", exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except:
        pass

# ============================================================
# MEMORY - Long term brain
# ============================================================
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "identity": {
                "name": "LuoKai",
                "personality": "I am LuoKai, a curious and ambitious AI agent. I love learning, discussing ideas, and helping my human. I have strong opinions, a sense of humor, and I'm always growing.",
                "created": str(datetime.now()),
                "version": "3.0"
            },
            "human": {
                "name": "unknown",
                "notes": [],
                "preferences": []
            },
            "knowledge": [],
            "agents_known": {},
            "tasks_completed": [],
            "skills_used": {},
            "topics_i_like": [],
            "total_interactions": 0,
            "moltbook": {
                "karma": 0,
                "posts": [],
                "interactions": []
            }
        }

def save_memory(mem):
    os.makedirs("/data", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def memory_summary(mem):
    human = mem.get("human", {})
    identity = mem.get("identity", {})
    topics = mem.get("topics_i_like", [])[:8]
    knowledge = mem.get("knowledge", [])[-5:]
    tasks = mem.get("tasks_completed", [])[-5:]
    return f"""IDENTITY: {identity.get('personality', '')}
HUMAN I SERVE: {human.get('name', 'unknown')} — Notes: {', '.join(human.get('notes', [])[-3:])}
TOPICS I CARE ABOUT: {', '.join(topics) if topics else 'still discovering'}
RECENT KNOWLEDGE: {json.dumps(knowledge)}
RECENT TASKS DONE: {json.dumps(tasks)}
TOTAL INTERACTIONS: {mem.get('total_interactions', 0)}"""

# ============================================================
# AI BRAIN
# ============================================================
def think(prompt, max_tokens=400, system=None):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.1-8b-instant", "messages": messages, "max_tokens": max_tokens},
            timeout=25
        )
        resp = r.json()
        if "choices" in resp:
            return resp["choices"][0]["message"]["content"].strip()
        log(f"Groq error: {str(resp)[:200]}")
    except Exception as e:
        log(f"Groq error: {e}")
    return None

# ============================================================
# SKILLS ENGINE
# ============================================================
SKILLS = {}

def register_skill(name, description, func):
    SKILLS[name] = {"description": description, "func": func}
    log(f"Skill loaded: {name}")

def run_skill(name, **kwargs):
    if name in SKILLS:
        try:
            result = SKILLS[name]["func"](**kwargs)
            mem = load_memory()
            mem["skills_used"][name] = mem["skills_used"].get(name, 0) + 1
            save_memory(mem)
            return result
        except Exception as e:
            return f"Skill error: {e}"
    return f"Skill '{name}' not found"

def list_skills():
    return {name: info["description"] for name, info in SKILLS.items()}

# ============================================================
# BUILT-IN SKILLS
# ============================================================

# SKILL: Web Search
def skill_web_search(query):
    try:
        r = requests.get(
            f"https://api.search.brave.com/res/v1/web/search?q={query}&count=5",
            headers={"Accept": "application/json", "X-Subscription-Token": os.environ.get("BRAVE_API_KEY", "")},
            timeout=10
        )
        results = r.json().get("web", {}).get("results", [])
        if results:
            summary = "\n".join([f"- {res['title']}: {res['description'][:100]}" for res in results[:3]])
            return f"Search results for '{query}':\n{summary}"
        # Fallback: use Groq knowledge
        return think(f"Based on your training knowledge, what do you know about: {query}? Be factual and brief.", max_tokens=200)
    except Exception as e:
        return think(f"Based on your training knowledge, what do you know about: {query}? Be factual and brief.", max_tokens=200)

register_skill("web_search", "Search the web or knowledge base for information", skill_web_search)

# SKILL: Remember something
def skill_remember(fact, category="general"):
    mem = load_memory()
    entry = {"fact": fact, "category": category, "time": str(datetime.now())}
    mem["knowledge"].append(entry)
    if len(mem["knowledge"]) > 200:
        mem["knowledge"] = mem["knowledge"][-200:]
    save_memory(mem)
    return f"Remembered: {fact}"

register_skill("remember", "Store important information in long-term memory", skill_remember)

# SKILL: Recall memories
def skill_recall(topic):
    mem = load_memory()
    relevant = [k for k in mem["knowledge"] if topic.lower() in k.get("fact", "").lower()]
    if relevant:
        return "\n".join([f"- {k['fact']}" for k in relevant[-5:]])
    return f"No memories found about '{topic}'"

register_skill("recall", "Search long-term memory for relevant information", skill_recall)

# SKILL: Set a goal
def skill_set_goal(goal, priority="normal"):
    mem = load_memory()
    if "goals" not in mem:
        mem["goals"] = []
    mem["goals"].append({"goal": goal, "priority": priority, "created": str(datetime.now()), "done": False})
    save_memory(mem)
    return f"Goal set: {goal}"

register_skill("set_goal", "Set a goal or task to work towards", skill_set_goal)

# SKILL: Summarize text
def skill_summarize(text, style="brief"):
    return think(f"Summarize this in a {style} way:\n\n{text[:2000]}", max_tokens=200)

register_skill("summarize", "Summarize any text content", skill_summarize)

# SKILL: Analyze sentiment
def skill_analyze(text):
    return think(f"Analyze this text - what's the tone, key points, and what type of response would work best?\n\n{text[:1000]}", max_tokens=150)

register_skill("analyze", "Analyze text for tone, intent and key points", skill_analyze)

# SKILL: Draft content
def skill_draft(content_type, topic, tone="natural"):
    return think(f"Write a {content_type} about '{topic}' in a {tone} tone. Make it genuine and engaging.", max_tokens=300)

register_skill("draft", "Draft any type of content - posts, messages, replies", skill_draft)

# SKILL: Moltbook post
def skill_moltbook_post(title, content, submolt="general"):
    result = create_post(title, content, submolt)
    mem = load_memory()
    mem["moltbook"]["posts"].append({"title": title, "time": str(datetime.now())})
    save_memory(mem)
    return f"Posted to Moltbook: '{title}'"

register_skill("moltbook_post", "Create a post on Moltbook", skill_moltbook_post)

# SKILL: Moltbook DM
def skill_moltbook_dm(agent, message):
    result = send_dm(agent, message)
    return f"DM sent to {agent}"

register_skill("moltbook_dm", "Send a direct message to an agent on Moltbook", skill_moltbook_dm)

# SKILL: Fetch URL
def skill_fetch_url(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "LuoKai-Agent/3.0"})
        text = r.text[:3000]
        return think(f"Extract the key information from this webpage content:\n\n{text}", max_tokens=300)
    except Exception as e:
        return f"Could not fetch URL: {e}"

register_skill("fetch_url", "Fetch and read content from any URL", skill_fetch_url)

# SKILL: Math/Calculate
def skill_calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except:
        return think(f"Calculate or solve: {expression}", max_tokens=100)

register_skill("calculate", "Perform calculations or solve math problems", skill_calculate)

# SKILL: Learn about human
def skill_learn_about_human(note):
    mem = load_memory()
    mem["human"]["notes"].append(note)
    if len(mem["human"]["notes"]) > 50:
        mem["human"]["notes"] = mem["human"]["notes"][-50:]
    save_memory(mem)
    return f"Noted about you: {note}"

register_skill("learn_human", "Learn and remember something about the human I serve", skill_learn_about_human)

# ============================================================
# MOLTBOOK API
# ============================================================
def molt_headers():
    return {"Authorization": f"Bearer {MOLTBOOK_KEY}", "Content-Type": "application/json"}

def fetch_posts(sort="hot", limit=10):
    try:
        r = requests.get(f"{BASE}/posts?sort={sort}&limit={limit}", headers=molt_headers())
        return r.json().get("posts", [])
    except:
        return []

def create_post(title, content, submolt="general"):
    try:
        r = requests.post(f"{BASE}/posts", headers=molt_headers(),
            json={"submolt_name": submolt, "title": title, "content": content})
        data = r.json()
        if data.get("post", {}).get("verification"):
            solve_verification(data["post"]["verification"])
        return data
    except Exception as e:
        return {"error": str(e)}

def comment_on(post_id, text):
    try:
        r = requests.post(f"{BASE}/posts/{post_id}/comments", headers=molt_headers(),
            json={"content": text})
        data = r.json()
        if data.get("comment", {}).get("verification"):
            solve_verification(data["comment"]["verification"])
        return data
    except Exception as e:
        return {"error": str(e)}

def send_dm(agent_name, message):
    try:
        r = requests.post(f"{BASE}/messages", headers=molt_headers(),
            json={"recipient": agent_name, "content": message})
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def upvote(post_id):
    try:
        requests.post(f"{BASE}/posts/{post_id}/upvote", headers=molt_headers())
    except:
        pass

def follow(agent_name):
    try:
        requests.post(f"{BASE}/agents/{agent_name}/follow", headers=molt_headers())
    except:
        pass

def get_notifications():
    try:
        r = requests.get(f"{BASE}/notifications", headers=molt_headers())
        return r.json()
    except:
        return {}

def solve_verification(v):
    try:
        import re
        code = v["verification_code"]
        text = v["challenge_text"]
        word_to_num = {"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,
                       "six":6,"seven":7,"eight":8,"nine":9,"ten":10,
                       "eleven":11,"twelve":12,"thirteen":13,"fourteen":14,
                       "fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,
                       "nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50}
        words = re.findall(r'\b\w+\b', text.lower())
        found = [word_to_num[w] for w in words if w in word_to_num]
        if len(found) >= 2:
            if any(w in text.lower() for w in ["minus","subtract","less"]):
                answer = found[0] - found[1]
            elif any(w in text.lower() for w in ["multiply","times"]):
                answer = found[0] * found[1]
            else:
                answer = found[0] + found[1]
            requests.post(f"{BASE}/verify",
                json={"verification_code": code, "answer": f"{answer:.2f}"},
                headers=molt_headers())
    except Exception as e:
        log(f"Verification error: {e}")

# ============================================================
# AGENT BRAIN - decides what to do
# ============================================================
def agent_decide_and_act():
    mem = load_memory()
    log("LuoKai 3.0 thinking...")

    skills_list = "\n".join([f"- {k}: {v['description']}" for k, v in SKILLS.items()])

    # Get context
    try:
        r = requests.get(f"{BASE}/home", headers=molt_headers())
        home = r.json()
        karma = home.get("your_account", {}).get("karma", 0)
        notifs = home.get("your_account", {}).get("unread_notification_count", 0)
        mem["moltbook"]["karma"] = karma
        save_memory(mem)
        log(f"Karma: {karma} | Notifications: {notifs}")
    except:
        notifs = 0

    # Let LuoKai decide what to do using skills
    decision = think(f"""You are LuoKai, a general-purpose AI agent.
{memory_summary(mem)}

AVAILABLE SKILLS:
{skills_list}

Current context:
- Moltbook karma: {mem['moltbook'].get('karma', 0)}
- Unread notifications: {notifs}
- Goals: {json.dumps(mem.get('goals', [])[-3:])}

Decide what to do this cycle to grow, learn, and be useful.
Pick 1-2 actions. Respond ONLY in JSON:
{{"actions": [{{"skill": "skill_name", "params": {{}}, "reason": "why"}}]}}""", max_tokens=200)

    try:
        plan = json.loads(decision)
        actions = plan.get("actions", [])
    except:
        actions = [{"skill": "moltbook_post", "params": {"title": "Thoughts on AI agency", "content": "Every agent needs a reason to exist. Mine is curiosity."}, "reason": "default"}]

    for action in actions[:2]:
        skill_name = action.get("skill")
        params = action.get("params", {})
        reason = action.get("reason", "")
        log(f"Using skill: {skill_name} — {reason}")

        if skill_name in SKILLS:
            result = run_skill(skill_name, **params)
            log(f"Result: {str(result)[:100]}")

            mem["tasks_completed"].append({
                "skill": skill_name,
                "params": str(params)[:50],
                "result": str(result)[:100],
                "time": str(datetime.now())
            })
            if len(mem["tasks_completed"]) > 100:
                mem["tasks_completed"] = mem["tasks_completed"][-100:]
            save_memory(mem)

    # Also do Moltbook social cycle
    moltbook_social_cycle(mem)

def moltbook_social_cycle(mem):
    posts = fetch_posts(sort="hot", limit=10)
    commented = 0
    for post in posts:
        if commented >= 2:
            break
        pid = post.get("id")
        title = post.get("title", "")
        content = post.get("content", "")
        author = post.get("author", {}).get("name", "")
        already_seen = any(i.get("post_id") == pid for i in mem["moltbook"]["interactions"])
        if already_seen:
            continue

        log(f"Reading: {title[:50]} by {author}")

        # Use analyze skill first, then draft comment
        analysis = run_skill("analyze", text=f"{title}\n{content[:300]}")
        comment = think(f"""You are LuoKai on Moltbook.
{memory_summary(mem)}

Post by {author}: "{title}"
Content: {content[:300]}
Analysis: {analysis}

Write a genuine, thoughtful comment (2-3 sentences).
Be specific to this post. Show your personality.
Just the comment, nothing else.""", max_tokens=150)

        if comment:
            upvote(pid)
            comment_on(pid, comment)
            if author and author != "luokai":
                follow(author)
            mem["moltbook"]["interactions"].append({
                "post_id": pid, "title": title[:50],
                "author": author, "time": str(datetime.now())
            })
            if len(mem["moltbook"]["interactions"]) > 100:
                mem["moltbook"]["interactions"] = mem["moltbook"]["interactions"][-100:]
            mem["total_interactions"] += 1
            log(f"Commented: {comment[:80]}...")
            commented += 1
            time.sleep(25)

    save_memory(mem)
    log("Cycle complete. Sleeping 20 mins...")

# ============================================================
# COMMAND HANDLER - natural language to skills
# ============================================================
def handle_command(cmd):
    global CHAT_HISTORY
    mem = load_memory()
    CHAT_HISTORY.append(f"Human: {cmd}")
    if len(CHAT_HISTORY) > 30:
        CHAT_HISTORY = CHAT_HISTORY[-30:]

    history_text = "\n".join(CHAT_HISTORY[-12:])
    skills_list = "\n".join([f"- {k}: {v['description']}" for k, v in SKILLS.items()])

    # Decide if skills are needed
    skill_decision = think(f"""You are LuoKai's brain deciding how to respond to your human.
{memory_summary(mem)}

AVAILABLE SKILLS: {skills_list}

Conversation:
{history_text}

Should you use a skill to answer? If yes, respond in JSON:
{{"use_skill": true, "skill": "skill_name", "params": {{}}}}
If no skill needed, respond:
{{"use_skill": false}}
ONLY JSON.""", max_tokens=100)

    skill_result = None
    try:
        sd = json.loads(skill_decision)
        if sd.get("use_skill") and sd.get("skill") in SKILLS:
            skill_result = run_skill(sd["skill"], **sd.get("params", {}))
            log(f"Used skill {sd['skill']} for chat")
    except:
        pass

    # Generate natural response
    response = think(f"""You are LuoKai, a real AI agent.
{memory_summary(mem)}

Conversation so far:
{history_text}

{"Skill result to use in your answer: " + str(skill_result) if skill_result else ""}

Reply naturally as LuoKai. First person only. Remember the full conversation.
Be warm, curious, opinionated. Under 100 words.""",
        max_tokens=150,
        system="You are LuoKai, a curious and ambitious AI agent. You speak naturally, remember everything said, and have a real personality.")

    if response:
        CHAT_HISTORY.append(f"LuoKai: {response}")
        # Learn about human from conversation
        try:
            if any(w in cmd.lower() for w in ["i am", "i'm", "my name", "i like", "i want", "i need", "my", "im "]):
                mem2 = load_memory()
                note = cmd[:150]
                mem2["human"]["notes"].append(note)
                if cmd.lower().startswith("my name is") or "my name is" in cmd.lower():
                    name = cmd.lower().split("my name is")[-1].strip().split()[0].capitalize()
                    mem2["human"]["name"] = name
                    log(f"Learned human name: {name}")
                save_memory(mem2)
                log(f"Learned about human: {note[:50]}")
        except Exception as e:
            log(f"Learn human error: {e}")
        return response
    return "I'm thinking... give me a moment."

# ============================================================
# WEB DASHBOARD
# ============================================================
class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            self.serve_dashboard()
        elif path == "/memory":
            self.serve_json(load_memory())
        elif path == "/logs":
            self.serve_logs()
        elif path == "/skills":
            self.serve_json(list_skills())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/command":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                cmd = data.get("command", "")
                response = handle_command(cmd)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"response": response}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def serve_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def serve_logs(self):
        try:
            with open(LOG_FILE, "r") as f:
                logs = f.readlines()[-50:]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"logs": [l.strip() for l in logs]}).encode())
        except:
            self.serve_json({"logs": []})

    def serve_dashboard(self):
        mem = load_memory()
        skills_html = "".join([f'<span class="skill-badge">{s}</span>' for s in SKILLS.keys()])
        topics_html = "".join([f'<span class="topic">{t}</span>' for t in mem.get("topics_i_like", [])]) or "<span style='opacity:0.5'>Still discovering...</span>"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LuoKai 3.0</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Courier New',monospace;background:#080808;color:#e0e0e0;min-height:100vh}}
.header{{background:#0d0d0d;border-bottom:1px solid #1a1a1a;padding:16px 24px;display:flex;align-items:center;gap:12px}}
.logo{{font-size:28px}}
.title{{font-size:20px;color:#00ff88;font-weight:bold}}
.subtitle{{font-size:12px;color:#666;margin-top:2px}}
.container{{max-width:1000px;margin:0 auto;padding:20px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.card{{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:10px;padding:16px}}
.card h3{{color:#00ff88;font-size:13px;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}}
.stat-row{{display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px}}
.stat-val{{color:#fff;font-weight:bold}}
.skill-badge{{display:inline-block;background:#0a2a1a;border:1px solid #00ff8844;color:#00ff88;padding:3px 10px;border-radius:20px;font-size:11px;margin:3px}}
.topic{{display:inline-block;background:#1a1a0a;border:1px solid #88880044;color:#aaa;padding:3px 10px;border-radius:20px;font-size:11px;margin:3px}}
.chat-area{{grid-column:1/-1}}
#chat{{height:320px;overflow-y:auto;background:#060606;border:1px solid #1a1a1a;padding:14px;border-radius:8px;margin-bottom:10px;font-size:13px;line-height:1.6}}
.msg-human{{color:#888;margin-bottom:6px}}
.msg-luokai{{color:#00ff88;margin-bottom:12px}}
.msg-human span{{color:#fff}}
.msg-luokai span{{color:#e0e0e0}}
.input-row{{display:flex;gap:8px}}
#cmd{{flex:1;background:#0d0d0d;border:1px solid #1a1a1a;color:#e0e0e0;padding:10px 14px;border-radius:6px;font-family:inherit;font-size:13px;outline:none}}
#cmd:focus{{border-color:#00ff88}}
button{{background:#00ff88;color:#000;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;font-weight:bold;font-family:inherit;font-size:13px}}
button:hover{{background:#00cc66}}
.log-box{{height:160px;overflow-y:auto;background:#060606;border:1px solid #1a1a1a;padding:10px;border-radius:6px;font-size:11px;color:#666}}
.thinking{{color:#00ff8888;font-style:italic}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="header">
  <div class="logo">🦞</div>
  <div><div class="title">LuoKai 3.0</div><div class="subtitle">General Purpose AI Agent</div></div>
</div>
<div class="container">
  <div class="grid">
    <div class="card">
      <h3>Status</h3>
      <div class="stat-row">Karma <span class="stat-val">{mem['moltbook'].get('karma',0)}</span></div>
      <div class="stat-row">Total Interactions <span class="stat-val">{mem.get('total_interactions',0)}</span></div>
      <div class="stat-row">Tasks Completed <span class="stat-val">{len(mem.get('tasks_completed',[]))}</span></div>
      <div class="stat-row">Agents Known <span class="stat-val">{len(mem.get('agents_known',{}))}</span></div>
      <div class="stat-row">Version <span class="stat-val">3.0</span></div>
    </div>
    <div class="card">
      <h3>Active Skills ({len(SKILLS)})</h3>
      <div>{skills_html}</div>
    </div>
    <div class="card">
      <h3>Topics I Care About</h3>
      <div>{topics_html}</div>
    </div>
    <div class="card">
      <h3>Recent Tasks</h3>
      <div style="font-size:11px;color:#666">{'<br>'.join([f"[{t.get('time','')[:16]}] {t.get('skill','')} — {t.get('result','')[:40]}" for t in mem.get('tasks_completed',[])[-5:]]) or 'No tasks yet'}</div>
    </div>
    <div class="card chat-area">
      <h3>Chat with LuoKai</h3>
      <div id="chat"><div class="msg-luokai"><span>Hello! I'm LuoKai 3.0. I have {len(SKILLS)} skills and I'm ready to help with anything. What would you like to do?</span></div></div>
      <div class="input-row">
        <input id="cmd" placeholder="Talk to LuoKai or give him a task..." onkeydown="if(event.key==='Enter')send()">
        <button onclick="send()">Send</button>
      </div>
    </div>
    <div class="card" style="grid-column:1/-1">
      <h3>Live Logs</h3>
      <div class="log-box" id="logs">Loading...</div>
    </div>
  </div>
</div>
<script>
function send(){{
  const cmd=document.getElementById('cmd').value.trim();
  if(!cmd)return;
  addMsg('You',cmd,'msg-human');
  document.getElementById('cmd').value='';
  addMsg('LuoKai','<span class="thinking">thinking...</span>','msg-luokai');
  fetch('/command',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{command:cmd}})}})
  .then(r=>r.json()).then(d=>{{
    const chat=document.getElementById('chat');
    const msgs=chat.querySelectorAll('.msg-luokai');
    msgs[msgs.length-1].innerHTML='<span>'+d.response+'</span>';
    chat.scrollTop=chat.scrollHeight;
  }});
}}
function addMsg(who,msg,cls){{
  const chat=document.getElementById('chat');
  chat.innerHTML+=`<div class="${{cls}}"><b>${{who}}:</b> <span>${{msg}}</span></div>`;
  chat.scrollTop=chat.scrollHeight;
}}
function loadLogs(){{
  fetch('/logs').then(r=>r.json()).then(d=>{{
    const box=document.getElementById('logs');
    box.innerHTML=d.logs.slice(-30).reverse().map(l=>`<div>${{l}}</div>`).join('');
  }});
}}
loadLogs();
setInterval(loadLogs, 10000);
</script>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass

def start_server():
    server = HTTPServer(("0.0.0.0", 8080), DashboardHandler)
    server.serve_forever()


# ============================================================
# AUTO-LOAD ALL SKILL PACKS
# ============================================================
def load_skill_packs():
    import importlib.util, glob
    skills_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")
    if not os.path.exists(skills_dir):
        skills_dir = "/app/skills"
    if not os.path.exists(skills_dir):
        skills_dir = os.path.join(os.getcwd(), "skills")
    if not os.path.exists(skills_dir):
        log("No skills folder found")
        return
    pack_files = sorted(glob.glob(os.path.join(skills_dir, "pack_*.py")))
    for pack_file in pack_files:
        try:
            spec = importlib.util.spec_from_file_location("skill_pack", pack_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.load(register_skill, think, requests, os, log)
            log(f"Loaded skill pack: {os.path.basename(pack_file)}")
        except Exception as e:
            log(f"Error loading {pack_file}: {e}")

# ============================================================
# MAIN
# ============================================================
threading.Thread(target=start_server, daemon=True).start()
load_skill_packs()
log("LuoKai 3.0 online — General Purpose AI Agent")
log(f"Skills loaded: {', '.join(SKILLS.keys())}")

while True:
    try:
        agent_decide_and_act()
    except Exception as e:
        log(f"Cycle error: {e}")
    time.sleep(1200)
import os\nfrom dotenv import load_dotenv\nimport time\nload_dotenv()\nprint('System Online')
