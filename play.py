# /// script
# dependencies = [
#   "pydantic",
#   "rich"
# ]
# ///

from pydantic import BaseModel
import json
from typing import Optional
from rich import print
import os

GAME_DATA_FILE_PATH = "./game-data.json"
SEPARATOR = "\n------------------------------------------------\n"

class AnswerChoice(BaseModel):
    aid: str
    choice: str
    correct: Optional[bool] = False

class Question(BaseModel):
    question: str
    answer_choices: list[AnswerChoice]

    def __str__(self) -> str:
        formatted_answer_choices = "\n".join([f"{choice.aid}. {choice.choice}" for choice in self.answer_choices])
        return f"\n{SEPARATOR}\n{self.question}\n\n{formatted_answer_choices}"

    def is_correct(self, user_input: str) -> bool:
        for answer_choice in self.answer_choices:
            if answer_choice.aid.lower() == user_input.lower() and answer_choice.correct:
                return True

        return False

    @property
    def input_prompt(self) -> str:
        possible_choices = ", ".join([answer_choice.aid for answer_choice in self.answer_choices])
        return f"\nEnter your answer ({possible_choices}): "

class UserAnswer(BaseModel):
    question: Question
    answered_correctly: bool

class Quiz(BaseModel):
    qid: str
    topic: str
    questions: list[Question]

    user_answers: list[UserAnswer] = []
    current_question_idx: int = 0

    @property
    def current_score(self) -> int:
        return sum([1 if answer.answered_correctly else 0 for answer in self.user_answers])

    @property
    def score(self) -> str:
        return f"\n{SEPARATOR}\nYour final score: {self.current_score} out of {len(self.questions)}"

    @property
    def question(self) -> Optional[Question]:
        if self.current_question_idx >= len(self.questions):
            return None

        return self.questions[self.current_question_idx]

    @property
    def previous_answer(self) -> Optional[Question]:
        if len(self.user_answers) == 0:
            return None

        return self.user_answers[-1]

    @property
    def input_prompt(self) -> str:
        return self.question.input_prompt

    @property
    def answer(self) -> Optional[str]:
        if not self.previous_answer:
            return None

        if self.previous_answer.answered_correctly:
            return "\n✅ Correct!"
        else:
            return "\n❌ Incorrect!"

    def answer_question(self, user_input: str) -> "Quiz":
        if not self.question:
            return None

        is_correct = self.question.is_correct(user_input)
        return self.model_copy(update={
            "current_question_idx": self.current_question_idx + 1,
            "user_answers": [*self.user_answers, UserAnswer(question=self.question, answered_correctly=is_correct)],
        })

class GamePlay:
    def __init__(self, games: list[Quiz]):
        self.games = games

    def select_game(self, selected_game_input: str) -> Optional[Quiz]:
        found_games = [game for game in self.games if game.qid == selected_game_input]
        if not found_games or len(found_games) == 0:
            return None

        return found_games[0]

    @property
    def select_game_input(self) -> str:
        return "\nEnter the number corresponding to the quiz you want to play: "

    def __str__(self) -> str:
        options = "\n".join([f"{game.qid}. {game.topic}" for game in self.games])
        return f"\nChoose a quiz topic:\n{options}"

    @classmethod
    def from_file(self, file_path: str) -> "Game":
        quizzes = []
        with open(file_path, "rb") as file:
            quiz_data = json.loads(file.read())
            for i, quiz_obj in enumerate(quiz_data):
                quizzes.append(Quiz(qid=str(i), **quiz_obj))
        
        return GamePlay(games=quizzes)


def play():
    print("===============================================================")
    print("                      Welcome to RecQuiz!                      ")
    print("===============================================================")
    print("Test your knowledge. Take one of our quizzes or build your own.\n")

    should_continue_user_input = input("Would you like to play? [Y/n]: ")
    should_continue = should_continue_user_input == "" or should_continue_user_input.lower() == "y"
    if not should_continue:
        exit()

    game_play = GamePlay.from_file(os.getenv("RECQUIZ_GAME_DATA_FILE_PATH") or GAME_DATA_FILE_PATH)
    print(game_play)
    selected_game_input = input(game_play.select_game_input)
    quiz = game_play.select_game(selected_game_input)
    if not quiz:
        exit()

    while quiz.question:
        print(str(quiz.question))
        answer_selection = input(quiz.input_prompt)
        quiz = quiz.answer_question(answer_selection)
        print(quiz.answer)

    print(quiz.score)

if __name__ == "__main__":
    play()

