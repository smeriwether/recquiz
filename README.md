# recquiz

A termainal-based Quiz game. Comes with a few built-in quizzes and the ability to generate
your own quiz with just a few words.


## Prerequisites

1. Python & `uv` installed
2. OpenAI API Key loaded in the `OPENAI_API_KEY` environment variable.

### Optionally

1. Set the `RECQUIZ_GAME_DATA_FILE_PATH` environment variable to point to a different file containing initial game state.

## How to run

`uv run play.py`


## How to run the tests

`uv run pytest test_play.py`
