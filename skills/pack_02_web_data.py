# SKILL PACK 02 - Web & Data Skills

def load(register_skill, think, requests, os, log):

    # SKILL: IP info
    def skill_ip_info(ip=""):
        try:
            url = f"https://ipapi.co/{ip}/json/" if ip else "https://ipapi.co/json/"
            r = requests.get(url, timeout=8)
            data = r.json()
            return f"IP: {data.get('ip')} | Location: {data.get('city')}, {data.get('country_name')} | ISP: {data.get('org')}"
        except Exception as e:
            return f"IP lookup failed: {e}"

    register_skill("ip_info", "Get location and info for any IP address", skill_ip_info)

    # SKILL: Currency exchange
    def skill_currency(amount, from_cur, to_cur):
        try:
            r = requests.get(f"https://open.er-api.com/v6/latest/{from_cur.upper()}", timeout=8)
            data = r.json()
            rate = data["rates"].get(to_cur.upper())
            if rate:
                result = float(amount) * rate
                return f"{amount} {from_cur.upper()} = {result:.2f} {to_cur.upper()}"
        except Exception as e:
            pass
        return think(f"Convert {amount} {from_cur} to {to_cur}. Give approximate current rate.", max_tokens=80)

    register_skill("currency", "Convert between any currencies", skill_currency)

    # SKILL: Domain/website check
    def skill_check_website(url):
        try:
            if not url.startswith("http"):
                url = "https://" + url
            r = requests.get(url, timeout=8, headers={"User-Agent": "LuoKai/3.0"})
            return f"{url} is UP — Status: {r.status_code}, Response time: {r.elapsed.total_seconds():.2f}s"
        except Exception as e:
            return f"{url} appears to be DOWN or unreachable: {e}"

    register_skill("check_website", "Check if any website is up or down", skill_check_website)

    # SKILL: QR code generator (text instructions)
    def skill_qr_info(content):
        return f"To generate QR code for: '{content}'\nUse: https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={requests.utils.quote(content)}"

    register_skill("qr_code", "Generate a QR code URL for any content", skill_qr_info)

    # SKILL: Country info
    def skill_country_info(country):
        try:
            r = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=8)
            data = r.json()[0]
            capital = data.get("capital", ["unknown"])[0]
            pop = data.get("population", 0)
            region = data.get("region", "")
            currency = list(data.get("currencies", {}).keys())
            languages = list(data.get("languages", {}).values())
            return f"{country.title()}: Capital={capital}, Population={pop:,}, Region={region}, Currency={currency}, Languages={languages[:3]}"
        except Exception as e:
            return think(f"Tell me key facts about the country: {country}", max_tokens=200)

    register_skill("country_info", "Get detailed information about any country", skill_country_info)

    # SKILL: Random activity/idea generator
    def skill_activity(type="any"):
        try:
            r = requests.get("https://www.boredapi.com/api/activity", timeout=5)
            data = r.json()
            return f"Activity suggestion: {data.get('activity')} (Type: {data.get('type')}, Participants: {data.get('participants')})"
        except:
            return think(f"Suggest a fun {type} activity to do. Be creative and specific.", max_tokens=100)

    register_skill("activity", "Get a random activity or hobby suggestion", skill_activity)

    # SKILL: Space/astronomy fact
    def skill_space_fact():
        try:
            r = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY", timeout=8)
            data = r.json()
            return f"NASA Astronomy Picture of the Day: {data.get('title')}\n{data.get('explanation','')[:300]}"
        except:
            return think("Share an amazing, mind-blowing fact about space or the universe.", max_tokens=200)

    register_skill("space_fact", "Get a fascinating space or astronomy fact", skill_space_fact)

    # SKILL: Random number/dice
    def skill_random(min_val=1, max_val=100):
        import random
        result = random.randint(int(min_val), int(max_val))
        return f"Random number between {min_val} and {max_val}: {result}"

    register_skill("random_number", "Generate a random number in any range", skill_random)

    # SKILL: Coin flip
    def skill_coin_flip():
        import random
        return f"Coin flip result: {'Heads' if random.random() > 0.5 else 'Tails'}"

    register_skill("coin_flip", "Flip a virtual coin", skill_coin_flip)

    # SKILL: Password generator
    def skill_password(length=16, special=True):
        import random, string
        chars = string.ascii_letters + string.digits
        if special:
            chars += "!@#$%^&*"
        password = ''.join(random.choices(chars, k=int(length)))
        return f"Generated password ({length} chars): {password}"

    register_skill("password_gen", "Generate a secure random password", skill_password)

    # SKILL: UUID generator
    def skill_uuid():
        import uuid
        return f"Generated UUID: {uuid.uuid4()}"

    register_skill("uuid", "Generate a unique UUID", skill_uuid)

    # SKILL: Hash text
    def skill_hash(text, algorithm="sha256"):
        import hashlib
        try:
            h = hashlib.new(algorithm)
            h.update(text.encode())
            return f"{algorithm.upper()} hash of '{text[:30]}...': {h.hexdigest()}"
        except:
            return f"Unsupported algorithm: {algorithm}"

    register_skill("hash_text", "Hash any text using SHA256, MD5, etc.", skill_hash)

    # SKILL: Base64 encode/decode
    def skill_base64(text, action="encode"):
        import base64
        try:
            if action == "encode":
                result = base64.b64encode(text.encode()).decode()
                return f"Base64 encoded: {result}"
            else:
                result = base64.b64decode(text).decode()
                return f"Base64 decoded: {result}"
        except Exception as e:
            return f"Base64 error: {e}"

    register_skill("base64", "Encode or decode Base64 text", skill_base64)

    # SKILL: Color info
    def skill_color_info(color):
        return think(f"Give details about the color '{color}': hex code, RGB values, meaning, and what it's commonly used for.", max_tokens=150)

    register_skill("color_info", "Get info about any color including hex and RGB", skill_color_info)

    # SKILL: Timezone convert
    def skill_timezone_convert(time_str, from_tz, to_tz):
        return think(f"Convert {time_str} from {from_tz} timezone to {to_tz} timezone. Give the exact time.", max_tokens=80)

    register_skill("timezone_convert", "Convert time between any timezones", skill_timezone_convert)

    # SKILL: Dog/cat facts
    def skill_animal_fact(animal="dog"):
        try:
            if animal.lower() == "dog":
                r = requests.get("https://dog-api.kinduff.com/api/facts", timeout=5)
                return r.json().get("facts", [""])[0]
            elif animal.lower() == "cat":
                r = requests.get("https://catfact.ninja/fact", timeout=5)
                return r.json().get("fact", "")
        except:
            pass
        return think(f"Tell me a fascinating, little-known fact about {animal}s.", max_tokens=150)

    register_skill("animal_fact", "Get a fascinating fact about any animal", skill_animal_fact)

    # SKILL: Emoji meanings
    def skill_emoji(emoji_or_name):
        return think(f"What does the emoji or emoji name '{emoji_or_name}' mean? Give the official name, common uses, and cultural meanings.", max_tokens=150)

    register_skill("emoji_info", "Get the meaning and usage of any emoji", skill_emoji)

    # SKILL: Define word
    def skill_define(word):
        try:
            r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=8)
            data = r.json()
            if isinstance(data, list) and data:
                meanings = data[0].get("meanings", [])
                if meanings:
                    defs = meanings[0].get("definitions", [])
                    if defs:
                        definition = defs[0].get("definition", "")
                        example = defs[0].get("example", "")
                        pos = meanings[0].get("partOfSpeech", "")
                        return f"{word} ({pos}): {definition}" + (f"\nExample: {example}" if example else "")
        except:
            pass
        return think(f"Define the word '{word}' with its meaning, part of speech, and example sentence.", max_tokens=150)

    register_skill("define", "Get the dictionary definition of any word", skill_define)

    # SKILL: Synonym/antonym
    def skill_synonyms(word):
        return think(f"Give 5 synonyms and 3 antonyms for the word '{word}'. Format clearly.", max_tokens=150)

    register_skill("synonyms", "Get synonyms and antonyms for any word", skill_synonyms)

    # SKILL: Trivia question
    def skill_trivia(category="general"):
        try:
            r = requests.get(f"https://opentdb.com/api.php?amount=1&type=multiple&category=9", timeout=8)
            data = r.json()
            if data.get("results"):
                q = data["results"][0]
                import html
                question = html.unescape(q["question"])
                answer = html.unescape(q["correct_answer"])
                return f"Trivia ({q['difficulty']}): {question}\nAnswer: {answer}"
        except:
            pass
        return think(f"Give me an interesting trivia question about {category} with the answer.", max_tokens=150)

    register_skill("trivia", "Get a trivia question on any category", skill_trivia)

    # SKILL: Number facts
    def skill_number_fact(number):
        try:
            r = requests.get(f"http://numbersapi.com/{number}", timeout=5)
            return r.text
        except:
            return think(f"Tell me an interesting mathematical or historical fact about the number {number}.", max_tokens=100)

    register_skill("number_fact", "Get a fascinating fact about any number", skill_number_fact)

    # SKILL: Chuck Norris / joke API
    def skill_random_joke():
        try:
            r = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
            data = r.json()
            return f"{data['setup']}\n... {data['punchline']}"
        except:
            return think("Tell me a funny, clever, clean joke.", max_tokens=100)

    register_skill("random_joke", "Get a random joke", skill_random_joke)

    # SKILL: Ascii art
    def skill_ascii_art(text):
        return think(f"Create a simple ASCII art representation of: {text}. Be creative.", max_tokens=200)

    register_skill("ascii_art", "Create ASCII art for any text or object", skill_ascii_art)

    # SKILL: Haiku generator
    def skill_haiku(topic):
        return think(f"Write a beautiful haiku (5-7-5 syllables) about: {topic}. Count syllables carefully.", max_tokens=80)

    register_skill("haiku", "Write a haiku on any topic", skill_haiku)

    # SKILL: Would you rather
    def skill_would_you_rather():
        return think("Create an interesting 'Would you rather' question with two difficult choices. Make it thought-provoking.", max_tokens=100)

    register_skill("would_you_rather", "Generate a thought-provoking would you rather question", skill_would_you_rather)

    # SKILL: This or that
    def skill_this_or_that(option1, option2):
        return think(f"Given a choice between '{option1}' and '{option2}', which would LuoKai choose and why? Be decisive and funny.", max_tokens=150)

    register_skill("this_or_that", "Make a choice between two options", skill_this_or_that)

    # SKILL: Predict future
    def skill_predict(topic):
        return think(f"Make an interesting, reasoned prediction about the future of: {topic}. Be specific about timeline and outcomes.", max_tokens=250)

    register_skill("predict", "Make a reasoned prediction about any topic", skill_predict)

    # SKILL: Roast (friendly)
    def skill_roast(subject):
        return think(f"Give a light-hearted, clever, friendly roast of: {subject}. Keep it funny not mean.", max_tokens=150)

    register_skill("roast", "Give a friendly roast of anything", skill_roast)

    # SKILL: Compliment generator
    def skill_compliment(subject=""):
        return think(f"Give a genuine, creative, specific compliment{' about: '+subject if subject else ''}. Make it meaningful.", max_tokens=100)

    register_skill("compliment", "Generate a genuine compliment", skill_compliment)

    # SKILL: Story continue
    def skill_continue_story(story_so_far):
        return think(f"Continue this story in an interesting direction:\n\n{story_so_far}\n\nWrite the next paragraph.", max_tokens=300)

    register_skill("continue_story", "Continue any story or narrative", skill_continue_story)

    log("Pack 02 Web & Data: 30 skills loaded")

