# FLASHCARDS_GAME
#### Description:

**Flashcards_Game** is a vocabulary flashcard game developed in Python using the Tkinter GUI library. The idea behind this project is to help users practice and improve their foreign language vocabulary by translating words under time pressure. The game is inspired by Angela Yu’s “100 Days of Code” (Day 31), but it was expanded with new features such as scoring, word frequency weighting, persistent highscores, and multiple screen navigation.

The game displays random words from the top 500 most common words in a given language, sourced from HermitDave’s word frequency datasets based on OpenSubtitles. The user has 60 seconds to translate as many words as possible into English. Correct translations award points, and the more rare the word is, the more points it gives — encouraging users to learn beyond just the most common words.

---

### How to Play

When the player clicks “Start,” the game begins with a 60-second timer. A foreign word appears in the center of the screen, and the player must type its English translation into the text entry box and press Enter. For every correct answer, the word changes, and points are added to the score based on the word’s position in the frequency list (1–500 points).

Once the timer reaches zero, the game ends, and the player is prompted to enter their name and save their score. Scores are saved in a local JSON file and can be viewed on the Highscores screen.

---

### Features

- **Menu Screen**: Allows the user to start a new game or view the highscores.
- **Game Screen**: Shows the current word, an entry box, a submit button, and a live-updating timer.
- **Score Entry Screen**: After the game ends, prompts the player to enter their name to save their score.
- **Highscores Screen**: Displays a list of the top saved scores sorted from highest to lowest.

---

### Project Structure

- `project.py`: The main Python script that runs the entire game. It contains all functions and Tkinter screen logic.
- `en-de.csv`: A CSV file example containing 500 German words paired with their English translations.
- `scores.json`: A local JSON file used to store highscore entries (name and score).
- `README.md`: This file, providing full documentation of the project.

---

### Design Decisions

To keep the project simple and accessible, the program uses a functional style rather than object-oriented programming. This made it easier to build and test quickly without creating multiple class structures. All screen transitions are managed using Tkinter `Frame` widgets and the `tkraise()` method.

For persistent data, JSON was chosen to store scores because it is lightweight, easy to use with Python, and human-readable. This also allows for easy future upgrades, like adding dates or expanding the data to support multiple languages.

The scoring system was intentionally designed to reward players for learning harder words. While the most frequent word gives 1 point, the rarest gives 500. This motivates users to go beyond just the basics and improve their overall vocabulary.

---

### Goals and Future Ideas

This project was created as a final project for **CS50P (Introduction to Programming with Python)**. It combines language learning with game design and GUI programming. In the future, it could be expanded to support:

- Multiple languages (selectable from a dropdown)
- Different difficulty modes (longer timers, more rare words)
- Saving highscore history per language
- Sound effects and visual feedback

---

This game was built both for fun and education, and it helped strengthen my skills in Python, file handling, GUI development, and user input management.
