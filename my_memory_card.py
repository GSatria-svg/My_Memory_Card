# Memory Card Application

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox,
    QRadioButton,
    QButtonGroup
)

from random import shuffle, randint


# =========================
# Question class
# =========================

class Question:
    """Contains the question, one correct answer, and three incorrect answers."""

    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3


# =========================
# Questions list
# =========================

questions_list = [
    Question(
        'Who is the current navigator of the Astral Express in Honkai: Star Rail?',
        'Himeko',
        'Isee',
        'Falcon Amundsen',
        'Sam-3000'
    ),

    Question(
        'Which Path does Dan Heng follow in his basic form?',
        'Hunt',
        'Destruction',
        'Preservation',
        'Permanence'
    ),

    Question(
        'Who is the leader of the Stellaron Hunters?',
        'Elio',
        'Kafka',
        'Blade',
        'SAM'
    )
]


# =========================
# Application setup
# =========================

app = QApplication([])

window = QWidget()
window.setWindowTitle('Memory Card')
window.resize(500, 400)


# =========================
# Widgets
# =========================

btn_OK = QPushButton('Answer')

lb_Question = QLabel('Question')


# =========================
# Answer panel
# =========================

RadioGroupBox = QGroupBox('Answer options')

rbtn_1 = QRadioButton('Option 1')
rbtn_2 = QRadioButton('Option 2')
rbtn_3 = QRadioButton('Option 3')
rbtn_4 = QRadioButton('Option 4')

answers = [
    rbtn_1,
    rbtn_2,
    rbtn_3,
    rbtn_4
]

RadioGroup = QButtonGroup()

for button in answers:
    RadioGroup.addButton(button)


layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()

layout_ans2.addWidget(rbtn_1)
layout_ans2.addWidget(rbtn_2)

layout_ans3.addWidget(rbtn_3)
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)

RadioGroupBox.setLayout(layout_ans1)


# =========================
# Result panel
# =========================

AnsGroupBox = QGroupBox('Test result')

lb_Result = QLabel('Are you correct or not?')
lb_Correct = QLabel('The answer will be here!')

layout_res = QVBoxLayout()

layout_res.addWidget(
    lb_Result,
    alignment=Qt.AlignLeft | Qt.AlignTop
)

layout_res.addWidget(
    lb_Correct,
    alignment=Qt.AlignHCenter
)

AnsGroupBox.setLayout(layout_res)

AnsGroupBox.hide()


# =========================
# Main layout
# =========================

layout_line1 = QHBoxLayout()
layout_line2 = QHBoxLayout()
layout_line3 = QHBoxLayout()

layout_line1.addWidget(
    lb_Question,
    alignment=Qt.AlignHCenter | Qt.AlignVCenter
)

layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2)
layout_line3.addStretch(1)


layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)

layout_card.setSpacing(5)

window.setLayout(layout_card)


# =========================
# Game variables
# =========================

window.score = 0
window.total = 0
window.cur_question = 0


# =========================
# Functions
# =========================

def show_result():
    """Show the result panel."""

    RadioGroupBox.hide()
    AnsGroupBox.show()

    btn_OK.setText('Next question')


def show_question():
    """Show the question panel."""

    RadioGroupBox.show()
    AnsGroupBox.hide()

    btn_OK.setText('Answer')

    # Clear all radio buttons
    RadioGroup.setExclusive(False)

    for button in answers:
        button.setChecked(False)

    RadioGroup.setExclusive(True)


def ask(q):
    """Display a question and shuffle its answers."""

    answer_options = [
        q.right_answer,
        q.wrong1,
        q.wrong2,
        q.wrong3
    ]

    shuffle(answer_options)

    # Put shuffled answers into the radio buttons
    for i in range(4):
        answers[i].setText(answer_options[i])

    lb_Question.setText(q.question)
    lb_Correct.setText(q.right_answer)

    show_question()


def show_correct(result):
    """Display whether the selected answer was correct."""

    lb_Result.setText(result)
    show_result()


def check_answer():
    """Check the selected answer."""

    selected_answer = None

    # Find which radio button is selected
    for button in answers:
        if button.isChecked():
            selected_answer = button.text()
            break

    # Don't continue if nothing was selected
    if selected_answer is None:
        lb_Result.setText('Please select an answer!')
        return

    # Check answer
    if selected_answer == lb_Correct.text():
        show_correct('Right!')
        window.score += 1
    else:
        show_correct('Wrong answer!')

    window.total += 1

    # Print statistics
    print('Statistic')
    print('- Total questions:', window.total)
    print('- Right answers:', window.score)

    rating = window.score / window.total * 100

    print('- Rating:', round(rating, 2), '%')
    print()


def next_question():
    """Show the next random question."""

    window.cur_question = randint(
        0,
        len(questions_list) - 1
    )

    q = questions_list[window.cur_question]

    ask(q)


def click_OK():
    """Handle the Answer / Next question button."""

    if btn_OK.text() == 'Answer':
        check_answer()
    else:
        next_question()


# =========================
# Button connection
# =========================

btn_OK.clicked.connect(click_OK)


# =========================
# Start application
# =========================

next_question()

window.show()

app.exec()
