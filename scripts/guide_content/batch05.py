"""Handwritten guides, batch 5: grown-up groups (shown only after the grown-up gate). Written by Claude Code from catalog data only."""
from guide_content._util import G
GUIDES = {}
CHECK = "Grown-ups: this entry is in the grown-up section. Please look at the site yourself before your child does."

G(GUIDES, "learn:Decentralized Systems", "Decentralized systems",
  "{entry_title} is in our Decentralized Systems group, a list about systems with no single owner, like peer-to-peer networks. We only know the title, short description and level from our list.",
  "It is for older learners who know some programming and are curious about how the internet can be built differently. It suits about age {age} and up, with a grown-up.",
  ["Read the description with a grown-up.", "Look at the site together before starting.", "Read the introduction only on your first try."],
  [("Day 1", 30, "Read the introduction with a grown-up."), ("Week 1", 60, "Read the main idea and draw it."), ("Week 2", 60, "Try a small example."), ("Week 3", 45, "Explain it to a grown-up.")], adult=CHECK + " Some of these involve accounts or social networks.")

G(GUIDES, "learn:Security", "Computer security",
  "{entry_title} is in our Security group, a list about protecting computers and data. We only know the title, short description and level from our list. This is a grown-up topic.",
  "It is for older learners who want to understand how to stay safe online, always with a grown-up. It suits about age {age} and up. Learning to protect things is the goal; never try things on systems that are not yours.",
  ["Read the description with a grown-up.", "Open the site together and read the first page.", "Talk about how it could help you stay safe."],
  [("Day 1", 30, "Read about the idea with a grown-up."), ("Week 1", 45, "Check your own accounts' safety settings."), ("Week 2", 45, "Learn one new protection."), ("Week 3", 30, "Teach someone else.")],
  adult="Grown-ups: security material can include attack techniques. Please review it first, and make sure it is only used on your own devices.")

G(GUIDES, "build:Build your own Bot", "Build your own bot",
  "{entry_title} is in our Bot build group, a list of tutorials about programs that chat or act on their own. We only know the title, short description and level from our list.",
  "It is for people who know some programming and like chat programs. It suits about age {age} and up. Many bots connect to chat apps, so a grown-up should help.",
  ["Pick a tutorial that runs on your own computer.", "Open it with a grown-up and check for accounts or keys.", "Make the bot answer one fixed message first."],
  [("Day 1", 30, "Read and set up."), ("Week 1", 60, "Reply to a fixed message."), ("Week 2", 60, "Add a few commands."), ("Week 3", 45, "Show a friend.")],
  adult=CHECK + " Many bots need chat accounts or private keys. Never share those keys.")

G(GUIDES, "build:Build your own Database", "Build your own database",
  "{entry_title} is in our Database build group, a list of tutorials about making a tiny database from scratch. We only know the title, short description and level from our list.",
  "It is for experienced programmers who want to see how data is stored. It suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up and read the first step.", "Store one value and read it back."],
  [("Day 1", 40, "Read and set up."), ("Week 1", 90, "Store and read values."), ("Week 2", 90, "Add searching."), ("Week 3", 60, "Test with fake data.")], adult=CHECK)

G(GUIDES, "build:Build your own Emulator / Virtual Machine", "Build your own emulator or virtual machine",
  "{entry_title} is in our Emulator / Virtual Machine build group, a list of tutorials about programs that pretend to be another computer. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are mostly Advanced, so it suits about age {age} and up.",
  ["Pick an emulator for a simple machine.", "Open the tutorial with a grown-up.", "Read one instruction and do it by hand."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Read a program file."), ("Week 2", 120, "Run the first instructions."), ("Week 3", 90, "Run a small program.")], adult=CHECK)

G(GUIDES, "learn:Health and Social Science", "Computing for health and social science",
  "{entry_title} is in our Health and Social Science group, a list about using computing in areas like health, history and society. We only know the title, short description and level from our list.",
  "It is for older learners who like people and society as much as computers. It suits about age {age} and up, with a grown-up.",
  ["Read the description.", "Look at the site with a grown-up.", "Write down one question it makes you ask."],
  [("Day 1", 20, "Read about one project."), ("Week 1", 30, "Find a second example."), ("Week 2", 40, "Try a small data activity."), ("Week 3", 30, "Share what you found.")], adult=CHECK + " Health and social topics may include sensitive subjects.")

G(GUIDES, "learn:Business", "Computing and business",
  "{entry_title} is in our Business group, a list about technology for companies and money. We only know the title, short description and level from our list.",
  "It is for older learners curious about how technology is used at work. It suits about age {age} and up, with a grown-up.",
  ["Read the description.", "Look at the site with a grown-up.", "Note one idea you could use in a club or project."],
  [("Day 1", 20, "Read the description."), ("Week 1", 30, "Read one article."), ("Week 2", 30, "Talk about it at home."), ("Week 3", 20, "Pick a small project idea.")], adult=CHECK + " Business and finance topics may involve accounts or payments.")

G(GUIDES, "build:Build your own Command-Line Tool", "Build your own command-line tool",
  "{entry_title} is in our Command-Line Tool build group, a list of tutorials about making programs you run by typing commands. We only know the title, short description and level from our list.",
  "It is for people who know some programming and have used a terminal. It suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up.", "Make the tool print a message first."],
  [("Day 1", 30, "Set up."), ("Week 1", 60, "Read an option from the command."), ("Week 2", 60, "Add a feature."), ("Week 3", 45, "Use it for a small job.")], adult=CHECK)

G(GUIDES, "build:Build your own Regex Engine", "Build your own regex engine",
  "{entry_title} is in our Regex Engine build group, a list of tutorials about pattern-matching in text. We only know the title, short description and level from our list.",
  "It is for experienced programmers who like puzzles. It suits about age {age} and up.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Match a single letter first."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Match fixed text."), ("Week 2", 90, "Add wildcards."), ("Week 3", 60, "Test on examples.")], adult=CHECK)

G(GUIDES, "build:Build your own Git", "Build your own Git",
  "{entry_title} is in our Git build group, a list of tutorials about how version control works inside. We only know the title, short description and level from our list.",
  "It is for people who already use Git or are curious about it. It suits about age {age} and up.",
  ["Make sure you know the basics of Git.", "Open the tutorial with a grown-up.", "Store one file and get it back."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Store a file."), ("Week 2", 90, "Add commits."), ("Week 3", 60, "Try a small history.")], adult=CHECK)

G(GUIDES, "build:Build your own Docker", "Build your own Docker",
  "{entry_title} is in our Docker build group, a list of tutorials about how containers work inside. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are Advanced, so it suits about age {age} and up.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Use a virtual machine, not your main computer."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Set up."), ("Week 2", 90, "Run a first container."), ("Week 3", 60, "Explain what happened.")], adult=CHECK + " Container tutorials can need administrator access; use a virtual machine.")

G(GUIDES, "build:Build your own Shell", "Build your own shell",
  "{entry_title} is in our Shell build group, a list of tutorials about making the program that reads typed commands. We only know the title, short description and level from our list.",
  "It is for people who know some programming and use a terminal. Items are Intermediate, so it suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up.", "Read one line of input and print it."],
  [("Day 1", 30, "Set up."), ("Week 1", 60, "Run a simple command."), ("Week 2", 60, "Add built-in commands."), ("Week 3", 60, "Add pipes or history.")], adult=CHECK)
