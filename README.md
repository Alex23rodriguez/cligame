# cligame

Lightweight python library to easily create CLI interactive games to learn or practice new concepts,
without having to worry about the game related aspects such as score or timers.

## Why?

When attempting to learn something quickly, it is often useful to quiz oneself repeatedly.
This library makes life easier by abstracting away the elements surrounding the game itself,
such as score, mistakes, streaks, time, etc.

With this library, it is easy and frictionless to quickly create a CLI game and start training as soon as possible,
knowing that the user experinence will be consitent and adequate from the get-go.

### Modes

The currently supported game modes are as follows:

- Timed mode. Game ends when timer runs out.
- Number of questions mode. Game ends after certain number of questions, regardless of right or wrong answer.
- Score mode. Game ends when a certain score is reached.
- Mistake mode. Game ends after a certain number of errors are made.
- Consecutive mode. Game ends after correctly answering a determined number of questions in a row.

## Usage

- install the library:

`pip install cligame`

- create a script that asks questions based on your logic

```python
### myscript.py ###

from cligame import Game
from random import randint

# create a function with the following signature: (bool) => (bool, str)
# in this example we ignore the bool that is passed in
def ask_question(_):
    x, y = randint(1, 10), randint(1, 10)
    ans = input(f"What is {x} + {y}?  ")
    correct_ans = str(x + y)
    return ans == correct_ans, correct_ans

# initizlize a Game object with that function, and start the game
mygame = Game(ask_question)
mygame.start()
```

- run the script:
  `python myscript.py`

That's it! Upon running the program, you will be prompted to choose a game mode and will be quizzed accordingly.

## Explanation

The user must provide a function that:

- takes in a boolean `repeat`
  - this indicates if the same question as last time should be asked again
  - for now, this functionallity must be implemented by the user
- returns a boolean and a string
  - the boolean indicates whether the correct answer was given
  - the string represents either the correct answer or an explanation on how to get the correct answer.
    - this will be shown to the user upon a wrong answer unless `noexplain` is enabled.

Let's see a more complete example of the above function

```python
x, y = randint(1, 10), randint(1, 10)
def ask_question(repeat):
    global x, y
    if not repeat:
        x, y = randint(1, 10), randint(1, 10)

    ans = input(f"What is {x} + {y}?  ")
    correct_ans = str(x + y)
    return ans == correct_ans, f"the correct answer was '{correct_ans}', but '{ans}' was given"
```

## Command-line arguments

(run `python myscript.py --help` to see all options)

Once you've become familiar with the different game modes, you can quick-start a game by passing command-line arguments:

- `python myscript.py t 5` will start a 5 minute game.
- `python myscript.py c 10` will start a game that ends after correctly answering 10 questions in a row.

### Further configuration

You can customize different aspects of the game using the following flags:

- `-E` or `--noexplain` to disable explanations. Upon answering a question incorrectly, the correct answer won't be shown.
- `-q` or `--quiet` to disable feedback. After answering a question, there will be no indication whether the answer was correct or not (implies `noexplain`)
- `-r` or `--repeat` to enable repetition. Upon answering a question incorrectly, the same question will be asked until the correct answer is given. Currently, this must be handled by the function created by the user, as indicated by the `repeated` argument (implies `noexplian`)

## Stats logging

If you want to keep track of your performance to track your progress over time, call the `save_raw` function after the game is done:

```python
mygame = Game(ask_question)
mygame.start()
mygame.save_raw("my_stats.json")
```

- If no filename is provided, "stats.json" will be used by default
  - if using this package with multiple games, be careful to store the stats in different files!

In the future, this package will implement modules to analize the resulting output

# TODO

- move `repeat` to game logic
- configuration without command-line arguments
- add submodes
- add more stats logging options
- add stats analizer
- add spaced repetition
