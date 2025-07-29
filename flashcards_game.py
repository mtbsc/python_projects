import tkinter as tk
from tkinter import messagebox, PhotoImage, Canvas, Entry
import random
from pandas import *
import json

"""
Flashcard Game - Inspired by "100 Days of Code - Day 31", by Angela Yu.
It uses word frequency lists compiled by hermitdave, which he compiled from opensubtitles.

This program is a vocabulary flashcard game built with Tkinter. It displays the top 500 most common words in a given language,
and the player needs to type the correct translation in english. Players score points for correct answers within a 60-second timer.
The more rare the word is, the more points the user gets, ranging from 1 to 500 points.
After the game ends, players can save their score and view a highscore list saved in a JSON file.

Screens:
- Menu: Start game or view highscores
- Game: Shows words and input field
- Score Entry: Save your name and score
- Highscores: Displays top scores

Developed for language practice and fun.
"""


# ui colors
BG_COLOR = "#B1DDC6"
TEXT_COLOR = "#005427"
# here you can add new languages
languages = {
    "German": "en-de.csv",
    "Portuguese": "en-pt.csv",
    "Norwegian": "en-no.csv",
}

# global values
total_time = 60
score = 0
words_guessed = 0
words_list = []
current_language = None
current_card = {}
timer_id = None
time_left = None
selected_button = None


# reads the csv
def language_choice(language, button):
    global words_list, current_language, selected_button
    df = read_csv(languages[language])
    words_list = DataFrame.to_dict(df, orient="records")
    current_language = language
    card_generator()

    # this is used to color the button you clicked
    if selected_button:
        selected_button.config(bg="SystemButtonFace")
    button.config(bg="#F2CAE0")
    selected_button = button


# generates new words from the selected language
def card_generator():
    global current_card
    if not words_list:
        return
    current_card = random.choice(words_list)
    key_language = current_language
    game_canvas.itemconfig(card_word, text=current_card[key_language])
    game_canvas.itemconfig(card_language, text=key_language)
    # this is used to show the user how rare their word is
    game_canvas.itemconfig(
        word_popularity,
        text=f"{key_language}'s {words_list.index(current_card)}th most popular word",
    )


# countdown function
def countdown(t):
    global time_left, timer_id
    time_left = t
    game_canvas.itemconfig(timer_text, text=f"Timer: {time_left}")
    if time_left > 0:
        timer_id = root.after(1000, countdown, time_left - 1)
    else:
        game_frame.pack_forget()
        record_frame.pack(fill="both", expand=True)
        score_text.config(
            text=f"Your Score: {score}\nYou guessed {words_guessed} words!\n\nPlease enter your name:"
        )
        new_highscore_text.config(text=f"NEW {current_language} HIGHSCORE!".upper())


# used to save the user highscore in highscore.json
def save_score():
    highscore_name = highscore_entry.get()
    highscore_score = score
    highscore_words = words_guessed
    highscore_language = current_language
    highscore_entry.delete(0, "end")

    new_data = {
        str(highscore_score): {
            "Name": highscore_name,
            "Words": highscore_words,
            "Language": highscore_language,
            "Score": highscore_score,
        }
    }

    try:
        with open("highscore.json", "r") as file:
            content = file.read().strip()
            if content:
                data = json.loads(content)
            else:
                data = {}
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)
    sorted_items = sorted(data.items(), key=lambda item: item[1]["Score"], reverse=True)
    sorted_data = {key: value for key, value in sorted_items}

    with open("highscore.json", "w") as f:
        json.dump(sorted_data, f, indent=2)

    highscores_screen()


# this starts up the game, reseting the score and time left, also removes the menu frame and opens the game frame
def start_game():
    global score, time_left, timer_id, words_guessed
    if not current_language:
        messagebox.showinfo("Choose Language", "Please choose a language first.")
        return
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    time_left = total_time
    words_guessed = 0
    score = 0
    game_canvas.itemconfig(score_tracker, text=f"Score: {score}")
    game_canvas.itemconfig(timer_text, text=f"Timer: {time_left}")
    menu_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    card_generator()
    countdown(time_left)


# sets up the highscore screen
def highscores_screen():
    try:
        with open("highscore.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    highscore_lines = []
    for i, (score_key, value) in enumerate(data.items()):
        name = value["Name"]
        words = value["Words"]
        language = value["Language"]
        score_val = value["Score"]
        line = f"{i+1}. {name} | {language} | {score_val} pts | {words} words guessed"
        highscore_lines.append(line)

    highscore_table.config(text="\n".join(highscore_lines[:10]))
    record_frame.pack_forget()
    menu_frame.pack_forget()
    highscore_frame.pack(fill="both", expand=True)


# goes back to main menu sfunction
def return_to_menu():
    global timer_id
    if messagebox.askokcancel(message="Are you sure you want to return to main menu?"):
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None
        game_frame.pack_forget()
        record_frame.pack_forget()
        highscore_frame.pack_forget()
        menu_frame.pack(fill="both", expand=True)


# exit the game function
def exit_game():
    if messagebox.askokcancel(
        title="Oh no!", message="Are you sure you want to exit the game?"
    ):
        root.destroy()


def game_reset():
    guess_entry.delete(0, "end")
    game_canvas.itemconfig(correct_text, state="hidden")
    game_canvas.itemconfig(wrong_text, state="hidden")
    game_canvas.itemconfig(card, image=card_front_img)
    card_generator()


def check_guess():
    global score, words_guessed
    if not current_card:
        return
    user_guess = guess_entry.get().lower()
    if not user_guess:
        return
    if user_guess == current_card["English"].lower():
        game_canvas.itemconfig(
            correct_text,
            text=f"Correct! +{words_list.index(current_card)} points!",
            state="normal",
        )
        game_canvas.itemconfig(card, image=card_back_img)
        game_canvas.itemconfig(card_language, text="English")
        game_canvas.itemconfig(card_word, text=current_card["English"])
        score += words_list.index(current_card)
        game_canvas.itemconfig(score_tracker, text=f"Score: {score}")
        words_guessed += 1
        root.after(1500, game_reset)
    else:
        game_canvas.itemconfig(wrong_text, state="normal")
        game_canvas.itemconfig(card, image=card_back_img)
        game_canvas.itemconfig(card_language, text="English")
        game_canvas.itemconfig(card_word, text=current_card["English"])
        root.after(1500, game_reset)


def main():
    global root, menu_frame, game_frame, record_frame, quit_button
    global game_canvas, card, card_language, card_word, correct_text, wrong_text, word_popularity
    global card_front_img, card_back_img
    global guess_entry, score_tracker, score, timer_text
    global new_highscore_text, score_text, highscore_entry, highscore_table, highscore_frame

    # root
    root = tk.Tk()
    root.title("Flashcards")
    root.attributes("-fullscreen", True)

    # main menu screen
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    menu_frame = tk.Frame(main_frame, bg=BG_COLOR)
    menu_frame.pack(fill="both", expand=True)

    tk.Label(
        menu_frame, text="Welcome to Flashcards!", font="Helvetica 48", bg=BG_COLOR
    ).pack(pady=140)
    tk.Label(
        menu_frame, text="Choose a Language:", font="Helvetica 20", bg=BG_COLOR
    ).pack(pady=40)
    lang_frame = tk.Frame(menu_frame, bg=BG_COLOR)
    lang_frame.pack()

    for lang in languages:
        btn = tk.Button(
            lang_frame,
            text=f"{lang}",
            width=10,
            height=2,
            font=("Helvetica", 20),
            fg=TEXT_COLOR,
        )
        btn.config(command=lambda l=lang, b=btn: language_choice(l, b))
        btn.pack(side="left", padx=10)

    tk.Button(
        menu_frame,
        text="Start Game",
        width=12,
        height=2,
        font=("Helvetica", 28),
        fg=TEXT_COLOR,
        command=start_game,
    ).pack(pady=40)

    tk.Button(
        menu_frame,
        text="View Highscores",
        width=12,
        height=2,
        font=("Helvetica", 20),
        fg=TEXT_COLOR,
        command=highscores_screen,
    ).pack(pady=10)

    # game frame
    game_frame = tk.Frame(main_frame, bg=BG_COLOR)

    card_front_img = PhotoImage(file="card_front.png")
    card_back_img = PhotoImage(file="card_back.png")

    game_canvas = Canvas(
        game_frame, width=1920, height=1080, bg=BG_COLOR, highlightthickness=0
    )
    game_canvas.place(relx=0.5, rely=0.5, anchor="center")

    card = game_canvas.create_image(960, 520, image=card_front_img)
    card_language = game_canvas.create_text(
        960, 340, font="Helvetica 25 italic", text="", fill="black"
    )
    card_word = game_canvas.create_text(
        960, 480, font="Helvetica 70 bold", text="", fill="black"
    )
    word_popularity = game_canvas.create_text(
        960, 630, font="Helvetica 20 italic", text="", fill="black"
    )

    correct_text = game_canvas.create_text(
        960,
        710,
        font="Helvetica 30 bold",
        text="Correct!",
        fill="green",
        state="hidden",
    )
    wrong_text = game_canvas.create_text(
        960, 710, font="Helvetica 30 bold", text="Wrong!", fill="red", state="hidden"
    )

    guess_entry = Entry(
        game_frame, width=30, font="helvetica 30 bold", justify="center"
    )
    guess_entry.place(relx=0.5, rely=0.78, anchor="center")
    guess_entry.bind("<Return>", lambda e: check_guess())

    score_tracker = game_canvas.create_text(
        960, 920, font="Helvetica 30 bold", text=f"Score: {score}", fill="green"
    )
    timer_text = game_canvas.create_text(
        960, 200, font="Helvetica 30 bold", text="", fill="black"
    )

    # return to menu button
    tk.Button(
        game_frame,
        text="Return to Menu",
        command=return_to_menu,
        font=("Helvetica", 16),
        fg=TEXT_COLOR,
    ).place(relx=0.95, rely=0.02, anchor="ne")


    #new score screen
    record_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tk.Label(record_frame, text="Time is over!", font="Helvetica 48", bg=BG_COLOR).pack(
        pady=140
    )
    new_highscore_text = tk.Label(
        record_frame, text="", font="Helvetica 35", bg=BG_COLOR, fg="red"
    )
    new_highscore_text.pack(pady=20)
    score_text = tk.Label(
        record_frame,
        text="Your Score: x\nYou guessed y words!\n\nPlease enter your name:",
        font="Helvetica 32",
        bg=BG_COLOR,
    )
    score_text.pack(pady=30)
    highscore_entry = Entry(
        record_frame, width=30, font="helvetica 30 bold", justify="center"
    )
    highscore_entry.bind("<Return>", lambda e: submit_button.invoke())
    highscore_entry.pack()
    submit_button = tk.Button(
        record_frame, bg=BG_COLOR, fg=BG_COLOR, command=save_score
    )
    submit_button.place(x=6000, y=6000)
    tk.Button(
        record_frame,
        text="Return to Menu",
        command=return_to_menu,
        font=("Helvetica", 16),
        fg=TEXT_COLOR,
    ).place(relx=0.95, rely=0.02, anchor="ne")
    record_frame.pack_forget()

    #highscore frame
    highscore_frame = tk.Frame(main_frame, bg=BG_COLOR)
    tk.Label(highscore_frame, text="HIGHSCORES", font="Helvetica 48", bg=BG_COLOR).pack(
        pady=60
    )
    highscore_table = tk.Label(
        highscore_frame, text="", font="Helvetica 24", justify="left", bg=BG_COLOR
    )
    highscore_table.pack()
    tk.Button(
        highscore_frame,
        text="Return to Menu",
        command=return_to_menu,
        font=("Helvetica", 16),
        fg=TEXT_COLOR,
    ).place(relx=0.95, rely=0.02, anchor="ne")
    highscore_frame.pack_forget()

    quit_button = tk.Button(
        root,
        text="Exit",
        command=exit_game,
        font=("Helvetica", 16),
        fg=TEXT_COLOR,
    )
    quit_button.place(relx=0.98, rely=0.02, anchor="ne")
    quit_button.lift()

    root.mainloop()

#phew
if __name__ == "__main__":
    main()
