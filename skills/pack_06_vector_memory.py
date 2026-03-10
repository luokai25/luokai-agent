# SKILL PACK 06 - Vector Memory (Semantic Search)

def load(register_skill, think, requests, os, log):
    import json, numpy as np

    VECTOR_FILE = "/data/vectors.json"

    def cosine_similarity(a, b):
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    def get_embedding(text):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/embeddings",
                headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY','')}",
                         "Content-Type": "application/json"},
                json={"model": "nomic-embed-text-v1.5", "input": text[:512]},
                timeout=10
            )
            data = r.json()
            if "data" in data:
                return data["data"][0]["embedding"]
        except:
            pass
        # Fallback: simple hash-based pseudo embedding
        words = text.lower().split()
        vec = [0.0] * 128
        for i, w in enumerate(words[:128]):
            vec[hash(w) % 128] += 1.0
        norm = sum(x*x for x in vec) ** 0.5
        return [x/(norm+1e-10) for x in vec]

    def load_vectors():
        try:
            with open(VECTOR_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_vectors(vecs):
        os.makedirs("/data", exist_ok=True)
        with open(VECTOR_FILE, "w") as f:
            json.dump(vecs, f)

    def skill_vector_remember(text, category="general"):
        vecs = load_vectors()
        embedding = get_embedding(text)
        vecs.append({
            "text": text,
            "category": category,
            "embedding": embedding,
            "time": str(__import__('datetime').datetime.now())
        })
        if len(vecs) > 1000:
            vecs = vecs[-1000:]
        save_vectors(vecs)
        return f"Stored in vector memory: {text[:80]}"

    register_skill("vector_remember", "Store information with semantic search capability", skill_vector_remember)

    def skill_vector_search(query, top_k=5):
        vecs = load_vectors()
        if not vecs:
            return "No vector memories yet"
        query_emb = get_embedding(query)
        scored = [(cosine_similarity(query_emb, v["embedding"]), v["text"]) for v in vecs]
        scored.sort(reverse=True)
        top = scored[:top_k]
        if top and top[0][0] > 0.3:
            results = "\n".join([f"- [{score:.2f}] {text}" for score, text in top])
            return f"Semantically relevant memories for '{query}':\n{results}"
        return f"No closely related memories found for '{query}'"

    register_skill("vector_search", "Search memory semantically - finds related concepts", skill_vector_search)

    def skill_vector_stats():
        vecs = load_vectors()
        categories = {}
        for v in vecs:
            cat = v.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        return f"Vector memory: {len(vecs)} entries\nCategories: {categories}"

    register_skill("vector_stats", "Get statistics about vector memory", skill_vector_stats)

    log("Pack 06 Vector Memory: 3 skills loaded")
