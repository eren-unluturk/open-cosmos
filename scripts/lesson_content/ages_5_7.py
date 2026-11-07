"""Adapted lessons for ages 5-7 (CS Unplugged, CC BY-SA 4.0). Rewritten and shortened by Claude Code.
Key = '<topic>__<lesson-slug>' (matches the CS Unplugged repo). No pictures: the original page has them."""
L = {}

L["binary-numbers__how-binary-digits-work-junior"] = dict(
    summary="Children pretend to be tiny switches inside a computer. Cards with dots can be turned over, and together they show numbers.",
    objectives=["Understand that a computer uses things that are either on or off.", "Count with cards of 1, 2, 4 and 8 dots.", "Notice that each card has double the dots of the one before."],
    materials=["Four cards with 1, 2, 4 and 8 dots (draw them on paper)", "Four volunteers", "A clear space to stand in a line"],
    steps=["Tell the children a computer is full of tiny things that can be on or off, like a light switch. One of these is called a bit.",
           "Pick four children to be bits. Stand them in a row. Give the 1-dot card to the child on the right.",
           "Give the next child the 2-dot card. Ask: how many dots will the next card have? Let them guess without telling them they are wrong.",
           "Hand out the 4-dot and 8-dot cards. Talk about the pattern: each card has double the dots of the one before.",
           "Each bit can show its card or hide it (turn it over). Call out a number from 0 to 15 and let the bits show or hide cards to make it. Add up the dots you can see.",
           "Swap places so everyone gets a turn being a different bit."],
    talk_about=["What number do you get if every card is hidden?", "What is the biggest number the four cards can make?", "Where else do we see things that are just on or off?"],
    grown_up="Do not correct wrong guesses straight away. Keep going so the children discover the pattern. Counting dots one by one is fine.")

L["binary-numbers__codes-for-letters-using-binary-representation-junior"] = dict(
    summary="Children turn letters into numbers, and numbers into on and off cards, to send a secret message.",
    objectives=["See that computers store letters as numbers.", "Use five cards (1, 2, 4, 8, 16 dots) to make a number.", "Send and read a short coded word."],
    materials=["Five dot cards: 16, 8, 4, 2, 1", "An alphabet strip (A = 1, B = 2, and so on)", "Paper and pencil"],
    steps=["Ask: how does a computer know which letter to show? Count the letters of the alphabet together.",
           "Explain that A is 1, B is 2, C is 3, and so on.",
           "Put the five cards in a row, biggest on the left (16, 8, 4, 2, 1).",
           "Say a pattern such as No, Yes, No, No, No. The cards with Yes are on. Add the dots: that is 8, which is the letter H.",
           "Say No, Yes, No, No, Yes. That is 9, the letter I. Together they spell HI.",
           "Let the children choose a short word, work out its codes, and send it to a partner who decodes it."],
    talk_about=["Why do we need a fifth card?", "Could we use other words than yes and no, like up and down?", "What other things on a keyboard need a code?"],
    grown_up="Print an alphabet strip with numbers to help children who are still learning the order of letters. Start with two or three letters and build up.")

L["binary-numbers__reinforcing-sequencing-in-binary-number-systems-junior"] = dict(
    summary="Small groups make up a short play that counts in binary using two opposite things instead of dot cards.",
    objectives=["Show on and off with any two opposite things.", "Count from 0 up to 8 or more using four 'bits'.", "Take turns being each bit."],
    materials=["Anything with two states: hats on or off, loud or quiet sounds, two kinds of counters", "Groups of four children", "A phone or camera (optional)"],
    steps=["Talk about opposites: hot and cold, up and down, happy and sad. A computer uses on and off in the same way.",
           "In groups of four, choose how to show on and off. It must not be the dot cards.",
           "Each child picks one bit: 8, 4, 2 or 1. Line up from the biggest to the smallest.",
           "Practise counting from 1 to 8 together. Each bit turns on or off at the right moment.",
           "Swap roles so everyone has been each bit.",
           "Each group shows their play and the class works out the number they are showing."],
    talk_about=["What did your group use for on and off?", "Which bit changed the most often?", "Which number was hardest to show?"],
    grown_up="If a group has extra children, they can film the play or be the audience that guesses the number.")

L["error-detection-and-correction__parity-magic-junior"] = dict(
    summary="A card trick that shows how a computer can find a mistake and fix it by adding one extra row and one extra column.",
    objectives=["Know that computers can notice when data changes by mistake.", "Count and add cards in rows and columns.", "Use the trick to find a flipped card."],
    materials=["36 two-sided cards (for example black on one side and white on the other)", "A table or whiteboard", "A helper"],
    steps=["Tell the class you have a magic trick. Ask a helper to lay out a 5 by 5 square of cards, some black and some white, in any pattern.",
           "Say you will add one more row and one more column. Add cards so that every row and every column has an even number of black cards.",
           "Now you have a 6 by 6 square. Ask the class to close their eyes while the helper flips exactly one card.",
           "Look at each row and column. Find the row that has an odd number of black cards, and the column that has an odd number.",
           "The card where that row and column cross is the one that was flipped. Flip it back.",
           "Let pairs try the trick on their own."],
    talk_about=["Why does the trick always work?", "Where might a computer need to find mistakes, like a scratched disc or a QR code?"],
    grown_up="Practise the trick yourself first. Children enjoy a bit of magic patter. The aim is the idea that extra information lets a computer check itself.")

L["image-representation__colour-by-numbers"] = dict(
    summary="Children colour grids using rows of 0s and 1s, and learn that a computer stores a picture as numbers.",
    objectives=["Know that screen pictures are made of tiny squares called pixels.", "Decode a row of numbers into black and white squares.", "Understand that a picture can be stored as a list of numbers."],
    materials=["Printed colour-by-number grids where 1 means black and 0 means white", "Black pencils or felt tips", "Spare copies for mistakes"],
    steps=["Explain that screens are made of tiny squares called pixels (short for picture elements).",
           "Show a simple black and white picture. Each pixel is either black or white, so a computer only needs to remember which.",
           "Hand out a small grid. Each row has numbers. Colour a square black for 1 and leave it white for 0.",
           "Colour row by row. A picture should appear. Check with a neighbour.",
           "Try a bigger picture in a group, with each child doing some rows.",
           "Discuss: how did the numbers tell you the picture?"],
    talk_about=["What would happen if one number were wrong?", "How many numbers do you need for a bigger picture?", "How could we show colours instead of black and white?"],
    grown_up="A megapixel camera has a million pixels. Pencil is easier than pen because children can rub out mistakes. Look at the original lesson page for the printable pictures.")

L["image-representation__squeezing-pictures-into-less-space"] = dict(
    summary="Children shrink a picture by writing how many squares in a row are the same, a trick called run-length encoding.",
    objectives=["Understand that computers try to store pictures using less space.", "Count runs of the same colour in a row.", "Rebuild a picture from a short code."],
    materials=["Grid paper or printed 8 by 8 grids", "Black and white pencils", "A whiteboard"],
    steps=["Show an 8 by 8 picture made of black and white squares. Ask how you could describe it without naming every square.",
           "Teach the trick: instead of naming each square, count how many of the same colour come in a row.",
           "Do the first row together. Start with white. For example, 3 white then 2 black then 3 white becomes 3, 2, 3.",
           "Let children write the code for the other rows.",
           "Swap codes with a partner. Each partner colours the picture back from the code.",
           "Compare: did the code use fewer numbers than the 64 squares?"],
    talk_about=["Which pictures squeeze well, and which do not?", "Why do computers want to use less space?", "Where have you seen pictures that were sent or saved?"],
    grown_up="Always start with white so the code is clear. This idea is part of how pictures get small enough to send in messages.")

L["kidbots__fitness-unplugged"] = dict(
    summary="Groups invent their own picture 'programming language' of exercises and then program a friend to follow it.",
    objectives=["See that a programming language is a set of commands someone designed.", "Make picture cards that stand for actions.", "Put commands in order to make a program."],
    materials=["Plain cards or paper and felt tips", "A hula hoop and whiteboards (optional)", "Space to exercise safely"],
    steps=["Talk about who makes programming languages. Today the class will design its own fitness language.",
           "As a class, list exercises: running on the spot, star jumps, catching a bean bag.",
           "In groups of three, draw a GO card, four exercise cards and a finishing pose card.",
           "Lay the cards in a row with GO first and the finishing pose last.",
           "Groups walk round and try to work out what the other groups' cards mean. Some will be easy and some will need to be learned.",
           "Join back together: this is like real programming languages, where some things look familiar and others must be learned.",
           "Run a program: a group lays out cards and a friend does each exercise in order."],
    talk_about=["Which cards were easy to understand?", "What would you add to your language?", "What happens if the cards are in a different order?"],
    grown_up="Keep activities gentle and safe. The learning is about commands and order, not about how fast the exercise is.")

L["kidbots__rescue-mission"] = dict(
    summary="Children act as programmer, tester and robot on a floor grid, and learn why clear step-by-step instructions matter.",
    objectives=["Write a simple program with arrow commands.", "Find and fix mistakes (debugging).", "Understand that a robot only does what its instructions say."],
    materials=["A grid on the floor (chalk, masking tape or a chessboard pattern)", "Arrow cards or paper: forward, turn left, turn right", "An object to rescue"],
    steps=["Make a floor grid and put an object to rescue on one square.",
           "Choose three roles: the Developer who writes the program, the Tester who reads it out, and the Bot who follows it.",
           "Decide the commands: an arrow for forward, and left and right turns.",
           "The Developer writes the whole program first. The Bot cannot be steered while it walks.",
           "The Tester reads the commands one at a time and the Bot moves. Does the Bot reach the object?",
           "If not, find the bug together and fix the program. Debugging is part of the fun.",
           "Swap roles and try a new rescue."],
    talk_about=["Why must instructions be very clear?", "When did you get unclear instructions in real life?", "What was the bug and how did you fix it?"],
    grown_up="The teacher can play the Developer first to show the idea. Praise finding bugs, not just getting it right the first time.")

L["searching-algorithms__how-many-guesses-junior"] = dict(
    summary="Children search for a hidden number one card at a time and count how many guesses it takes.",
    objectives=["Understand searching means looking for one thing in a list.", "Predict and count the number of guesses.", "See that luck changes how many guesses you need."],
    materials=["15 cards with an animal on one side and a hidden number on the other, in no order", "Sticky notes", "A line on the board for predictions"],
    steps=["Ask: you lent a book to a friend and forgot who. You visit six houses. How many visits will you need?",
           "Each child writes a guess on a sticky note and puts it on a line from 1 to 6.",
           "Lay out 15 cards animal-side up. The numbers underneath are in no order.",
           "Pick a target number. A child turns over cards one at a time until they find it, while the class counts.",
           "Try again with different targets. Write the number of guesses each time.",
           "Look at the results. Was it ever the first card? The last?"],
    talk_about=["Is it ever fast to search when nothing is in order?", "What is the most guesses you could need?", "How could we make searching faster?"],
    grown_up="Change the numbers to match what the children are learning. It is good if the numbers are not neatly spread out.")

L["searching-algorithms__divide-and-conquer-junior"] = dict(
    summary="With cards in order from smallest to biggest, children find a number in only a few guesses.",
    objectives=["Know that sorted lists are quicker to search.", "Use the middle card to throw away half the cards at once.", "Compare with searching an unsorted list."],
    materials=["15 cards in order from lowest to highest, numbers between 1 and 100, animal side up", "A target number such as 52"],
    steps=["Lay out the 15 cards in order. Tell the children the numbers go from small to large.",
           "Ask them to find 52 by turning over as few cards as possible.",
           "Start in the middle. If the number is too small, the card you want is to the right. If too big, to the left.",
           "Throw away half the cards and look at the middle of what is left.",
           "Count the guesses with the class. It is only a few.",
           "Try other targets. Compare with last time, when the cards were not in order."],
    talk_about=["Why does sorting help?", "What would you do with 100 cards?", "What if the number is not in the list?"],
    grown_up="Avoid using numbers 1 to 15 in order, since children will just count along. Spread the numbers out.")

L["sorting-networks__reinforcing-numeracy-through-a-sorting-network-junior"] = dict(
    summary="Six children walk through a chalk network, comparing numbers at each box, until they end up in order.",
    objectives=["Compare two numbers and say which is smaller.", "Follow a step-by-step set of rules.", "See how six people can finish the job sooner than one."],
    materials=["A network of circles, lines and boxes drawn with chalk or tape", "Six number cards (1 to 6)", "Six children per turn"],
    steps=["Draw the network on the ground. Six circles at the start, lines that lead into boxes, six circles at the end.",
           "Give six children one number card each, in a mixed-up order, and let them stand at the start.",
           "Two children follow their lines until they meet at a box. They say hello and show their cards.",
           "The child with the smaller number leaves by the left line. The bigger leaves by the right.",
           "Everyone keeps following lines and meeting in boxes until they reach the end.",
           "Look: are they in order? Try again with new cards."],
    talk_about=["Which jobs go faster if more people help?", "Which do not?", "Did you need to know all the numbers to take part?"],
    grown_up="Only one team uses the network at a time while others watch. Later try fractions, bigger numbers or other things to sort.")

L["sorting-networks__investigating-variations-using-the-sorting-network-junior"] = dict(
    summary="Children try the sorting network with repeated numbers and with things that are not numbers, like heights.",
    objectives=["Predict what a program will do before running it.", "See that the network still works when two cards are the same.", "Sort things other than numbers."],
    materials=["The chalk sorting network from the first lesson", "Number cards with two the same, for example 1, 2, 3, 3, 4, 5", "Other things to sort: heights, colours, sizes"],
    steps=["Remind the class how the network works: meet in a box, smaller to the left, bigger to the right.",
           "Variation 1: use cards where two numbers are the same. Ask what happens when two equal cards meet. (It does not matter who goes where.)",
           "Ask the class to predict the ending, then run it. The equal cards end up next to each other.",
           "Variation 2: ask what else we could sort. Try heights, colours, or sizes.",
           "Run the network with one of those and check the result.",
           "Talk about what stayed the same each time."],
    talk_about=["Did you guess right?", "What can you sort besides numbers?", "Why does the network still work?"],
    grown_up="Do the first sorting network lesson first. Letting children predict is the key part.")
