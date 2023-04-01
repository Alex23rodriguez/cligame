from threading import Timer
from time import time
from collections.abc import Callable

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("gamemode", nargs="?", choices=["t", "n", "s", "m", "c"])
parser.add_argument("param", nargs="?", type=int)
parser.add_argument(
    "--quiet",
    "-q",
    action="store_true",
    help="disable feedback (whether an answer is correct or not)",
)
parser.add_argument(
    "--noexplain",
    "-e",
    action="store_true",
    help="a wrong answer won't be explained",
)

parser.add_argument(
    "--repeat",
    "-r",
    action="store_true",
    help="a wrong answer will be repeated until gotten right (overrides -e)",
)

args = parser.parse_args()

if args.gamemode and not args.param:
    parser.error("if gamemode is given, param must be given too")


def setTimeout(fn, secs, *args, **kwargs):
    t = Timer(secs, fn, args=args, kwargs=kwargs)
    t.start()


def countdown_done(game: "Game"):
    game.timeup = True
    game.endtime = time()
    print("\n\r-------TIME'S UP!!-------")  # , end="")


gamemodestr = """t: timed mode. game ends when timer runs out
n: number of questions mode. game ends after a certain number of questions,\
 regardless of right or wrong answer
s: score mode. game ends when a certain score is reached
m: mistake mode. game ends when a certain number of errors are made
c: consecutive mode. game ends after correctly answering n questions in a row
mode: """, [
    "t",
    "n",
    "s",
    "m",
    "c",
]


def getmainmode():
    # main game mode
    print("enter mode:")
    prompt, ans = gamemodestr
    mode = input(prompt)
    while mode not in ans:
        print("\noption not found")
        mode = input("mode: ")
    print()

    # parameter for main game mode
    if mode == "t":
        param = getparam("Enter max time in minutes", int)
    elif mode == "n":
        param = getparam("Enter max questions", int)
    elif mode == "s":
        param = getparam("Enter max score", int)
    elif mode == "m":
        param = getparam("Enter max mistakes", int)
    elif mode == "c":
        param = getparam("Enter num of consecutive answers", int)
    else:
        raise Exception("submode not found")
    return mode, param


def getparam(prompt: str, validfunc):
    ans = None
    while ans is None:
        ans = input(prompt + ": ")
        try:
            ans = validfunc(ans)
        except Exception:
            print("invalid parameter")
            ans = None
    return ans


class Game:
    def __init__(
        self,
        question: Callable[[bool], tuple[bool, str]],
    ):
        self.question = question
        self.quiet = args.quiet
        self.repeat = args.repeat
        self.explain = not args.noexplain and not self.repeat
        self._reset()

    def _reset(self):
        self.score = 0
        self.mistakes = 0
        self.streak = 0
        self.starttime = time()

        self.endtime: float | None = None
        self.timeup = False

        self.raw_answers: list[tuple[float, bool]] = []

    def start(self):
        self._reset()

        if args.gamemode:
            self.gamemode, self.param = args.gamemode, args.param
        else:
            self.gamemode, self.param = getmainmode()

        if self.gamemode == "t":
            setTimeout(countdown_done, self.param * 60, self)
        self._play()

    def _play(self):
        correct = False
        while not self._done():
            correct, explanation = self.question(self.repeat and not correct)
            should_explain = self.explain and explanation is not None

            if not self.timeup:
                self.raw_answers.append((time(), correct))
                if correct:
                    if not self.quiet:
                        print("\tcorrect!")
                    self.score += 1
                    self.streak += 1
                else:
                    if not self.quiet:
                        print(f"\twrong... {explanation if should_explain else ''}")
                    self.mistakes += 1
                    self.streak = 0

        print("===stats===")
        if self.endtime:
            t = int(self.endtime - self.starttime)
        else:
            t = int(time() - self.starttime)

        count = self.score + self.mistakes
        avg = t // count

        print(f"time:\t{t//60} mins {t%60} seconds")
        print(f"avg:\t{avg // 60} mins {avg%60} seconds")
        print(f"score:\t{self.score}/{count}")
        print(f"percent:\t{self.score/count*100:.2f}%")

    def _done(self):
        return (
            (self.gamemode == "t" and self.timeup)
            or (self.gamemode == "s" and self.param == self.score)
            or (self.gamemode == "m" and self.param == self.mistakes)
            or (self.gamemode == "n" and self.param == self.score + self.mistakes)
            or (self.gamemode == "c" and self.param == self.streak)
        )

    def save_raw(self, file="./stats.json"):
        import json
        from pathlib import Path

        config = {
            "starttime": self.starttime,
            "gamemode": self.gamemode,
            "param": self.param,
            "answers": self.raw_answers,
        }

        if Path(file).exists():
            with open(file, "r") as f:
                jsn = json.load(f)
                jsn.append(config)
        else:
            jsn = [config]

        with open(file, "w") as f:
            json.dump(jsn, f)
