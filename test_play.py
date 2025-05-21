from play import Question, AnswerChoice, Quiz, UserAnswer, GamePlay, GAME_DATA_FILE_PATH

def test_question_knows_when_it_is_correct():
    question = Question(
        question="example",
        answer_choices=[
            AnswerChoice(aid="A", choice="choice 1"),
            AnswerChoice(aid="B", choice="choice 2", correct=True),
            AnswerChoice(aid="C", choice="choice 3"),
            AnswerChoice(aid="D", choice="choice 4"),
        ],
    )

    assert not question.is_correct("A")
    assert question.is_correct("B")
    assert not question.is_correct("C")
    assert not question.is_correct("D")

def test_question_can_pretty_print_itself():
    question = Question(
        question="This is an example question",
        answer_choices=[
            AnswerChoice(aid="A", choice="choice 1"),
            AnswerChoice(aid="B", choice="choice 2", correct=True),
        ],
    )
    
    pretty_question = str(question)
    assert "This is an example question" in pretty_question
    assert "choice 1" in pretty_question
    assert "choice 2" in pretty_question


def test_quiz_keeps_track_of_the_current_score():
    questions = [
        Question(question="example", answer_choices=[]),
        Question(question="example", answer_choices=[]),
    ]
    quiz = Quiz(
        qid="1",
        topic="example",
        questions=questions,
    )

    quiz.user_answers = []
    assert quiz.current_score == 0

    quiz.user_answers = [
        UserAnswer(question=questions[0], answered_correctly=False), 
        UserAnswer(question=questions[1], answered_correctly=False)
    ]
    assert quiz.current_score == 0

    quiz.user_answers = [
        UserAnswer(question=questions[0], answered_correctly=True), 
        UserAnswer(question=questions[1], answered_correctly=False)
    ]
    assert quiz.current_score == 1

    quiz.user_answers = [
        UserAnswer(question=questions[0], answered_correctly=True), 
        UserAnswer(question=questions[1], answered_correctly=True)
    ]
    assert quiz.current_score == 2

def test_quiz_knows_what_question_it_is_on():
    questions = [
        Question(question="example", answer_choices=[]),
        Question(question="example", answer_choices=[]),
    ]
    quiz = Quiz(
        qid="1",
        topic="example",
        questions=questions,
    )

    assert quiz.question == questions[0]

    quiz.answer_question("")
    assert quiz.question == questions[1]

def test_quiz_keeps_track_of_answers():
    quiz = Quiz(
        qid="1",
        topic="example",
        questions=[
            Question(question="example", answer_choices=[]),
            Question(question="example", answer_choices=[]),
        ],
    )

    assert not quiz.answer

    quiz.user_answers = [UserAnswer(question=quiz.questions[0], answered_correctly=True)]
    assert "Correct" in quiz.answer

    quiz.user_answers = [
        UserAnswer(question=quiz.questions[0], answered_correctly=False),
        UserAnswer(question=quiz.questions[0], answered_correctly=True),
    ]
    assert "Correct" in quiz.answer

    quiz.user_answers = [UserAnswer(question=quiz.questions[0], answered_correctly=False)]
    assert "Incorrect" in quiz.answer

    quiz.user_answers = [
        UserAnswer(question=quiz.questions[0], answered_correctly=True),
        UserAnswer(question=quiz.questions[0], answered_correctly=False),
    ]
    assert "Incorrect" in quiz.answer

def test_quiz_can_answer_its_own_questions():
    quiz = Quiz(
        qid="1",
        topic="example",
        questions=[
            Question(
                question="example",
                answer_choices=[
                    AnswerChoice(aid="A", choice="choice 1"),
                    AnswerChoice(aid="B", choice="choice 2", correct=True),
                    AnswerChoice(aid="C", choice="choice 3"),
                    AnswerChoice(aid="D", choice="choice 4"),
                ],
            ),
            Question(
                question="example",
                answer_choices=[
                    AnswerChoice(aid="A", choice="choice 1", correct=True),
                    AnswerChoice(aid="B", choice="choice 2"),
                    AnswerChoice(aid="C", choice="choice 3"),
                    AnswerChoice(aid="D", choice="choice 4"),
                ],
            )
        ],
    )

    assert quiz.current_score == 0
    quiz = quiz.answer_question("B")
    assert quiz.current_score == 1
    quiz = quiz.answer_question("A")
    assert quiz.current_score == 2

def test_game_play_can_select_a_game():
    game_play = GamePlay(
        games=[
            Quiz(qid="1", topic="example1", questions=[]),
            Quiz(qid="2", topic="example2", questions=[]),
            Quiz(qid="3", topic="example3", questions=[]),
        ]
    )

    assert game_play.select_game("1") == game_play.games[0]
    assert game_play.select_game("2") == game_play.games[1]
    assert game_play.select_game("3") == game_play.games[2]

def test_game_play_can_pretty_print_itself():
    game_play = GamePlay(
        games=[
            Quiz(qid="1", topic="example1", questions=[]),
            Quiz(qid="2", topic="example2", questions=[]),
            Quiz(qid="3", topic="example3", questions=[]),
        ]
    )

    pretty_game_play = str(game_play)
    assert "example1" in pretty_game_play
    assert "example2" in pretty_game_play
    assert "example3" in pretty_game_play

def test_game_can_load_itself_from_a_file():
    game_play = GamePlay.from_file(GAME_DATA_FILE_PATH)
    assert len(game_play.games) > 0

