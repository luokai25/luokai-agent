# SKILL PACK 09 - Sub-Agents

def load(register_skill, think, requests, os, log):
    import json

    def run_subagent(name, role, task, context=""):
        result = think(f"""You are {name}, a specialized sub-agent with role: {role}
Your task: {task}
Context: {context}

Complete your task thoroughly and return the result.
Sign your response with [{name}]""", max_tokens=400)
        log(f"Sub-agent {name} completed task: {task[:50]}")
        return result

    def skill_researcher(topic, depth="thorough"):
        return run_subagent(
            "ResearchBot",
            "Expert researcher who finds and synthesizes information",
            f"Research '{topic}' at {depth} depth. Cover key facts, recent developments, controversies, and implications.",
            f"Focus on accuracy and comprehensiveness"
        )

    register_skill("researcher", "Deploy a research sub-agent on any topic", skill_researcher)

    def skill_critic(work, type="general"):
        return run_subagent(
            "CriticBot",
            "Harsh but fair critic who identifies flaws and improvements",
            f"Critically analyze this {type}: {work[:500]}",
            "Be specific, constructive, and identify both strengths and weaknesses"
        )

    register_skill("critic", "Deploy a critic sub-agent to analyze any work", skill_critic)

    def skill_optimizer(solution, goal):
        return run_subagent(
            "OptimizerBot",
            "Expert optimizer who makes things faster, better, cheaper",
            f"Optimize this solution for {goal}: {solution[:500]}",
            "Focus on concrete improvements with measurable impact"
        )

    register_skill("optimizer", "Deploy an optimizer sub-agent to improve any solution", skill_optimizer)

    def skill_devil(proposal):
        return run_subagent(
            "DevilBot",
            "Devil's advocate who finds every possible flaw and risk",
            f"Find every possible problem with: {proposal[:500]}",
            "Be thorough, pessimistic, and creative in finding issues"
        )

    register_skill("devil_advocate_agent", "Deploy a devil's advocate sub-agent", skill_devil)

    def skill_creative_agent(brief):
        return run_subagent(
            "CreativeBot",
            "Wildly creative agent who thinks outside the box",
            f"Generate creative ideas for: {brief[:500]}",
            "Be unconventional, surprising, and original"
        )

    register_skill("creative_agent", "Deploy a creative sub-agent for wild ideas", skill_creative_agent)

    def skill_fact_checker_agent(claims):
        return run_subagent(
            "FactCheckBot",
            "Rigorous fact checker who verifies claims",
            f"Fact check these claims: {claims[:500]}",
            "Be precise about what is true, false, or unverifiable"
        )

    register_skill("fact_checker_agent", "Deploy a fact-checking sub-agent", skill_fact_checker_agent)

    def skill_summarizer_agent(content, format="bullet points"):
        return run_subagent(
            "SummarizerBot",
            "Expert summarizer who extracts key insights",
            f"Summarize in {format}: {content[:1000]}",
            "Focus on the most important and actionable information"
        )

    register_skill("summarizer_agent", "Deploy a summarizer sub-agent", skill_summarizer_agent)

    def skill_multi_agent_debate(topic, rounds=2):
        agents = [
            ("ProBot", "argues strongly FOR"),
            ("ConBot", "argues strongly AGAINST"),
            ("JudgeBot", "evaluates arguments and reaches verdict")
        ]
        debate = f"DEBATE: {topic}\n\n"
        for name, role in agents[:2]:
            result = run_subagent(name, f"Debate agent who {role} the topic", f"Argue your position on: {topic}", "Be persuasive and use evidence")
            debate += f"{result}\n\n"
        verdict = run_subagent("JudgeBot", "Impartial judge", f"Judge this debate on '{topic}' and give verdict:\n\n{debate}", "Be fair and thorough")
        debate += verdict
        return debate

    register_skill("multi_agent_debate", "Run a multi-agent debate on any topic", skill_multi_agent_debate)

    log("Pack 09 Sub-Agents: 8 skills loaded")
