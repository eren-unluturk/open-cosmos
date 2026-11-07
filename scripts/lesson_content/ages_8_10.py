"""Adapted lessons for ages 8-10 and 11-13 (CS Unplugged, CC BY-SA 4.0). Rewritten and shortened by Claude Code."""
L = {}

L["binary-numbers__how-binary-digits-work"] = dict(
    summary="Children use cards with 1, 2, 4 and 8 dots as 'bits' to make any number from 0 to 15, and see how a computer counts using only on and off.",
    objectives=["Explain how binary digits (bits) represent numbers.", "Make numbers from 0 to 15 with four cards.", "Spot the doubling pattern and count in binary."],
    materials=["Cards with 1, 2, 4 and 8 dots (a fifth card with 16 dots for later)", "Four volunteers", "Paper to record results"],
    steps=["Ask: how does a digital device store information? Write down every answer, then come back to them at the end.",
           "Four children stand in a line and hold the cards 8, 4, 2, 1 from left to right, with the dots hidden at first.",
           "Reveal the pattern: each card has twice as many dots as the one to its right.",
           "A card is either shown (on, 1) or hidden (off, 0). Call out a number and let the line show the right cards. Add the dots to check.",
           "Count from 0 to 15 by changing as few cards as possible each time. Write the pattern of ones and zeros on the board.",
           "Add a fifth card. What is the biggest number now?"],
    talk_about=["What is the biggest number with four cards? With five?", "Why does a computer use on and off?", "Which card changes most often when counting?"],
    grown_up="Resist the urge to correct guesses. Let the children find the doubling rule themselves. Real computers have billions of bits.")

L["binary-numbers__codes-for-letters-using-binary-representation"] = dict(
    summary="Children write secret messages by turning letters into numbers and numbers into patterns of on and off.",
    objectives=["Show that letters can be stored as numbers.", "Convert a letter to a binary pattern with five bits.", "Send and decode a short message."],
    materials=["Five dot cards: 16, 8, 4, 2, 1", "An alphabet chart (A = 1, B = 2, ...)", "Paper and pencils"],
    steps=["Ask how a computer knows which letter to show. Number the alphabet from 1 to 26.",
           "Work out the code for one letter together, for example D is 4, which needs the 4 card on and the others off: OFF OFF ON OFF OFF.",
           "Write the code for your name or a short word, one letter at a time.",
           "Swap messages with a partner. Decode each other's patterns back into letters.",
           "Discuss what a computer must also store: capital letters, digits and punctuation, and letters of other languages."],
    talk_about=["Why do we need five bits for 26 letters?", "What else would a computer need codes for?", "How could you send your code to someone far away?"],
    grown_up="If your alphabet has extra letters or accents, talk about how a code would need more bits. Real computers use a bigger standard code.")

L["binary-numbers__reinforcing-sequencing-in-binary-number-systems"] = dict(
    summary="Groups invent a play that counts in binary using any two opposite things, then perform it for the class.",
    objectives=["Show on and off with different objects, sounds or actions.", "Order four bits from biggest to smallest and count to 15.", "Explain the pattern to someone else."],
    materials=["Anything with two states (hats, sounds, lights, counters)", "Groups of four", "Optional camera or phone"],
    steps=["Brainstorm opposites together. A computer uses on and off in the same way.",
           "In groups of four, pick how to show on and off and decide who is the 8, 4, 2 and 1 bit.",
           "Practise counting up from 0, with each person switching at the right time.",
           "Swap roles so everyone is each bit once.",
           "Perform: the audience calls a number and the group shows it. Others work out which number it is."],
    talk_about=["Which bit moved the most when counting?", "Which idea did you like best from another group?", "Could you show a number bigger than 15?"],
    grown_up="Extra children can film the plays or be the audience. Be open to unusual ideas.")

L["error-detection-and-correction__parity-magic"] = dict(
    summary="A card trick shows how a computer adds one extra row and column so it can find and fix a single mistake.",
    objectives=["Explain why computers need to check data for errors.", "Make every row and column have an even number of black cards.", "Find a flipped card using the odd row and odd column."],
    materials=["36 two-sided cards (black and white)", "Pairs of children, each with their own set", "A whiteboard or table"],
    steps=["Ask: have you ever had a disc or QR code that would not work? Computers often correct such mistakes automatically.",
           "Lay out a 5 by 5 square of black and white cards with no pattern.",
           "Add a sixth row and a sixth column so every row and every column has an even number of black cards. (This extra card is called a parity bit.)",
           "While everyone looks away, flip exactly one card.",
           "Find the one row and the one column that now have an odd number of black cards. The card where they cross is the flipped one.",
           "Pairs practise. Then try flipping two cards. What happens?"],
    talk_about=["Why does the trick work?", "What happens if two cards flip?", "Where do computers use this idea?"],
    grown_up="Practise first so you can do the trick smoothly. Real systems use much better versions, but the idea is the same.")

L["error-detection-and-correction__product-code-check-digits"] = dict(
    summary="Children use a short recipe of adding and multiplying to find the last digit of a barcode, which is how scanners notice mistakes.",
    objectives=["Know that barcodes include a check digit.", "Follow a step-by-step recipe (an algorithm).", "Detect a mistake in a barcode."],
    materials=["Real barcodes from products (12 or 13 digits)", "Paper, pencil and a calculator if needed", "A whiteboard"],
    steps=["Ask: do you check your receipt at the shop? Barcodes are so reliable that we trust them.",
           "Take a 13-digit barcode and cover the last digit.",
           "Write the 12 digits in two rows: the 1st, 3rd, 5th... digits on top and the 2nd, 4th, 6th... on the bottom.",
           "Add up the top row. Add up the bottom row and multiply that total by 3. Add the two results together.",
           "Take the last digit of that sum. The check digit is what you need to add to reach the next multiple of ten.",
           "Compare with the covered digit. Then change one digit and see that the check fails."],
    talk_about=["Why is the last digit useful?", "What if two digits swap places?", "Where else do check digits appear, like library books or bank cards?"],
    grown_up="This is an arithmetic-heavy lesson, so let children use a calculator if they like. The modulo lesson is a good lead-in.")

L["kidbots__modulo"] = dict(
    summary="Children explore 'clock arithmetic' and remainders, a calculation that computers use all the time.",
    objectives=["Understand that counting can wrap around, like the hours on a clock.", "Find a remainder after dividing.", "Know why computers use the modulo operator."],
    materials=["A clock face with only 10 points (0 to 9)", "Paper and pencils", "Counters"],
    steps=["Ask: what month comes after December? What day is 4 days before Friday?",
           "If you park at 5pm for 8 hours, when does the ticket run out? Add 8 to 17 and wrap around the 24-hour clock.",
           "Show a clock with only ten positions. Start at 0, add numbers and say where you land.",
           "Connect to remainders: 23 divided by 10 leaves 3, which is the same as where you land after going round the ten-point clock.",
           "Practise with different clock sizes and numbers.",
           "Discuss where wrapping around is useful, like repeating patterns, turns and angles."],
    talk_about=["What does going round the clock have to do with remainders?", "Where do you meet wrap-around in everyday life?", "What would a clock with 7 points look like?"],
    grown_up="This lesson is mostly maths. It prepares for the barcode and error-checking lessons.")

L["kidbots__sending-a-rocket-to-mars"] = dict(
    summary="Children program a 'rocket' to cross a floor grid, using clear instructions and debugging with three roles.",
    objectives=["Write a program as a list of clear steps.", "Test and debug a program.", "Explain why computers need exact instructions."],
    materials=["A grid on the floor (chalk or tape)", "Arrow cards or paper", "A target square to mark 'Mars'"],
    steps=["Ask: why is it important to give very clear instructions? Share a time when instructions were unclear.",
           "Make a grid and mark the target. One child is the rocket (the Bot), one is the Programmer, one is the Tester.",
           "Agree on the commands: arrows for forward, turn left, turn right.",
           "The Programmer writes the whole program first. The Bot cannot be steered halfway.",
           "The Tester reads the program out. The Bot follows it. Did the rocket reach Mars?",
           "Debug: find what went wrong and change the program. Swap roles and try a harder route."],
    talk_about=["What was the hardest bug to find?", "Why not just steer the rocket step by step?", "What instructions would a real rocket need?"],
    grown_up="Show the idea yourself first by being the Programmer. Celebrate bugs found.")

L["searching-algorithms__how-many-guesses"] = dict(
    summary="Children search for a hidden number one card at a time and discover how many guesses it takes when the list is in no order.",
    objectives=["Define searching and a search algorithm.", "Predict, count and graph the number of guesses.", "Understand why unsorted lists take longer."],
    materials=["15 cards with a hidden number on the back, in no order", "Sticky notes", "A line or graph on the board"],
    steps=["Ask how many house visits you would need to find a lent book among six houses. Everyone puts a prediction on a line.",
           "Lay out the cards face down with a picture up. The numbers underneath are not in order.",
           "Choose a target number. One child turns cards over until they find it. The class counts the guesses.",
           "Repeat with other targets and record each count.",
           "Look at the spread: sometimes lucky, sometimes the last card. On average, about half the cards.",
           "Discuss how the number of guesses grows as the list gets bigger."],
    talk_about=["Was it ever one guess? Was it ever all of them?", "What if there were a million cards?", "Could sorting the cards help?"],
    grown_up="Try different numbers so children cannot guess where the target is. Keep a class tally.")

L["searching-algorithms__divide-and-conquer"] = dict(
    summary="With the cards in order, children find a number in just a few guesses by always checking the middle.",
    objectives=["Use the order of a list to search faster.", "Explain binary search in their own words.", "Compare with searching an unsorted list."],
    materials=["15 cards sorted from lowest to highest (spread between 1 and 100)", "A target number such as 52"],
    steps=["Lay out sorted cards face down. Say they run from small to large.",
           "Ask the class to find 52 using as few turned cards as possible.",
           "Turn over the middle card. If it is too big, throw away the right half. If too small, throw away the left half.",
           "Look at the middle of what is left and repeat until you find 52.",
           "Count the guesses with the class. Try other targets.",
           "Compare with the unsorted search. What changed?"],
    talk_about=["How many guesses at most for 15 cards?", "What if we doubled the cards?", "What if the number is not there?"],
    grown_up="This method is called binary search. Do not use 1 to 15 in order, or children will just count along.")

L["searching-algorithms__the-great-number-hunt-unsorted"] = dict(
    summary="Pairs play a guessing game on a sheet of 31 hidden numbers that are in no order, and count how many guesses they need.",
    objectives=["Search an unsorted list.", "Count and record guesses.", "See why unsorted data is slow to search."],
    materials=["The Number Hunt sheets (printable on the original lesson page)", "Pencils", "A class chart to record guesses"],
    steps=["Ask how you would find a book on a shelf if the books are in no order.",
           "Put children in pairs, back to back. Each has a sheet of 31 boxes.",
           "One partner picks a number that the other must find by guessing boxes one at a time.",
           "Count how many guesses it takes. Write it on the class chart or spreadsheet.",
           "Swap roles and play again.",
           "Look at the chart together. What do you notice?"],
    talk_about=["What is the fewest guesses? The most?", "Is there a smarter way to guess?", "What would help?"],
    grown_up="Have other games ready for children who finish early, since some searches take many guesses.")

L["searching-algorithms__the-great-number-hunt-sorted"] = dict(
    summary="Pairs play the same hunt game, but this time the numbers are in order, and they discover binary search.",
    objectives=["Use the order of the list to cut the search short.", "Describe binary search.", "Compare with the unsorted game."],
    materials=["Sorted Number Hunt sheets (printable on the original lesson page)", "Pencils", "A class chart"],
    steps=["Ask: is it easier to find a book in a library if the books are in alphabetical order?",
           "Pairs sit back to back with a sheet of 31 sorted boxes.",
           "One partner picks a number that the other must find. Guess the middle box first.",
           "After each guess, the partner says higher or lower. Discard half the boxes every time.",
           "Count guesses and add them to the class chart.",
           "Compare this chart with the unsorted one."],
    talk_about=["How many guesses did it take at most?", "Why is guessing the middle smart?", "Could this work for billions of items?"],
    grown_up="This method is called binary search. It can search huge lists with only a handful of guesses.")

L["sorting-networks__reinforcing-numeracy-through-a-sorting-network"] = dict(
    summary="Six children walk through a chalk network and compare numbers at each box until they come out in order.",
    objectives=["Compare numbers and put them in order.", "Follow a fixed algorithm.", "See how teamwork lets many steps happen at once."],
    materials=["A sorting network drawn on the ground", "Number cards (whole numbers, then bigger numbers, fractions or decimals)", "Six children per turn"],
    steps=["Ask for jobs that finish sooner with more helpers, and jobs that do not.",
           "Draw the network: six start circles, lines meeting in boxes, six end circles.",
           "Six children start at the circles holding mixed-up number cards.",
           "Two children meet in a box, say hello and compare. The smaller number goes left, the bigger goes right.",
           "Everyone follows the lines and meets in more boxes until they reach the end.",
           "Check: are they in order? Run it again with new cards."],
    talk_about=["Which steps could happen at the same time?", "Does it work with any six numbers?", "How would you sort twenty?"],
    grown_up="Use bigger numbers, decimals or fractions for a challenge.")

L["sorting-networks__investigating-variations-using-the-sorting-network"] = dict(
    summary="Children test the sorting network with repeated numbers and with other things to sort, and predict what will happen.",
    objectives=["Predict an outcome before testing it.", "Explain why the network works even with repeated values.", "Sort things other than numbers."],
    materials=["The sorting network from the first lesson", "Cards with repeated numbers", "Things to sort: heights, colours, sizes, words"],
    steps=["Recap how the network works.",
           "Use cards where two values are equal. Ask what happens when equal cards meet.",
           "Predict, then run the network. Equal cards end up next to each other.",
           "Choose something new to sort, like heights or the alphabet. Decide what 'smaller' means for it.",
           "Run the network with the new cards and check the result.",
           "Discuss what stays the same each time and why."],
    talk_about=["Did your prediction match?", "What else could you sort?", "What if the rule for smaller changed?"],
    grown_up="Complete the first sorting network lesson first. Prediction is the heart of this lesson.")

L["data-structures-for-searching__binary-search-trees"] = dict(
    summary="Children walk through a large tree drawn on the ground, turning over nodes, and learn how a binary search tree stores things so they are quick to find.",
    objectives=["Describe a binary search tree.", "Search a tree by going left or right.", "Compare it with searching a sorted list."],
    materials=["A big tree drawn on the ground with chalk or tape", "Large cards or plates with a number hidden underneath", "Space outside or in a hall"],
    steps=["Remind the class how binary search works on a sorted list.",
           "Show the tree: lines to follow and nodes with hidden numbers underneath.",
           "Pick a target. The child starts at the top node and turns it over.",
           "If the target is smaller, go left. If it is bigger, go right. Repeat until you find it.",
           "Let children arrange new numbers into their own tree shapes.",
           "Compare how many nodes you visit with searching a list."],
    talk_about=["Does the shape of the tree change the search?", "How is this different from binary search on a list?", "Where could a computer use a tree?"],
    grown_up="Children often mix up binary search and binary search trees. They share a half-at-a-time idea, but they are different. This is the most advanced lesson in the set.")
