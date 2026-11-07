"""Lesson catalogue rules: which lessons we may host, which are done on other sites.

hostable  CS Unplugged (CC BY-SA 4.0). The license lets us show the lesson on our pages,
          if we give credit, link the license, say what we changed, and share under the same license.
external  Everything else. Our two CC0 sources are lists of links. CC0 covers the list, not the
          pages it points to, so those lessons are done on the other site and we only link out.

Pure functions and plain data. No Flask, so tests can import it.
"""
from urllib.parse import urlparse

HOSTABLE_LICENSES = {"CC-BY-SA-4.0"}
LEVELS = ["Beginner", "Intermediate", "Advanced"]

ATTRIBUTION = (
    "Lesson from CS Unplugged, University of Canterbury CSER Group, licensed CC BY-SA 4.0 "
    "(https://creativecommons.org/licenses/by-sa/4.0/). Changes were made: translated and "
    "level-tagged by Hackcessability, with AI. Shared under the same license."
)

VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")
REPO_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org")


def _host(url):
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def _is_host(host, names):
    return any(host == n or host.endswith("." + n) for n in names)


def kind_of(entry):
    """What the learner will open: unit | lesson | challenge | activity (hostable),
    or video | repo | document | article (external)."""
    url = entry.get("url", "")
    if entry.get("side") == "kids":
        path = urlparse(url).path.rstrip("/")
        if path.endswith("/programming"):
            return "challenge"
        if "/integrations/" in path:
            return "activity"
        return "unit" if path.count("/") <= 3 else "lesson"  # /en/topics/<topic> vs .../<lesson>
    host = _host(url)
    if _is_host(host, VIDEO_HOSTS):
        return "video"
    if _is_host(host, REPO_HOSTS):
        return "repo"
    if urlparse(url).path.lower().endswith(".pdf"):
        return "document"
    return "article"


def classify(entry):
    """Return the fields we add to every entry at load time. Never written to the JSON files."""
    kind = kind_of(entry)
    if entry.get("license") in HOSTABLE_LICENSES and entry.get("side") == "kids":
        return {
            "delivery": "hostable", "kind": kind, "attribution": ATTRIBUTION,
            "delivery_reason": "Open license that lets us show the lesson here, with credit.",
        }
    return {
        "delivery": "external", "kind": kind, "attribution": None,
        "delivery_reason": "We only link to this one. Its owner keeps the rights, so you do the lesson on their site.",
    }


# ---------------------------------------------------------------------------
# How-to guides for lessons done on another site. English source text; the
# translate pipeline can add other languages later (the site falls back to English).
# ---------------------------------------------------------------------------

ACCESS_COMMON = [
    "Language: in Chrome or Edge, right-click the page and pick Translate. In Safari, use the page "
    "menu button, then Translate. The translation is by a machine, so check anything that looks odd.",
    "Read it aloud: Edge has Read aloud (Ctrl+Shift+U). Windows has Narrator (Win+Ctrl+Enter). "
    "Mac has VoiceOver (Cmd+F5). NVDA is a free screen reader for Windows.",
    "Make it bigger: press Ctrl and + (Cmd and + on a Mac). Reset with Ctrl+0.",
    "Keyboard only: Tab moves to the next link or button, Shift+Tab goes back, Enter opens it.",
    "Tire easily or lose focus? Work in short blocks, for example 15 minutes, then rest.",
]

LEVEL_COMMON = {
    "Beginner": [
        "Pick Beginner lessons first. They need no installs and no sign-up.",
        "Do one small piece at a time and stop when you feel stuck. Come back later.",
        "Children: do this with a grown-up beside you.",
    ],
    "Intermediate": [
        "You can follow along with a code editor. Free ones: VS Code, or an online one.",
        "Type the code yourself instead of pasting it. It helps you remember.",
        "If a lesson needs an account or payment, ask a grown-up first.",
    ],
    "Advanced": [
        "Expect to read documentation and to install tools. Allow a few hours or days.",
        "Work in small steps and test often. Keep notes of what you tried.",
        "Forums and chat rooms are open to strangers. Only go there with a grown-up, and never share personal details.",
    ],
}

GUIDES = {
    "video": {
        "title": "How to learn from a video lesson",
        "summary": "A video is on another site (most often YouTube). You watch it there and follow along here.",
        "steps": [
            "Open the link. It opens the video on the other site. Check with a grown-up if you are a child.",
            "Turn on captions: press C, or click the CC button. For another language open Settings, then Subtitles, then Auto-translate.",
            "Slow it down or speed it up: Settings, then Playback speed. Use 0.75 if the speaker is fast.",
            "Pause often. Use K or the space bar to pause, and J or the left arrow to go back 5 seconds.",
            "Do the step on your own computer right after you watch it. Then play the next part.",
            "Skip the comments section. It can have rude or unsafe messages, and it is not part of the lesson.",
        ],
        "accessibility": [
            "No sound? Use captions and read along. Many videos also have a transcript under the three-dot menu, labelled Show transcript.",
            "Low vision? Use full screen (press F) and zoom the page with Ctrl and +.",
            "Autoplay: turn it off in the player so the next video does not start by itself.",
        ],
    },
    "repo": {
        "title": "How to learn from a GitHub project or list",
        "summary": "This link goes to a GitHub page. It may be a list of lessons, a tutorial, or code to read.",
        "steps": [
            "Open the link. You do not need an account to read a public GitHub page.",
            "Start with the README. It is the text shown below the file list. It tells you what the project is for.",
            "Look for a folder called docs, tutorial or examples. Those are the lessons.",
            "To get the code on your PC, click the green Code button, then Download ZIP. Unzip it. You do not need Git for this.",
            "Follow the README steps in order. If one step fails, read the Issues tab for the same error.",
            "Check the license (the LICENSE file) before you reuse code in your own project.",
        ],
        "accessibility": [
            "GitHub pages are long. Use the headings list in your screen reader to jump between sections.",
            "Press / on GitHub to open search, and T to find a file by name.",
            "Dark or high-contrast theme: GitHub Settings, then Appearance. Needs an account.",
        ],
    },
    "article": {
        "title": "How to learn from an article or tutorial site",
        "summary": "This link goes to a web page written by someone else. It may have ads, pop-ups, or a sign-up wall.",
        "steps": [
            "Open the link. If a pop-up asks you to sign up or pay, close it. Ask a grown-up before you give an email.",
            "Switch to reading mode to hide ads: in Edge press F9, in Safari click the reader icon in the address bar.",
            "Read the whole page once without typing. Then go back to the start and do each step.",
            "Copy code into your own editor by typing it. Read any comment lines in the code too.",
            "If the page asks for an account or card to continue, stop and ask a grown-up. Other lessons here are free.",
            "If the page is old, tools may have new versions. Search the error message if a step does not work.",
        ],
        "accessibility": [
            "Reading mode also gives a bigger, calmer layout and is friendlier for screen readers.",
            "Use Translate (see the tips below) for pages in another language. Keep code in English: do not translate it.",
            "Dyslexia or low vision? Reading mode lets you change font size and background colour.",
        ],
    },
    "document": {
        "title": "How to learn from a PDF or book",
        "summary": "This link opens a document file, such as a PDF book or paper.",
        "steps": [
            "Open the link. The file may download, or open in your browser.",
            "Look at the table of contents first and choose one chapter. You do not need to read it all.",
            "Read a section, then try the example right away.",
            "Use Ctrl+F to find a word inside the document.",
            "Take notes in your own words. Short notes are enough.",
        ],
        "accessibility": [
            "Some PDFs are scans of pages. A screen reader cannot read these. Pick a version with text you can select, if there is one.",
            "Edge and Adobe Reader can read a PDF aloud. In Edge: Ctrl+Shift+U.",
            "Zoom with Ctrl and +, or choose Fit to width.",
        ],
    },
}

for _guide in GUIDES.values():
    _guide["accessibility"] = _guide["accessibility"] + ACCESS_COMMON
    _guide["by_level"] = LEVEL_COMMON
    _guide["safety"] = [
        "Children: ask a grown-up before you open an outside link.",
        "Never share your name, school, address or photos on another site.",
        "This site does not run the other site. Its content and ads are not ours.",
    ]


def guide_for(kind):
    return GUIDES.get(kind)
