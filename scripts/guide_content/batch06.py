"""Handwritten guides, batch 6: the last grown-up groups. Written by Claude Code from catalog data only."""
from guide_content._util import G
GUIDES = {}
CHECK = "Grown-ups: this entry is in the grown-up section. Please look at the site yourself before your child does."

G(GUIDES, "build:Build your own BitTorrent Client", "Build your own BitTorrent client",
  "{entry_title} is in our BitTorrent build group, a list of tutorials about how file-sharing programs work inside. We only know the title, short description and level from our list.",
  "It is for experienced programmers curious about how files are shared between computers. It suits about age {age} and up.",
  ["Read the description with a grown-up.", "Open the tutorial together.", "Try it only with files that are free to share."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Read a torrent description file."), ("Week 2", 90, "Connect to a test source."), ("Week 3", 60, "Explain the idea to a grown-up.")],
  adult=CHECK + " File sharing can involve copyrighted material. Use only files you are allowed to share.")

G(GUIDES, "learn:Editors", "Code editors",
  "{entry_title} is in our Editors group, a list of programs for writing code. We only know the title, short description and level from our list.",
  "It is for people who write code and want a better editor. Items are Intermediate, so it suits about age {age} and up.",
  ["Pick one editor to try.", "Open its site with a grown-up and read how to install it.", "Open a small file in it."],
  [("Day 1", 20, "Read about it."), ("Week 1", 40, "Install and open a file."), ("Week 2", 40, "Learn three shortcuts."), ("Week 3", 30, "Decide whether to keep it.")], adult=CHECK + " Installing programs changes a computer.")

G(GUIDES, "learn:Entertainment", "Entertainment and tech",
  "{entry_title} is in our Entertainment group, a mixed list about tech culture, like newsletters and shows. We only know the title, short description and level from our list.",
  "It is for older learners who like keeping up with tech news. It suits about age {age} and up, with a grown-up, since content may not be written for children.",
  ["Read the description.", "Look at the site with a grown-up.", "Decide together whether it is right for you."],
  [("Day 1", 15, "Look at one item."), ("Week 1", 20, "Read an article."), ("Week 2", 20, "Pick a topic to follow."), ("Week 3", 15, "Share one thing you learned.")], adult=CHECK + " Newsletters may ask for your email address; do not share a child's address.")

G(GUIDES, "learn:Networking", "Computer networks",
  "{entry_title} is in our Networking group, a list about how computers talk to each other. We only know the title, short description and level from our list.",
  "It is for experienced learners curious about how the internet works. Items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Read the description.", "Open the site with a grown-up.", "Draw how two computers could talk to each other."],
  [("Day 1", 30, "Read the introduction."), ("Week 1", 45, "Draw the main idea."), ("Week 2", 60, "Try a safe example on your own computer."), ("Week 3", 45, "Explain it to someone.")], adult=CHECK + " Networking tools should only be used on your own network.")

G(GUIDES, "learn:Related", "Related tools and lists",
  "{entry_title} is in our Related group, a list of other 'awesome' lists and tools connected to learning to code. We only know the title, short description and level from our list.",
  "It is for people who want to explore further. Most items are Intermediate, so it suits about age {age} and up.",
  ["Read the description.", "Open the list with a grown-up.", "Pick one item that looks fun."],
  [("Day 1", 20, "Look at one list."), ("Week 1", 30, "Try one item from it."), ("Week 2", 30, "Try another."), ("Week 3", 20, "Share your favourite.")], adult=CHECK)

G(GUIDES, "build:Build your own Network Stack", "Build your own network stack",
  "{entry_title} is in our Network Stack build group, a list of tutorials about the code that sends data between computers. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are mostly Advanced, so it suits about age {age} and up.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Use an isolated test setup."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Send a first message."), ("Week 2", 120, "Handle replies."), ("Week 3", 90, "Test with two programs.")], adult=CHECK + " Use only your own computer and network.")

G(GUIDES, "learn:Events", "Tech events",
  "{entry_title} is in our Events group, a list of conferences and meet-ups about creative technology. We only know the title, short description and level from our list.",
  "It is for older learners who might like to meet others who code. It suits about age {age} and up, with a grown-up, because events involve strangers and travel.",
  ["Read the description.", "Look at the site with a grown-up.", "Check the age rules and location together."],
  [("Day 1", 15, "Read about one event."), ("Week 1", 20, "Check dates and age rules."), ("Week 2", 20, "Ask a grown-up about going."), ("Week 3", 15, "Look for a free online option.")], adult=CHECK + " Events may have age limits, costs and travel; please check them.")

G(GUIDES, "build:Build your own Visual Recognition System", "Build your own visual recognition system",
  "{entry_title} is in our Visual Recognition build group, a list of tutorials about programs that recognise things in pictures. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are Advanced, so it suits about age {age} and up.",
  ["Read the description with a grown-up.", "Open the tutorial together.", "Use pictures of objects, not of people."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Run a first example."), ("Week 2", 90, "Try your own pictures."), ("Week 3", 60, "Look at what it got wrong.")], adult=CHECK + " Please do not use photos of people, especially children, with recognition programs.")

G(GUIDES, "build:Build your own Web Browser", "Build your own web browser",
  "{entry_title} is in our Web Browser build group, a list of tutorials about making a program that shows web pages. We only know the title, short description and level from our list.",
  "It is for experienced programmers curious about how browsers work. Items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Fetch a single web page first."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Fetch and show text."), ("Week 2", 90, "Read simple tags."), ("Week 3", 90, "Draw a page.")], adult=CHECK)

G(GUIDES, "build:Build your own Distributed Systems", "Build your own distributed system",
  "{entry_title} is in our Distributed Systems build group, a list of tutorials about programs that work across many computers. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are Advanced, so it suits about age {age} and up, and is hard.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Run everything on your own computer."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Run one node."), ("Week 2", 120, "Run two nodes."), ("Week 3", 90, "Test what happens when one stops.")], adult=CHECK)

G(GUIDES, "build:Build your own Memory Allocator", "Build your own memory allocator",
  "{entry_title} is in our Memory Allocator build group, a list of tutorials about how programs get memory. We only know the title, short description and level from our list.",
  "It is for experienced programmers. Items are Advanced, so it suits about age {age} and up, and is hard.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Draw memory as a row of boxes."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Hand out a block."), ("Week 2", 90, "Free a block."), ("Week 3", 90, "Test with many blocks.")], adult=CHECK)

G(GUIDES, "build:Build your own Processor", "Build your own processor",
  "{entry_title} is in our Processor build group, a list of tutorials about how a computer's brain works. We only know the title, short description and level from our list.",
  "It is for experienced learners. Items are Advanced, so it suits about age {age} and up, and is hard.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Start with logic gates drawn on paper."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Learn the logic gates."), ("Week 2", 120, "Add numbers."), ("Week 3", 90, "Run a tiny program.")], adult=CHECK)

G(GUIDES, "build:Build your own Voxel Engine", "Build your own voxel engine",
  "{entry_title} is in our Voxel Engine build group, a list of tutorials about making a block-world game like those made of cubes. We only know the title, short description and level from our list.",
  "It is for experienced programmers who like games and 3D. Items are Advanced, so it suits about age {age} and up.",
  ["Read the description.", "Open the tutorial with a grown-up.", "Draw a single cube first."],
  [("Day 1", 40, "Read the introduction."), ("Week 1", 90, "Draw a cube."), ("Week 2", 120, "Draw many cubes."), ("Week 3", 90, "Add moving around.")], adult=CHECK)
