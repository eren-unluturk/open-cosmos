"""Handwritten guides, batch 3. Written by Claude Code from catalog data only."""
from guide_content._util import G
GUIDES = {}

G(GUIDES, "build:Build your own Augmented Reality", "Build your own augmented reality",
  "{entry_title} is in our Augmented Reality build group, a list of tutorials about adding digital things on top of the real world through a camera. We only know the title, short description and level from our list.",
  "It is for people who like cameras, phones and 3D ideas. It suits about age {age} and up, and some programming helps.",
  ["Read the description to see what you would need, like a phone or a camera.", "Open the tutorial with a grown-up and check the setup.", "Get a simple shape to show over the camera first."],
  [("Day 1", 30, "Check what you need and set up."), ("Week 1", 60, "Show a simple object on screen."), ("Week 2", 60, "Make it respond to movement."), ("Week 3", 45, "Show a friend.")],
  adult="Grown-ups: camera apps can touch privacy. Please check what the tutorial's app asks for.")

G(GUIDES, "learn:Development Environment", "Your coding workspace",
  "{entry_title} is in our Development Environment group, a list about the tools programmers use to write and manage code. We only know the title, short description and level from our list.",
  "It is for people who already write a little code and want better tools. It suits about age {age} and up. Many items are Intermediate.",
  ["Pick one tool that fits what you already do.", "Open the site with a grown-up and read the first page.", "Try it on a small project, not an important one."],
  [("Day 1", 20, "Read what the tool does."), ("Week 1", 40, "Install or try it."), ("Week 2", 40, "Use it on a project."), ("Week 3", 30, "Decide whether to keep it.")],
  adult="Grown-ups: installing tools changes a computer, so please help and check.")

G(GUIDES, "build:Build your own Physics Engine", "Build your own physics engine",
  "{entry_title} is in our Physics Engine build group, a list of tutorials about making things bounce, fall and collide in a program. We only know the title, short description and level from our list.",
  "It is for people who like games, maths and science. Most items need some programming, so it suits about age {age} and up.",
  ["Pick a tutorial that uses a language you know.", "Open it with a grown-up and read the first step.", "Make one ball fall on the screen first."],
  [("Day 1", 30, "Set up and draw a ball."), ("Week 1", 60, "Add gravity."), ("Week 2", 60, "Add bouncing."), ("Week 3", 60, "Add a second object.")],
  adult="Grown-ups: this includes maths. A beginner can ignore the hardest parts at first.")

G(GUIDES, "build:Build your own Web Server", "Build your own web server",
  "{entry_title} is in our Web Server build group, a list of tutorials about making a program that sends web pages to browsers. We only know the title, short description and level from our list.",
  "It is for people who know a little programming and want to see how websites are sent. It suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up and read the first step.", "Make a server that sends one short page."],
  [("Day 1", 40, "Read and set up."), ("Week 1", 60, "Serve one page."), ("Week 2", 60, "Serve two pages."), ("Week 3", 60, "Handle a simple form.")],
  adult="Grown-ups: a web server can be reached from other computers. Run it only on your own computer and don't expose it to the internet.")

G(GUIDES, "kids:CS Unplugged: Data structures for searching", "Data structures for searching (CS Unplugged)",
  "{entry_title} is part of a CS Unplugged unit about organising data so it is quick to search. You act out a tree on the ground and walk through it.",
  "It is for older children, about {age} and up, who have already tried the searching games, with a grown-up or teacher. It is an {level} activity.",
  ["Draw a big tree on the ground with chalk or tape.", "Pick a target number and walk the tree, turning over nodes.", "Compare with searching a sorted list."],
  [("Day 1", 45, "Walk through the tree."), ("Day 2", 30, "Build your own tree with new numbers."), ("Week 1", 30, "Compare with the sorted list game.")],
  adult="Grown-ups: children often mix up binary search and binary search trees. They are related, but not the same.")

G(GUIDES, "learn:Back-End Development", "Back-end development",
  "{entry_title} is in our Back-End Development group, a list of tools for the part of a website that works behind the scenes, like storing data. We only know the title, short description and level from our list.",
  "It is for people who already know some web or programming basics. Items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Check that the tool uses a language you know.", "Open the site with a grown-up and read the getting-started page.", "Run the smallest example."],
  [("Day 1", 30, "Read the intro."), ("Week 1", 60, "Run a hello-world example."), ("Week 2", 90, "Build something small that saves data."), ("Week 3", 60, "Show a friend how it works.")],
  adult="Grown-ups: back-end tools can store personal data. Please keep any test data fake.")

G(GUIDES, "learn:Content Management Systems", "Content management systems",
  "{entry_title} is in our Content Management Systems group, a list of tools that let people run websites and edit their pages without coding everything. We only know the title, short description and level from our list.",
  "It is for people who want to build a site for a club, class or hobby. It suits about age {age} and up, with a grown-up for any accounts or hosting.",
  ["Decide what site you want to make.", "Open the tool's site with a grown-up and read how it starts.", "Make a test page that only you can see."],
  [("Day 1", 30, "Choose a tool and read about it."), ("Week 1", 60, "Make a first page."), ("Week 2", 60, "Add pictures and links."), ("Week 3", 45, "Show it to your family.")],
  adult="Grown-ups: running a public site needs accounts and responsibility. Keep your child's name and details off it.")

G(GUIDES, "build:Build your own Neural Network", "Build your own neural network",
  "{entry_title} is in our Neural Network build group, a list of tutorials about building a tiny learning program from scratch. We only know the title, short description and level from our list.",
  "It is for people who know some programming and some maths. Most items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Pick a tutorial in a language you know.", "Open it with a grown-up and read the first step.", "Run the smallest example and see its output."],
  [("Day 1", 40, "Read the intro."), ("Week 1", 90, "Build a one-neuron example."), ("Week 2", 90, "Train it on a tiny data set."), ("Week 3", 60, "Change a setting and see what happens.")],
  adult="Grown-ups: this is a maths-heavy topic. It is fine to watch an explanation first.")

G(GUIDES, "build:Build your own Front-end Framework / Library", "Build your own front-end library",
  "{entry_title} is in our front-end framework build group, a list of tutorials about how tools like React work inside, by building a small one. We only know the title, short description and level from our list.",
  "It is for people who already build web pages and want to look under the hood. It suits about age {age} and up.",
  ["Make sure you can build a basic web page.", "Open the tutorial with a grown-up and read the first step.", "Build the smallest working piece."],
  [("Day 1", 40, "Read and set up."), ("Week 1", 90, "Build the first part."), ("Week 2", 90, "Add updating."), ("Week 3", 60, "Use it in a small page.")],
  adult="Grown-ups: this is an advanced topic. Starting with the basics of web pages first is a good idea.")

G(GUIDES, "learn:Testing", "Testing your code",
  "{entry_title} is in our Testing group, a list of tools that check whether a program does what it should. We only know the title, short description and level from our list.",
  "It is for people who already write programs and want them to be more reliable. It suits about age {age} and up.",
  ["Pick a tool that matches your language.", "Open its site with a grown-up and read the first page.", "Write one test for a tiny function."],
  [("Day 1", 30, "Read the first page."), ("Week 1", 45, "Write one test."), ("Week 2", 60, "Write tests for a small project."), ("Week 3", 45, "Fix a bug a test finds.")],
  adult="Grown-ups: testing tools are mostly for people with some programming experience.")
