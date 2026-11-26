"""Original Learnova curriculum and explicit prerequisite relationships."""

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
