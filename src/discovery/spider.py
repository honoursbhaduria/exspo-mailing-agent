import scrapy
import json
import re
from bs4 import BeautifulSoup
from src.discovery.items import InfluencerItem

class MicroInfluencerSpider(scrapy.Spider):
    name = "micro_influencers"
    allowed_domains = ["collabstr.com"]
    
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 0.5,
        "CONCURRENT_REQUESTS": 4,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
    }

    def __init__(self, target_niche="Fashion & Beauty", limit=70, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_niche = target_niche
        self.limit = int(limit)
        self.discovered_count = 0
        self.seen_handles = set()

    async def start(self):
        categories_map = {
            "Fashion & Beauty": ["Fashion", "Beauty", "Model", "Lifestyle"],
            "Technology & AI": ["Technology", "Gaming", "Business", "Education"],
            "Fitness & Wellness": ["Health+%26+Fitness", "Athlete+%26+Sports", "Lifestyle"],
            "Lifestyle & Travel": ["Lifestyle", "Travel", "Food+%26+Drink", "Family+%26+Children"],
            "Fintech & Crypto": ["Business", "Technology", "Education"]
        }
        
        cats = categories_map.get(self.target_niche, ["Fashion", "Beauty", "Lifestyle"])
        for cat in cats:
            url = f"https://collabstr.com/api/search-results?c={cat}"
            yield scrapy.Request(
                url,
                headers={"X-Requested-With": "XMLHttpRequest"},
                callback=self.parse_category_results,
                meta={"category": cat.replace("+%26+", " & ").replace("+", " ")},
                dont_filter=True
            )

    def parse_category_results(self, response):
        try:
            data = json.loads(response.text)
            html_content = data.get("results", "")
        except Exception:
            html_content = response.text

        soup = BeautifulSoup(html_content, "html.parser")
        cards = soup.find_all(class_="profile-listing-holder")

        for card in cards:
            if self.discovered_count >= self.limit:
                break

            a_tag = card.find("a", href=True)
            if not a_tag:
                continue

            href = a_tag["href"].strip("/")
            handle = href.split("/")[-1]
            if not handle or handle in self.seen_handles:
                continue

            self.seen_handles.add(handle)
            self.discovered_count += 1

            card_text = card.get_text(separator=" | ", strip=True)
            parts = [p.strip() for p in card_text.split("|") if p.strip()]

            # Determine platform / follower indicator from card text
            follower_str = "0"
            location = "Not Specified"
            name = handle.replace("-", " ").title()
            price = "N/A"
            rating = 5.0

            for p in parts:
                if re.match(r"^[\d\.]+[kKmM]?$", p):
                    follower_str = p
                elif "$" in p:
                    price = p
                elif re.match(r"^[\d\.]+$", p) and float(p) <= 5.0:
                    try:
                        rating = float(p)
                    except ValueError:
                        pass
                elif any(geo in p for geo in [", US", ", GB", ", CA", ", AU", ", IN", ", FR", ", DE", ", ES"]):
                    location = p

            if len(parts) >= 2 and not any(char in parts[1] for char in ["$", "%"]):
                name = parts[1]

            item = InfluencerItem()
            item["handle"] = handle
            item["name"] = name
            item["platform"] = "Instagram" if "instagram" in card_text.lower() else ("TikTok" if "tiktok" in card_text.lower() else "Instagram & TikTok")
            item["profile_url"] = f"https://collabstr.com/{handle}"
            item["follower_str"] = follower_str
            item["niche"] = response.meta.get("category", self.target_niche)
            item["location"] = location
            item["price"] = price
            item["rating"] = rating
            item["content_themes"] = "Fashion, Lifestyle, UGC"
            item["contact_email"] = "Not Found"
            item["bio"] = ""

            # Follow profile page for enrichment (detailed bio, verified email, themes)
            profile_url = f"https://collabstr.com/{handle}"
            yield scrapy.Request(
                profile_url,
                callback=self.parse_profile_detail,
                meta={"item": item},
                dont_filter=True
            )

    def parse_profile_detail(self, response):
        item = response.meta["item"]
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Headline / Bio
        h1 = soup.find("h1")
        headline = h1.get_text(strip=True) if h1 else ""

        # Extract packages / offerings text for rich context
        bio_snippets = []
        if headline:
            bio_snippets.append(headline)

        for div in soup.find_all("div"):
            t = div.get_text(separator=" ", strip=True)
            if any(term in t for term in ["I will create", "content creator", "passionate about", "sharing my"]):
                if len(t) < 300 and t not in bio_snippets:
                    bio_snippets.append(t)

        full_bio = " | ".join(bio_snippets) if bio_snippets else headline
        item["bio"] = full_bio[:400] if full_bio else f"{item['name']} is a verified creator in {item['niche']}."

        # Extract Email from profile if publicly mentioned
        page_text = soup.get_text()
        found_emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_text)
        valid_emails = [
            e for e in found_emails 
            if not any(x in e.lower() for x in ["collabstr", "example", "sentry", "w3.org", "domain.com", "email.com"])
        ]
        item["contact_email"] = valid_emails[0] if valid_emails else "Not Found"

        # Check for social links
        item["instagram_url"] = f"https://instagram.com/{item['handle']}"
        item["tiktok_url"] = f"https://tiktok.com/@{item['handle']}"
        item["youtube_url"] = ""

        # Extract follower count and engagement from page metrics if available
        # Collabstr metric value parsing
        metrics = re.findall(r"([\d\.]+[kKmM\%]?)\s+(Followers|Engagement)", page_text)
        for val, metric_type in metrics:
            if metric_type == "Followers" and val not in ["0.0k", "0", "1.5M"]:
                item["follower_str"] = val
            elif metric_type == "Engagement" and val not in ["0.0%", "5.0%"]:
                try:
                    item["engagement_rate"] = float(val.replace("%", ""))
                except ValueError:
                    pass

        yield item
