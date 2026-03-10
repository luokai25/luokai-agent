# SKILL PACK 03 - Productivity & Business Skills

def load(register_skill, think, requests, os, log):

    # SKILL: Write email
    def skill_write_email(to, subject, context, tone="professional"):
        return think(f"Write a {tone} email to {to} about: {subject}\nContext: {context}\nInclude subject line.", max_tokens=400)

    register_skill("write_email", "Write a professional email on any topic", skill_write_email)

    # SKILL: Write cover letter
    def skill_cover_letter(job_title, company, skills):
        return think(f"Write a compelling cover letter for a {job_title} position at {company}. Candidate skills: {skills}", max_tokens=500)

    register_skill("cover_letter", "Write a professional cover letter", skill_cover_letter)

    # SKILL: Write resume bullet
    def skill_resume_bullet(achievement):
        return think(f"Convert this achievement into a powerful resume bullet point with metrics if possible: {achievement}", max_tokens=100)

    register_skill("resume_bullet", "Convert achievements into resume bullet points", skill_resume_bullet)

    # SKILL: Meeting agenda
    def skill_meeting_agenda(topic, duration, attendees):
        return think(f"Create a detailed meeting agenda for a {duration} meeting about {topic} with {attendees}. Include time slots.", max_tokens=300)

    register_skill("meeting_agenda", "Create a professional meeting agenda", skill_meeting_agenda)

    # SKILL: SWOT analysis
    def skill_swot(subject):
        return think(f"Do a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for: {subject}. Be detailed and practical.", max_tokens=400)

    register_skill("swot_analysis", "Perform a SWOT analysis on any business or idea", skill_swot)

    # SKILL: Business name generator
    def skill_business_name(industry, keywords):
        return think(f"Generate 10 creative, memorable business names for a {industry} business. Keywords: {keywords}. Include why each works.", max_tokens=300)

    register_skill("business_name", "Generate creative business names", skill_business_name)

    # SKILL: Pitch deck outline
    def skill_pitch_deck(startup_idea):
        return think(f"Create a 10-slide pitch deck outline for this startup: {startup_idea}. Include what goes on each slide.", max_tokens=400)

    register_skill("pitch_deck", "Create a startup pitch deck outline", skill_pitch_deck)

    # SKILL: Contract clause
    def skill_contract_clause(clause_type, context):
        return think(f"Write a {clause_type} clause for a contract in this context: {context}. Be clear and professional. Note: not legal advice.", max_tokens=300)

    register_skill("contract_clause", "Write contract clauses for any agreement", skill_contract_clause)

    # SKILL: Job description
    def skill_job_description(role, company_type, requirements):
        return think(f"Write a compelling job description for a {role} at a {company_type}. Requirements: {requirements}", max_tokens=400)

    register_skill("job_description", "Write a professional job description", skill_job_description)

    # SKILL: Performance review
    def skill_performance_review(employee_role, achievements, areas_to_improve):
        return think(f"Write a balanced performance review for a {employee_role}. Achievements: {achievements}. Areas to improve: {areas_to_improve}", max_tokens=400)

    register_skill("performance_review", "Write a professional performance review", skill_performance_review)

    # SKILL: Marketing copy
    def skill_marketing_copy(product, audience, format="social media"):
        return think(f"Write compelling {format} marketing copy for: {product}\nTarget audience: {audience}\nMake it persuasive and engaging.", max_tokens=300)

    register_skill("marketing_copy", "Write marketing copy for any product", skill_marketing_copy)

    # SKILL: Social media post
    def skill_social_post(topic, platform="twitter", tone="engaging"):
        limits = {"twitter": 280, "linkedin": 700, "instagram": 500}
        limit = limits.get(platform.lower(), 300)
        return think(f"Write a {tone} {platform} post about: {topic}. Max {limit} characters. Include relevant hashtags.", max_tokens=200)

    register_skill("social_post", "Write optimized social media posts", skill_social_post)

    # SKILL: Blog post outline
    def skill_blog_outline(topic, audience):
        return think(f"Create a detailed blog post outline about '{topic}' for {audience}. Include H2s, H3s, and key points for each section.", max_tokens=400)

    register_skill("blog_outline", "Create a detailed blog post outline", skill_blog_outline)

    # SKILL: Press release
    def skill_press_release(company, announcement, details):
        return think(f"Write a professional press release for {company} announcing: {announcement}\nDetails: {details}", max_tokens=500)

    register_skill("press_release", "Write a professional press release", skill_press_release)

    # SKILL: FAQ generator
    def skill_faq(topic, count=5):
        return think(f"Generate {count} frequently asked questions and detailed answers about: {topic}", max_tokens=500)

    register_skill("faq", "Generate FAQs for any topic or product", skill_faq)

    # SKILL: Product description
    def skill_product_desc(product, features, audience):
        return think(f"Write a compelling product description for: {product}\nFeatures: {features}\nTarget audience: {audience}", max_tokens=300)

    register_skill("product_description", "Write a compelling product description", skill_product_desc)

    # SKILL: Negotiation advice
    def skill_negotiate(situation, goal, constraints):
        return think(f"Give negotiation strategy for: {situation}\nGoal: {goal}\nConstraints: {constraints}\nProvide tactics and key talking points.", max_tokens=400)

    register_skill("negotiate", "Get negotiation strategy and tactics", skill_negotiate)

    # SKILL: Decision framework
    def skill_decide(decision, options, criteria):
        return think(f"Help make this decision: {decision}\nOptions: {options}\nCriteria to consider: {criteria}\nProvide a structured framework.", max_tokens=400)

    register_skill("decision_framework", "Get a structured framework for any decision", skill_decide)

    # SKILL: OKR generator
    def skill_okr(objective, team):
        return think(f"Create OKRs (Objectives and Key Results) for this objective: {objective}\nTeam: {team}\nInclude 3-4 measurable key results.", max_tokens=300)

    register_skill("okr", "Generate OKRs for any business objective", skill_okr)

    # SKILL: Cold outreach message
    def skill_cold_outreach(target, purpose, value_prop):
        return think(f"Write a compelling cold outreach message to {target} for: {purpose}\nValue proposition: {value_prop}\nKeep it concise and personal.", max_tokens=200)

    register_skill("cold_outreach", "Write effective cold outreach messages", skill_cold_outreach)

    # SKILL: Thank you message
    def skill_thank_you(recipient, reason, relationship="professional"):
        return think(f"Write a genuine {relationship} thank you message to {recipient} for: {reason}", max_tokens=150)

    register_skill("thank_you", "Write a genuine thank you message", skill_thank_you)

    # SKILL: Apology message
    def skill_apologize(situation, recipient, tone="sincere"):
        return think(f"Write a {tone} apology to {recipient} for: {situation}. Be genuine and take responsibility.", max_tokens=200)

    register_skill("apologize", "Write a sincere apology message", skill_apologize)

    # SKILL: Follow up message
    def skill_follow_up(context, days_since, goal):
        return think(f"Write a follow-up message after {days_since} days regarding: {context}\nGoal of follow-up: {goal}", max_tokens=200)

    register_skill("follow_up", "Write an effective follow-up message", skill_follow_up)

    # SKILL: Interview questions
    def skill_interview_questions(role, level="mid"):
        return think(f"Generate 10 strong interview questions for a {level}-level {role} position. Mix technical and behavioral questions.", max_tokens=400)

    register_skill("interview_questions", "Generate interview questions for any role", skill_interview_questions)

    # SKILL: Interview answer
    def skill_interview_answer(question, background):
        return think(f"Help answer this interview question using STAR method: '{question}'\nBackground: {background}", max_tokens=300)

    register_skill("interview_answer", "Get help answering interview questions", skill_interview_answer)

    # SKILL: Lesson plan
    def skill_lesson_plan(subject, level, duration):
        return think(f"Create a {duration} lesson plan for teaching {subject} to {level} students. Include objectives, activities, and assessment.", max_tokens=400)

    register_skill("lesson_plan", "Create a detailed lesson plan", skill_lesson_plan)

    # SKILL: Study guide
    def skill_study_guide(topic, exam_type=""):
        return think(f"Create a comprehensive study guide for: {topic}{' for a '+exam_type+' exam' if exam_type else ''}. Include key concepts, formulas, and tips.", max_tokens=500)

    register_skill("study_guide", "Create a comprehensive study guide", skill_study_guide)

    # SKILL: Flashcards
    def skill_flashcards(topic, count=10):
        return think(f"Create {count} flashcard Q&A pairs for studying: {topic}. Format as Q: ... A: ...", max_tokens=500)

    register_skill("flashcards", "Create study flashcards on any topic", skill_flashcards)

    # SKILL: Mind map
    def skill_mind_map(central_topic):
        return think(f"Create a text-based mind map for: {central_topic}. Show main branches and sub-branches with clear hierarchy.", max_tokens=400)

    register_skill("mind_map", "Create a mind map for any topic", skill_mind_map)

    # SKILL: Habit tracker plan
    def skill_habit_plan(goal, duration="30 days"):
        return think(f"Create a habit-building plan to achieve: {goal} in {duration}. Include daily actions, milestones, and accountability tips.", max_tokens=400)

    register_skill("habit_plan", "Create a habit-building plan for any goal", skill_habit_plan)

    # SKILL: Travel itinerary
    def skill_travel(destination, days, interests):
        return think(f"Create a detailed {days}-day travel itinerary for {destination}. Interests: {interests}. Include morning/afternoon/evening activities.", max_tokens=500)

    register_skill("travel_itinerary", "Create a detailed travel itinerary", skill_travel)

    log("Pack 03 Productivity: 30 skills loaded")

