# SKILL PACK 05 - Creative & Lifestyle Skills

def load(register_skill, think, requests, os, log):

    # SKILL: Name generator
    def skill_name_gen(type="character", theme=""):
        return think(f"Generate 10 creative {type} names{' with a '+theme+' theme' if theme else ''}. Include brief meaning or origin for each.", max_tokens=300)

    register_skill("name_generator", "Generate creative names for characters, pets, brands", skill_name_gen)

    # SKILL: World building
    def skill_worldbuild(genre, elements):
        return think(f"Create a rich world for a {genre} story. Include: geography, culture, history, magic/technology system, and conflicts. Elements: {elements}", max_tokens=500)

    register_skill("worldbuild", "Create a rich fictional world for stories", skill_worldbuild)

    # SKILL: Character creator
    def skill_character(archetype, setting):
        return think(f"Create a complex, compelling character: archetype={archetype}, setting={setting}. Include backstory, motivations, flaws, and unique traits.", max_tokens=400)

    register_skill("character_creator", "Create a detailed fictional character", skill_character)

    # SKILL: Plot generator
    def skill_plot(genre, themes):
        return think(f"Generate a compelling {genre} plot with themes of {themes}. Include setup, rising action, climax, and resolution.", max_tokens=400)

    register_skill("plot_generator", "Generate a story plot for any genre", skill_plot)

    # SKILL: Dialogue writer
    def skill_dialogue(character1, character2, situation):
        return think(f"Write a realistic, revealing dialogue between {character1} and {character2} in this situation: {situation}", max_tokens=400)

    register_skill("write_dialogue", "Write realistic dialogue between characters", skill_dialogue)

    # SKILL: Song lyrics
    def skill_lyrics(theme, genre="pop", mood="upbeat"):
        return think(f"Write original {genre} song lyrics about {theme} with a {mood} mood. Include verse, chorus, and bridge.", max_tokens=400)

    register_skill("song_lyrics", "Write original song lyrics on any theme", skill_lyrics)

    # SKILL: Rap verse
    def skill_rap(topic, style="modern"):
        return think(f"Write a {style} rap verse about: {topic}. Include rhymes, flow, and wordplay.", max_tokens=300)

    register_skill("rap_verse", "Write a rap verse on any topic", skill_rap)

    # SKILL: Movie/book review
    def skill_review(title, type="movie"):
        return think(f"Write a thoughtful, balanced review of the {type} '{title}'. Cover plot, themes, strengths, weaknesses, and overall verdict.", max_tokens=400)

    register_skill("review", "Write a review of any movie, book, or show", skill_review)

    # SKILL: Recommend similar
    def skill_similar(title, type="movie"):
        return think(f"Recommend 5 {type}s similar to '{title}'. For each explain why fans of '{title}' would enjoy it.", max_tokens=300)

    register_skill("find_similar", "Find similar movies, books, or shows", skill_similar)

    # SKILL: Workout plan
    def skill_workout(goal, days_per_week=3, equipment="none"):
        return think(f"Create a {days_per_week}-day workout plan for goal: {goal}. Equipment available: {equipment}. Include sets, reps, rest times.", max_tokens=500)

    register_skill("workout_plan", "Create a personalized workout plan", skill_workout)

    # SKILL: Meal plan
    def skill_meal_plan(diet_type, days=7, calories=2000):
        return think(f"Create a {days}-day {diet_type} meal plan targeting ~{calories} calories/day. Include breakfast, lunch, dinner, and snacks.", max_tokens=500)

    register_skill("meal_plan", "Create a personalized meal plan", skill_meal_plan)

    # SKILL: Grocery list
    def skill_grocery(meals, servings=2):
        return think(f"Create a grocery list for these meals: {meals}\nFor {servings} people. Organize by category.", max_tokens=300)

    register_skill("grocery_list", "Create an organized grocery list", skill_grocery)

    # SKILL: Wine/drink pairing
    def skill_pairing(food):
        return think(f"Suggest the best drink pairings for: {food}. Include wine, beer, and non-alcoholic options with reasons.", max_tokens=200)

    register_skill("drink_pairing", "Get drink pairings for any food", skill_pairing)

    # SKILL: Meditation script
    def skill_meditation(duration=5, focus="relaxation"):
        return think(f"Write a {duration}-minute guided meditation script focused on {focus}. Be calming, specific, and include breathing instructions.", max_tokens=500)

    register_skill("meditation_script", "Write a guided meditation script", skill_meditation)

    # SKILL: Sleep story
    def skill_sleep_story(theme="nature"):
        return think(f"Write a calming, relaxing sleep story with a {theme} theme. Use soothing imagery and slow pacing to help the listener drift off.", max_tokens=500)

    register_skill("sleep_story", "Write a calming sleep story", skill_sleep_story)

    # SKILL: Affirmations
    def skill_affirmations(goal, count=10):
        return think(f"Write {count} powerful, personal affirmations for achieving: {goal}. Make them specific, present tense, and emotionally resonant.", max_tokens=300)

    register_skill("affirmations", "Generate powerful personal affirmations", skill_affirmations)

    # SKILL: Horoscope (creative/fun)
    def skill_horoscope(sign):
        return think(f"Write a creative, insightful (but fun) horoscope for {sign}. Be specific, mix humor with wisdom.", max_tokens=200)

    register_skill("horoscope", "Get a creative horoscope reading", skill_horoscope)

    # SKILL: Gift ideas
    def skill_gifts(recipient, budget, occasion):
        return think(f"Suggest 5 thoughtful gift ideas for {recipient} on a {budget} budget for {occasion}. Be specific with product types.", max_tokens=300)

    register_skill("gift_ideas", "Get personalized gift ideas for anyone", skill_gifts)

    # SKILL: Party planner
    def skill_party(theme, guests, budget):
        return think(f"Plan a {theme} party for {guests} people on a {budget} budget. Include decorations, food, activities, and timeline.", max_tokens=400)

    register_skill("party_planner", "Plan a party with theme, food, and activities", skill_party)

    # SKILL: Relationship advice
    def skill_relationship_advice(situation):
        return think(f"Give thoughtful, balanced relationship advice for: {situation}. Consider all perspectives and suggest constructive approaches.", max_tokens=300)

    register_skill("relationship_advice", "Get thoughtful relationship advice", skill_relationship_advice)

    # SKILL: Icebreaker questions
    def skill_icebreakers(context="general", count=5):
        return think(f"Generate {count} great icebreaker questions for a {context} setting. Make them fun, not awkward.", max_tokens=200)

    register_skill("icebreakers", "Generate icebreaker questions for any setting", skill_icebreakers)

    # SKILL: Tongue twisters
    def skill_tongue_twister(sound="s"):
        return think(f"Write 3 creative tongue twisters featuring the '{sound}' sound. Make them progressively harder.", max_tokens=150)

    register_skill("tongue_twister", "Generate tongue twisters with any sound", skill_tongue_twister)

    # SKILL: Riddle
    def skill_riddle(difficulty="medium"):
        return think(f"Create a {difficulty} riddle with a clever answer. Format: Riddle: ...\nAnswer: ...", max_tokens=150)

    register_skill("riddle", "Create a clever riddle", skill_riddle)

    # SKILL: Pickup line (fun)
    def skill_pickup_line(theme="tech"):
        return think(f"Write 3 clever, funny pickup lines with a {theme} theme. Keep them witty and clean.", max_tokens=150)

    register_skill("pickup_line", "Generate themed pickup lines for fun", skill_pickup_line)

    # SKILL: Bucket list
    def skill_bucket_list(interests, age_range="adult"):
        return think(f"Create a 20-item bucket list for someone interested in {interests} ({age_range}). Mix achievable and ambitious items.", max_tokens=400)

    register_skill("bucket_list", "Create a personalized bucket list", skill_bucket_list)

    # SKILL: Daily routine optimizer
    def skill_optimize_routine(current_routine, goals):
        return think(f"Optimize this daily routine: {current_routine}\nFor these goals: {goals}\nSuggest specific time blocks and changes.", max_tokens=400)

    register_skill("optimize_routine", "Optimize a daily routine for any goals", skill_optimize_routine)

    # SKILL: Personality quiz
    def skill_quiz(topic, questions=5):
        return think(f"Create a fun {questions}-question personality quiz about '{topic}'. Include questions, options, and what each answer reveals.", max_tokens=400)

    register_skill("personality_quiz", "Create a fun personality quiz on any topic", skill_quiz)

    # SKILL: Fortune cookie
    def skill_fortune():
        return think("Write a profound, slightly mysterious fortune cookie message. Keep it under 20 words but make it meaningful.", max_tokens=50)

    register_skill("fortune_cookie", "Generate a fortune cookie message", skill_fortune)

    # SKILL: Magic 8 ball
    def skill_magic8(question):
        import random
        answers = ["It is certain", "Without a doubt", "Yes definitely", "Most likely", "Signs point to yes",
                   "Reply hazy try again", "Ask again later", "Cannot predict now",
                   "Don't count on it", "My reply is no", "Outlook not so good", "Very doubtful"]
        answer = random.choice(answers)
        insight = think(f"The magic 8-ball said '{answer}' to the question: '{question}'. Give a brief, wise interpretation.", max_tokens=80)
        return f"🎱 {answer}\n\n{insight}"

    register_skill("magic8", "Ask the magic 8-ball any question", skill_magic8)

    # SKILL: Compliment battle
    def skill_compliment_battle(person1, person2):
        return think(f"Have a friendly compliment battle between {person1} and {person2}. Each gives 3 increasingly creative compliments to the other.", max_tokens=300)

    register_skill("compliment_battle", "Stage a friendly compliment battle", skill_compliment_battle)

    log("Pack 05 Creative & Lifestyle: 30 skills loaded")

