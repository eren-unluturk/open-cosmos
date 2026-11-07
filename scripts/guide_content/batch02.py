"""Handwritten guides, batch 2. Written by Claude Code from catalog data only."""
from guide_content._util import G
GUIDES = {}
L1 = "Look around and pick one thing to try."

G(GUIDES, "learn:Programming Languages", "Programming languages",
  "{entry_title} is in our Programming Languages group, a long list of resources for learning particular programming languages. We only know each item's title, short description and level from our list.",
  "It is for anyone ready to learn a language. Most items are Intermediate, so some coding experience helps. The Beginner items are the best start, and it suits about age {age} and up.",
  ["Pick a language you have heard of or are curious about.", "Open the original site with a grown-up and read the first page.", "Type in one tiny example and see what it does."],
  [("Day 1", 30, "Read the first page and run one tiny example."), ("Week 1", 45, "Work through the first few lessons."), ("Week 2", 60, "Write a very short program of your own."), ("Week 3", 60, "Fix one bug and show someone.")],
  adult="Grown-ups: you may need to help install software. Please check the site first.")

G(GUIDES, "learn:Miscellaneous", "More resources",
  "{entry_title} is in our Miscellaneous group, a mixed bag of resources that did not fit in the other groups. We only know the title, short description, topic and level from our list, so the best way to find out more is to look.",
  "It might be for you if you like exploring. Items vary a lot in difficulty, so check the level ({level}) and ask a grown-up if you are unsure. It is marked for about age {age} and up.",
  ["Read the description to see what the item is about.", "Look at the original site with a grown-up before you start.", "Stop if it feels too hard and pick something easier."],
  [("Day 1", 20, L1), ("Week 1", 30, "Try the first part and note what you learned."), ("Week 2", 40, "Try to make or change something small."), ("Week 3", 30, "Tell someone about it.")],
  adult="Grown-ups: this group is mixed, so some items are not for children. Please look first.")

G(GUIDES, "learn:Computer Science", "Computer science",
  "{entry_title} is in our Computer Science group, a list of resources about the ideas behind computing, like how algorithms and data work. We only know the title, short description and level from our list.",
  "It is for curious people who want to know why computers work, not only how to use them. Many items are Advanced or Intermediate, so it suits about age {age} and up.",
  ["Read the description and see if the idea sounds interesting.", "Open the original site with a grown-up and read the first section.", "Draw or write the main idea in your own words."],
  [("Day 1", 30, "Read the first section."), ("Week 1", 45, "Take notes and try one example."), ("Week 2", 60, "Explain the idea to someone."), ("Week 3", 60, "Look for the idea in a program you know.")],
  adult="Grown-ups: some material is university level. A hard item is not a problem; just choose an easier one.")

G(GUIDES, "build:Build your own Game", "Build your own game",
  "{entry_title} is in our Build your own Game group, a list of tutorials about making a game from the ground up. We only know the title, short description and level from our list.",
  "It is for anyone who wants to make a game, not only play one. There are Beginner, Intermediate and Advanced items. It suits about age {age} and up, and a little programming experience helps.",
  ["Pick a game idea that looks small, like a simple arcade game.", "Open the tutorial with a grown-up and read the first step.", "Follow it step by step and run it often to see what changes."],
  [("Day 1", 30, "Read the first step and set up what you need."), ("Week 1", 60, "Get something moving on the screen."), ("Week 2", 60, "Add a rule or score."), ("Week 3", 60, "Change the look and play it with a friend.")],
  adult="Grown-ups: tutorials may need software installed. Please check before your child downloads anything.")

G(GUIDES, "build:Uncategorized", "Build-it tutorials",
  "{entry_title} is in our Uncategorized build group, a collection of 'build it yourself' tutorials that did not fit a more specific group. We only know the title, short description and level from our list.",
  "It is for people who learn by making things. Most items are Intermediate, so some programming experience helps. It suits about age {age} and up.",
  ["Read the description and the level.", "Open the tutorial with a grown-up and check what you need to install.", "Build the first small part and test it."],
  [("Day 1", 30, "Read the tutorial and set up."), ("Week 1", 60, "Build the first part."), ("Week 2", 60, "Build the next part and fix problems."), ("Week 3", 60, "Finish and change something to make it yours.")],
  adult="Grown-ups: please look at the tutorial before your child starts.")

G(GUIDES, "learn:Media", "Pictures, sound and media",
  "{entry_title} is in our Media group, a list of resources about images, icons, sound and other media for programs and websites. We only know the title, short description and level from our list.",
  "It is for people who like design, drawing or music and want to use them in their projects. It suits about age {age} and up, and the art-minded will like it.",
  ["Pick a type of media you like, such as pictures or sound.", "Open the site with a grown-up and look at examples.", "Try to use one in a project you already have."],
  [("Day 1", 20, "Browse and pick one you like."), ("Week 1", 30, "Try it in a small project."), ("Week 2", 40, "Make something that uses it."), ("Week 3", 30, "Show your work to a friend.")],
  adult="Grown-ups: check the licenses of any pictures or sounds before sharing a project.")

G(GUIDES, "learn:Theory", "Computer theory",
  "{entry_title} is in our Theory group, a list of resources about the ideas and maths behind computing. We only know the title, short description and level from our list.",
  "It is for curious people who like puzzles and maths. Items are mostly Intermediate or Advanced, so it suits about age {age} and up and can be hard.",
  ["Read the description to decide if it sounds interesting.", "Open the original site with a grown-up.", "Try one small idea or visualization and stop when it gets hard."],
  [("Day 1", 30, "Read the first section."), ("Week 1", 45, "Work through one example."), ("Week 2", 60, "Explain the idea to someone."), ("Week 3", 60, "Compare it with another resource.")],
  adult="Grown-ups: this material can be abstract. Easier items are fine to start with.")

G(GUIDES, "build:Build your own 3D Renderer", "Build your own 3D renderer",
  "{entry_title} is in our Build your own 3D Renderer group, a list of tutorials about making a program that draws 3D scenes. We only know the title, short description and level from our list.",
  "It is for people who like graphics and maths. There are Beginner items, but most take some programming experience. It suits about age {age} and up.",
  ["Pick a Beginner tutorial.", "Open it with a grown-up and read the first step.", "Draw a single shape on the screen before anything else."],
  [("Day 1", 30, "Set up and draw one shape."), ("Week 1", 60, "Draw a cube or a simple scene."), ("Week 2", 60, "Add colour and light."), ("Week 3", 60, "Move the camera and share your picture.")],
  adult="Grown-ups: graphics tutorials usually need a programming language installed.")

G(GUIDES, "build:Build your own Programming Language", "Build your own programming language",
  "{entry_title} is in our Build your own Programming Language group, a list of tutorials about making your own tiny language and a program that runs it. We only know the title, short description and level from our list.",
  "It is for people who already know a bit of programming and want to see how languages work inside. Most items are Intermediate or Advanced, so it suits about age {age} and up.",
  ["Make sure you can write a simple program in some language.", "Open the tutorial with a grown-up and read the first step.", "Build the smallest part first, like reading numbers."],
  [("Day 1", 40, "Read the intro and set up."), ("Week 1", 90, "Build a tiny calculator."), ("Week 2", 90, "Add variables or commands."), ("Week 3", 90, "Write a program in your new language.")],
  adult="Grown-ups: this is an advanced topic. It is fine to take it slowly or leave it for later.")

G(GUIDES, "learn:Books", "Free programming books",
  "{entry_title} is in our Books group, a list of free books about programming. We only know the title, short description and level from our list.",
  "It is for readers who like to learn from a book. Items are mostly Intermediate, so it suits about age {age} and up, with a grown-up to help find a good one.",
  ["Pick a book whose title sounds interesting.", "Open it with a grown-up and look at the contents.", "Read one short chapter and try one example."],
  [("Day 1", 20, "Read the introduction."), ("Week 1", 30, "Read one chapter and try its examples."), ("Week 2", 30, "Read the next chapter."), ("Week 3", 30, "Write down three things you learned.")],
  adult="Grown-ups: check that the book is the right level for your child.")
