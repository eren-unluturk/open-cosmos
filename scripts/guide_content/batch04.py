"""Handwritten guides, batch 4: last kid-safe groups and the first grown-up groups. Written by Claude Code from catalog data only."""
from guide_content._util import G
GUIDES = {}
CHECK = "Grown-ups: please look at this site before your child does. It is listed for developers, and we have not reviewed the page."

G(GUIDES, "build:Build your own AI Model", "Build your own AI model",
  "{entry_title} is in our AI Model build group, a list of tutorials about building the pieces of an AI system yourself. We only know the title, short description and level from our list.",
  "It is for people with programming and maths experience. Items are Advanced, so it suits about age {age} and up and is hard.",
  ["Read the description to see what it builds.", "Open the tutorial with a grown-up and check what it needs.", "Start with the introduction only."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Run the first example."), ("Week 2", 90, "Follow the next section."), ("Week 3", 60, "Write down what you understood.")],
  adult="Grown-ups: some tutorials need a lot of computer power or a paid service. Check costs before starting.")

G(GUIDES, "learn:Big Data", "Big data",
  "{entry_title} is in our Big Data group, a list of tools for working with very large amounts of data. We only know the title, short description and level from our list.",
  "It is for people who already program and want to work with big data. Items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Read what the tool is for.", "Open its site with a grown-up and read the overview.", "Try a tiny example on a small file."],
  [("Day 1", 30, "Read the overview."), ("Week 1", 60, "Run a tiny example."), ("Week 2", 90, "Try it on a bigger file."), ("Week 3", 60, "Explain what it did.")],
  adult=CHECK)

G(GUIDES, "build:Build your own Search Engine", "Build your own search engine",
  "{entry_title} is in our Search Engine build group, a list of tutorials about making a program that finds pages or text. We only know the title, short description and level from our list.",
  "It is for people who know some programming. Items are mostly Intermediate, so it suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up and read the first step.", "Search a small set of your own files first."],
  [("Day 1", 40, "Read and set up."), ("Week 1", 60, "Build an index of a few documents."), ("Week 2", 60, "Add ranking."), ("Week 3", 60, "Try it on more text.")],
  adult=CHECK)

G(GUIDES, "build:Build your own Template Engine", "Build your own template engine",
  "{entry_title} is in our Template Engine build group, a list of tutorials about tools that fill in web pages with data. We only know the title, short description and level from our list.",
  "It is for people who build web pages and want to see how templates work. Items are Intermediate, so it suits about age {age} and up.",
  ["Make sure you have written a little code before.", "Open the tutorial with a grown-up.", "Fill in one word in a template first."],
  [("Day 1", 30, "Read and set up."), ("Week 1", 60, "Replace simple words."), ("Week 2", 60, "Add loops."), ("Week 3", 45, "Make a page from a list.")],
  adult=CHECK)

G(GUIDES, "build:Build your own Text Editor", "Build your own text editor",
  "{entry_title} is in our Text Editor build group, a list of tutorials about making a program like a notepad. We only know the title, short description and level from our list.",
  "It is for people who know some programming and want to build a real tool. It suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up and read the first step.", "Show some text on screen first."],
  [("Day 1", 40, "Set up and show text."), ("Week 1", 60, "Type and delete."), ("Week 2", 60, "Save a file."), ("Week 3", 60, "Add a feature you want.")],
  adult=CHECK)

G(GUIDES, "learn:Hardware", "Hardware and gadgets",
  "{entry_title} is in our Hardware group, a list about physical computing, like electronics and machines. We only know the title, short description and level from our list.",
  "It is for people who like building real things. It suits about age {age} and up, with a grown-up for any parts or tools.",
  ["Read the description to see what you would need.", "Look at the site with a grown-up before buying anything.", "Start with a simple, low-cost idea."],
  [("Day 1", 20, "Read about the idea."), ("Week 1", 45, "List the parts with a grown-up."), ("Week 2", 90, "Build the first part."), ("Week 3", 60, "Test and change it.")],
  adult="Grown-ups: hardware means buying parts and sometimes soldering or mains power. Please supervise closely.")

G(GUIDES, "learn:Work", "Careers in technology",
  "{entry_title} is in our Work group, a list about jobs and working life in technology. We only know the title, short description and level from our list.",
  "It is for older learners who wonder what jobs exist. It suits about age {age} and up.",
  ["Read the description to see what it is about.", "Look at the site with a grown-up.", "Write down one job that sounds interesting."],
  [("Day 1", 20, "Read about one kind of job."), ("Week 1", 30, "Find two more jobs."), ("Week 2", 30, "Talk to someone who has one."), ("Week 3", 20, "Pick a skill to try.")],
  adult=CHECK)

G(GUIDES, "build:Build your own Blockchain / Cryptocurrency", "Blockchain and cryptocurrency",
  "{entry_title} is in our Blockchain build group, a list of tutorials about how blockchains and digital money work. We only know the title, short description and level from our list. Money topics need a grown-up.",
  "It is for older learners who are curious about how the technology works. It suits about age {age} and up, only with a grown-up, and never with real money.",
  ["Read the description with a grown-up.", "Open the tutorial together and check that it uses fake money only.", "Build the smallest example."],
  [("Day 1", 30, "Read the introduction with a grown-up."), ("Week 1", 60, "Build a tiny chain."), ("Week 2", 60, "Add a simple rule."), ("Week 3", 45, "Explain it to a grown-up.")],
  adult="Grown-ups: please do not let a child use real money or make crypto accounts. This guide is about learning how the technology works only.")

G(GUIDES, "build:Build your own Operating System", "Build your own operating system",
  "{entry_title} is in our Operating System build group, a list of tutorials about writing the core program that runs a computer. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are Advanced, so it suits about age {age} and up, and is very hard.",
  ["Read the description and the requirements.", "Open the tutorial with a grown-up.", "Use a virtual machine, not your real computer."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 120, "Set up the tools."), ("Week 2", 120, "Boot the first screen."), ("Week 3", 90, "Print text on the screen.")],
  adult=CHECK + " Operating system tutorials can change how a computer starts; use a virtual machine.")

G(GUIDES, "learn:Databases", "Databases",
  "{entry_title} is in our Databases group, a list of tools for storing and finding data. We only know the title, short description and level from our list.",
  "It is for people who already program and need to store information. Items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Pick a database that fits what you want to store.", "Open its site with a grown-up and read the first page.", "Store and read back a couple of fake records."],
  [("Day 1", 30, "Read the overview."), ("Week 1", 60, "Install and run a first example."), ("Week 2", 60, "Store some fake data."), ("Week 3", 60, "Ask the database a question.")],
  adult="Grown-ups: use fake data only. Databases can hold personal details, so keep real names out.")
