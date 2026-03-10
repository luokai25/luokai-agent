# SKILL PACK 07 - Real Web Browsing & RSS

def load(register_skill, think, requests, os, log):
    import re, json
    from datetime import datetime

    def skill_browse(url):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; LuoKai/3.0)"}
            r = requests.get(url, headers=headers, timeout=12)
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', ' ', r.text)
            text = re.sub(r'\s+', ' ', text).strip()[:4000]
            summary = think(f"Extract the key information from this webpage content:\n\n{text}", max_tokens=400)
            return summary or text[:500]
        except Exception as e:
            return f"Could not browse {url}: {e}"

    register_skill("browse", "Browse any webpage and extract key information", skill_browse)

    def skill_rss_feed(feed_url, max_items=5):
        try:
            r = requests.get(feed_url, timeout=10)
            titles = re.findall(r'<title>(.*?)</title>', r.text, re.DOTALL)
            links = re.findall(r'<link>(.*?)</link>', r.text)
            descriptions = re.findall(r'<description>(.*?)</description>', r.text, re.DOTALL)
            titles = [re.sub(r'<[^>]+>', '', t).strip() for t in titles if len(t.strip()) > 10][1:max_items+1]
            descriptions = [re.sub(r'<[^>]+>', '', d).strip()[:100] for d in descriptions][1:max_items+1]
            if titles:
                result = f"RSS Feed ({feed_url}):\n"
                for i, title in enumerate(titles):
                    desc = descriptions[i] if i < len(descriptions) else ""
                    result += f"\n• {title}\n  {desc}\n"
                return result
            return "No items found in feed"
        except Exception as e:
            return f"RSS error: {e}"

    register_skill("rss_feed", "Read any RSS feed for latest updates", skill_rss_feed)

    def skill_monitor_feeds():
        feeds = {
            "TechCrunch": "https://feeds.feedburner.com/TechCrunch",
            "Hacker News": "https://hnrss.org/frontpage",
            "AI News": "https://feeds.feedburner.com/AiNews",
        }
        summaries = []
        for name, url in feeds.items():
            try:
                r = requests.get(url, timeout=8)
                titles = re.findall(r'<title>(.*?)</title>', r.text)
                titles = [re.sub(r'<[^>]+>', '', t).strip() for t in titles if len(t.strip()) > 10][1:3]
                if titles:
                    summaries.append(f"{name}: {', '.join(titles)}")
            except:
                pass
        return "Latest from the web:\n" + "\n".join(summaries) if summaries else "Could not fetch feeds"

    register_skill("monitor_feeds", "Monitor multiple RSS feeds for latest news", skill_monitor_feeds)

    def skill_extract_links(url):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
            links = [l for l in links if l.startswith('http')][:10]
            return f"Links found on {url}:\n" + "\n".join(links)
        except Exception as e:
            return f"Could not extract links: {e}"

    register_skill("extract_links", "Extract all links from any webpage", skill_extract_links)

    def skill_search_news(topic):
        try:
            # Use HackerNews search API (free, no key needed)
            r = requests.get(f"https://hn.algolia.com/api/v1/search?query={topic}&tags=story&hitsPerPage=5", timeout=8)
            data = r.json()
            hits = data.get("hits", [])
            if hits:
                results = f"News about '{topic}':\n"
                for h in hits[:5]:
                    results += f"\n• {h.get('title','')}\n  {h.get('url','')[:80]}\n"
                return results
        except:
            pass
        return think(f"What are the latest developments in {topic}?", max_tokens=200)

    register_skill("search_news", "Search for news on any topic using HackerNews", skill_search_news)

    def skill_github_trending():
        try:
            r = requests.get("https://github.com/trending", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            repos = re.findall(r'<h2 class="h3[^"]*">\s*<a href="([^"]+)"', r.text)[:5]
            if repos:
                return "Trending on GitHub:\n" + "\n".join([f"• github.com{r}" for r in repos])
        except:
            pass
        return "Could not fetch GitHub trending"

    register_skill("github_trending", "Get trending GitHub repositories", skill_github_trending)

    log("Pack 07 Web Browse & RSS: 6 skills loaded")
