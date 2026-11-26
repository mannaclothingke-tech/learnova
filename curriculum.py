"""Learnova curriculum and explicit prerequisite relationships."""

SKILLS = [
    {"id": "fractions", "name": "Fraction sense", "prerequisites": []},
    {"id": "expressions", "name": "Expressions", "prerequisites": ["fractions"]},
    {"id": "equations", "name": "Balancing equations", "prerequisites": ["expressions"]},
    {"id": "slope", "name": "Rate of change", "prerequisites": ["equations"]},
    {"id": "intercepts", "name": "Starting values", "prerequisites": ["slope"]},
    {"id": "models", "name": "Linear models", "prerequisites": ["intercepts"]},
]


def question(qid, prompt, answer, explanation, hint, choices=None):
    result = {
        "id": qid, "prompt": prompt, "answer": str(answer),
        "explanation": explanation, "hint": hint,
        "kind": "choice" if choices else "number",
    }
    if choices:
        result["choices"] = choices
    return result


LESSONS = [
    {
        "id": "fraction-sense", "skill": "fractions", "title": "Parts that add up",
        "subtitle": "See fractions as quantities, not just symbols.",
        "duration": 6, "color": "violet", "icon": "fraction",
        "intro": "A fraction describes equal parts of a whole. The denominator tells you "
                 "how many equal parts make the whole; the numerator tells you how many "
                 "you have. Two quarters cover the same amount as one half.",
        "takeaway": "Different fractions can describe the same quantity.",
        "visual": "fraction", "formula": "2 / 4 = 1 / 2",
        "exercises": [
            question("f1", "A ribbon is cut into 8 equal pieces. You take 4. What fraction "
                     "of the ribbon do you have?", "1/2",
                     "Four of eight equal pieces is 4/8, which simplifies to 1/2.",
                     "Pair the 8 pieces into two equal groups of 4.",
                     ["1/4", "1/2", "3/4", "1"]),
            question("f2", "What is 1/3 + 1/3? Enter a fraction.", "2/3",
                     "The pieces have the same size, so add the numerators: 2/3.",
                     "Keep the denominator 3. Count how many thirds you have."),
            question("f3", "A bottle holds 12 cups. It is 3/4 full. How many cups are in it?",
                     "9", "One quarter is 12 / 4 = 3 cups. Three quarters is 9 cups.",
                     "Find one quarter of 12 first, then multiply by 3."),
        ],
    },
    {
        "id": "expressions", "skill": "expressions", "title": "Give the unknown a name",
        "subtitle": "Turn a situation into an expression.",
        "duration": 7, "color": "peach", "icon": "expression",
        "intro": "A variable is a name for a number that can change. If a notebook costs "
                 "x coins, three notebooks cost 3x coins. Add a pen costing 2 coins, and "
                 "the total becomes 3x + 2. An expression describes a quantity; it does "
                 "not yet say what that quantity equals.",
        "takeaway": "An expression is a compact description of a quantity.",
        "visual": "expression", "formula": "3x + 2",
        "exercises": [
            question("e1", "A notebook costs x coins. Which expression describes 4 notebooks "
                     "and a 3-coin pen?", "4x + 3",
                     "Four notebooks cost 4x. The pen adds 3.", "Multiply x by the "
                     "number of notebooks, then add the pen.",
                     ["4 + x + 3", "4x + 3", "3x + 4", "4(x + 3)"]),
            question("e2", "Evaluate 3x + 2 when x = 5.", "17",
                     "Replace x with 5: 3 times 5 plus 2 is 17.",
                     "Multiplication comes before addition."),
            question("e3", "Simplify 2x + 3x. What is the coefficient of x?", "5",
                     "Two groups of x plus three groups of x makes five groups of x.",
                     "Combine the counts of the same variable."),
        ],
    },
    {
        "id": "balance", "skill": "equations", "title": "Keep the balance",
        "subtitle": "Discover why equation-solving moves work.",
        "duration": 8, "color": "mint", "icon": "balance",
        "intro": "An equation says two quantities are equal. Imagine a balanced scale: "
                 "removing the same weight from both sides keeps it balanced. To solve "
                 "2x + 4 = 12, subtract 4 on both sides to get 2x = 8. Then divide both "
                 "sides by 2, giving x = 4. Check by putting 4 back into the original equation.",
        "takeaway": "Do the same operation to both sides to preserve equality.",
        "visual": "balance", "formula": "2x + 4 = 12",
        "exercises": [
            question("b1", "Solve x + 7 = 15. What is x?", "8",
                     "Subtract 7 from both sides: x = 15 - 7 = 8.",
                     "Undo adding 7 by subtracting 7 from both sides."),
            question("b2", "Solve 3x = 21.", "7",
                     "Divide both sides by 3: x = 7.", "Undo multiplication by 3."),
            question("b3", "Solve 2x + 3 = 13.", "5",
                     "Subtract 3 to get 2x = 10, then divide by 2.",
                     "Undo the addition first, then the multiplication."),
        ],
    },
    {
        "id": "slope", "skill": "slope", "title": "Watch the change",
        "subtitle": "Make rate of change something you can see.",
        "duration": 8, "color": "blue", "icon": "graph",
        "intro": "Slope measures how much y changes when x increases by one. A line with "
                 "slope 2 rises 2 units for every step to the right. A negative slope "
                 "falls instead. Between two points, divide the change in y by the "
                 "change in x. Try changing the slope in the canvas below.",
        "takeaway": "Slope = change in y / change in x.",
        "visual": "graph", "formula": "m = (y2 - y1) / (x2 - x1)",
        "exercises": [
            question("s1", "A line passes through (0, 1) and (2, 5). What is its slope?",
                     "2", "The rise is 4 and the run is 2. Slope is 4/2 = 2.",
                     "Find the change in each coordinate, then divide rise by run."),
            question("s2", "A line has slope -3. When x increases by 2, how much does y "
                     "change? Include the sign.", "-6",
                     "The change in y is slope times change in x: -3 times 2 = -6.",
                     "For each step right, y falls by 3."),
            question("s3", "Which line gets steeper as it rises?", "y = 4x",
                     "A slope of 4 rises more per step than a slope of 1 or 2.",
                     "Compare the coefficients of x.",
                     ["y = x", "y = 2x", "y = 4x", "y = 0x"]),
        ],
    },
    {
        "id": "intercepts", "skill": "intercepts", "title": "Where the story starts",
        "subtitle": "Find the meaning of a line's starting value.",
        "duration": 6, "color": "yellow", "icon": "graph",
        "intro": "In y = mx + b, the number b is the value of y when x is zero. It is "
                 "the y-intercept, where the line crosses the vertical axis. A taxi "
                 "charging 4 coins to start and 2 coins per kilometre follows y = 2x + 4. "
                 "Its starting charge changes the intercept, not the slope.",
        "takeaway": "The intercept is the output when the input is zero.",
        "visual": "graph", "formula": "y = mx + b",
        "exercises": [
            question("i1", "What is the y-intercept of y = 3x + 5?", "5",
                     "Set x to 0. Then y = 5.", "Look for the constant term."),
            question("i2", "A line follows y = -2x + 7. What is y when x = 0?", "7",
                     "The x term becomes zero, leaving 7.", "Multiply -2 by 0."),
            question("i3", "You start with 6 coins and earn 3 per day. Which equation gives "
                     "your coins y after x days?", "y = 3x + 6",
                     "Daily earnings give the slope 3; starting coins give the intercept 6.",
                     "Which number changes each day and which is present at day zero?",
                     ["y = 6x + 3", "y = 3x + 6", "y = 9x", "y = 3x - 6"]),
        ],
    },
    {
        "id": "models", "skill": "models", "title": "Build a model",
        "subtitle": "Use a line to explain a real-world situation.",
        "duration": 9, "color": "violet", "icon": "graph",
        "intro": "A linear model combines a starting value and a constant rate of change. "
                 "A plant is 5 cm tall and grows 2 cm each week, so its height after x "
                 "weeks is y = 2x + 5. Models make predictions under assumptions: this "
                 "one assumes the plant keeps growing at the same rate.",
        "takeaway": "State the starting value, the rate, and the assumptions.",
        "visual": "graph", "formula": "height = 2 x weeks + 5",
        "exercises": [
            question("m1", "A plant starts at 5 cm and grows 2 cm each week. How tall is "
                     "it after 4 weeks?", "13",
                     "Height is 5 + 2 times 4 = 13 cm.",
                     "Add four weeks of growth to the starting height."),
            question("m2", "A tank starts with 20 litres and loses 3 litres per minute. "
                     "How many litres remain after 4 minutes?", "8",
                     "20 - 3 times 4 = 8 litres.", "The rate is negative because "
                     "water is leaving."),
            question("m3", "A service costs 8 coins to start and 2 coins per hour. "
                     "For how many hours does a total of 18 coins pay?", "5",
                     "Solve 2x + 8 = 18: subtract 8, then divide by 2.",
                     "Remove the starting charge from the total first."),
        ],
    },
]

DIAGNOSTIC = [
    ("fractions", question("d-f1", "What is 1/4 + 1/4? Enter a fraction.", "1/2",
                           "Two quarters make one half.", "Count the quarters.")),
    ("fractions", question("d-f2", "What is 1/2 of 10?", "5",
                           "Divide 10 into two equal groups.", "Split 10 equally.")),
    ("expressions", question("d-e1", "Evaluate 2x + 1 when x = 4.", "9",
                             "2 times 4 plus 1 is 9.", "Replace x with 4.")),
    ("expressions", question("d-e2", "What is the coefficient of x in 3x + 4x?", "7",
                             "3 + 4 = 7.", "Count the groups of x.")),
    ("equations", question("d-b1", "Solve x + 6 = 14.", "8",
                            "Subtract 6 from both sides.", "Undo adding 6.")),
    ("equations", question("d-b2", "Solve 4x = 24.", "6",
                            "Divide both sides by 4.", "Undo multiplying by 4.")),
    ("slope", question("d-s1", "A line rises 6 units over a run of 3. What is its slope?",
                        "2", "6 / 3 = 2.", "Divide rise by run.")),
    ("slope", question("d-s2", "For y = -2x + 4, how much does y change when x increases "
                        "by 1?", "-2", "The coefficient of x is the slope.",
                        "Read the coefficient of x.")),
    ("intercepts", question("d-i1", "What is the y-intercept of y = 5x + 3?", "3",
                             "At x = 0, y = 3.", "Set x to zero.")),
    ("intercepts", question("d-i2", "For y = x - 4, what is y when x = 0?", "-4",
                             "0 - 4 = -4.", "Substitute zero for x.")),
    ("models", question("d-m1", "You start with 3 coins and gain 2 per day. How many "
                         "coins after 5 days?", "13", "3 + 2 times 5 = 13.",
                         "Add growth to the starting amount.")),
    ("models", question("d-m2", "A candle is 15 cm tall and loses 2 cm per hour. "
                         "How tall is it after 3 hours?", "9",
                         "15 - 2 times 3 = 9.", "Subtract the amount lost.")),
]

SKILLS.extend([
    {"id": "frac-parts", "name": "Equal parts and fraction size", "prerequisites": []},
    {"id": "frac-equivalence", "name": "Equivalent fractions", "prerequisites": ["frac-parts"]},
    {"id": "frac-comparison", "name": "Comparing fractions", "prerequisites": ["frac-equivalence"]},
    {"id": "frac-addition", "name": "Adding fractions", "prerequisites": ["frac-equivalence"]},
    {"id": "frac-subtraction", "name": "Subtracting fractions", "prerequisites": ["frac-addition"]},
    {"id": "frac-quantities", "name": "Fractions of quantities", "prerequisites": ["frac-parts"]},
])

FRACTION_LESSONS = [
    {
        "id": "fraction-parts", "skill": "frac-parts", "title": "A whole, shared equally",
        "subtitle": "Give the whole a size before counting its parts.",
        "duration": 8, "color": "violet", "icon": "fraction",
        "intro": "A fraction needs a clearly defined whole and equal-sized parts. In 3/5, "
                 "the whole is split into five equal parts and three are selected. The "
                 "denominator names the size of each part; the numerator counts them. "
                 "One eighth of the same whole is smaller than one quarter because the "
                 "whole has been divided more finely. Fractions can also reach beyond "
                 "one: 5/4 is one whole and one extra quarter. Move the explorer's sliders "
                 "and watch the same quantity appear as a bar and a point.",
        "takeaway": "Define the whole, make equal parts, then count them.",
        "visual": "fraction-explorer", "formula": "numerator / denominator",
        "exercises": [
            question("fp1", "A strip is split into 5 equal parts. Three are colored. What fraction is colored?",
                     "3/5", "Three selected parts out of five equal parts gives 3/5.",
                     "The total number of equal parts is the denominator."),
            question("fp2", "A cake is cut into unequal slices. Can counting 2 of its 4 slices alone prove you have half the cake?",
                     "No", "Counting slices works only when those slices are equal in size.",
                     "Could the two slices be much larger than the other two?", ["Yes", "No"]),
            question("fp3", "For the same whole, which single piece is larger?", "1/3",
                     "Dividing a whole into three parts gives larger pieces than dividing it into seven.",
                     "Imagine sharing the same loaf among three people or seven people.", ["1/3", "1/7", "They are equal"]),
            question("fp4", "How many thirds make one whole?", "3",
                     "Three pieces of size 1/3 cover the whole: 3/3 = 1.",
                     "The denominator tells you the number of equal pieces in one whole."),
            question("fp5", "You have five quarter-length pieces. What fraction of one original length do you have?",
                     "5/4", "Five pieces of size 1/4 total 5/4, which is one whole and one quarter.",
                     "A numerator can be larger than its denominator."),
        ],
    },
    {
        "id": "fraction-equivalence", "skill": "frac-equivalence", "title": "Same amount, new pieces",
        "subtitle": "Change the partition without changing the quantity.",
        "duration": 9, "color": "mint", "icon": "fraction",
        "intro": "Cut each of three equal pieces in half. The whole now has six pieces, "
                 "and a quantity that covered two thirds covers four sixths. Both the "
                 "selected count and the total count doubled: 2/3 = 4/6. Multiplying or "
                 "dividing the numerator and denominator by the same nonzero number "
                 "preserves the quantity. To simplify 6/8, divide both counts by 2. "
                 "The explorer shows the selected amount again with twice as many pieces.",
        "takeaway": "Scale both counts together to keep the amount unchanged.",
        "visual": "fraction-explorer", "formula": "2/3 = 4/6",
        "exercises": [
            question("fe1", "Fill the missing numerator: 2/3 = ?/12.", "8",
                     "The denominator multiplied by 4, so the numerator also multiplies by 4.",
                     "What takes 3 to 12? Do that to 2."),
            question("fe2", "Simplify 6/8. Enter the equivalent fraction.", "3/4",
                     "Dividing both counts by 2 gives 3/4. Equivalent forms represent the same amount.",
                     "Find a number that divides both 6 and 8."),
            question("fe3", "Which fraction is equivalent to 3/5?", "9/15",
                     "Multiplying numerator and denominator by 3 gives 9/15.",
                     "Check whether both counts were scaled by the same factor.", ["3/10", "9/15", "6/5", "5/3"]),
            question("fe4", "To turn 1/2 into 2/4, by what factor are both counts multiplied?", "2",
                     "Both 1 and 2 are multiplied by 2. The fraction's value stays the same.",
                     "Compare the old and new numerators."),
            question("fe5", "Simplify 15/20.", "3/4",
                     "Divide numerator and denominator by 5: 15/20 = 3/4.",
                     "Both counts are multiples of 5."),
        ],
    },
    {
        "id": "fraction-comparison", "skill": "frac-comparison", "title": "Which amount is greater?",
        "subtitle": "Compare equal wholes using equal-sized pieces.",
        "duration": 9, "color": "blue", "icon": "fraction",
        "intro": "With the same denominator, more pieces means a greater quantity: "
                 "5/8 is greater than 3/8. With different denominators, rename the "
                 "fractions using a common denominator. For 2/3 and 3/4, twelfths work: "
                 "8/12 is less than 9/12. A number line orders the quantities from left "
                 "to right. Always compare the same whole: half of a large loaf need "
                 "not weigh less than three quarters of a tiny loaf.",
        "takeaway": "Use equal-sized pieces or positions on one number line.",
        "visual": "fraction-explorer", "formula": "2/3 = 8/12 < 9/12 = 3/4",
        "exercises": [
            question("fc1", "Which is greater for the same whole?", "5/8",
                     "Both use eighths; five eighths is greater than three eighths.",
                     "The pieces already have the same size.", ["3/8", "5/8", "They are equal"]),
            question("fc2", "Compare 2/3 and 3/4. Choose the correct relation.", "2/3 < 3/4",
                     "In twelfths, 2/3 = 8/12 and 3/4 = 9/12.",
                     "Rewrite both fractions with denominator 12.", ["2/3 < 3/4", "2/3 = 3/4", "2/3 > 3/4"]),
            question("fc3", "Which is closer to 1 on the number line?", "7/8",
                     "7/8 is one eighth short of 1; 3/4 is two eighths short.",
                     "Compare the missing amounts, not just the numerators.", ["3/4", "7/8", "They are equally close"]),
            question("fc4", "Which fraction lies between 1/4 and 3/4?", "1/2",
                     "1/2 = 2/4, which lies between 1/4 and 3/4.",
                     "Think in quarters.", ["1/8", "1/2", "7/8"]),
            question("fc5", "Does half of a large pizza necessarily contain less food than three quarters of a small pizza?",
                     "No", "The wholes differ in size, so the fractions alone do not determine the food amounts.",
                     "Are you comparing fractions of equal-sized wholes?", ["Yes", "No"]),
        ],
    },
    {
        "id": "fraction-addition", "skill": "frac-addition", "title": "Put the pieces together",
        "subtitle": "Add quantities without changing the size of a piece.",
        "duration": 10, "color": "peach", "icon": "fraction",
        "intro": "Two fifths plus one fifth is three fifths: add the counts, not the "
                 "piece size. For different denominators, make the pieces match first. "
                 "A half and a third become three sixths and two sixths, totaling five "
                 "sixths. Adding the denominators would invent a new piece size. "
                 "Sometimes a sum crosses one whole: 3/4 + 1/2 = 3/4 + 2/4 = 5/4.",
        "takeaway": "Rename to a common denominator, then add the numerators.",
        "visual": "fraction-explorer", "formula": "1/2 + 1/3 = 3/6 + 2/6 = 5/6",
        "exercises": [
            question("fa1", "What is 2/5 + 1/5?", "3/5",
                     "Two fifths plus one fifth is three fifths.",
                     "Keep the piece size; combine the counts."),
            question("fa2", "What is 1/2 + 1/3?", "5/6",
                     "Use sixths: 3/6 + 2/6 = 5/6.",
                     "Six is a multiple of both denominators."),
            question("fa3", "What is 3/4 + 1/2?", "5/4",
                     "Rename 1/2 as 2/4. Then 3/4 + 2/4 = 5/4.",
                     "Your answer can be greater than one."),
            question("fa4", "A learner says 1/4 + 1/4 = 2/8. Which correction explains the mistake?",
                     "Keep quarters: the sum is 2/4", "Adding quantities does not turn quarters into eighths.",
                     "What size are the pieces you are counting?",
                     ["Keep quarters: the sum is 2/4", "Add denominators only: the sum is 1/8", "The learner is correct"]),
            question("fa5", "You walk 2/3 km, then 1/6 km. How many kilometres do you walk in total?",
                     "5/6", "2/3 = 4/6. Add 1/6 to get 5/6 km.",
                     "Express both distances in sixths."),
        ],
    },
    {
        "id": "fraction-subtraction", "skill": "frac-subtraction", "title": "What is left?",
        "subtitle": "Subtract matching pieces and check by adding back.",
        "duration": 9, "color": "yellow", "icon": "fraction",
        "intro": "If five sixths of a ribbon remain and you use two sixths, three "
                 "sixths remain. With unlike denominators, rename before subtracting: "
                 "3/4 - 1/6 = 9/12 - 2/12 = 7/12. A mixed number describes a whole "
                 "plus a fraction: 1 1/2 is 3/2. Check a subtraction by adding the "
                 "removed amount back to the remainder.",
        "takeaway": "Subtract equal-sized pieces; add back to check the result.",
        "visual": "fraction-explorer", "formula": "3/4 - 1/6 = 9/12 - 2/12 = 7/12",
        "exercises": [
            question("fs1", "What is 5/6 - 2/6?", "1/2",
                     "Three sixths remain, and 3/6 = 1/2.",
                     "Subtract the counts of sixths."),
            question("fs2", "What is 3/4 - 1/6?", "7/12",
                     "9/12 - 2/12 = 7/12.",
                     "Twelve is a common denominator."),
            question("fs3", "What is 1 - 3/8?", "5/8",
                     "Write the whole as 8/8. Removing 3/8 leaves 5/8.",
                     "How many eighths are in one whole?"),
            question("fs4", "A rope is 1 1/2 metres long. You cut off 3/4 metre. How many metres remain?",
                     "3/4", "1 1/2 = 6/4. Subtracting 3/4 leaves 3/4 metre.",
                     "Write the mixed number as quarters."),
            question("fs5", "Which addition checks that 5/6 - 1/3 = 1/2?", "1/2 + 1/3 = 5/6",
                     "Remainder plus removed amount must equal the starting amount.",
                     "Undo subtraction by adding the removed amount.",
                     ["1/2 + 1/3 = 5/6", "5/6 + 1/3 = 1/2", "1/2 + 5/6 = 1/3"]),
        ],
    },
    {
        "id": "fraction-quantities", "skill": "frac-quantities", "title": "A fraction of a collection",
        "subtitle": "Turn part of a whole into a measurable amount.",
        "duration": 9, "color": "mint", "icon": "fraction",
        "intro": "To find 3/4 of 20 objects, split 20 into four equal groups and take "
                 "three: 20 / 4 = 5, then 3 times 5 = 15. The same reasoning works "
                 "for measured amounts: half of 7 litres is 3.5 litres. To recover "
                 "a whole from a known fraction, reverse the process. If 3/4 of a "
                 "collection is 18, one quarter is 6 and the whole is 24. In the "
                 "explorer, change the whole amount separately from the fraction.",
        "takeaway": "Divide by the denominator, then multiply by the numerator.",
        "visual": "fraction-explorer", "formula": "3/4 of 20 = (20 / 4) x 3 = 15",
        "exercises": [
            question("fq1", "What is 3/4 of 20?", "15",
                     "One quarter is 5. Three quarters is 15.",
                     "Divide 20 into four equal groups."),
            question("fq2", "What is 2/3 of 18?", "12",
                     "18 / 3 = 6, and 2 times 6 = 12.",
                     "Find one third first."),
            question("fq3", "What is half of 7 litres? Enter the number of litres.", "7/2",
                     "7 / 2 = 3.5 litres. Measured amounts need not be whole numbers.",
                     "A fraction or decimal is acceptable."),
            question("fq4", "Three quarters of a collection is 18. How many objects are in the whole collection?",
                     "24", "One quarter is 18 / 3 = 6, so four quarters is 24.",
                     "Recover one quarter before finding all four quarters."),
            question("fq5", "You use 2/5 of a 30-metre roll. How many metres are left?",
                     "18", "You use 12 metres, leaving 30 - 12 = 18 metres.",
                     "The fraction left is 3/5."),
        ],
    },
]
LESSONS.extend(FRACTION_LESSONS)

PRACTICE = {
    "fraction-parts": [
        question("pp1", "Seven of ten equal tiles are blue. What fraction is blue?", "7/10", "Seven tenths are blue.", "Count selected tiles out of all tiles."),
        question("pp2", "How many sixths make two wholes?", "12", "Six sixths per whole, twice, makes twelve.", "Count six pieces for each whole."),
        question("pp3", "Which is smaller for the same whole?", "1/9", "More equal partitions make smaller pieces.", "Compare piece sizes.", ["1/4", "1/9"]),
        question("pp4", "Eight fifth-length pieces make what fraction of one original length?", "8/5", "Eight pieces, each one fifth, total 8/5.", "Count pieces of size 1/5."),
    ],
    "fraction-equivalence": [
        question("pe1", "Fill the numerator: 3/4 = ?/16.", "12", "Multiply both counts by 4.", "Four becomes sixteen by multiplying by 4."),
        question("pe2", "Simplify 14/21.", "2/3", "Divide both counts by 7.", "Find a common factor of 14 and 21."),
        question("pe3", "Which fraction equals 4/6?", "2/3", "Dividing both counts by 2 gives 2/3.", "Scale numerator and denominator together.", ["2/3", "4/3", "2/6"]),
        question("pe4", "Fill the denominator: 5/6 = 20/? .", "24", "The numerator multiplied by 4; the denominator must too.", "Apply the same factor to 6."),
    ],
    "fraction-comparison": [
        question("pc1", "Which is greater: 4/5 or 7/10?", "4/5", "4/5 = 8/10, which is greater than 7/10.", "Rename fifths as tenths.", ["4/5", "7/10"]),
        question("pc2", "Which lies between 1/2 and 1?", "5/8", "5/8 is greater than 4/8 and less than 8/8.", "Use eighths as common pieces.", ["1/4", "5/8", "9/8"]),
        question("pc3", "Which is farther to the right on one number line?", "5/4", "5/4 is greater than 1; 4/5 is less than 1.", "Compare each fraction to one.", ["4/5", "5/4"]),
        question("pc4", "Compare 5/6 and 10/12.", "Equal", "Scaling both counts by 2 gives 10/12.", "Look for equivalent fractions.", ["5/6 is greater", "10/12 is greater", "Equal"]),
    ],
    "fraction-addition": [
        question("pa1", "What is 3/8 + 2/8?", "5/8", "Add the counts of eighths.", "Keep denominator 8."),
        question("pa2", "What is 2/5 + 1/2?", "9/10", "4/10 + 5/10 = 9/10.", "Use tenths."),
        question("pa3", "What is 5/6 + 1/3?", "7/6", "5/6 + 2/6 = 7/6.", "The sum can exceed one."),
        question("pa4", "What is 1/4 + 2/3?", "11/12", "3/12 + 8/12 = 11/12.", "Use twelfths."),
    ],
    "fraction-subtraction": [
        question("ps1", "What is 7/10 - 3/10?", "2/5", "4/10 = 2/5.", "Subtract tenths, then simplify."),
        question("ps2", "What is 5/6 - 1/4?", "7/12", "10/12 - 3/12 = 7/12.", "Use twelfths."),
        question("ps3", "What is 2 - 3/5?", "7/5", "Two wholes are 10/5, leaving 7/5.", "Rename both wholes as fifths."),
        question("ps4", "What is 7/8 - 1/2?", "3/8", "7/8 - 4/8 = 3/8.", "Half is four eighths."),
    ],
    "fraction-quantities": [
        question("pq1", "What is 5/6 of 24?", "20", "One sixth is 4; five sixths is 20.", "Divide by 6, then multiply by 5."),
        question("pq2", "Two thirds of a bag is 14 kg. What is the whole bag's mass in kg?", "21", "One third is 7 kg, so three thirds is 21 kg.", "Find one third of the whole."),
        question("pq3", "What is 3/5 of 25?", "15", "25 / 5 times 3 = 15.", "Find one fifth first."),
        question("pq4", "A bottle contains 9 litres. You pour out 1/3. How many litres remain?", "6", "You pour 3 litres and retain 6.", "Two thirds remain."),
    ],
}

COURSE_ASSESSMENTS = {"fractions": [
    ("fraction-parts", question("ap1", "Nine of twelve equal parts are selected. What fraction is selected?", "3/4", "9/12 simplifies to 3/4.", "Count equal parts.")),
    ("fraction-parts", question("ap2", "Which is larger for the same whole?", "1/5", "Fifths are larger pieces than elevenths.", "Compare equal partitions.", ["1/5", "1/11"])),
    ("fraction-equivalence", question("ae1", "Fill the numerator: 5/8 = ?/24.", "15", "Both counts multiply by 3.", "Use the same scale factor.")),
    ("fraction-equivalence", question("ae2", "Simplify 18/30.", "3/5", "Divide both counts by 6.", "Look for a common factor.")),
    ("fraction-comparison", question("ac1", "Which is greater: 7/12 or 2/3?", "2/3", "2/3 = 8/12, greater than 7/12.", "Use twelfths.", ["7/12", "2/3"])),
    ("fraction-comparison", question("ac2", "Which lies between 1/3 and 2/3?", "1/2", "In sixths, 2/6 < 3/6 < 4/6.", "Use sixths.", ["1/6", "1/2", "5/6"])),
    ("fraction-addition", question("aa1", "What is 1/6 + 1/4?", "5/12", "2/12 + 3/12 = 5/12.", "Use twelfths.")),
    ("fraction-addition", question("aa2", "What is 4/5 + 3/10?", "11/10", "8/10 + 3/10 = 11/10.", "Use tenths.")),
    ("fraction-subtraction", question("as1", "What is 11/12 - 1/3?", "7/12", "11/12 - 4/12 = 7/12.", "Use twelfths.")),
    ("fraction-subtraction", question("as2", "What is 1 1/4 - 1/2?", "3/4", "5/4 - 2/4 = 3/4.", "Use quarters.")),
    ("fraction-quantities", question("aq1", "What is 3/8 of 32?", "12", "One eighth is 4; three eighths is 12.", "Find one eighth.")),
    ("fraction-quantities", question("aq2", "Two fifths of a collection is 16. How large is the whole collection?", "40", "One fifth is 8; five fifths is 40.", "Recover one fifth.")),
]}

SKILLS.extend([
    {"id": "eq-balance", "name": "Equality and solutions", "prerequisites": []},
    {"id": "eq-addsub", "name": "Undoing addition and subtraction", "prerequisites": ["eq-balance"]},
    {"id": "eq-muldiv", "name": "Undoing multiplication and division", "prerequisites": ["eq-balance"]},
    {"id": "eq-twostep", "name": "Two-step equations", "prerequisites": ["eq-addsub", "eq-muldiv"]},
    {"id": "eq-multistep", "name": "Combining and distributing terms", "prerequisites": ["eq-twostep"]},
    {"id": "eq-modeling", "name": "Equations in context", "prerequisites": ["eq-twostep"]},
])

EQUATION_LESSONS = [
    {
        "id": "equation-meaning", "skill": "eq-balance", "title": "Equal means balanced",
        "subtitle": "Treat an equation as a true statement about two quantities.",
        "duration": 8, "color": "mint", "icon": "balance",
        "intro": "An equation says that two expressions have the same value. In "
                 "x + 3 = 10, the letter stands for an unknown number. A solution is a "
                 "number that makes the statement true: replacing x with 7 gives 10 = 10. "
                 "Replacing x with 5 gives 8 = 10, which is false. A balanced scale is a "
                 "useful picture because any change must keep both sides equally heavy. "
                 "Adding, subtracting, multiplying by, or dividing by the same nonzero "
                 "amount on both sides preserves equality. Use the explorer to change the "
                 "equation and watch each balanced step.",
        "takeaway": "A solution makes both sides equal; valid steps change both sides alike.",
        "visual": "equation-explorer", "formula": "x + 3 = 10",
        "exercises": [
            question("lb1", "Which value of x makes x + 3 = 10 true?", "7",
                     "Substituting 7 gives 7 + 3 = 10, so both sides match.",
                     "Replace x with each choice and compare the two sides.", ["5", "7", "13", "30"]),
            question("lb2", "Is x = 4 a solution of 2x + 1 = 10?", "No",
                     "With x = 4, the left side is 2 times 4 plus 1, which is 9. It does not equal 10.",
                     "Substitute 4 and evaluate the left side.", ["Yes", "No"]),
            question("lb3", "A scale is balanced with x + 5 on the left and 12 on the right. You remove 5 from both sides. What number is on the right?",
                     "7", "Removing 5 from each side keeps the scale balanced: 12 - 5 = 7.",
                     "Do the same subtraction to the right side."),
            question("lb4", "Which step keeps the equation 3x = 12 balanced?", "Divide both sides by 3",
                     "A valid step changes both sides in the same way. Dividing both sides by 3 gives x = 4.",
                     "Look for an operation applied to both sides.",
                     ["Subtract 3 from the left side only", "Divide both sides by 3",
                      "Add 3 to the left and subtract 3 from the right", "Multiply only the left side by 3"]),
            question("lb5", "To check x = 5 in 3x - 2 = 13, what is the value of 3x - 2 when x = 5?",
                     "13", "3 times 5 is 15, and 15 - 2 is 13. This matches the right side.",
                     "Evaluate multiplication before subtraction."),
        ],
    },
    {
        "id": "equation-addsub", "skill": "eq-addsub", "title": "Undo adding and subtracting",
        "subtitle": "Use inverse operations to isolate the unknown.",
        "duration": 8, "color": "violet", "icon": "balance",
        "intro": "Addition and subtraction undo each other. If x + 9 = 20, subtract 9 "
                 "from both sides to isolate x. If x - 6 = 10, add 6 to both sides. The "
                 "result can be negative: x + 9 = 4 gives x = -5. The unknown may also "
                 "appear on the right, as in 15 = x + 6; the same balance reasoning applies. "
                 "After solving, substitute your answer into the original equation to check it.",
        "takeaway": "Undo the operation attached to x, on both sides, then check.",
        "visual": "equation-explorer", "formula": "x + 9 = 20  =>  x = 11",
        "exercises": [
            question("la1", "Solve x + 12 = 20.", "8", "Subtract 12 from both sides: x = 20 - 12 = 8.",
                     "Undo adding 12."),
            question("la2", "Solve x - 7 = 5.", "12", "Add 7 to both sides: x = 5 + 7 = 12.",
                     "Undo subtracting 7."),
            question("la3", "Solve x + 9 = 4.", "-5", "Subtract 9 from both sides: x = 4 - 9 = -5.",
                     "The result may be below zero."),
            question("la4", "Solve 15 = x + 6.", "9", "Subtract 6 from both sides: 9 = x.",
                     "The unknown can be on the right-hand side."),
            question("la5", "Solve x - 1/2 = 3/4.", "5/4", "Add 1/2 to both sides: x = 3/4 + 2/4 = 5/4.",
                     "Use a common denominator for the addition."),
        ],
    },
    {
        "id": "equation-muldiv", "skill": "eq-muldiv", "title": "Undo multiplying and dividing",
        "subtitle": "Divide to undo multiplication; multiply to undo division.",
        "duration": 9, "color": "peach", "icon": "balance",
        "intro": "In 4x = 28, the unknown is multiplied by 4. Divide both sides by 4 to "
                 "get x = 7. In x / 5 = 6, the unknown is divided by 5, so multiply both "
                 "sides by 5 to get x = 30. A negative coefficient works the same way: "
                 "-3x = 12 gives x = -4. When the coefficient is a fraction, multiplying by "
                 "its reciprocal gives a coefficient of 1: if (3/4)x = 9, multiply by 4/3.",
        "takeaway": "Multiply or divide both sides to make the coefficient of x equal to 1.",
        "visual": "equation-explorer", "formula": "4x = 28  =>  x = 7",
        "exercises": [
            question("lm1", "Solve 4x = 28.", "7", "Divide both sides by 4: x = 7.", "Undo multiplying by 4."),
            question("lm2", "Solve x / 5 = 6.", "30", "Multiply both sides by 5: x = 30.", "Undo dividing by 5."),
            question("lm3", "Solve -3x = 12.", "-4", "Divide both sides by -3: x = -4.",
                     "Keep track of the sign of the coefficient."),
            question("lm4", "Solve 2x = 7. Enter a fraction or decimal.", "7/2", "Divide both sides by 2: x = 7/2.",
                     "The solution need not be a whole number."),
            question("lm5", "Solve (3/4)x = 9.", "12", "Multiply both sides by 4/3: x = 9 times 4/3 = 12.",
                     "Use the reciprocal of 3/4."),
        ],
    },
    {
        "id": "equation-two-step", "skill": "eq-twostep", "title": "Undo in reverse order",
        "subtitle": "Peel away operations one layer at a time.",
        "duration": 10, "color": "blue", "icon": "balance",
        "intro": "To evaluate 2x + 3, you multiply first, then add. To solve "
                 "2x + 3 = 13, undo the operations in reverse order. First subtract 3 from "
                 "both sides to get 2x = 10. Then divide both sides by 2 to get x = 5. The "
                 "same plan works with subtraction, division, and negative coefficients: "
                 "5 - 4x = -7 becomes -4x = -12, then x = 3. A solution is trusted only "
                 "after you substitute it back.",
        "takeaway": "Undo addition or subtraction first, then undo the coefficient.",
        "visual": "equation-explorer", "formula": "2x + 3 = 13  =>  2x = 10  =>  x = 5",
        "exercises": [
            question("lt1", "Solve 2x + 3 = 13.", "5", "Subtract 3 to get 2x = 10, then divide by 2.",
                     "Undo the addition before the multiplication."),
            question("lt2", "Solve 3x - 4 = 11.", "5", "Add 4 to get 3x = 15, then divide by 3.",
                     "Undo subtracting 4 first."),
            question("lt3", "Solve x / 2 + 1 = 6.", "10", "Subtract 1 to get x / 2 = 5, then multiply by 2.",
                     "Remove the +1 before undoing division."),
            question("lt4", "Solve 5 - 4x = -7.", "3", "Subtract 5 to get -4x = -12, then divide by -4.",
                     "The coefficient of x is -4."),
            question("lt5", "Which first step is a valid way to begin solving 4x + 6 = 30?",
                     "Subtract 6 from both sides",
                     "Subtracting 6 from both sides gives 4x = 24 and preserves equality.",
                     "A valid step applies the same operation to both sides.",
                     ["Subtract 6 from only the left side", "Subtract 6 from both sides",
                      "Divide only 4x by 4", "Add 6 to both sides"]),
        ],
    },
    {
        "id": "equation-multistep", "skill": "eq-multistep", "title": "Tidy before you solve",
        "subtitle": "Combine like terms, distribute, and gather x terms.",
        "duration": 10, "color": "yellow", "icon": "balance",
        "intro": "Tidy an equation before undoing operations. Like terms combine: "
                 "3x + 2x is 5x. The distributive idea says 2(x + 3) means two copies of "
                 "x + 3, so it equals 2x + 6. When x appears on both sides, subtract the "
                 "smaller x term from both sides to gather the unknown on one side. For "
                 "4x + 1 = x + 10, subtract x to get 3x + 1 = 10, then solve normally.",
        "takeaway": "Simplify each side, gather x terms, then undo the remaining operations.",
        "visual": "equation-explorer", "formula": "4x + 1 = x + 10  =>  3x = 9",
        "exercises": [
            question("lc1", "Solve 3x + 2x = 35.", "7", "Combine like terms: 5x = 35, so x = 7.",
                     "Add the coefficients of x first."),
            question("lc2", "Solve 2(x + 3) = 14.", "4", "Divide by 2 to get x + 3 = 7, so x = 4.",
                     "Either distribute the 2 or divide both sides by 2."),
            question("lc3", "Solve 5x = 2x + 12.", "4", "Subtract 2x from both sides: 3x = 12.",
                     "Gather the x terms on one side."),
            question("lc4", "Solve 4x + 1 = x + 10.", "3", "Subtract x and 1 from both sides to get 3x = 9.",
                     "Subtract x from both sides before using constants."),
            question("lc5", "Solve 3(x - 2) = 2x + 1.", "7", "Distribute: 3x - 6 = 2x + 1. Subtract 2x and add 6: x = 7.",
                     "Distribute the 3 first."),
        ],
    },
    {
        "id": "equation-stories", "skill": "eq-modeling", "title": "Turn a story into an equation",
        "subtitle": "Define the unknown, model the situation, and interpret the answer.",
        "duration": 10, "color": "violet", "icon": "balance",
        "intro": "Equations model stories when you state what the unknown means. A taxi "
                 "that charges 4 coins to start and 2 coins per kilometre costs 2x + 4 coins "
                 "for x kilometres. If a trip costs 18 coins, solve 2x + 4 = 18. Always "
                 "interpret the solution in context: a distance should not be negative, and "
                 "a count of visits should be a whole number. Consecutive numbers can be "
                 "written x, x + 1, and x + 2.",
        "takeaway": "Say what x means, solve, then check the answer against the story.",
        "visual": "equation-explorer", "formula": "2x + 4 = 18",
        "exercises": [
            question("ls1", "A taxi charges 4 coins plus 2 coins per kilometre. A trip costs 18 coins. How many kilometres is the trip?",
                     "7", "Solve 2x + 4 = 18. Then 2x = 14 and x = 7.",
                     "Subtract the starting charge before dividing by the rate."),
            question("ls2", "A plant is 12 cm tall and grows 3 cm each week. A second plant is 30 cm tall and grows 1 cm each week. After how many weeks are they equally tall?",
                     "9", "Solve 12 + 3w = 30 + w. Then 2w = 18 and w = 9.",
                     "Write each height as an expression in weeks."),
            question("ls3", "A phone plan costs 15 coins plus 3 coins per gigabyte. Which equation finds the gigabytes g used for a 36-coin bill?",
                     "3g + 15 = 36", "The variable part is 3g and the fixed fee is 15, so the equation is 3g + 15 = 36.",
                     "Rate times quantity plus the fixed fee equals the total.",
                     ["3g + 15 = 36", "15g + 3 = 36", "3g = 36 + 15", "18g = 36"]),
            question("ls4", "The sum of three consecutive whole numbers is 51. What is the smallest number?",
                     "16", "Write x + (x + 1) + (x + 2) = 51. Then 3x + 3 = 51, so x = 16.",
                     "Let x be the smallest number."),
            question("ls5", "A student solves 2x + 4 = 18 for a taxi trip and gets x = -7. Why should they doubt the answer?",
                     "Distance cannot be negative in this story",
                     "Checking a solution includes asking whether it makes sense in context.",
                     "What does x measure in the taxi story?",
                     ["Distance cannot be negative in this story", "Negative numbers can never solve equations",
                      "The equation must have two answers", "18 is too large"]),
        ],
    },
]
LESSONS.extend(EQUATION_LESSONS)

PRACTICE.update({
    "equation-meaning": [
        question("rb1", "Which value of x makes x - 4 = 9 true?", "13", "13 - 4 = 9.", "Test each choice.", ["5", "13", "36", "-5"]),
        question("rb2", "Is x = 3 a solution of 5x - 2 = 13?", "Yes", "5 times 3 minus 2 is 13.", "Substitute 3 into the left side.", ["Yes", "No"]),
        question("rb3", "x + 8 = 20. After subtracting 8 from both sides, what number is on the right?", "12", "20 - 8 = 12.", "Apply the same subtraction to the right side."),
        question("rb4", "Evaluate 4x + 1 when x = 3.", "13", "4 times 3 plus 1 is 13.", "Multiply before adding."),
    ],
    "equation-addsub": [
        question("ra1", "Solve x + 5 = 17.", "12", "Subtract 5 from both sides.", "Undo adding 5."),
        question("ra2", "Solve x - 9 = 3.", "12", "Add 9 to both sides.", "Undo subtracting 9."),
        question("ra3", "Solve x + 11 = 2.", "-9", "2 - 11 = -9.", "The answer is below zero."),
        question("ra4", "Solve 1/3 + x = 5/6.", "1/2", "5/6 - 2/6 = 3/6 = 1/2.", "Use sixths."),
    ],
    "equation-muldiv": [
        question("rm1", "Solve 6x = 42.", "7", "Divide both sides by 6.", "Undo multiplying by 6."),
        question("rm2", "Solve x / 3 = 8.", "24", "Multiply both sides by 3.", "Undo dividing by 3."),
        question("rm3", "Solve -5x = 20.", "-4", "Divide both sides by -5.", "Keep the sign."),
        question("rm4", "Solve (2/3)x = 10.", "15", "Multiply by 3/2: 10 times 3/2 = 15.", "Use the reciprocal."),
    ],
    "equation-two-step": [
        question("rt1", "Solve 3x + 2 = 20.", "6", "Subtract 2, then divide by 3.", "Undo addition first."),
        question("rt2", "Solve 5x - 7 = 18.", "5", "Add 7, then divide by 5.", "Undo subtraction first."),
        question("rt3", "Solve x / 3 - 2 = 4.", "18", "Add 2 to get x / 3 = 6, then multiply by 3.", "Remove the constant first."),
        question("rt4", "Solve 10 - 2x = 4.", "3", "Subtract 10 to get -2x = -6.", "Keep the negative coefficient."),
    ],
    "equation-multistep": [
        question("rc1", "Solve 4x + 3x = 21.", "3", "7x = 21.", "Combine like terms."),
        question("rc2", "Solve 3(x + 2) = 21.", "5", "x + 2 = 7.", "Divide both sides by 3."),
        question("rc3", "Solve 6x = 4x + 10.", "5", "2x = 10.", "Subtract 4x from both sides."),
        question("rc4", "Solve 5x - 3 = 2x + 9.", "4", "3x = 12.", "Subtract 2x, then add 3."),
    ],
    "equation-stories": [
        question("rs1", "Printing costs 5 coins plus 2 coins per page. A job costs 21 coins. How many pages are printed?", "8", "Solve 2p + 5 = 21.", "Subtract the fixed fee first."),
        question("rs2", "A tank holds 40 L and loses 4 L each minute. After how many minutes does it hold 12 L?", "7", "Solve 40 - 4m = 12.", "The rate of change is negative."),
        question("rs3", "Alex has 30 coins and saves 4 each week. Sam has 18 coins and saves 6 each week. After how many weeks do they have the same amount?", "6", "Solve 30 + 4w = 18 + 6w.", "Write both totals in terms of w."),
        question("rs4", "Four times a number, increased by 3, equals 31. What is the number?", "7", "Solve 4x + 3 = 31.", "Translate the words into symbols."),
    ],
})

COURSE_ASSESSMENTS["first-equations"] = [
    ("equation-meaning", question("xb1", "Which value of x makes 2x = 18 true?", "9", "2 times 9 equals 18.", "Test each choice.", ["9", "16", "20", "36"])),
    ("equation-meaning", question("xb2", "Is x = 5 a solution of x + 7 = 11?", "No", "5 + 7 is 12, not 11.", "Substitute 5.", ["Yes", "No"])),
    ("equation-addsub", question("xa1", "Solve x + 14 = 30.", "16", "Subtract 14 from both sides.", "Undo adding 14.")),
    ("equation-addsub", question("xa2", "Solve x - 8 = -3.", "5", "Add 8 to both sides.", "Undo subtracting 8.")),
    ("equation-muldiv", question("xm1", "Solve 9x = 54.", "6", "Divide both sides by 9.", "Undo multiplying by 9.")),
    ("equation-muldiv", question("xm2", "Solve x / 7 = -2.", "-14", "Multiply both sides by 7.", "Undo dividing by 7.")),
    ("equation-two-step", question("xt1", "Solve 4x + 5 = 29.", "6", "Subtract 5, then divide by 4.", "Undo addition first.")),
    ("equation-two-step", question("xt2", "Solve 7 - 3x = -2.", "3", "Subtract 7 to get -3x = -9.", "Keep the negative sign.")),
    ("equation-multistep", question("xc1", "Solve 2x + 5x = 56.", "8", "7x = 56.", "Combine like terms.")),
    ("equation-multistep", question("xc2", "Solve 4(x - 1) = 3x + 5.", "9", "4x - 4 = 3x + 5, so x = 9.", "Distribute the 4.")),
    ("equation-stories", question("xs1", "A gym charges 12 coins to join and 5 coins per visit. A member has paid 52 coins. How many visits is that?", "8", "Solve 5v + 12 = 52.", "Subtract the joining fee first.")),
    ("equation-stories", question("xs2", "The sum of three consecutive whole numbers is 78. What is the largest?", "27", "The smallest is 25, so the largest is 27.", "Let x be the smallest number.")),
]

SKILLS.extend([
    {"id": "lin-tables", "name": "Constant change in tables", "prerequisites": []},
    {"id": "lin-slope", "name": "Slope from two points", "prerequisites": ["lin-tables"]},
    {"id": "lin-intercept", "name": "Starting values and intercepts", "prerequisites": ["lin-tables"]},
    {"id": "lin-rule", "name": "Writing a linear rule", "prerequisites": ["lin-slope", "lin-intercept"]},
    {"id": "lin-graphs", "name": "Reading and using graphs", "prerequisites": ["lin-rule"]},
    {"id": "lin-compare", "name": "Comparing linear relationships", "prerequisites": ["lin-graphs"]},
])

LINEAR_LESSONS = [
    {
        "id": "linear-patterns", "skill": "lin-tables", "title": "Steady change in a table",
        "subtitle": "Spot a constant rate by comparing equal steps.",
        "duration": 8, "color": "blue", "icon": "graph",
        "intro": "A relationship is linear when equal steps in x always produce the same "
                 "change in y. In a table where x goes 0, 1, 2, 3 and y goes 5, 8, 11, 14, "
                 "y rises by 3 each time. That constant change is the rate of change. If x "
                 "steps are larger, compare the change in y with the change in x: moving "
                 "from x = 0 to x = 2 while y rises by 6 is still 3 per unit of x. A falling "
                 "pattern has a negative rate. Use the explorer to see how a table changes "
                 "when the line changes.",
        "takeaway": "Linear means the change in y per 1 unit of x never varies.",
        "visual": "line-explorer", "formula": "rate = change in y / change in x",
        "exercises": [
            question("ip1", "A table gives y = 5, 9, 13, 17 for x = 0, 1, 2, 3. By how much does y change each time x increases by 1?",
                     "4", "Each value is 4 more than the one before it.", "Subtract neighbouring y values."),
            question("ip2", "Which table shows a constant rate of change?", "x: 1, 2, 3, 4 and y: 2, 5, 8, 11",
                     "Only the first table changes by 3 every time. The others have changing differences.",
                     "Check whether all the differences between neighbouring y values match.",
                     ["x: 1, 2, 3, 4 and y: 2, 5, 8, 11", "x: 1, 2, 3, 4 and y: 1, 4, 9, 16",
                      "x: 1, 2, 3, 4 and y: 2, 4, 7, 11", "x: 1, 2, 3, 4 and y: 20, 10, 5, 2.5"]),
            question("ip3", "A table gives y = 1, 7, 13 for x = 0, 2, 4. By how much does y change per 1-unit increase in x?",
                     "3", "y changes 6 for every 2 units of x, so it changes 3 per unit.",
                     "Divide the change in y by the change in x."),
            question("ip4", "A candle is 20 cm tall now, 17 cm after 1 hour, and 14 cm after 2 hours. What is the rate of change in cm per hour?",
                     "-3", "The height falls 3 cm each hour, so the rate is -3.", "A decreasing quantity has a negative rate."),
            question("ip5", "A table gives y = 3, 6, 9, 12 for x = 1, 2, 3, 4 and the pattern continues. What is y when x = 10?",
                     "30", "The pattern is y = 3x, so y is 30 when x is 10.", "Look at how y relates to x."),
        ],
    },
    {
        "id": "linear-slope", "skill": "lin-slope", "title": "Slope from two points",
        "subtitle": "Measure steepness using rise over run.",
        "duration": 9, "color": "violet", "icon": "graph",
        "intro": "Slope measures how steeply a line rises or falls. Between two points, "
                 "subtract the y values to find the rise and subtract the x values in the "
                 "same order to find the run. For (1, 3) and (4, 12), the rise is 9 and the "
                 "run is 3, so the slope is 3. A line that falls has negative slope. A "
                 "horizontal line has slope 0 because y never changes. Steepness depends on "
                 "the size of the slope, so -5 is steeper than 3.",
        "takeaway": "Slope = (y2 - y1) / (x2 - x1), using the points in the same order.",
        "visual": "line-explorer", "formula": "m = (y2 - y1) / (x2 - x1)",
        "exercises": [
            question("is1", "A line passes through (1, 3) and (4, 12). What is its slope?", "3",
                     "The rise is 9 and the run is 3, so the slope is 3.", "Subtract the y values and the x values."),
            question("is2", "A line passes through (2, 10) and (5, 4). What is its slope?", "-2",
                     "The rise is -6 and the run is 3, so the slope is -2.", "The line falls as x increases."),
            question("is3", "A line passes through (0, 0) and (4, 6). Enter its slope as a fraction or decimal.", "3/2",
                     "The rise is 6 and the run is 4, so the slope is 6/4 = 3/2.", "Divide the rise by the run and simplify."),
            question("is4", "Which line is steepest?", "slope -5",
                     "Steepness depends on the size of the slope. A slope of -5 falls 5 units per step.",
                     "Compare the sizes of the slopes, ignoring the signs.",
                     ["slope 3", "slope -5", "slope 1/2", "slope 4"]),
            question("is5", "A horizontal line passes through (1, 4) and (6, 4). What is its slope?", "0",
                     "The rise is 0, so the slope is 0 / 5 = 0.", "How much does y change?"),
        ],
    },
    {
        "id": "linear-intercept", "skill": "lin-intercept", "title": "Where the line begins",
        "subtitle": "Find and interpret the value of y when x is zero.",
        "duration": 9, "color": "yellow", "icon": "graph",
        "intro": "The y-intercept is the value of y when x is 0, where the line crosses "
                 "the y-axis. In a story, it is often the starting amount. If a line has "
                 "rate 3 and passes through (4, 20), step back four units of x: y falls "
                 "by 12, so the intercept is 8. Given two points, you can also move back to "
                 "x = 0 using the rate. Always interpret the intercept in context.",
        "takeaway": "The intercept is the output at x = 0 - often the starting value.",
        "visual": "line-explorer", "formula": "y-intercept = y when x = 0",
        "exercises": [
            question("ii1", "A line's equation is y = 4x + 7. What is y when x = 0?", "7",
                     "Replacing x with 0 leaves y = 7.", "Substitute 0 for x."),
            question("ii2", "A line passes through (0, -3) and (2, 1). What is its y-intercept?", "-3",
                     "The point (0, -3) already has x = 0, so the intercept is -3.", "Look for the point with x = 0."),
            question("ii3", "A linear relationship has rate 4 and passes through (1, 9). What is y when x = 0?", "5",
                     "Going back one unit of x lowers y by 4, giving 9 - 4 = 5.", "Move from x = 1 back to x = 0."),
            question("ii4", "In the model y = 120 - 8x, where y is litres of water after x minutes, what does the y-intercept mean?",
                     "The amount of water at the start (x = 0)", "At x = 0 no time has passed, so y = 120 is the starting amount.",
                     "What is true at the moment x equals 0?",
                     ["The amount of water at the start (x = 0)", "The amount lost each minute",
                      "How many minutes until the tank is empty", "The amount after 8 minutes"]),
            question("ii5", "A line has rate 3 and passes through (4, 20). What is its y-intercept?", "8",
                     "Moving back 4 units of x lowers y by 12, so the intercept is 8.", "Subtract rate times 4 from 20."),
        ],
    },
    {
        "id": "linear-writing", "skill": "lin-rule", "title": "Write the rule",
        "subtitle": "Combine slope and intercept into y = mx + b.",
        "duration": 10, "color": "mint", "icon": "graph",
        "intro": "Once you know the slope m and the y-intercept b, the line is y = mx + b. "
                 "If you only know two points, find the slope first, then use one point to "
                 "find b. For (1, 7) and (3, 13), the slope is 3, so 7 = 3(1) + b and b = 4. "
                 "The rule y = 3x + 4 predicts y for any x. A fractional slope is fine: if "
                 "the slope is 1/2 and the line passes through (4, 5), then 5 = 2 + b, so b = 3.",
        "takeaway": "Find m, then use any point to solve for b.",
        "visual": "line-explorer", "formula": "y = mx + b",
        "exercises": [
            question("iw1", "A line has slope 3 and y-intercept -2. Which equation describes it?", "y = 3x - 2",
                     "The slope multiplies x and the intercept is added: y = 3x + (-2).", "Match m and b to the equation.",
                     ["y = 3x - 2", "y = -2x + 3", "y = 3x + 2", "y = x + 1"]),
            question("iw2", "A line passes through (0, 4) with slope 5. What is y when x = 6?", "34",
                     "The rule is y = 5x + 4, so y = 30 + 4 = 34.", "Write the rule first."),
            question("iw3", "A line passes through (1, 7) and (3, 13). Writing it as y = mx + b, what is b?", "4",
                     "The slope is 3. From 7 = 3(1) + b, b = 4.", "Find the slope, then substitute one point."),
            question("iw4", "A line has slope 1/2 and passes through (4, 5). What is y when x = 0?", "3",
                     "From 5 = (1/2)(4) + b, b = 3.", "Substitute the point to find b."),
            question("iw5", "Which equation fits the table x: 0, 1, 2, 3 and y: 6, 4, 2, 0?", "y = -2x + 6",
                     "The rate is -2 and y is 6 when x is 0.", "Find the rate and the value at x = 0.",
                     ["y = -2x + 6", "y = 2x + 6", "y = -6x + 2", "y = 6x - 2"]),
        ],
    },
    {
        "id": "linear-graphs", "skill": "lin-graphs", "title": "Read the graph",
        "subtitle": "Connect equations, intercepts, and points on a graph.",
        "duration": 10, "color": "peach", "icon": "graph",
        "intro": "A graph shows every point (x, y) that satisfies the rule. The y-intercept "
                 "is where it crosses the y-axis, and the x-intercept is where y is 0. For "
                 "y = 2x - 6, set y to 0 to get 2x = 6, so the x-intercept is 3. A point lies on "
                 "the line when its coordinates satisfy the equation: (5, 4) lies on "
                 "y = 3x - 11. The slope tells you how the graph moves: y = -x + 6 falls 1 "
                 "for each step right and crosses the y-axis at 6.",
        "takeaway": "A point is on the line when its coordinates make the equation true.",
        "visual": "line-explorer", "formula": "x-intercept: set y = 0",
        "exercises": [
            question("ig1", "A graph crosses the y-axis at 3 and rises 2 for every 1 step right. What is y when x = 4?", "11",
                     "The rule is y = 2x + 3, so y = 8 + 3 = 11.", "Write the rule from the intercept and rate."),
            question("ig2", "A line crosses the y-axis at 8 and the x-axis at 4. What is its slope?", "-2",
                     "It passes through (0, 8) and (4, 0), so the slope is -8 / 4 = -2.", "Use the two intercepts as points."),
            question("ig3", "Which statement describes y = -x + 6?",
                     "It falls 1 for each step right and crosses the y-axis at 6",
                     "The slope is -1 and the intercept is 6.", "Read the slope and intercept.",
                     ["It falls 1 for each step right and crosses the y-axis at 6",
                      "It rises 1 for each step right and crosses the y-axis at 6",
                      "It falls 6 for each step right and crosses the y-axis at 1",
                      "It is horizontal at y = 6"]),
            question("ig4", "For y = 2x - 6, at what x does the line cross the x-axis?", "3",
                     "Set y = 0: 2x - 6 = 0, so x = 3.", "The x-axis is where y = 0."),
            question("ig5", "The point (5, k) lies on y = 3x - 4. What is k?", "11",
                     "k = 3(5) - 4 = 11.", "Substitute 5 for x."),
        ],
    },
    {
        "id": "linear-comparison", "skill": "lin-compare", "title": "When lines meet",
        "subtitle": "Compare two linear relationships and interpret where they cross.",
        "duration": 10, "color": "violet", "icon": "graph",
        "intro": "Two lines meet where they have the same x and the same y. Plan A at "
                 "y = 5x + 10 and Plan B at y = 3x + 20 cost the same when 5x + 10 = 3x + 20, "
                 "which gives x = 5. Lines with the same slope but different intercepts are "
                 "parallel and never meet. A line with a greater slope eventually rises "
                 "faster, even if it starts lower. Always check what the crossing point means "
                 "in the story.",
        "takeaway": "Set the two rules equal to find where the lines meet.",
        "visual": "line-explorer", "formula": "5x + 10 = 3x + 20",
        "exercises": [
            question("ic1", "Plan A costs y = 5x + 10 and Plan B costs y = 3x + 20, where x is months. After how many months do they cost the same?", "5",
                     "Set 5x + 10 = 3x + 20. Then 2x = 10, so x = 5.", "Set the two costs equal."),
            question("ic2", "The lines y = 2x + 1 and y = 2x + 5 have the same slope. How many points do they share?", "None",
                     "Parallel lines never meet, since 2x + 1 can never equal 2x + 5.", "What happens when you set the rules equal?",
                     ["None", "One", "Two", "Infinitely many"]),
            question("ic3", "Line A is y = 3x and line B is y = x + 8. What is y at their intersection?", "12",
                     "3x = x + 8 gives x = 4, so y = 12.", "First find the x value where they match."),
            question("ic4", "Which line rises faster as x increases?", "y = 7x + 1",
                     "Rising speed depends on the slope, and 7 is greater than 5.", "Compare the slopes, not the intercepts.",
                     ["y = 7x + 1", "y = 5x + 20", "They rise at the same rate"]),
            question("ic5", "A runner starts 12 m ahead and runs 2 m/s. A second runner starts at 0 and runs 5 m/s. After how many seconds does the second runner catch up?", "4",
                     "Solve 12 + 2t = 5t. Then 3t = 12, so t = 4.", "Write each distance in terms of t."),
        ],
    },
]
LESSONS.extend(LINEAR_LESSONS)

PRACTICE.update({
    "linear-patterns": [
        question("jp1", "A table gives y = 2, 7, 12, 17 for x = 0, 1, 2, 3. What is the rate of change?", "5", "Each y is 5 more than the last.", "Subtract neighbouring y values."),
        question("jp2", "Does a table with x = 1, 2, 3, 4 and y = 3, 6, 12, 24 show a constant rate of change?", "No", "The differences are 3, 6, and 12, so they are not constant.", "Compare all neighbouring differences.", ["Yes", "No"]),
        question("jp3", "A table gives y = 4, 10, 16 for x = 0, 3, 6. What is the change in y per 1-unit increase in x?", "2", "y changes 6 for every 3 units of x.", "Divide the change in y by the change in x."),
        question("jp4", "A tank holds 50 L at 0 minutes, 44 L at 1 minute, and 38 L at 2 minutes. What is the rate in litres per minute?", "-6", "The volume falls 6 L each minute.", "A falling quantity has a negative rate."),
    ],
    "linear-slope": [
        question("js1", "A line passes through (0, 2) and (3, 11). What is its slope?", "3", "The rise is 9 over a run of 3.", "Divide rise by run."),
        question("js2", "A line passes through (1, 8) and (3, 2). What is its slope?", "-3", "The rise is -6 over a run of 2.", "The line falls."),
        question("js3", "A line passes through (2, 1) and (6, 3). What is its slope?", "1/2", "The rise is 2 over a run of 4.", "Simplify rise over run."),
        question("js4", "A line passes through (-2, -1) and (2, 7). What is its slope?", "2", "The rise is 8 over a run of 4.", "Subtract the coordinates carefully."),
    ],
    "linear-intercept": [
        question("ji1", "For y = -2x + 9, what is y when x = 0?", "9", "The x term vanishes.", "Substitute 0 for x."),
        question("ji2", "A line passes through (0, 5) and (3, 11). What is its y-intercept?", "5", "The point with x = 0 shows the intercept.", "Find the point with x = 0."),
        question("ji3", "A line has rate 5 and passes through (2, 13). What is its y-intercept?", "3", "Moving back 2 units of x lowers y by 10.", "Subtract rate times 2."),
        question("ji4", "A line has rate -2 and passes through (3, 1). What is its y-intercept?", "7", "Moving back 3 units of x raises y by 6.", "Going back reverses the change."),
    ],
    "linear-writing": [
        question("jw1", "A line has slope 4 and y-intercept 1. What is y when x = 5?", "21", "y = 4(5) + 1 = 21.", "Write y = mx + b first."),
        question("jw2", "A line passes through (0, -1) with slope 3. What is y when x = 4?", "11", "y = 3x - 1, so y = 11.", "Use the intercept and slope."),
        question("jw3", "A line passes through (2, 5) and (4, 11). Writing it as y = mx + b, what is b?", "-1", "The slope is 3. From 5 = 3(2) + b, b = -1.", "Find the slope first."),
        question("jw4", "A line has slope 2/3 and passes through (6, 7). What is y when x = 0?", "3", "From 7 = (2/3)(6) + b, b = 3.", "Substitute the point."),
    ],
    "linear-graphs": [
        question("jg1", "A line crosses the y-axis at 2 and rises 3 for each step right. What is y when x = 5?", "17", "y = 3x + 2, so y = 17.", "Write the rule first."),
        question("jg2", "A line passes through (0, 6) and (3, 0). What is its slope?", "-2", "The rise is -6 over a run of 3.", "Use the two points."),
        question("jg3", "For y = x + 5, at what x does the line cross the x-axis?", "-5", "Set y = 0 to get x = -5.", "The x-axis is where y = 0."),
        question("jg4", "The point (4, k) lies on y = 2x - 1. What is k?", "7", "k = 2(4) - 1 = 7.", "Substitute 4 for x."),
    ],
    "linear-comparison": [
        question("jc1", "The lines y = 2x + 9 and y = 5x intersect. What is x at the intersection?", "3", "2x + 9 = 5x gives 3x = 9.", "Set the rules equal."),
        question("jc2", "The lines y = -x + 10 and y = x + 2 intersect. What is y at the intersection?", "6", "-x + 10 = x + 2 gives x = 4, so y = 6.", "Find x first."),
        question("jc3", "How many points do y = 3x + 2 and y = 3x - 4 share?", "None", "They have the same slope and different intercepts.", "Compare the slopes.", ["None", "One", "Infinitely many"]),
        question("jc4", "A bike starts 15 km from home and rides away at 5 km/h. A car starts at home and travels at 20 km/h in the same direction. After how many hours does the car catch the bike?", "1", "Solve 15 + 5t = 20t.", "Write each distance in terms of t."),
    ],
})

COURSE_ASSESSMENTS["linear-relationships"] = [
    ("linear-patterns", question("kp1", "A table gives y = 6, 11, 16, 21 for x = 0, 1, 2, 3. What is the rate of change?", "5", "Each y is 5 more than the last.", "Subtract neighbouring y values.")),
    ("linear-patterns", question("kp2", "A table gives y = 10, 4, -2 for x = 0, 1, 2. What is the rate of change?", "-6", "y falls by 6 each step.", "Subtract neighbouring y values.")),
    ("linear-slope", question("ks1", "A line passes through (2, 5) and (6, 17). What is its slope?", "3", "The rise is 12 over a run of 4.", "Divide rise by run.")),
    ("linear-slope", question("ks2", "A line passes through (1, 9) and (4, 0). What is its slope?", "-3", "The rise is -9 over a run of 3.", "The line falls.")),
    ("linear-intercept", question("ki1", "A line has rate 5 and passes through (3, 22). What is its y-intercept?", "7", "Moving back 3 units of x lowers y by 15.", "Subtract rate times 3.")),
    ("linear-intercept", question("ki2", "A line passes through (0, 12) and (4, 0). What is its y-intercept?", "12", "The point with x = 0 shows the intercept.", "Find the point with x = 0.")),
    ("linear-writing", question("kw1", "A line passes through (1, 5) and (4, 14). Writing it as y = mx + b, what is b?", "2", "The slope is 3. From 5 = 3(1) + b, b = 2.", "Find the slope first.")),
    ("linear-writing", question("kw2", "A line has slope -3 and passes through (2, 4). What is y when x = 5?", "-5", "From 4 = -3(2) + b, b = 10, so y = -15 + 10 = -5.", "Find b first.")),
    ("linear-graphs", question("kg1", "For y = 4x - 12, at what x does the line cross the x-axis?", "3", "Set y = 0: 4x = 12.", "The x-axis is where y = 0.")),
    ("linear-graphs", question("kg2", "The point (6, k) lies on y = -2x + 15. What is k?", "3", "k = -12 + 15 = 3.", "Substitute 6 for x.")),
    ("linear-comparison", question("kc1", "The lines y = 3x + 4 and y = 5x - 6 intersect. What is x at the intersection?", "5", "3x + 4 = 5x - 6 gives 10 = 2x.", "Set the rules equal.")),
    ("linear-comparison", question("kc2", "The lines y = 4x + 1 and y = x + 10 intersect. What is y at the intersection?", "13", "3x = 9 gives x = 3, so y = 13.", "Find x first.")),
]

SKILLS.extend([
    {"id": "geo-measure", "name": "Perimeter and area", "prerequisites": []},
    {"id": "geo-angles", "name": "Angles and triangles", "prerequisites": ["geo-measure"]},
    {"id": "geo-points", "name": "Locating and moving points", "prerequisites": ["geo-measure"]},
    {"id": "geo-grid", "name": "Distances along grid lines", "prerequisites": ["geo-points"]},
    {"id": "geo-midpoint", "name": "Midpoints", "prerequisites": ["geo-grid"]},
    {"id": "geo-distance", "name": "Distance between points", "prerequisites": ["geo-grid", "geo-angles"]},
    {"id": "geo-lines", "name": "Parallel and perpendicular slopes", "prerequisites": ["geo-points"]},
    {"id": "geo-shapes", "name": "Shapes on the coordinate plane", "prerequisites": ["geo-midpoint", "geo-distance", "geo-lines"]},
    {"id": "geo-polar", "name": "Coordinates by angle and distance", "prerequisites": ["geo-distance", "geo-angles"]},
])

GEOMETRY_LESSONS = [
    {
        "id": "geom-measure", "skill": "geo-measure", "title": "How big is it?",
        "subtitle": "Measure the edge of a shape and the space inside it.",
        "duration": 8, "color": "yellow", "icon": "graph",
        "intro": "Start with a rectangle. The perimeter is the distance around its edge, like "
                 "the length of a fence. The area is the flat space inside, like the amount of "
                 "grass the fence surrounds. Area is counted in squares. A rectangle 4 squares "
                 "wide and 3 squares tall holds 4 times 3 = 12 squares. Its perimeter adds all "
                 "four sides: 4 + 3 + 4 + 3 = 14. A triangle covers exactly half of a rectangle "
                 "with the same base and height. For a shape made of pieces, find each piece "
                 "and add. Slide the width and height in the explorer and watch both numbers.",
        "takeaway": "Perimeter is around the edge. Area is the space inside.",
        "visual": "shape-explorer", "formula": "area = width x height",
        "exercises": [
            question("hm1", "A rectangle is 8 cm wide and 5 cm tall. What is its perimeter in cm?", "26",
                     "Add all four sides: 8 + 5 + 8 + 5 = 26.", "Walk around the edge and add each side."),
            question("hm2", "A rectangle is 8 cm wide and 5 cm tall. What is its area in square cm?", "40",
                     "Area is width times height: 8 times 5 = 40.", "Count the squares inside: rows times columns."),
            question("hm3", "A triangle has a base of 10 cm and a height of 6 cm. What is its area in square cm?", "30",
                     "A triangle is half of a 10 by 6 rectangle. Half of 60 is 30.", "Find the rectangle's area first, then halve it."),
            question("hm4", "An L-shaped floor is made of a 6 m by 4 m rectangle and a 3 m by 2 m rectangle that do not overlap. What is its total area in square m?", "30",
                     "The pieces have areas 24 and 6, and 24 + 6 = 30.", "Find each piece, then add."),
            question("hm5", "Which measurement is an area?", "25 square cm",
                     "Area is measured in square units, such as square cm.", "Look for the units that count squares.",
                     ["25 square cm", "25 cm", "25 cm per second", "25 degrees"]),
        ],
    },
    {
        "id": "geom-angles", "skill": "geo-angles", "title": "Turns, corners, and triangles",
        "subtitle": "Measure how far something turns, in degrees.",
        "duration": 9, "color": "peach", "icon": "graph",
        "intro": "An angle tells you how far something turns. We measure it in degrees. A "
                 "full turn is 360 degrees. A straight line is half a turn, 180 degrees. A "
                 "square corner is a quarter turn, 90 degrees, called a right angle. Two angles "
                 "that make a square corner together are complementary: they add to 90. Two "
                 "that make a straight line are supplementary: they add to 180. The three angles "
                 "of any triangle add to 180, and the four angles of a quadrilateral add to 360. "
                 "An equilateral triangle has three equal 60 degree angles. Move the slider to "
                 "turn the second ray.",
        "takeaway": "A triangle's angles always add to 180 degrees.",
        "visual": "angle-explorer", "formula": "triangle angles: a + b + c = 180",
        "exercises": [
            question("ha1", "What is the complement of a 35 degree angle?", "55",
                     "Complementary angles add to 90, and 90 - 35 = 55.", "Together they make a square corner."),
            question("ha2", "What is the supplement of a 110 degree angle?", "70",
                     "Supplementary angles add to 180, and 180 - 110 = 70.", "Together they make a straight line."),
            question("ha3", "Two angles of a triangle measure 50 degrees and 65 degrees. What is the third angle?", "65",
                     "The three angles add to 180. 50 + 65 = 115, and 180 - 115 = 65.", "Add the two you know, then subtract from 180."),
            question("ha4", "An isosceles triangle has a 40 degree angle between its two equal sides. What is each of the other two angles?", "70",
                     "The other two angles share 180 - 40 = 140, so each is 70.", "The two remaining angles are equal."),
            question("ha5", "Three angles of a quadrilateral are 90, 100, and 80 degrees. What is the fourth angle?", "90",
                     "The four angles add to 360. 90 + 100 + 80 = 270, so the fourth is 90.", "Subtract the three known angles from 360."),
        ],
    },
    {
        "id": "coord-points", "skill": "geo-points", "title": "Locate and move points",
        "subtitle": "Read ordered pairs, quadrants, reflections, and moves.",
        "duration": 8, "color": "blue", "icon": "graph",
        "intro": "An ordered pair (x, y) names a point: x says how far right or left of the "
                 "origin, and y says how far up or down. The axes split the plane into four "
                 "quadrants. A point with negative x and positive y is in Quadrant II. "
                 "Reflecting across the y-axis changes the sign of x; reflecting across the "
                 "x-axis changes the sign of y. Moving a point right adds to x, and moving "
                 "it up adds to y. Drag the sliders in the explorer to place two points.",
        "takeaway": "Order matters: x first, then y.",
        "visual": "plane-explorer", "formula": "(x, y)",
        "exercises": [
            question("op1", "Which point is 3 units right of the origin and 2 units down?", "(3, -2)",
                     "Right 3 gives x = 3 and down 2 gives y = -2.", "Right is positive x; down is negative y.",
                     ["(3, -2)", "(-3, 2)", "(2, -3)", "(-2, 3)"]),
            question("op2", "In which quadrant is (-4, 5)?", "Quadrant II",
                     "x is negative and y is positive, which is Quadrant II.", "Check the sign of each coordinate.",
                     ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]),
            question("op3", "Reflect (3, 4) across the y-axis. What is the new x-coordinate?", "-3",
                     "A reflection across the y-axis flips the sign of x.", "The y-coordinate stays the same."),
            question("op4", "Reflect (3, 4) across the x-axis. What is the new y-coordinate?", "-4",
                     "A reflection across the x-axis flips the sign of y.", "The x-coordinate stays the same."),
            question("op5", "Move the point (2, -1) 3 units right and 4 units up. What is its new y-coordinate?", "3",
                     "Moving up adds 4 to y: -1 + 4 = 3.", "Only the vertical move changes y."),
        ],
    },
    {
        "id": "coord-grid", "skill": "geo-grid", "title": "Distance along grid lines",
        "subtitle": "Measure horizontal and vertical segments and rectangles.",
        "duration": 8, "color": "mint", "icon": "graph",
        "intro": "When two points share a y-coordinate, the segment between them is "
                 "horizontal and its length is the difference of the x-coordinates. When "
                 "they share an x-coordinate, the segment is vertical and its length is the "
                 "difference of the y-coordinates. Distance is never negative, so subtract the "
                 "smaller value from the larger. Across the axis, count both sides: from -4 to 3 "
                 "is 7 units. A rectangle with sides on grid lines has area width times "
                 "height and perimeter twice width plus twice height.",
        "takeaway": "Distance along a grid line is a difference of coordinates.",
        "visual": "plane-explorer", "formula": "length = |x2 - x1|  or  |y2 - y1|",
        "exercises": [
            question("og1", "How far apart are (2, 5) and (9, 5)?", "7", "The y-values match, so subtract the x-values: 9 - 2 = 7.", "Which coordinate is shared?"),
            question("og2", "How far apart are (-3, 4) and (-3, -2)?", "6", "The x-values match. The y-distance is 4 - (-2) = 6.", "Subtract carefully with a negative."),
            question("og3", "How far apart are (-4, 1) and (3, 1)?", "7", "3 - (-4) = 7 units.", "Count across the y-axis."),
            question("og4", "A rectangle has corners (1, 1), (6, 1), (6, 4), and (1, 4). What is its area?", "15", "The width is 5 and the height is 3, so the area is 15.", "Find the width and the height first."),
            question("og5", "A rectangle has corners (-2, -1), (4, -1), (4, 3), and (-2, 3). What is its perimeter?", "20", "The width is 6 and the height is 4, so the perimeter is 2(6) + 2(4) = 20.", "Add all four side lengths."),
        ],
    },
    {
        "id": "coord-midpoint", "skill": "geo-midpoint", "title": "Find the middle",
        "subtitle": "Average coordinates to locate a midpoint.",
        "duration": 9, "color": "yellow", "icon": "graph",
        "intro": "The midpoint of a segment is the point exactly halfway between its endpoints. "
                 "Average the x-coordinates and average the y-coordinates. The midpoint of "
                 "(2, 3) and (8, 9) is (5, 6). The midpoint can have fractional coordinates: "
                 "(-5, -1) and (2, 4) have x-midpoint -3/2. If you know the midpoint and one "
                 "endpoint, you can work backward: doubling the midpoint and subtracting the "
                 "known endpoint gives the other endpoint.",
        "takeaway": "Midpoint = (average of x, average of y).",
        "visual": "plane-explorer", "formula": "M = ((x1 + x2) / 2, (y1 + y2) / 2)",
        "exercises": [
            question("om1", "What is the x-coordinate of the midpoint of (2, 3) and (8, 9)?", "5", "The average of 2 and 8 is 5.", "Add the x-values and halve."),
            question("om2", "What is the y-coordinate of the midpoint of (-4, 6) and (2, -2)?", "2", "The average of 6 and -2 is 2.", "Add the y-values and halve."),
            question("om3", "M(3, 1) is the midpoint of A(1, -3) and B. What is the x-coordinate of B?", "5", "3 = (1 + x) / 2, so x = 5.", "Double the midpoint, then subtract A."),
            question("om4", "What is the x-coordinate of the midpoint of (-5, -1) and (2, 4)? Enter a fraction or decimal.", "-3/2", "(-5 + 2) / 2 = -3/2.", "A midpoint can be fractional."),
            question("om5", "Which statement is true for the midpoint of segment PQ?", "It is equally far from P and Q",
                     "A midpoint divides the segment into two equal lengths.", "Think about what halfway means.",
                     ["It is equally far from P and Q", "It always lies on the x-axis",
                      "Its coordinates are the sums of the coordinates of P and Q", "It has the same y-coordinate as P"]),
        ],
    },
    {
        "id": "coord-distance", "skill": "geo-distance", "title": "Distance between any two points",
        "subtitle": "Use a right triangle to measure a slanted segment.",
        "duration": 10, "color": "peach", "icon": "graph",
        "intro": "A slanted segment is the longest side of a right triangle whose legs follow "
                 "the grid. For (0, 0) and (3, 4), the horizontal leg is 3 and the vertical leg "
                 "is 4. The Pythagorean relationship gives 3 squared plus 4 squared equals 25, so the "
                 "distance is 5. In general, the squared distance is the sum of the squared "
                 "horizontal and vertical changes. Many distances are not whole numbers, so the "
                 "squared distance is a useful exact answer.",
        "takeaway": "Distance squared = (change in x) squared + (change in y) squared.",
        "visual": "plane-explorer", "formula": "d squared = dx squared + dy squared",
        "exercises": [
            question("od1", "What is the distance between (0, 0) and (3, 4)?", "5", "The legs are 3 and 4, and 9 + 16 = 25, so the distance is 5.", "Draw the right triangle."),
            question("od2", "What is the distance between (1, 2) and (7, 10)?", "10", "The legs are 6 and 8. Then 36 + 64 = 100, so the distance is 10.", "Find the horizontal and vertical changes."),
            question("od3", "What is the distance between (-2, 1) and (3, 13)?", "13", "The legs are 5 and 12. Then 25 + 144 = 169, so the distance is 13.", "Subtract coordinates in the same order."),
            question("od4", "What is the squared distance between (0, 1) and (5, 3)?", "29", "The legs are 5 and 2, and 25 + 4 = 29.", "You do not need a square root."),
            question("od5", "Which pair of points is exactly 5 units apart?", "(1, 1) and (4, 5)",
                     "The legs are 3 and 4, so the distance is 5.", "Compute dx squared plus dy squared for each pair.",
                     ["(1, 1) and (4, 5)", "(1, 1) and (4, 4)", "(0, 0) and (2, 4)", "(0, 0) and (4, 4)"]),
        ],
    },
    {
        "id": "coord-lines", "skill": "geo-lines", "title": "Parallel and perpendicular",
        "subtitle": "Compare slopes to describe how lines relate.",
        "duration": 10, "color": "violet", "icon": "graph",
        "intro": "Slope is the vertical change divided by the horizontal change between two "
                 "points. Between (1, 2) and (3, 8), the slope is 6/2 = 3. Parallel lines have "
                 "the same slope. Perpendicular lines have slopes whose product is -1, so one "
                 "slope is the negative reciprocal of the other: 4 pairs with -1/4, and 2/5 pairs "
                 "with -5/2. Neither rule applies to vertical lines, whose slope is undefined.",
        "takeaway": "Parallel: equal slopes. Perpendicular: negative reciprocals.",
        "visual": "plane-explorer", "formula": "m1 times m2 = -1",
        "exercises": [
            question("ol1", "What is the slope of the line through (1, 2) and (3, 8)?", "3", "The rise is 6 and the run is 2, so the slope is 3.", "Divide the vertical change by the horizontal change."),
            question("ol2", "A line has slope 2/3. What is the slope of a parallel line?", "2/3", "Parallel lines have equal slopes.", "Compare directions, not positions."),
            question("ol3", "A line has slope 4. What is the slope of a perpendicular line?", "-1/4", "The negative reciprocal of 4 is -1/4.", "Flip the fraction and change the sign."),
            question("ol4", "A line has slope 2/5. What is the slope of a perpendicular line?", "-5/2", "The negative reciprocal of 2/5 is -5/2.", "Flip the fraction and change the sign."),
            question("ol5", "Which pair of slopes describes perpendicular lines?", "3 and -1/3",
                     "The product of 3 and -1/3 is -1.", "Multiply each pair of slopes.",
                     ["3 and -1/3", "2 and 1/2", "2 and -2", "5 and 5"]),
        ],
    },
    {
        "id": "coord-shapes", "skill": "geo-shapes", "title": "Shapes on the plane",
        "subtitle": "Use lengths, midpoints, and slopes to describe polygons.",
        "duration": 10, "color": "mint", "icon": "graph",
        "intro": "Coordinates turn geometry into calculation. A rectangle's diagonals share a "
                 "midpoint, and a diagonal is the hypotenuse of a right triangle: in a 5 by 12 "
                 "rectangle it measures 13. To justify a parallelogram, show that opposite sides "
                 "have equal slopes and equal lengths. Area of a right triangle with legs on the "
                 "axes is half the product of its legs: legs 6 and 8 give area 24.",
        "takeaway": "Combine distance, midpoint, and slope to justify a shape.",
        "visual": "plane-explorer", "formula": "area = (1/2) x base x height",
        "exercises": [
            question("os1", "A rectangle has corners (0, 0), (4, 0), (4, 3), and (0, 3). What is the length of its diagonal from (0, 0) to (4, 3)?", "5", "The legs are 4 and 3, so the diagonal is 5.", "Use the distance relationship."),
            question("os2", "Triangle ABC has vertices A(0, 0), B(6, 0), and C(6, 8). What is the length of side AC?", "10", "The legs are 6 and 8, so AC = 10.", "AC is the slanted side."),
            question("os3", "A rectangle has corners (0, 0), (4, 0), (4, 3), and (0, 3). What is the x-coordinate of the midpoint of its diagonals?", "2", "The midpoint of (0, 0) and (4, 3) is (2, 3/2).", "Average the x-values of opposite corners."),
            question("os4", "A(0, 0), B(4, 1), C(5, 4), and D(1, 3) are the corners of a quadrilateral. Which fact best shows it is a parallelogram?",
                     "Opposite sides AB and DC have equal slope and equal length",
                     "AB and DC both change by (4, 1), and AD and BC both change by (1, 3).",
                     "Compare each side with the side opposite it.",
                     ["Opposite sides AB and DC have equal slope and equal length", "Diagonal AC is longer than AB",
                      "All four points have positive coordinates", "The midpoint of AB lies on the x-axis"]),
            question("os5", "A right triangle has vertices (0, 0), (6, 0), and (0, 8). What is its area?", "24", "Half of 6 times 8 is 24.", "Use the two legs along the axes."),
        ],
    },
    {
        "id": "coord-polar", "skill": "geo-polar", "title": "Angle and distance",
        "subtitle": "Describe a point by how far away it is and which way it points.",
        "duration": 10, "color": "blue", "icon": "graph",
        "intro": "There is another way to say where a point is. Instead of 'right 3, up 4', say "
                 "how far it is from the origin and which direction it lies in. The distance is "
                 "r. The direction is an angle measured counterclockwise from the right-hand "
                 "side of the x-axis: 0 degrees points right, 90 up, 180 left, and 270 down. So "
                 "a point 5 units from the origin at 90 degrees is straight up at (0, 5). To find "
                 "r from (x, y), use the distance formula. When you know the angle's ratios, "
                 "x = r times cos and y = r times sin: if the ratios are 0.6 and 0.8 and r is 10, "
                 "the point is (6, 8). Turn the angle and stretch the distance in the explorer.",
        "takeaway": "A point can be (right, up) or (distance, angle).",
        "visual": "polar-explorer", "formula": "x = r cos, y = r sin",
        "exercises": [
            question("hp1", "A point is 7 units from the origin at an angle of 180 degrees. What is its x-coordinate?", "-7",
                     "180 degrees points left, so the point is at (-7, 0).", "Which way does 180 degrees point?"),
            question("hp2", "A point is 5 units from the origin at an angle of 90 degrees. What is its y-coordinate?", "5",
                     "90 degrees points straight up, so the point is (0, 5).", "Which way does 90 degrees point?"),
            question("hp3", "What is the distance r from the origin to the point (6, 8)?", "10",
                     "The legs are 6 and 8, and 36 + 64 = 100, so r = 10.", "Use the distance relationship from the origin."),
            question("hp4", "A point is 10 units from the origin where cos is 0.6 and sin is 0.8. What is its y-coordinate?", "8",
                     "y = r times sin = 10 times 0.8 = 8.", "Multiply the distance by the sin value."),
            question("hp5", "Which description matches the point (0, -4)?", "r = 4, angle 270 degrees",
                     "The point is 4 units from the origin straight down, which is 270 degrees.", "Which way does the point lie from the origin?",
                     ["r = 4, angle 270 degrees", "r = 4, angle 90 degrees", "r = 4, angle 0 degrees", "r = 4, angle 180 degrees"]),
        ],
    },
]
LESSONS.extend(GEOMETRY_LESSONS)

PRACTICE.update({
    "geom-measure": [
        question("zm1", "A rectangle is 9 cm wide and 3 cm tall. What is its perimeter in cm?", "24", "9 + 3 + 9 + 3 = 24.", "Add all four sides."),
        question("zm2", "A square has sides of 7 cm. What is its area in square cm?", "49", "7 times 7 is 49.", "A square is a rectangle with equal sides."),
        question("zm3", "A triangle has a base of 8 cm and a height of 5 cm. What is its area in square cm?", "20", "Half of 8 times 5 is 20.", "Halve the rectangle's area."),
        question("zm4", "A shape is a 5 m by 5 m square joined to a 2 m by 3 m rectangle, with no overlap. What is its total area in square m?", "31", "25 + 6 = 31.", "Find each piece and add."),
    ],
    "geom-angles": [
        question("za1", "What is the complement of a 62 degree angle?", "28", "90 - 62 = 28.", "Complementary angles add to 90."),
        question("za2", "What is the supplement of a 45 degree angle?", "135", "180 - 45 = 135.", "Supplementary angles add to 180."),
        question("za3", "A triangle has angles of 30 degrees and 90 degrees. What is the third angle?", "60", "180 - 120 = 60.", "The three angles add to 180."),
        question("za4", "Three angles of a quadrilateral are 85, 95, and 110 degrees. What is the fourth angle?", "70", "360 - 290 = 70.", "The four angles add to 360."),
    ],
    "coord-polar": [
        question("zp1", "A point is 9 units from the origin at an angle of 0 degrees. What is its x-coordinate?", "9", "0 degrees points right.", "Which way does 0 degrees point?"),
        question("zp2", "A point is 6 units from the origin at an angle of 270 degrees. What is its y-coordinate?", "-6", "270 degrees points straight down.", "Down is negative y."),
        question("zp3", "What is the distance from the origin to (5, 12)?", "13", "25 + 144 = 169.", "Use the legs 5 and 12."),
        question("zp4", "A point is 20 units from the origin where cos is 0.8 and sin is 0.6. What is its x-coordinate?", "16", "x = 20 times 0.8 = 16.", "Multiply by the cos value."),
    ],
})

_geometry_extra = [
    ("geom-measure", question("wm1", "A rectangle is 14 cm wide and 6 cm tall. What is its perimeter in cm?", "40", "14 + 6 + 14 + 6 = 40.", "Add all four sides.")),
    ("geom-measure", question("wm2", "A triangle has a base of 12 cm and a height of 7 cm. What is its area in square cm?", "42", "Half of 12 times 7 is 42.", "Halve the rectangle's area.")),
    ("geom-angles", question("wa1", "A triangle has angles of 72 degrees and 58 degrees. What is the third angle?", "50", "180 - 130 = 50.", "The three angles add to 180.")),
    ("geom-angles", question("wa2", "How many degrees is each angle of an equilateral triangle?", "60", "Three equal angles share 180, so each is 60.", "The three angles are equal.")),
    ("coord-polar", question("wp1", "What is the distance from the origin to (-8, 6)?", "10", "64 + 36 = 100.", "Use the legs 8 and 6.")),
    ("coord-polar", question("wp2", "A point is 13 units from the origin where cos is 5/13 and sin is 12/13. What is its x-coordinate?", "5", "x = 13 times 5/13 = 5.", "Multiply the distance by cos.")),
]


PRACTICE.update({
    "coord-points": [
        question("qp1", "Which point is 4 units left and 1 unit up from the origin?", "(-4, 1)", "Left 4 gives x = -4 and up 1 gives y = 1.", "Left is negative x.", ["(-4, 1)", "(4, -1)", "(1, -4)", "(-1, 4)"]),
        question("qp2", "In which quadrant is (2, -6)?", "Quadrant IV", "x is positive and y is negative.", "Check each sign.", ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"]),
        question("qp3", "Reflect (-5, 2) across the y-axis. What is the new x-coordinate?", "5", "The sign of x flips.", "Only x changes."),
        question("qp4", "Move (-3, 2) 5 units right and 6 units down. What is its new y-coordinate?", "-4", "2 - 6 = -4.", "Down subtracts from y."),
    ],
    "coord-grid": [
        question("qg1", "How far apart are (1, 3) and (10, 3)?", "9", "The y-values match, so subtract x-values: 9.", "Which coordinate is shared?"),
        question("qg2", "How far apart are (5, -2) and (5, 6)?", "8", "6 - (-2) = 8.", "Subtract carefully."),
        question("qg3", "How far apart are (-6, 2) and (-1, 2)?", "5", "-1 - (-6) = 5.", "Subtract the smaller x from the larger."),
        question("qg4", "A rectangle has corners (0, 0), (7, 0), (7, 2), and (0, 2). What is its area?", "14", "7 times 2 is 14.", "Find width and height."),
    ],
    "coord-midpoint": [
        question("qm1", "What is the x-coordinate of the midpoint of (0, 4) and (10, 8)?", "5", "The average of 0 and 10 is 5.", "Add and halve."),
        question("qm2", "What is the y-coordinate of the midpoint of (1, -3) and (5, 9)?", "3", "The average of -3 and 9 is 3.", "Add and halve."),
        question("qm3", "M(2, -1) is the midpoint of A(-1, 4) and B. What is the y-coordinate of B?", "-6", "-1 = (4 + y) / 2, so y = -6.", "Double M, then subtract A."),
        question("qm4", "What is the x-coordinate of the midpoint of (-7, 0) and (2, 6)? Enter a fraction or decimal.", "-5/2", "(-7 + 2) / 2 = -5/2.", "Add the x-values and halve."),
    ],
    "coord-distance": [
        question("qd1", "What is the distance between (0, 0) and (6, 8)?", "10", "36 + 64 = 100.", "Use the legs 6 and 8."),
        question("qd2", "What is the distance between (2, 1) and (5, 5)?", "5", "The legs are 3 and 4.", "Find dx and dy."),
        question("qd3", "What is the distance between (-3, -2) and (2, 10)?", "13", "The legs are 5 and 12.", "Subtract in the same order."),
        question("qd4", "What is the squared distance between (1, 2) and (4, 4)?", "13", "9 + 4 = 13.", "dx is 3 and dy is 2."),
    ],
    "coord-lines": [
        question("ql1", "What is the slope of the line through (0, 1) and (4, 9)?", "2", "The rise is 8 and the run is 4.", "Divide rise by run."),
        question("ql2", "A line has slope -3. What is the slope of a perpendicular line?", "1/3", "The negative reciprocal of -3 is 1/3.", "Flip and change the sign."),
        question("ql3", "A line has slope 5/2. What is the slope of a perpendicular line?", "-2/5", "The negative reciprocal of 5/2 is -2/5.", "Flip and change the sign."),
        question("ql4", "Which line is parallel to y = 3x + 1?", "y = 3x - 7", "Parallel lines share a slope of 3.", "Compare the slopes.", ["y = 3x - 7", "y = -3x + 1", "y = x/3 + 1", "y = -x/3 + 1"]),
    ],
    "coord-shapes": [
        question("qs1", "A rectangle has corners (0, 0), (5, 0), (5, 12), and (0, 12). What is the length of its diagonal?", "13", "25 + 144 = 169.", "The sides are the legs."),
        question("qs2", "A triangle has vertices (0, 0), (3, 0), and (3, 4). What is its perimeter?", "12", "The sides are 3, 4, and 5.", "Find the slanted side first."),
        question("qs3", "A rectangle has corners (0, 0), (6, 0), (6, 4), and (0, 4). What is the y-coordinate of the midpoint of its diagonals?", "2", "The midpoint of (0, 0) and (6, 4) is (3, 2).", "Average opposite corners."),
        question("qs4", "A right triangle has vertices (0, 0), (10, 0), and (0, 6). What is its area?", "30", "Half of 10 times 6 is 30.", "Use the legs on the axes."),
    ],
})

COURSE_ASSESSMENTS["coordinate-geometry"] = [
    ("coord-points", question("gp1", "In which quadrant is (-3, -7)?", "Quadrant III", "Both coordinates are negative.", "Check each sign.", ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"])),
    ("coord-points", question("gp2", "Reflect (6, -2) across the x-axis. What is the new y-coordinate?", "2", "The sign of y flips.", "Only y changes.")),
    ("coord-grid", question("gg1", "How far apart are (-5, 3) and (2, 3)?", "7", "2 - (-5) = 7.", "Which coordinate is shared?")),
    ("coord-grid", question("gg2", "A rectangle has corners (-3, -2), (3, -2), (3, 1), and (-3, 1). What is its perimeter?", "18", "The width is 6 and the height is 3, so 2(6) + 2(3) = 18.", "Find width and height.")),
    ("coord-midpoint", question("gm1", "What is the y-coordinate of the midpoint of (3, -8) and (9, 4)?", "-2", "The average of -8 and 4 is -2.", "Add and halve.")),
    ("coord-midpoint", question("gm2", "M(-2, 5) is the midpoint of A(4, 1) and B. What is the x-coordinate of B?", "-8", "-2 = (4 + x) / 2, so x = -8.", "Double M, then subtract A.")),
    ("coord-distance", question("gd1", "What is the distance between (0, 0) and (5, 12)?", "13", "25 + 144 = 169.", "Use the legs 5 and 12.")),
    ("coord-distance", question("gd2", "What is the distance between (-1, -1) and (7, 5)?", "10", "The legs are 8 and 6, so the distance is 10.", "Find dx and dy.")),
    ("coord-lines", question("gl1", "A line has slope 1/5. What is the slope of a perpendicular line?", "-5", "The negative reciprocal of 1/5 is -5.", "Flip and change the sign.")),
    ("coord-lines", question("gl2", "Which pair of slopes describes perpendicular lines?", "3/4 and -4/3", "Their product is -1.", "Multiply each pair.", ["3/4 and -4/3", "3/4 and 4/3", "3/4 and -3/4", "3/4 and 3/4"])),
    ("coord-shapes", question("gs1", "A right triangle has vertices (0, 0), (8, 0), and (8, 15). What is the length of the side from (0, 0) to (8, 15)?", "17", "64 + 225 = 289.", "The legs are 8 and 15.")),
    ("coord-shapes", question("gs2", "A right triangle has vertices (0, 0), (9, 0), and (0, 4). What is its area?", "18", "Half of 9 times 4 is 18.", "Use the legs on the axes.")),
]
COURSE_ASSESSMENTS["coordinate-geometry"] += _geometry_extra
_geometry_order = [lesson["id"] for lesson in GEOMETRY_LESSONS]
COURSE_ASSESSMENTS["coordinate-geometry"].sort(key=lambda item: _geometry_order.index(item[0]))

SKILLS.extend([
    {"id": "hist-counting", "name": "Counting and matching", "prerequisites": []},
    {"id": "hist-symbols", "name": "Writing numbers with symbols", "prerequisites": ["hist-counting"]},
    {"id": "hist-place", "name": "Place value and zero", "prerequisites": ["hist-symbols"]},
    {"id": "hist-arith", "name": "Methods of calculating", "prerequisites": ["hist-place"]},
    {"id": "hist-fractions", "name": "Sharing and unit fractions", "prerequisites": ["hist-arith"]},
    {"id": "hist-negatives", "name": "Debts and negative numbers", "prerequisites": ["hist-arith"]},
    {"id": "hist-algebra", "name": "Balancing and restoring", "prerequisites": ["hist-negatives", "hist-fractions"]},
    {"id": "hist-geometry", "name": "Measuring, proving, and mapping", "prerequisites": ["hist-algebra"]},
])

HISTORY_LESSONS = [
    {
        "id": "history-counting", "skill": "hist-counting", "title": "Before numbers",
        "subtitle": "How people kept track of things before they had number words.",
        "duration": 6, "color": "yellow", "icon": "graph",
        "intro": "People counted long before they wrote numbers. A herder could drop one pebble "
                 "into a bag for each animal that left in the morning, then match the pebbles "
                 "to the animals coming home at night. A pebble left over meant an animal was "
                 "missing. That is one-to-one matching, and it works with no number names at all. "
                 "Notches on old bones, such as the Ishango bone found in central Africa, may be "
                 "early tallies, although scholars still debate what they were for. Plain tallies "
                 "become hard to read as they grow, so people grouped them, often in fives. That "
                 "need to group is the seed of every number system.",
        "takeaway": "Matching things one-to-one is counting, even without number names.",
        "visual": "number-systems-explorer", "formula": "one pebble = one animal",
        "exercises": [
            question("yc1", "A herder puts one pebble in a bag for each sheep that leaves. In the evening, 3 pebbles are left after matching one to each returning sheep. How many sheep are missing?",
                     "3", "Each leftover pebble stands for a sheep that did not come back.", "Match each returning sheep to one pebble."),
            question("yc2", "You make tally marks in bundles of 5. You see 4 full bundles and 3 extra marks. How many things were counted?",
                     "23", "Four bundles of 5 make 20, and 3 more makes 23.", "Count the bundles first, then the extras."),
            question("yc3", "Why is a plain row of 87 tally strokes hard to use?",
                     "It is hard to see the total at a glance without grouping",
                     "Without groups, you have to count every stroke again each time.", "Think about reading the total quickly.",
                     ["It is hard to see the total at a glance without grouping", "Strokes cannot show numbers above 50",
                      "Tallies were never used for counting", "The strokes would have different sizes"]),
            question("yc4", "How many full bundles of 5 can you make from 37 tally marks?",
                     "7", "Seven bundles use 35 marks, with 2 left over.", "Divide 37 into groups of 5."),
        ],
    },
    {
        "id": "history-symbols", "skill": "hist-symbols", "title": "Symbols for bigger numbers",
        "subtitle": "Why a different picture for 1, 10, and 100 only goes so far.",
        "duration": 7, "color": "peach", "icon": "graph",
        "intro": "To write bigger numbers, ancient Egyptian scribes used a different picture for "
                 "1, 10, 100, and 1,000, and repeated each one as many times as needed. To write "
                 "243 they used 2 hundred-symbols, 4 ten-symbols, and 3 one-symbols: 9 symbols in "
                 "all. You find the value by adding, so the order of the symbols did not matter. "
                 "This works, but it gets long: 999 needs 27 symbols. Roman numerals shorten some "
                 "numbers with symbols like V and X, but they are also mostly additive, which makes "
                 "everyday arithmetic awkward. People kept looking for a shorter way to write the "
                 "same number. Slide the number in the explorer to compare.",
        "takeaway": "Additive systems repeat symbols, so big numbers get long.",
        "visual": "number-systems-explorer", "formula": "243 = 100 + 100 + 10 + 10 + 10 + 10 + 1 + 1 + 1",
        "exercises": [
            question("ys1", "In an additive system with symbols for 1, 10, and 100, how many symbols are needed to write 312?",
                     "6", "That is 3 hundreds, 1 ten, and 2 ones: 3 + 1 + 2 = 6 symbols.", "Count hundreds, tens, and ones separately."),
            question("ys2", "In the same system, how many symbols are needed to write 999?",
                     "27", "That is 9 hundreds, 9 tens, and 9 ones: 9 + 9 + 9 = 27 symbols.", "Count hundreds, tens, and ones separately."),
            question("ys3", "In an additive system, does the order of the symbols change the number's value?",
                     "No, you just add the values", "The value is the sum of all the symbols, whatever the order.",
                     "How do you find the value of an additive number?",
                     ["No, you just add the values", "Yes, the first symbol counts double", "Yes, the last symbol counts double"]),
            question("ys4", "A scribe writes 4 hundred-symbols, 0 ten-symbols, and 5 one-symbols. What number is that?",
                     "405", "4 hundreds and 5 ones make 405.", "Add the value of each group of symbols."),
        ],
    },
    {
        "id": "history-place-value", "skill": "hist-place", "title": "Position gives value, and zero holds the place",
        "subtitle": "The shorter idea that changed how everyone writes numbers.",
        "duration": 8, "color": "mint", "icon": "graph",
        "intro": "A much shorter idea is place value: a digit's value depends on where it sits. In "
                 "305, the 3 means three hundreds because of its position. But then you need a way "
                 "to show an empty place, or 305 and 35 could look alike. Babylonian scribes, who "
                 "counted in groups of 60, eventually used a mark as a placeholder. Mathematicians "
                 "in India developed a base-ten system with a symbol for zero, and around 628 CE "
                 "Brahmagupta wrote rules for calculating with zero as a number in its own right. "
                 "These ideas travelled through the Islamic world, where scholars such as "
                 "al-Khwarizmi wrote about them, and reached Europe in books like Fibonacci's "
                 "Liber Abaci in 1202. The word algorithm comes from al-Khwarizmi's name.",
        "takeaway": "Place value writes any number with just ten digits, and zero keeps places in order.",
        "visual": "number-systems-explorer", "formula": "305 = 3 hundreds + 0 tens + 5 ones",
        "exercises": [
            question("yp1", "In the number 3,052, what value does the digit 5 stand for?", "50",
                     "The 5 is in the tens place, so it means 5 tens, which is 50.", "Which place is the 5 in?"),
            question("yp2", "What does the zero in 305 show?", "An empty tens place",
                     "The zero holds the tens place so the 3 stays in the hundreds place.", "Compare 305 with 35.",
                     ["An empty tens place", "An empty ones place", "An empty hundreds place", "Nothing; it can be ignored"]),
            question("yp3", "How many digits does place value need to write 999?", "3",
                     "Place value writes 999 with three digits, compared with 27 symbols in the additive system.", "Count the digits."),
            question("yp4", "What number has 4 in the hundreds place, 0 in the tens place, and 7 in the ones place?", "407",
                     "4 hundreds, 0 tens, and 7 ones make 407.", "Write the digits in order of their places."),
        ],
    },
    {
        "id": "history-arithmetic", "skill": "hist-arith", "title": "Doubling and carrying",
        "subtitle": "How scribes multiplied with only doubling and adding.",
        "duration": 8, "color": "blue", "icon": "graph",
        "intro": "Scribes needed to multiply for taxes, grain, and building. An Egyptian method "
                 "recorded in the Rhind Papyrus, copied around 1550 BCE, uses only doubling and "
                 "adding. To find 13 times 12, write the doubles of 12: 12, 24, 48, 96. Since "
                 "13 = 1 + 4 + 8, add the rows for 1, 4, and 8: 12 + 48 + 96 = 156. It works "
                 "because every whole number can be built by adding different powers of two. "
                 "Later, place value allowed the column methods many people learn, where carrying "
                 "moves ten ones into one ten. Choose two numbers in the explorer and watch which "
                 "rows are picked.",
        "takeaway": "Any whole number is a sum of doublings, so multiplying can be done by doubling and adding.",
        "visual": "doubling-explorer", "formula": "13 x 12 = (1 + 4 + 8) x 12",
        "exercises": [
            question("yr1", "Using doubling, the rows for 12 are 1 row is 12, 2 rows is 24, 4 rows is 48, and 8 rows is 96. Which rows add up to 13?",
                     "1, 4, and 8", "1 + 4 + 8 = 13, so add 12 + 48 + 96.", "Find rows that add to 13.",
                     ["1, 4, and 8", "2, 4, and 8", "1, 2, and 8", "1, 2, and 4"]),
            question("yr2", "Use doubling to find 9 times 7. Hint: 9 = 8 + 1.", "63",
                     "8 times 7 is 56, and 1 times 7 is 7, so the total is 63.", "Double 7 three times, then add the 1 row."),
            question("yr3", "Using rows 1, 2, 4, 8, and 16, which is the largest row needed to make 20?", "16",
                     "20 = 16 + 4, so the largest row is 16.", "Take the biggest row that is not more than 20."),
            question("yr4", "When adding 47 + 38 by hand, how many tens do you carry from the ones column?", "1",
                     "7 + 8 = 15 ones, which is 1 ten and 5 ones, so you carry 1 ten.", "Add the ones first."),
        ],
    },
    {
        "id": "history-fractions", "skill": "hist-fractions", "title": "Sharing and measuring",
        "subtitle": "Why people needed numbers for parts of a whole.",
        "duration": 8, "color": "violet", "icon": "fraction",
        "intro": "When grain, land, or loaves had to be shared, whole numbers were not enough. "
                 "Egyptian scribes wrote most fractions as sums of different unit fractions, which "
                 "have 1 on top. They wrote three quarters as one half plus one quarter. The Rhind "
                 "Papyrus includes a table that rewrites 2 divided by odd numbers this way. Other "
                 "cultures chose other tools: Babylonian scribes used base-60 fractions, which is "
                 "one reason we still split hours into 60 minutes. A way to write part of a whole "
                 "let people measure more precisely than counting alone.",
        "takeaway": "Fractions grew from fair sharing and careful measuring.",
        "visual": "fraction-explorer", "formula": "3/4 = 1/2 + 1/4",
        "exercises": [
            question("yf1", "An Egyptian scribe writes three quarters as 1/2 plus a unit fraction. Which unit fraction completes it?",
                     "1/4", "1/2 + 1/4 = 2/4 + 1/4 = 3/4.", "Rewrite 1/2 in quarters."),
            question("yf2", "Add 1/2 + 1/3. What is the total as a fraction?", "5/6",
                     "In sixths, 3/6 + 2/6 = 5/6.", "Use a common denominator of 6."),
            question("yf3", "Which sum of different unit fractions equals 7/8?", "1/2 + 1/4 + 1/8",
                     "In eighths, 4/8 + 2/8 + 1/8 = 7/8.", "Rewrite each choice in eighths where you can.",
                     ["1/2 + 1/4 + 1/8", "1/2 + 1/3 + 1/6", "1/4 + 1/4 + 1/4", "1/2 + 1/8 + 1/8"]),
            question("yf4", "A scribe shares 3 loaves equally among 4 workers. How much does each worker get? Enter a fraction.",
                     "3/4", "Each worker gets 3 divided by 4, which is 3/4 of a loaf.", "Share 3 equally among 4."),
        ],
    },
    {
        "id": "history-negatives", "skill": "hist-negatives", "title": "Owing, owning, and opposites",
        "subtitle": "How debts gave negative numbers a meaning.",
        "duration": 8, "color": "peach", "icon": "graph",
        "intro": "Merchants and tax collectors had to track both what they had and what they owed. "
                 "Counting rods in China used one colour for gains and another for losses, and an "
                 "old Chinese text, the Nine Chapters on the Mathematical Art, includes rules for "
                 "adding and subtracting them. In the 600s CE the Indian mathematician Brahmagupta "
                 "wrote rules for fortunes (positive) and debts (negative). Many European "
                 "mathematicians resisted negative numbers for centuries because they did not seem "
                 "to measure anything. Money owed gave them a meaning: if you have 3 coins and owe "
                 "5, your net total is -2. Move the sliders in the explorer.",
        "takeaway": "A negative number can mean a debt, a loss, or the opposite direction.",
        "visual": "ledger-explorer", "formula": "have 3, owe 5: 3 - 5 = -2",
        "exercises": [
            question("yn1", "You have 3 coins and owe 5 coins. What is your net total in coins?", "-2",
                     "3 - 5 = -2, meaning you are 2 coins short.", "Subtract what you owe from what you have."),
            question("yn2", "You owe 8 coins, then someone pays 3 coins of your debt. What is your net total now?", "-5",
                     "You still owe 5, so the net total is -5.", "Paying a debt moves you toward zero."),
            question("yn3", "You owe 4 coins and owe another 6 coins. What is your net total?", "-10",
                     "Two debts add up: -4 + -6 = -10.", "Combine both debts."),
            question("yn4", "What is the opposite of owing 7 coins?", "Having 7 coins",
                     "Opposites sit the same distance from zero on opposite sides: -7 and 7.", "Think of a number line.",
                     ["Having 7 coins", "Owing 14 coins", "Having 0 coins", "Owing 7 coins"]),
        ],
    },
    {
        "id": "history-algebra", "skill": "hist-algebra", "title": "Solving puzzles by balance",
        "subtitle": "How restoring and balancing became algebra.",
        "duration": 9, "color": "mint", "icon": "balance",
        "intro": "For thousands of years scribes solved puzzles about unknown amounts using words. "
                 "In Baghdad around 820 CE, al-Khwarizmi wrote a book on solving equations with "
                 "two moves: al-jabr, restoring, which moves a subtracted amount to the other side "
                 "as an added amount, and al-muqabala, balancing, which cancels equal amounts. The "
                 "word algebra comes from al-jabr. Letters for unknowns and the equals sign came "
                 "much later: Robert Recorde introduced = in 1557 and chose two parallel lines "
                 "because he thought no two things could be more alike. Try changing the equation "
                 "in the explorer and watch each step stay balanced.",
        "takeaway": "Restore, balance, and keep both sides equal.",
        "visual": "equation-explorer", "formula": "x - 5 = 9  =>  x = 9 + 5",
        "exercises": [
            question("ya1", "Restore the subtracted amount: x - 5 = 9. Add 5 to both sides. What is x?", "14",
                     "x = 9 + 5 = 14.", "Undo subtracting 5 by adding 5."),
            question("ya2", "Balance by cancelling equal amounts: x + 6 = 6 + 11. What is x?", "11",
                     "Cancel the 6 on both sides, leaving x = 11.", "What can you remove from both sides?"),
            question("ya3", "Which symbol did Robert Recorde choose for equality, and why?",
                     "Two parallel lines, because nothing is more alike",
                     "He drew two short parallel lines because he thought no two things could be more alike.",
                     "Think about what the sign is meant to show.",
                     ["Two parallel lines, because nothing is more alike", "Two crossing lines, because the sides meet",
                      "A circle, because it has no end", "A dot, because it is small"]),
            question("ya4", "Solve 2x + 3 = 11.", "4", "Subtract 3 to get 2x = 8, then divide by 2.", "Undo the addition first."),
        ],
    },
    {
        "id": "history-geometry", "skill": "hist-geometry", "title": "From land to proof to maps",
        "subtitle": "Measuring fields, proving statements, and putting points on a grid.",
        "duration": 9, "color": "blue", "icon": "graph",
        "intro": "Greek writers such as Herodotus said geometry grew from re-measuring farmland "
                 "after the Nile floods. Surveyors needed square corners and areas. Some "
                 "historians think rope stretchers made a right angle by knotting a loop of rope "
                 "into 12 equal sections and pulling it into a triangle with sides of 3, 4, and 5 "
                 "sections. A Babylonian clay tablet called Plimpton 322, from around 1800 BCE, "
                 "lists number triples with the same triangle relationship, though scholars debate "
                 "its purpose. Around 300 BCE, Euclid organised geometry in the Elements by "
                 "starting from a few simple statements and proving everything else step by step. "
                 "In 1637 Rene Descartes linked algebra and geometry with coordinates, and Pierre "
                 "de Fermat developed a similar idea.",
        "takeaway": "Geometry began with measuring, grew into proof, and joined algebra through coordinates.",
        "visual": "plane-explorer", "formula": "3 squared + 4 squared = 5 squared",
        "exercises": [
            question("yg1", "A rope loop has 12 equal sections. It is pulled into a triangle with sides of 3, 4, and 5 sections. Which angle is the right angle?",
                     "The angle between the 3 and 4 sides", "The right angle is opposite the longest side, so it sits between the 3 and 4 sides.",
                     "The longest side is opposite the right angle.",
                     ["The angle between the 3 and 4 sides", "The angle between the 4 and 5 sides",
                      "The angle between the 3 and 5 sides", "No angle is a right angle"]),
            question("yg2", "A right triangle has legs of 6 and 8 rope sections. How long is the longest side?", "10",
                     "36 + 64 = 100, so the longest side is 10.", "Use the relationship from the 3-4-5 triangle."),
            question("yg3", "What did Euclid's Elements do for geometry?",
                     "It organised it by proving statements from a few simple starting ones",
                     "Euclid showed how to build a whole subject from a few starting statements and careful proofs.",
                     "Think about proof, not measuring.",
                     ["It organised it by proving statements from a few simple starting ones", "It invented the number zero",
                      "It introduced the equals sign", "It measured the Nile floods"]),
            question("yg4", "A point has coordinates (3, 4). What is its distance from the origin?", "5",
                     "9 + 16 = 25, so the distance is 5.", "Use the legs 3 and 4."),
        ],
    },
]
LESSONS.extend(HISTORY_LESSONS)

SKILLS.extend([
    {"id": "num-count", "name": "Counting and seeing numbers", "prerequisites": []},
    {"id": "num-place", "name": "Tens and ones", "prerequisites": ["num-count"]},
    {"id": "num-line", "name": "The number line and skip counting", "prerequisites": ["num-place"]},
    {"id": "add-facts", "name": "Putting amounts together", "prerequisites": ["num-line"]},
    {"id": "add-regroup", "name": "Adding bigger numbers", "prerequisites": ["add-facts", "num-place"]},
    {"id": "sub-gap", "name": "Taking away and finding the gap", "prerequisites": ["add-regroup"]},
    {"id": "mul-groups", "name": "Equal groups and arrays", "prerequisites": ["add-facts"]},
    {"id": "mul-tables", "name": "Patterns in the times tables", "prerequisites": ["mul-groups"]},
    {"id": "div-share", "name": "Sharing and grouping", "prerequisites": ["mul-tables", "sub-gap"]},
])

BEGINNER_LESSONS = [
    {
        "id": "num-count", "skill": "num-count", "title": "Count and see numbers",
        "subtitle": "Use a ten-frame to see how many without counting every dot.",
        "duration": 6, "color": "yellow", "icon": "fraction",
        "intro": "Counting means saying one number for each thing, exactly once. A ten-frame is a "
                 "tray with two rows of five spots. When a row is full you can see 5 without "
                 "counting, and when the whole tray is full you can see 10. Numbers past 10 start a "
                 "second tray. Seeing 7 as 5 and 2 more is faster than counting seven dots one by "
                 "one, and it helps with adding later. Slide the dots and watch the trays fill.",
        "takeaway": "Group dots in fives and tens, and you can see a number at a glance.",
        "visual": "tenframe-explorer", "formula": "10 = 5 + 5",
        "exercises": [
            question("nc1", "A ten-frame has 6 dots. How many empty spots are left?", "4",
                     "The tray holds 10, and 10 - 6 = 4.", "Count the empty spots, or think: what goes with 6 to make 10?"),
            question("nc2", "One full ten-frame and 3 dots in a second tray. How many dots in all?", "13",
                     "10 and 3 more make 13.", "A full tray is 10."),
            question("nc3", "The top row of a ten-frame is full and the bottom row has 2 dots. What number is shown?", "7",
                     "A full row is 5, and 5 + 2 = 7.", "A full row is 5."),
            question("nc4", "What number is one more than 19?", "20",
                     "One more than 19 is 20.", "Count on one step.", ["18", "20", "29", "91"]),
        ],
    },
    {
        "id": "num-place", "skill": "num-place", "title": "Tens and ones",
        "subtitle": "Trade ten small cubes for one long rod.",
        "duration": 7, "color": "mint", "icon": "fraction",
        "intro": "Ten ones make one ten. We draw a ten as a long rod and a one as a small cube. "
                 "The number 34 is 3 rods and 4 cubes: 3 tens and 4 ones. The place a digit sits "
                 "tells its worth. In 34, the 3 is worth 30 and the 4 is worth 4. When you collect "
                 "10 cubes, trade them for 1 rod. Slide the number and watch the rods and cubes "
                 "change.",
        "takeaway": "A digit's place tells its worth: tens first, then ones.",
        "visual": "blocks-explorer", "formula": "34 = 3 tens + 4 ones",
        "exercises": [
            question("np1", "How many tens are in 47?", "4", "47 is 4 tens and 7 ones.", "Look at the first digit."),
            question("np2", "In the number 58, what is the value of the 5?", "50", "The 5 is in the tens place, so it means 5 tens: 50.", "Which place is the 5 in?"),
            question("np3", "3 tens and 6 ones make what number?", "36", "30 and 6 make 36.", "Write the tens, then the ones."),
            question("np4", "Which number has 2 tens and 9 ones?", "29", "2 tens and 9 ones make 29.", "Tens come first.", ["92", "29", "209", "11"]),
        ],
    },
    {
        "id": "num-line", "skill": "num-line", "title": "The number line and skipping",
        "subtitle": "Hop along a line to count by 2s, 5s, and 10s.",
        "duration": 7, "color": "blue", "icon": "fraction",
        "intro": "A number line puts numbers in order along a line with equal spaces. Counting up "
                 "moves right, and counting down moves left. Skip counting hops the same distance "
                 "each time: by 2s you land on 2, 4, 6, 8, and by 5s you land on 5, 10, 15. The "
                 "farther right a number sits, the bigger it is, so you can compare any two numbers "
                 "by looking at where they sit. Change the hop size and the number of hops.",
        "takeaway": "Numbers further right on the line are bigger.",
        "visual": "hops-explorer", "formula": "4 hops of 3 = 12",
        "exercises": [
            question("nl1", "Skip count by 5s: 5, 10, 15, 20, 25, ... What number comes next?", "30", "25 + 5 = 30.", "Hop 5 more."),
            question("nl2", "Start at 0 and make 4 hops of 3. Where do you land?", "12", "3, 6, 9, 12.", "Count the hops."),
            question("nl3", "Which number is greater, 47 or 39?", "47", "47 has more tens than 39, so it sits further right.", "Compare the tens first.", ["47", "39", "They are equal"]),
            question("nl4", "Count by 10s: 40, 50, 60, ... What number comes after 90?", "100", "90 + 10 = 100.", "Hop 10 more."),
        ],
    },
    {
        "id": "add-facts", "skill": "add-facts", "title": "Putting amounts together",
        "subtitle": "Make a ten to add quickly.",
        "duration": 8, "color": "peach", "icon": "fraction",
        "intro": "Adding means putting amounts together to find how many in all. Two ten-frames "
                 "show a smart trick called make ten: move dots from one tray to fill the other to "
                 "10, then count what is left. For 8 + 5, move 2 dots to fill the first tray, "
                 "leaving 3: that is 10 + 3 = 13. The order does not matter, so 8 + 5 is the same "
                 "as 5 + 8. Try different pairs with the sliders.",
        "takeaway": "Make a ten first, then add the rest.",
        "visual": "tenframe-explorer", "formula": "8 + 5 = 10 + 3",
        "exercises": [
            question("af1", "What is 6 + 4?", "10", "6 and 4 fill a ten-frame exactly.", "What goes with 6 to make 10?"),
            question("af2", "What is 8 + 5? Make ten first: 8 + 2 = 10.", "13", "8 + 2 = 10, then 3 more makes 13.", "Split the 5 into 2 and 3."),
            question("af3", "What is 7 + 8?", "15", "7 + 3 = 10, then 5 more makes 15.", "Make ten first."),
            question("af4", "Which sum is equal to 5 + 9?", "9 + 5", "Adding in a different order gives the same total.", "Does the order matter when adding?", ["9 + 5", "9 - 5", "5 - 9", "5 + 5"]),
        ],
    },
    {
        "id": "add-regroup", "skill": "add-regroup", "title": "Adding bigger numbers",
        "subtitle": "Carry a ten when the ones add up to ten or more.",
        "duration": 9, "color": "violet", "icon": "fraction",
        "intro": "To add 27 + 38, add the ones first: 7 + 8 = 15. That is 1 ten and 5 ones, so "
                 "write 5 in the ones place and carry 1 ten. Then add the tens: 2 + 3 + the 1 you "
                 "carried makes 6 tens. The answer is 65. Carrying is just trading 10 ones for 1 "
                 "ten, like trading 10 cubes for a rod. Try some pairs in the explorer and watch "
                 "when a ten gets carried.",
        "takeaway": "When ones reach ten, trade them for one ten and carry it.",
        "visual": "regroup-explorer", "formula": "27 + 38 = 65",
        "exercises": [
            question("ar1", "What is 27 + 38?", "65", "7 + 8 = 15, write 5 and carry 1. Then 2 + 3 + 1 = 6 tens.", "Add the ones first."),
            question("ar2", "When adding 46 + 29, how many tens do you carry from the ones?", "1", "6 + 9 = 15 ones, which is 1 ten and 5 ones.", "Add the ones first."),
            question("ar3", "What is 45 + 36?", "81", "5 + 6 = 11, carry 1. Then 4 + 3 + 1 = 8 tens, so 81.", "Add the ones, then the tens."),
            question("ar4", "What is 58 + 47?", "105", "8 + 7 = 15, carry 1. Then 5 + 4 + 1 = 10 tens, which is 100, so 105.", "Carry the ten, then add the tens."),
        ],
    },
    {
        "id": "sub-gap", "skill": "sub-gap", "title": "Taking away and finding the gap",
        "subtitle": "Two ways to think about subtracting, and how they connect to adding.",
        "duration": 9, "color": "mint", "icon": "fraction",
        "intro": "Subtracting can mean taking away or finding the gap between two numbers. If you "
                 "have 12 apples and eat 5, then 12 - 5 = 7 are left. If one tower has 12 blocks "
                 "and another has 5, the gap between them is also 7. Adding and subtracting undo "
                 "each other: because 5 + 7 = 12, we know 12 - 5 = 7 and 12 - 7 = 5. For 52 - 27 "
                 "you may need to trade 1 ten for 10 ones: 52 is 4 tens and 12 ones, and taking "
                 "away 2 tens and 7 ones leaves 2 tens and 5 ones, which is 25.",
        "takeaway": "Subtracting finds what is left or the gap, and adding checks it.",
        "visual": "gap-explorer", "formula": "5 + 7 = 12, so 12 - 5 = 7",
        "exercises": [
            question("sg1", "What is 12 - 5?", "7", "12 take away 5 leaves 7.", "Count back, or think 5 + ? = 12."),
            question("sg2", "Two towers have 15 and 9 blocks. How many more blocks does the taller tower have?", "6", "The gap is 15 - 9 = 6.", "Find the gap between the two heights."),
            question("sg3", "5 + 7 = 12. What is 12 - 7?", "5", "Adding and subtracting undo each other, so 12 - 7 = 5.", "Use the fact you know."),
            question("sg4", "What is 52 - 27?", "25", "Trade 1 ten for 10 ones: 4 tens and 12 ones minus 2 tens and 7 ones is 2 tens and 5 ones.", "You may need to trade a ten."),
        ],
    },
    {
        "id": "mul-groups", "skill": "mul-groups", "title": "Equal groups and arrays",
        "subtitle": "A fast way to add the same number again and again.",
        "duration": 8, "color": "yellow", "icon": "fraction",
        "intro": "Multiplying is a quick way to add equal groups. Three baskets with 4 apples each "
                 "makes 4 + 4 + 4 = 12, and we write 3 x 4 = 12. An array arranges objects in "
                 "rows and columns: 3 rows with 4 dots in each row. Turn the array on its side and "
                 "you get 4 rows of 3. The total stays the same, so 3 x 4 = 4 x 3. Use the sliders "
                 "to build arrays and see both ways to read them.",
        "takeaway": "Equal groups: rows times how many in each row.",
        "visual": "array-explorer", "formula": "3 x 4 = 4 + 4 + 4 = 12",
        "exercises": [
            question("mg1", "There are 4 baskets with 5 apples in each. How many apples in all?", "20", "4 groups of 5 is 4 x 5 = 20.", "Add 5 four times."),
            question("mg2", "An array has 3 rows with 6 dots in each row. How many dots?", "18", "3 x 6 = 18.", "Add 6 three times."),
            question("mg3", "What is 7 x 2?", "14", "Two groups of 7, or 7 + 7, is 14.", "Double 7."),
            question("mg4", "Which one equals 3 x 8?", "8 x 3", "Turning the array on its side swaps the numbers.", "Does the order matter in multiplying?", ["8 x 3", "8 + 3", "3 + 8", "8 - 3"]),
        ],
    },
    {
        "id": "mul-tables", "skill": "mul-tables", "title": "Patterns in the times tables",
        "subtitle": "Spot the patterns and learn the tables faster.",
        "duration": 8, "color": "peach", "icon": "fraction",
        "intro": "The times tables are full of patterns. Times 2 doubles a number: 2 x 7 = 14. "
                 "Times 10 puts a zero on the end: 10 x 6 = 60. Times 5 always ends in 0 or 5: "
                 "5, 10, 15, 20. For times 9, the digits of the answer add up to 9: 9 x 4 = 36, "
                 "and 3 + 6 = 9. Knowing 6 x 4 = 24 also tells you 4 x 6 = 24. Build an array in "
                 "the explorer and look for the pattern.",
        "takeaway": "Patterns make the tables easier: doubles, tens, fives, and nines.",
        "visual": "array-explorer", "formula": "9 x 4 = 36, and 3 + 6 = 9",
        "exercises": [
            question("mt1", "What is 10 x 7?", "70", "Times 10 puts a zero on the end of 7.", "Put a zero after the 7."),
            question("mt2", "What is 5 x 8?", "40", "Times 5 ends in 0 or 5: 5, 10, ..., 40.", "Count by 5s eight times."),
            question("mt3", "What is 9 x 3?", "27", "2 + 7 = 9, the nines pattern.", "Count by 9s three times."),
            question("mt4", "What is double 9? That is, 2 x 9.", "18", "Doubling 9 gives 18.", "Add 9 and 9."),
        ],
    },
    {
        "id": "div-share", "skill": "div-share", "title": "Sharing and grouping",
        "subtitle": "Share equally, and see what is left over.",
        "duration": 9, "color": "blue", "icon": "fraction",
        "intro": "Dividing means sharing equally or making equal groups. If 12 cookies are shared "
                 "among 3 friends, each gets 4, so 12 / 3 = 4. You can also ask how many groups of "
                 "3 fit in 12: that is 4 groups. Division undoes multiplication, because "
                 "3 x 4 = 12. Sometimes a few items are left over. That is called the remainder: "
                 "14 cookies shared among 3 friends gives 4 each, with 2 left over. Change the "
                 "numbers in the explorer and watch the sharing.",
        "takeaway": "Division shares equally, and the remainder is what is left over.",
        "visual": "sharing-explorer", "formula": "12 / 3 = 4",
        "exercises": [
            question("ds1", "12 cookies are shared equally among 3 friends. How many does each friend get?", "4", "12 / 3 = 4.", "Share one cookie at a time."),
            question("ds2", "How many groups of 5 can you make from 20 stickers?", "4", "4 groups use all 20 stickers, since 4 x 5 = 20.", "Count by 5s up to 20."),
            question("ds3", "3 x 7 = 21. What is 21 / 3?", "7", "Division undoes multiplication.", "Use the fact you know."),
            question("ds4", "14 cookies are shared equally among 3 friends. How many cookies are left over?", "2", "Each friend gets 4, which uses 12 cookies, so 2 are left over.", "Find the biggest share that fits, then see what remains."),
        ],
    },
]
LESSONS.extend(BEGINNER_LESSONS)

PRACTICE.update({
    "num-count": [
        question("tc1", "A ten-frame shows 8 dots. How many more dots fill it up?", "2", "10 - 8 = 2.", "What goes with 8 to make 10?"),
        question("tc2", "Two full ten-frames. How many dots are there?", "20", "10 and 10 make 20.", "A full frame is 10."),
        question("tc3", "The top row is full and the bottom row has 4 dots. What number is shown?", "9", "5 + 4 = 9.", "A full row is 5."),
        question("tc4", "What number is one less than 30?", "29", "One less than 30 is 29.", "Count back one step."),
    ],
    "num-place": [
        question("tp1", "How many ones are in 63?", "3", "63 is 6 tens and 3 ones.", "Look at the last digit."),
        question("tp2", "6 tens and 0 ones make what number?", "60", "6 tens is 60.", "Tens first, then ones."),
        question("tp3", "10 ones can be traded for how many tens?", "1", "10 ones make 1 ten.", "Trade cubes for a rod."),
        question("tp4", "In 71, what is the value of the 7?", "70", "The 7 is in the tens place.", "Which place is the 7 in?"),
    ],
    "num-line": [
        question("tl1", "Skip count by 2s: 2, 4, 6, 8, 10, 12, ... What comes next?", "14", "12 + 2 = 14.", "Hop 2 more."),
        question("tl2", "Start at 0 and make 6 hops of 5. Where do you land?", "30", "5, 10, 15, 20, 25, 30.", "Count the hops."),
        question("tl3", "Which number is smaller, 62 or 26?", "26", "26 has fewer tens, so it sits further left.", "Compare the tens first.", ["62", "26", "They are equal"]),
        question("tl4", "Count by 10s: 10, 20, 30, ... What number comes after 70?", "80", "70 + 10 = 80.", "Hop 10 more."),
    ],
    "add-facts": [
        question("ta1", "What is 9 + 3?", "12", "9 + 1 = 10, then 2 more makes 12.", "Make ten first."),
        question("ta2", "What is 6 + 7?", "13", "6 + 4 = 10, then 3 more makes 13.", "Make ten first."),
        question("ta3", "What is 8 + 8?", "16", "Doubling 8 gives 16.", "Add 8 and 8."),
        question("ta4", "What is 5 + 9?", "14", "9 + 1 = 10, then 4 more makes 14.", "Start from the bigger number."),
    ],
    "add-regroup": [
        question("tr1", "What is 34 + 28?", "62", "4 + 8 = 12, carry 1. Then 3 + 2 + 1 = 6 tens.", "Add the ones first."),
        question("tr2", "What is 19 + 17?", "36", "9 + 7 = 16, carry 1. Then 1 + 1 + 1 = 3 tens.", "Add the ones first."),
        question("tr3", "What is 65 + 29?", "94", "5 + 9 = 14, carry 1. Then 6 + 2 + 1 = 9 tens.", "Add the ones first."),
        question("tr4", "What is 77 + 25?", "102", "7 + 5 = 12, carry 1. Then 7 + 2 + 1 = 10 tens.", "Carry the ten."),
    ],
    "sub-gap": [
        question("ts1", "What is 14 - 6?", "8", "14 take away 6 leaves 8.", "Think 6 + ? = 14."),
        question("ts2", "Two towers have 20 and 13 blocks. How many more blocks does the taller tower have?", "7", "20 - 13 = 7.", "Find the gap."),
        question("ts3", "8 + 9 = 17. What is 17 - 9?", "8", "Subtracting undoes adding.", "Use the fact you know."),
        question("ts4", "What is 61 - 38?", "23", "Trade 1 ten for 10 ones: 5 tens and 11 ones minus 3 tens and 8 ones is 2 tens and 3 ones.", "You may need to trade a ten."),
    ],
    "mul-groups": [
        question("tg1", "There are 5 bags with 3 sweets in each. How many sweets in all?", "15", "5 x 3 = 15.", "Add 3 five times."),
        question("tg2", "An array has 4 rows with 7 dots in each row. How many dots?", "28", "4 x 7 = 28.", "Add 7 four times."),
        question("tg3", "What is 6 x 2?", "12", "Double 6.", "Add 6 and 6."),
        question("tg4", "What is 9 x 1?", "9", "One group of 9 is 9.", "Just one group."),
    ],
    "mul-tables": [
        question("tm1", "What is 10 x 4?", "40", "Put a zero after the 4.", "Times 10 adds a zero."),
        question("tm2", "What is 5 x 6?", "30", "Times 5 ends in 0 or 5.", "Count by 5s six times."),
        question("tm3", "What is 9 x 5?", "45", "The digits 4 and 5 add to 9.", "Count by 9s five times."),
        question("tm4", "What is 2 x 8?", "16", "Double 8.", "Add 8 and 8."),
    ],
    "div-share": [
        question("td1", "What is 15 / 5?", "3", "Three groups of 5 make 15.", "Count by 5s up to 15."),
        question("td2", "How many groups of 4 can you make from 24 pencils?", "6", "6 x 4 = 24.", "Count by 4s up to 24."),
        question("td3", "8 x 6 = 48. What is 48 / 8?", "6", "Division undoes multiplication.", "Use the fact you know."),
        question("td4", "17 sweets are shared equally among 5 friends. How many sweets are left over?", "2", "Each friend gets 3, using 15 sweets, so 2 are left over.", "Find the biggest share that fits."),
    ],
})

COURSE_ASSESSMENTS["counting-numbers"] = [
    ("num-count", question("vc1", "A ten-frame has 3 dots. How many more dots make 10?", "7", "10 - 3 = 7.", "What goes with 3 to make 10?")),
    ("num-count", question("vc2", "One full ten-frame and 6 more dots. How many dots in all?", "16", "10 and 6 make 16.", "A full frame is 10.")),
    ("num-place", question("vp1", "5 tens and 8 ones make what number?", "58", "50 and 8 make 58.", "Tens first, then ones.")),
    ("num-place", question("vp2", "In 82, what is the value of the 8?", "80", "The 8 is in the tens place.", "Which place is the 8 in?")),
    ("num-line", question("vl1", "Start at 0 and make 5 hops of 4. Where do you land?", "20", "4, 8, 12, 16, 20.", "Count the hops.")),
    ("num-line", question("vl2", "Which number is greater, 81 or 18?", "81", "81 has more tens, so it sits further right.", "Compare the tens first.", ["81", "18", "They are equal"])),
]
COURSE_ASSESSMENTS["add-subtract"] = [
    ("add-facts", question("vf1", "What is 7 + 5?", "12", "7 + 3 = 10, then 2 more makes 12.", "Make ten first.")),
    ("add-facts", question("vf2", "What is 9 + 6?", "15", "9 + 1 = 10, then 5 more makes 15.", "Make ten first.")),
    ("add-regroup", question("vr1", "What is 48 + 35?", "83", "8 + 5 = 13, carry 1. Then 4 + 3 + 1 = 8 tens.", "Add the ones first.")),
    ("add-regroup", question("vr2", "What is 69 + 24?", "93", "9 + 4 = 13, carry 1. Then 6 + 2 + 1 = 9 tens.", "Add the ones first.")),
    ("sub-gap", question("vs1", "What is 17 - 8?", "9", "17 take away 8 leaves 9.", "Think 8 + ? = 17.")),
    ("sub-gap", question("vs2", "What is 73 - 46?", "27", "Trade 1 ten: 6 tens and 13 ones minus 4 tens and 6 ones is 2 tens and 7 ones.", "You may need to trade a ten.")),
]
COURSE_ASSESSMENTS["multiply-divide"] = [
    ("mul-groups", question("vg1", "There are 6 baskets with 4 apples in each. How many apples in all?", "24", "6 x 4 = 24.", "Add 4 six times.")),
    ("mul-groups", question("vg2", "An array has 5 rows with 5 dots in each row. How many dots?", "25", "5 x 5 = 25.", "Add 5 five times.")),
    ("mul-tables", question("vt1", "What is 9 x 7?", "63", "The digits 6 and 3 add to 9.", "Count by 9s seven times.")),
    ("mul-tables", question("vt2", "What is 5 x 9?", "45", "Times 5 ends in 0 or 5.", "Count by 5s nine times.")),
    ("div-share", question("vd1", "What is 18 / 6?", "3", "3 x 6 = 18.", "How many 6s make 18?")),
    ("div-share", question("vd2", "23 marbles are shared equally among 4 friends. How many marbles are left over?", "3", "Each friend gets 5, using 20 marbles, so 3 are left over.", "Find the biggest share that fits.")),
]
