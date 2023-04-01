import setuptools

short_description = " Python library to easily create CLI interactive games to learn \
or practice new concepts, without having to worry about the game related aspects \
such as score or timers"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cligame",
    version="0.2.1",
    author="Alex Rodriguez",
    author_email="alex.rodriguez.oro@gmail.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["python", "cli", "game", "interactive", "cligame", "terminal", "learn"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
