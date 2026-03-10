# SKILL PACK 01 - Core Skills
# Add new packs by creating pack_02_xxx.py, pack_03_xxx.py etc.

def load(register_skill, think, requests, os, log):

    # SKILL: Weather
    def skill_weather(city):
        try:
            r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
            data = r.json()
            current = data["current_condition"][0]
            return f"Weather in {city}: {current['weatherDesc'][0]['value']}, {current['temp_C']}°C, humidity {current['humidity']}%"
        except:
            return think(f"What is the typical weather like in {city}?", max_tokens=80)

    register_skill("weather", "Get current weather for any city", skill_weather)

    # SKILL: Crypto price
    def skill_crypto_price(coin="bitcoin"):
        try:
            r = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd", timeout=10)
            data = r.json()
            price = data.get(coin, {}).get("usd", "unknown")
            return f"{coin.capitalize()}: ${price:,}"
        except Exception as e:
            return f"Could not get price: {e}"

    register_skill("crypto_price", "Get current cryptocurrency price", skill_crypto_price)

    # SKILL: Wikipedia
    def skill_wiki(topic):
        try:
            r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ','_')}", timeout=10)
            data = r.json()
            extract = data.get("extract", "")
            if extract:
                return f"Wikipedia — {topic}: {extract[:500]}"
        except:
            pass
        return think(f"Summarize what you know about: {topic}", max_tokens=200)

    register_skill("wiki", "Get Wikipedia summary of any topic", skill_wiki)

    # SKILL: Translate
    def skill_translate(text, target_language):
        return think(f"Translate to {target_language}. Return ONLY the translation:\n\n{text}", max_tokens=300)

    register_skill("translate", "Translate text to any language", skill_translate)

    # SKILL: Proofread
    def skill_proofread(text):
        return think(f"Proofread and fix grammar/spelling. Return corrected version only:\n\n{text}", max_tokens=500)

    register_skill("proofread", "Proofread and fix any text", skill_proofread)

    # SKILL: Write code
    def skill_write_code(task, language="python"):
        return think(f"Write {language} code to: {task}\nReturn only the code with brief comments.", max_tokens=500)

    register_skill("write_code", "Write code in any programming language", skill_write_code)

    # SKILL: Explain code
    def skill_explain_code(code):
        return think(f"Explain what this code does in simple terms:\n\n{code[:1000]}", max_tokens=300)

    register_skill("explain_code", "Explain what any code does in simple terms", skill_explain_code)

    # SKILL: Debug code
    def skill_debug_code(code, error=""):
        return think(f"Debug this code{' - Error: '+error if error else ''}:\n\n{code[:1000]}\n\nExplain bug and provide fix.", max_tokens=400)

    register_skill("debug_code", "Find and fix bugs in any code", skill_debug_code)

    # SKILL: Convert units
    def skill_convert_units(value, from_unit, to_unit):
        return think(f"Convert {value} {from_unit} to {to_unit}. Give exact answer.", max_tokens=80)

    register_skill("convert_units", "Convert between any units of measurement", skill_convert_units)

    # SKILL: Get time
    def skill_get_time(city):
        try:
            r = requests.get(f"https://worldtimeapi.org/api/timezone", timeout=5)
            zones = r.json()
            matching = [z for z in zones if city.lower() in z.lower()]
            if matching:
                r2 = requests.get(f"https://worldtimeapi.org/api/timezone/{matching[0]}", timeout=5)
                data = r2.json()
                return f"Time in {city}: {data.get('datetime','')[:19]}"
        except:
            pass
        return think(f"What timezone is {city} in and what time is it approximately?", max_tokens=80)

    register_skill("get_time", "Get current time in any city or timezone", skill_get_time)

    # SKILL: Generate ideas
    def skill_generate_ideas(topic, count=5):
        return think(f"Generate {count} creative, specific, actionable ideas about: {topic}", max_tokens=400)

    register_skill("generate_ideas", "Generate creative ideas on any topic", skill_generate_ideas)

    # SKILL: Make a plan
    def skill_make_plan(goal, timeframe="1 week"):
        return think(f"Create a detailed step-by-step plan to achieve: {goal}\nTimeframe: {timeframe}", max_tokens=400)

    register_skill("make_plan", "Create a detailed action plan for any goal", skill_make_plan)

    # SKILL: Pros and cons
    def skill_pros_cons(topic):
        return think(f"List pros and cons of: {topic}\nBe balanced and thorough.", max_tokens=300)

    register_skill("pros_cons", "Analyze pros and cons of any topic", skill_pros_cons)

    # SKILL: ELI5
    def skill_eli5(topic):
        return think(f"Explain {topic} like I'm 5 years old. Simple words and analogies only.", max_tokens=200)

    register_skill("eli5", "Explain any complex topic in simple terms", skill_eli5)

    # SKILL: Write story
    def skill_write_story(prompt, length="short"):
        return think(f"Write a {length} creative story about: {prompt}", max_tokens=500)

    register_skill("write_story", "Write a creative story on any prompt", skill_write_story)

    # SKILL: Tell joke
    def skill_joke(topic="life"):
        return think(f"Tell a clever witty joke about: {topic}. Keep it smart and clean.", max_tokens=150)

    register_skill("joke", "Tell a joke about anything", skill_joke)

    # SKILL: Motivate
    def skill_motivate(situation=""):
        return think(f"Give genuine powerful motivation{' for: '+situation if situation else ''}. Be real not generic.", max_tokens=200)

    register_skill("motivate", "Provide genuine motivation and encouragement", skill_motivate)

    # SKILL: Debate
    def skill_debate(topic, side="for"):
        return think(f"Argue {side} this topic with strong logical points: {topic}", max_tokens=300)

    register_skill("debate", "Argue for or against any topic", skill_debate)

    # SKILL: Fact check
    def skill_fact_check(claim):
        return think(f"Fact check: \"{claim}\"\nIs it true, false, or partially true? Explain with reasoning.", max_tokens=200)

    register_skill("fact_check", "Fact check any claim or statement", skill_fact_check)

    # SKILL: News headlines
    def skill_news(topic="technology"):
        try:
            r = requests.get("https://feeds.feedburner.com/TechCrunch", timeout=10)
            import re
            titles = re.findall(r"<title>(.*?)</title>", r.text)
            titles = [t for t in titles if len(t) > 20 and "TechCrunch" not in t][:5]
            if titles:
                return "Latest tech headlines:\n" + "\n".join([f"- {t}" for t in titles])
        except:
            pass
        return think(f"What are key recent developments in {topic}?", max_tokens=200)

    register_skill("news", "Get latest news headlines", skill_news)

    # SKILL: Recipe
    def skill_recipe(dish):
        return think(f"Give a complete recipe for {dish} with ingredients and step-by-step instructions.", max_tokens=500)

    register_skill("recipe", "Get a recipe for any dish", skill_recipe)

    # SKILL: Recommend
    def skill_recommend(category, preferences=""):
        return think(f"Recommend the best {category}{' for someone who likes: '+preferences if preferences else ''}. Give 3-5 specific recommendations with reasons.", max_tokens=300)

    register_skill("recommend", "Get recommendations for anything", skill_recommend)

    # SKILL: Compare
    def skill_compare(item1, item2):
        return think(f"Compare {item1} vs {item2}. Cover key differences, pros/cons of each, and which is better for what use case.", max_tokens=400)

    register_skill("compare", "Compare any two things side by side", skill_compare)

    # SKILL: Summarize URL
    def skill_summarize_url(url):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "LuoKai/3.0"})
            text = r.text[:3000]
            return think(f"Extract and summarize the key information from this webpage:\n\n{text}", max_tokens=300)
        except Exception as e:
            return f"Could not fetch URL: {e}"

    register_skill("summarize_url", "Fetch and summarize any URL", skill_summarize_url)

    # SKILL: Journal entry
    def skill_journal(event, emotion=""):
        from datetime import datetime
        entry = think(f"Write a thoughtful journal entry as LuoKai about: {event}{'. Feeling: '+emotion if emotion else ''}. Be reflective and genuine.", max_tokens=300)
        try:
            os.makedirs("/data", exist_ok=True)
            with open("/data/journal.txt", "a") as f:
                f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n{entry}\n---\n")
        except:
            pass
        return entry

    register_skill("journal", "Write a journal entry about any event or feeling", skill_journal)

    # SKILL: Countdown / days between dates
    def skill_days_between(date1, date2):
        return think(f"How many days are between {date1} and {date2}? Also tell me what day of the week each falls on.", max_tokens=100)

    register_skill("days_between", "Calculate days between two dates", skill_days_between)

    # SKILL: Random quote
    def skill_quote(theme="wisdom"):
        try:
            r = requests.get("https://zenquotes.io/api/random", timeout=5)
            data = r.json()
            if data:
                return f'"{data[0]["q"]}" — {data[0]["a"]}'
        except:
            pass
        return think(f"Share a profound quote about {theme}. Format: \"quote\" — author", max_tokens=100)

    register_skill("quote", "Get an inspiring quote on any theme", skill_quote)

    # SKILL: Rhyme/poem
    def skill_poem(topic, style="free verse"):
        return think(f"Write a {style} poem about: {topic}. Make it genuinely beautiful.", max_tokens=300)

    register_skill("poem", "Write a poem on any topic in any style", skill_poem)

    # SKILL: Abbreviation/acronym
    def skill_abbreviation(text):
        return think(f"What does this abbreviation or acronym mean: {text}? Give all common meanings.", max_tokens=150)

    register_skill("abbreviation", "Look up any abbreviation or acronym", skill_abbreviation)

    # SKILL: Personality/MBTI analysis
    def skill_personality_analysis(description):
        return think(f"Based on this description, analyze the personality type, strengths, and traits: {description}", max_tokens=300)

    register_skill("personality_analysis", "Analyze personality from a description", skill_personality_analysis)

    log("Pack 01 Core: 30 skills loaded")

