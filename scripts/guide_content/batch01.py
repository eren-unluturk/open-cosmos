"""Handwritten guides, batch 1: CS Unplugged units (kids, ages 5-10) and the first big learn groups.
Written by Claude Code from catalog data only (titles, descriptions, categories, levels, topics)."""
GUIDES = {}

GUIDES["kids:CS Unplugged: Binary numbers"] = dict(
    title="Binary numbers (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about binary numbers. Binary is how computers store numbers using only two states, on and off. The activities use cards, movement and games, with no screen.",
    for_me="It is made for children about {age} and up, and it is meant to be done together with a grown-up or teacher. You do not need to know any coding. It is a {level} activity.",
    steps=["Ask a grown-up to read the lesson or open our simple version with you.", "Gather what you need, like paper cards with dots, and clear a little space.", "Do the activity together and say out loud what you notice."],
    time="Most lessons take 30 to 60 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 45, "Do the first lesson of the unit together."), ("Day 2", 30, "Do it again and teach someone at home."), ("Week 1", 45, "Try the next lesson in the unit."), ("Week 2", 30, "Make up your own binary game.")],
    adult="Grown-ups: these are teacher and parent lesson plans. Be the guide, let the child discover patterns, and do not worry about correct answers at first.")

GUIDES["kids:CS Unplugged: Kidbots"] = dict(
    title="Kidbots (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about giving clear instructions to a robot, like a toy bot or a friend pretending to be one. You learn what a program is by writing one for a friend to follow.",
    for_me="It is for children about {age} and up who like moving around and giving or following instructions. You do not need a computer. It is a {level} activity to do with a grown-up or teacher.",
    steps=["Make a grid on the floor with tape or chalk.", "Choose who is the programmer and who is the robot, and agree on simple commands.", "Write the program, run it, and fix any mistakes you find."],
    time="Most lessons take 30 to 45 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 30, "Be the robot and follow a friend's instructions."), ("Day 2", 30, "Write a longer program for a new route."), ("Week 1", 45, "Add a rule and find the bugs."), ("Week 2", 30, "Teach someone else the game.")],
    adult="Grown-ups: bugs are good. Praise finding and fixing mistakes, not only getting it right the first time.")

GUIDES["kids:CS Unplugged: Error detection and correction"] = dict(
    title="Error detection and correction (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about how computers notice and fix mistakes in the information they store and send. The activities use card tricks and number games.",
    for_me="It is for children about {age} and up who like puzzles and magic tricks, with a grown-up or teacher to help. It is a {level} activity and needs no computer.",
    steps=["Get a set of two-sided cards or make some from paper.", "Try the card trick or number game with a grown-up.", "Swap roles, and try to explain why it works."],
    time="Most lessons take about 30 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 30, "Learn the card trick."), ("Day 2", 30, "Show the trick to a friend or family member."), ("Week 1", 30, "Try the next activity in the unit."), ("Week 2", 30, "Look for where mistakes get fixed in real life.")],
    adult="Grown-ups: practise the trick before you show it. Some activities in this unit use arithmetic, so a calculator is fine.")

GUIDES["kids:CS Unplugged: Searching algorithms"] = dict(
    title="Searching algorithms (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about how computers find things in a list. You play guessing games with number cards and find out why putting things in order makes finding them faster.",
    for_me="It is for children about {age} and up who like games and guessing, with a grown-up or teacher. No computer is needed. It is a {level} activity.",
    steps=["Make number cards, or print the sheets from the lesson page.", "Play the finding game and count how many guesses you need.", "Try again with the cards in order, and compare."],
    time="Most lessons take 30 to 45 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 30, "Play the hide-and-find game with cards in no order."), ("Day 2", 30, "Play again with the cards in order."), ("Week 1", 45, "Compare your guess counts and chart them."), ("Week 2", 30, "Invent a new searching game.")],
    adult="Grown-ups: change the numbers to match what your child is learning in maths, and keep another game ready for fast finishers.")

GUIDES["kids:CS Unplugged: Sorting networks"] = dict(
    title="Sorting networks (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about sorting. You walk through a path drawn on the ground, comparing numbers with other people, until everyone ends up in order.",
    for_me="It is for children about {age} and up who like moving around and working in a team, with a grown-up or teacher. It is a {level} activity and needs chalk or tape and some space.",
    steps=["Draw the sorting path on the ground with chalk or tape.", "Give six people a number each and let them walk through, comparing at each meeting.", "Check if everyone ended up in order, then try new numbers."],
    time="Most lessons take 30 to 45 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 45, "Walk through the path with six numbers."), ("Day 2", 30, "Try different cards, such as bigger numbers."), ("Week 1", 30, "Sort other things, like heights."), ("Week 2", 30, "Draw your own bigger network.")],
    adult="Grown-ups: only one team walks the path at a time, so give the watchers a job, like checking the results.")

GUIDES["kids:CS Unplugged: Image Representation"] = dict(
    title="Image representation (CS Unplugged)",
    what="{entry_title} is part of a CS Unplugged unit about how computers store pictures. You colour squares using number codes and learn that a picture on a screen is a grid of tiny squares called pixels.",
    for_me="It is for children about {age} and up who like drawing and colouring, with a grown-up. It is a {level} activity, and you only need paper and pencils.",
    steps=["Print the grid, or draw one on squared paper.", "Colour the squares using the number code.", "Swap with a friend and see if you got the same picture."],
    time="Most lessons take about 45 minutes. Plan about {minutes} minutes for a session.",
    timeline=[("Day 1", 45, "Colour a small picture from its numbers."), ("Day 2", 30, "Make up a picture and write its number code."), ("Week 1", 45, "Try the next lesson on squeezing pictures into less space."), ("Week 2", 30, "Look for pixels on a screen with a magnifying glass.")],
    adult="Grown-ups: pencil is easier than pen, because mistakes can be rubbed out. The original lesson page has the printable pictures.")

GUIDES["learn:Gaming"] = dict(
    title="Gaming and game making",
    what="{entry_title} is in our Gaming group, a list of resources about making games and learning with games. These are listings, so we only know the title, the short description and the level.",
    for_me="It is for anyone who likes games and wants to see how they are made. Most items here are Intermediate or Beginner, for about age {age} and up. Pick one that sounds fun and not too hard.",
    steps=["Read the title and description and pick one that sounds fun.", "Go to the original site with a grown-up and look at the first page.", "Try the first small thing you find and stop when it gets too hard."],
    time="Plan about {minutes} minutes at a time, over about {sessions} sessions (a first try is usually shorter).",
    timeline=[("Day 1", 20, "Look around and pick one thing to try."), ("Week 1", 40, "Follow a first small tutorial or example."), ("Week 2", 40, "Change one thing to make it your own."), ("Week 3", 40, "Share what you made with a friend.")],
    adult="Grown-ups: some game tools ask for accounts or downloads. Please check the site before your child uses it.")

GUIDES["learn:Platforms"] = dict(
    title="Computers and platforms",
    what="{entry_title} is in our Platforms group, a list about computers, boards and systems you can build things on, such as small computers. We only know the title, short description and level from our list.",
    for_me="It is for curious people who want to know what to build on. Many items are Intermediate, so it is best for about age {age} and up, with a grown-up for setup and buying anything.",
    steps=["Read the description and decide whether it matches what you want to build.", "Look at the site with a grown-up and check what you would need first.", "Start with the beginner page if there is one."],
    time="Plan about {minutes} minutes at a time over about {sessions} sessions. Setting up can take longer than the first project.",
    timeline=[("Day 1", 20, "Read about what it is and what it can do."), ("Week 1", 40, "Check what you need and ask a grown-up about it."), ("Week 2", 60, "Set it up if you can, or watch someone set it up."), ("Week 3", 60, "Try a first small project.")],
    adult="Grown-ups: some of these involve buying hardware or making an account. That is your decision, not ours.")

GUIDES["learn:Learn"] = dict(
    title="Learning resources",
    what="{entry_title} is in our Learn group, a general list of places and tools for learning to program. We only know the title, short description and level from our list.",
    for_me="It is for beginners and for anyone who wants a place to start. Many items are Beginner. It is a good choice for about age {age} and up, ideally with a grown-up nearby for the first try.",
    steps=["Choose one that looks fun or that matches something you already like.", "Open it with a grown-up and spend a few minutes looking around.", "Try the first activity and then talk about what you learned."],
    time="Plan about {minutes} minutes at a time over about {sessions} sessions.",
    timeline=[("Day 1", 20, "Explore and try one activity."), ("Week 1", 30, "Do a few more activities."), ("Week 2", 30, "Pick a goal, like making a tiny game or story."), ("Week 3", 30, "Show someone what you made.")],
    adult="Grown-ups: some learning sites ask for an account. Please check the site's rules before your child signs up.")

GUIDES["learn:Front-End Development"] = dict(
    title="Making websites (front-end)",
    what="{entry_title} is in our Front-End Development group, a long list of tools and resources for building the part of a website that people see and click. We only know the title, short description and level from our list.",
    for_me="It is for people who want to build web pages. Many items are Intermediate, so some web basics help. It suits about age {age} and up, and the beginner items are the best start.",
    steps=["Start with the Beginner items if you are new to web pages.", "Open the original site with a grown-up and read the first page.", "Try one small change, like a colour or a heading, and see it in the browser."],
    time="Plan about {minutes} minutes at a time over about {sessions} sessions.",
    timeline=[("Day 1", 30, "Look at what the tool does and try the very first example."), ("Week 1", 45, "Build a tiny page."), ("Week 2", 60, "Add one new feature, like a button."), ("Week 3", 60, "Share the page with a friend or family member.")],
    adult="Grown-ups: many of these are tools for developers. Look at the page first and help with installs.")

# Notes for resuming: see docs/GUIDE_PROGRESS.md
