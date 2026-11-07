"""Categorize every entry: topic, level, age_group and a child-safety tier.

Run AFTER fetch.py and BEFORE translate.py.

  Pass 1 (rules, no API): keyword / category / link-host rules.
  Pass 2 (Claude, optional): only for entries the rules can't decide (unknown topic
  or unknown level). Results are validated against the allowed values and cached in
  scripts/cache/categorize.json, so reruns only process new or changed entries.

IMPORTANT: we classify TITLES, DESCRIPTIONS, CATEGORIES AND LINK HOSTS only. We never
open the linked pages, so a "kid-safe" tag means "nothing in the listing looks risky",
not "we reviewed the page". Safety fails closed: anything unclear is "ask-a-grown-up",
and the AI may only make an entry stricter, never looser than the rules.

Usage: python scripts/categorize.py [--limit N] [--no-ai]
Requires ANTHROPIC_API_KEY in a local .env for pass 2 (never committed).
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
CACHE = ROOT / "scripts" / "cache" / "categorize.json"
OVERRIDES = ROOT / "scripts" / "cache" / "safety_overrides.json"  # human decisions, applied LAST
MODEL = "claude-haiku-5-5"
PROMPT_VERSION = 1  # bump to invalidate the cache after changing the AI prompt
BATCH = 20

LEVELS = ["Beginner", "Intermediate", "Advanced"]
AGES = ["5-7", "8-10", "11-13", "teen+"]
TOPICS = ["games", "art", "web", "general", "systems", "security", "other"]
SAFETY = ["kid-safe", "ask-a-grown-up", "adult-only"]
KID_TOPICS = {"games", "art", "web", "general"}

# ---------------------------------------------------------------- rule tables
def rx(words):
    return re.compile(r"\b(?:" + "|".join(words) + r")\b", re.I)

TOPIC_RULES = {
    "security": rx([r"hack(?!athon)\w*", r"exploit\w*", r"malware", r"reverse engineering", r"pentest\w*", r"penetration",
                    r"vulnerabilit\w+", r"security", r"cryptograph\w+", r"encryption", r"forensic\w*", r"ctf",
                    r"fuzz\w*", r"shellcode", r"ransomware", r"botnet", r"osint", r"steganograph\w+"]),
    "games": rx([r"games?", r"gamedev", r"unity", r"unreal", r"godot", r"minecraft", r"pico-8", r"phaser",
                 r"sprites?", r"roguelike", r"chess", r"tetris", r"snake", r"pong", r"text adventure"]),
    "art": rx([r"art", r"draw\w*", r"music", r"animation", r"creative coding", r"generative", r"p5(?:\.?js)?",
               r"processing", r"paint\w*", r"pixel\w*", r"sketch\w*", r"graphics", r"ray tracing", r"renderer",
               r"shaders?", r"3d"]),
    "web": rx([r"web\w*", r"html5?", r"css3?", r"javascript", r"front-?end", r"react", r"vue", r"angular", r"svelte",
               r"browsers?", r"dom", r"jquery", r"node\.?js"]),
    "systems": rx([r"operating system", r"kernel", r"compilers?", r"interpreters?", r"database", r"assembly",
                   r"emulator", r"virtual machine", r"docker", r"linux", r"shell", r"hypervisor", r"allocator",
                   r"garbage collector", r"file ?system", r"distributed", r"blockchain", r"network\w*"]),
    "general": rx([r"programming", r"learn\w*", r"python", r"computer science", r"algorithms?", r"data structures?",
                   r"tutorial", r"course", r"books?", r"beginners?", r"coding", r"intro\w*", r"scratch"]),
}
TOPIC_ORDER = ["security", "games", "art", "web", "systems", "general"]  # tie-break priority

BEGINNER = rx([r"beginners?", r"intro\w*", r"getting started", r"basics?", r"kids?", r"children", r"first",
               r"simple", r"101", r"learn(?:ing)? to", r"step[- ]by[- ]step", r"scratch", r"from zero", r"easy"])
ADVANCED = rx([r"advanced", r"internals", r"deep dive", r"distributed", r"kernel", r"compilers?",
               r"operating system", r"garbage collector", r"virtual machine", r"hypervisor", r"type checker",
               r"cryptograph\w+", r"assembly", r"ray tracing", r"concurren\w+", r"consensus"])
KIDS = rx([r"kids?", r"children", r"teachers?", r"elementary", r"scratch", r"unplugged", r"ages? \d+"])
LITTLE_KIDS = rx([r"scratch", r"preschool", r"toddlers?", r"unplugged", r"ages? [5-7]\b"])

# safety rules: (reason, pattern)
ADULT_RULES = [
    ("security-tooling", rx([r"hack(?!athon)\w*", r"exploit\w*", r"malware", r"reverse engineering", r"pentest\w*",
                             r"penetration", r"ransomware", r"botnet", r"shellcode", r"keylogger\w*", r"jailbreak\w*",
                             r"osint", r"red team"])),
    ("adult-content", rx([r"porn\w*", r"nsfw", r"gambl\w+", r"casino", r"betting", r"adult content", r"erotic"])),
]
ASK_RULES = [
    ("security-topic", rx([r"security", r"encryption", r"cryptograph\w+", r"crypto", r"privacy", r"passwords?",
                           r"authentication", r"forensic\w*"])),
    ("networking-tools", rx([r"packets?", r"sniff\w*", r"proxy", r"proxies", r"vpn", r"tor", r"port scan\w*",
                             r"firewall", r"wi-?fi", r"network\w*"])),
    ("finance-crypto", rx([r"blockchain", r"bitcoin", r"ethereum", r"cryptocurrenc\w+", r"crypto", r"nft",
                           r"trading", r"defi"])),
    ("external-forum", rx([r"forums?", r"chat", r"community", r"discussion", r"discord", r"reddit"])),
    ("social-platform", rx([r"slack", r"telegram", r"twitter", r"tweets?", r"facebook", r"messenger", r"whatsapp",
                            r"instagram", r"tiktok", r"mastodon", r"linkedin", r"snapchat"])),
    ("account-required", rx([r"sign ?up", r"log ?in", r"accounts?", r"register\w*", r"enroll\w*"])),
]
HOST_REASONS = [  # (reason, domains)
    ("external-forum", ["reddit.com", "news.ycombinator.com", "quora.com", "stackexchange.com", "stackoverflow.com",
                        "discord.com", "discord.gg", "slack.com", "gitter.im", "meetup.com", "lobste.rs",
                        "forum.", "community."]),
    ("social-platform", ["twitter.com", "x.com", "facebook.com", "instagram.com", "linkedin.com", "tiktok.com",
                         "mastodon.", "telegram.", "whatsapp.com", "t.me", "twitch.tv"]),
    ("account-required", ["coursera.org", "udemy.com", "edx.org", "codecademy.com", "pluralsight.com",
                          "skillshare.com", "udacity.com", "linkedin.com/learning", "datacamp.com"]),
    ("may-require-payment", ["udemy.com", "pluralsight.com", "skillshare.com", "datacamp.com", "educative.io",
                             "frontendmasters.com", "egghead.io", "codecrafters.io", "leanpub.com", "amazon."]),
]
# Hosts we are comfortable showing to children. Anything else is "unvetted-external-site".
# Set STRICT_UNVETTED_HOSTS = False to stop gating on this (the reason then never appears).
STRICT_UNVETTED_HOSTS = True
KNOWN_OK_HOSTS = ["github.com", "gitlab.com", "github.io", "developer.mozilla.org", "w3schools.com",
                  "freecodecamp.org", "khanacademy.org", "scratch.mit.edu", "code.org", "csunplugged.org",
                  "python.org", "wikipedia.org", "readthedocs.io", "processing.org", "p5js.org", "w3.org",
                  "javascript.info", "learnxinyminutes.com",
                  # first-tier hosts vetted by the Data lead (open-licensed / academic / vendor docs, no ads)
                  "aosabook.org", "scratchapixel.com", "fullstackpython.com", "nand2tetris.org",
                  "developer.ibm.com", "swtch.com",
                  # YouTube/Vimeo: we rely on the platform's own age restrictions (team decision).
                  "youtube.com", "youtu.be", "vimeo.com"]


def host_of(url):
    return re.sub(r"^www\.", "", (urlparse(url).netloc or "").lower())


def host_matches(host, url, domains):
    full = host + urlparse(url).path.lower()
    return any(d in host if d.endswith(".") else (host == d or host.endswith("." + d) or d in full)
               for d in domains)


# ---------------------------------------------------------------- pass 1: rules
def normalize(text):
    """Remove phrases that would trigger false matches ('from scratch' != Scratch, 'neural network' != networking)."""
    text = re.sub(r"\bfrom (?:the )?(?:ground up|scratch)\b", " ", text, flags=re.I)
    text = re.sub(r"\bsorting networks?\b", "sortingnet", text, flags=re.I)  # not computer networking
    return re.sub(r"\bneural net(?:work)?s?\b", "neuralnet", text, flags=re.I)


def rule_pass(e):
    text = normalize(" ".join([e["title"]["en"], e["desc"]["en"], e["category"], e.get("tag", "")]))
    title_cat = normalize(" ".join([e["title"]["en"], e["category"]]))
    host = host_of(e["url"])

    scores = {t: len(rx_.findall(text)) + len(rx_.findall(title_cat)) for t, rx_ in TOPIC_RULES.items()}
    best = max(scores.values())
    topic = next((t for t in TOPIC_ORDER if scores[t] == best), "other") if best else "other"
    topic_known = bool(best)

    b, a = len(BEGINNER.findall(text)), len(ADVANCED.findall(text))
    level_known = b != a
    level = "Beginner" if b > a else "Advanced" if a > b else "Intermediate"

    if KIDS.search(text):
        age = "5-7" if LITTLE_KIDS.search(text) else "8-10"
    elif level == "Beginner" and topic in KID_TOPICS:
        age = "11-13"
    else:
        age = "teen+"

    adult, ask = [], []
    for reason, pat in ADULT_RULES:
        if pat.search(text):
            adult.append(reason)
    for reason, pat in ASK_RULES:
        if pat.search(text):
            ask.append(reason)
    for reason, domains in HOST_REASONS:
        if host_matches(host, e["url"], domains):
            ask.append(reason)
    if topic not in KID_TOPICS:
        ask.append("unclassified" if topic == "other" else "not-kid-oriented-topic")
    if STRICT_UNVETTED_HOSTS and not host_matches(host, e["url"], KNOWN_OK_HOSTS) \
            and not any(r in ask for r in ("external-forum", "social-platform")):
        ask.append("unvetted-external-site")
    return {
        "topic": topic, "level": level, "age_group": age,
        "adult": list(dict.fromkeys(adult)), "ask": list(dict.fromkeys(ask)),
        "decided": topic_known and level_known,
    }


def safety_from(adult, ask):
    if adult:
        return "adult-only", adult + [r for r in ask if r not in adult]
    if ask:
        return "ask-a-grown-up", ask
    return "kid-safe", []


# ---------------------------------------------------------------- pass 2: Claude
PROMPT = """You label programming-learning resources for a children's learning site. For each item
(title/description/category only; you cannot see the linked page) return a JSON object:
{{"id": same id, "topic": one of {topics}, "level": one of {levels},
  "age_group": youngest suitable age, one of {ages},
  "safety": one of {safety}, "safety_reasons": [short kebab-case strings, e.g. "security-tooling"]}}
Be conservative: if unsure about safety choose "ask-a-grown-up". Return ONLY a JSON list.

Items:
{items}"""


def cache_key(e):
    blob = json.dumps([PROMPT_VERSION, e["id"], e["title"]["en"], e["desc"]["en"], e["category"],
                       e.get("tag", ""), e["url"]], ensure_ascii=False)
    return hashlib.sha1(blob.encode()).hexdigest()


def validate(r):
    """Return a cleaned AI result or None if it has any invalid value."""
    if not isinstance(r, dict):
        return None
    if r.get("topic") not in TOPICS or r.get("level") not in LEVELS \
            or r.get("age_group") not in AGES or r.get("safety") not in SAFETY:
        return None
    reasons = r.get("safety_reasons", [])
    if not isinstance(reasons, list) or not all(isinstance(x, str) for x in reasons):
        return None
    reasons = [re.sub(r"[^a-z0-9-]+", "-", x.lower()).strip("-")[:40] for x in reasons if x.strip()]
    return {"topic": r["topic"], "level": r["level"], "age_group": r["age_group"],
            "safety": r["safety"], "safety_reasons": [x for x in reasons if x]}


def parse_ai_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    return json.loads(text)


def ai_batch(client, batch):
    items = json.dumps([{"id": e["id"], "title": e["title"]["en"], "desc": e["desc"]["en"],
                         "category": e["category"], "host": host_of(e["url"])} for e in batch],
                       ensure_ascii=False)
    msg = client.messages.create(model=MODEL, max_tokens=4000, messages=[{"role": "user", "content": PROMPT.format(
        topics=TOPICS, levels=LEVELS, ages=AGES, safety=SAFETY, items=items)}])
    out = {}
    for r in parse_ai_json(msg.content[0].text):
        v = validate(r)
        if v and isinstance(r, dict) and r.get("id") in {e["id"] for e in batch}:
            out[r["id"]] = v
    return out


# ---------------------------------------------------------------- combine
def apply(e, rules, ai):
    topic, level, age = rules["topic"], rules["level"], rules["age_group"]
    adult, ask = list(rules["adult"]), list(rules["ask"])
    if ai and not rules["decided"]:
        # AI fills only what rules could not decide.
        topic = ai["topic"] if rules["topic"] == "other" else topic
        level = ai["level"] if rules["level"] == "Intermediate" else level
        age = ai["age_group"]
        if topic in KID_TOPICS:
            ask = [r for r in ask if r not in ("unclassified", "not-kid-oriented-topic")]
        else:
            ask = [r for r in ask if r != "unclassified"]
            if "not-kid-oriented-topic" not in ask:
                ask.append("not-kid-oriented-topic")
    safety, reasons = safety_from(adult, ask)
    if ai:  # AI may only make safety stricter
        order = {s: i for i, s in enumerate(SAFETY)}
        if order[ai["safety"]] > order[safety]:
            safety = ai["safety"]
            reasons = reasons + (ai["safety_reasons"] or ["ai-flagged"])
        elif ai["safety_reasons"] and safety != "kid-safe":
            reasons = reasons + [r for r in ai["safety_reasons"] if r not in reasons]
    if safety != "kid-safe" and not reasons:
        reasons = ["unclassified"]
    e.update({"topic": topic, "level": level, "age_group": age,
              "safety": safety, "safety_reasons": list(dict.fromkeys(reasons))})


def apply_override(e, ov):
    """Human override (id -> {"safety": tier, "reason": text}). May loosen OR tighten; applied last."""
    if ov["safety"] not in SAFETY:
        raise ValueError(f"bad override safety for {e['id']}: {ov['safety']}")
    e["safety"] = ov["safety"]
    e["safety_reasons"] = [] if ov["safety"] == "kid-safe" else ["human-review: " + ov.get("reason", "reviewed")]


# Sources whose age_group comes from the source itself (fetch_kids.py): categorize must not overwrite it.
PRESET_AGE_SOURCES = {"https://github.com/uccser/cs-unplugged"}


def sort_key(e):
    return (SAFETY.index(e["safety"]), LEVELS.index(e["level"]), AGES.index(e["age_group"]),
            e["category"], e["title"]["en"].lower(), e["id"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="max entries sent to Claude this run")
    ap.add_argument("--no-ai", action="store_true", help="rules only, no API calls")
    args = ap.parse_args()

    files = {n: json.loads((DATA / f"{n}.json").read_text())
             for n in ("learn", "build", "kids") if (DATA / f"{n}.json").exists()}
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

    rules = {e["id"]: rule_pass(e) for es in files.values() for e in es}
    undecided = [e for es in files.values() for e in es if not rules[e["id"]]["decided"]]
    todo = [e for e in undecided if cache_key(e) not in cache]
    client = None
    if not args.no_ai and todo:
        from dotenv import load_dotenv
        load_dotenv()
        if os.environ.get("ANTHROPIC_API_KEY"):
            import anthropic
            client = anthropic.Anthropic()
        else:
            print("No ANTHROPIC_API_KEY found: skipping the AI pass (rules only).")
    if client:
        todo = todo[: args.limit]
        for i in range(0, len(todo), BATCH):
            batch = todo[i:i + BATCH]
            try:
                results = ai_batch(client, batch)
            except Exception as ex:  # keep going; those entries fall back to rules (fail closed)
                print(f"AI batch failed ({type(ex).__name__}: {ex}); falling back to rules for it.")
                continue
            for e in batch:
                if e["id"] in results:
                    cache[cache_key(e)] = results[e["id"]]
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
            print(f"AI: {min(i + BATCH, len(todo))}/{len(todo)}")

    overrides = json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    known = {e["id"] for es in files.values() for e in es}
    for oid in overrides:
        if oid not in known:
            print(f"WARNING: override for unknown id {oid} ignored")
    used_ai = changed = 0
    for name, es in files.items():
        for e in es:
            ai = cache.get(cache_key(e)) if not rules[e["id"]]["decided"] else None
            used_ai += bool(ai)
            preset_age = e.get("age_group") if e["source"] in PRESET_AGE_SOURCES else None
            apply(e, rules[e["id"]], ai)
            if preset_age in AGES:
                e["age_group"] = preset_age
            if e["id"] in overrides:
                before = e["safety"]
                apply_override(e, overrides[e["id"]])
                changed += before != e["safety"]
        es.sort(key=sort_key)
        (DATA / f"{name}.json").write_text(json.dumps(es, ensure_ascii=False, indent=2) + "\n")
        print(f"{name}: {len(es)} entries categorized")
    print(f"rules decided: {len(rules) - len(undecided)}, undecided: {len(undecided)}, resolved by AI/cache: {used_ai}")
    print(f"human overrides: {len(overrides)} entries listed, {changed} changed the rules' safety tier")


if __name__ == "__main__":
    main()
