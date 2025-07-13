from tkinter import *
import pandas as pd
import random
from tkinter import messagebox
import os

# ----------------- CONSTANTS ----------------- #
BACKGROUND_COLOR = "#B1DDC6"
DATA_FILE = "data/french_words.csv"
PROGRESS_FILE = "data/words_to_learn.csv"

# ----------------- DATA LOADING ----------------- #
try:
    data = pd.read_csv(PROGRESS_FILE)
except FileNotFoundError:
    data = pd.read_csv(DATA_FILE)

to_learn = data.to_dict(orient="records")

# ----------------- FUNCTIONS ----------------- #

def next_card(source: str):
    global current_card, after_id

    if not to_learn:
        messagebox.showinfo(title="Congratulations!", message="You have successfully learnt all the words!")
        window.quit()
        os.remove(PROGRESS_FILE)
        return

    window.after_cancel(after_id)
    current_card = random.choice(to_learn)

    canvas.itemconfig(card_img, image=front_card_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")

    if source == "buttonR":
        to_learn.remove(current_card)
        pd.DataFrame(to_learn).to_csv(PROGRESS_FILE, index=False)

    progress_label.config(text=f"Words Remaining: {len(to_learn)}")
    after_id = window.after(3000, show_meaning)

def show_meaning():
    canvas.itemconfig(card_img, image=back_card_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def reset_progress():
    if messagebox.askyesno(title="Reset Progress", message="Are you sure you want to reset your progress?"):
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
        window.quit()

# ----------------- UI SETUP ----------------- #

#Window
window = Tk()
window.title("This Ain’t Duolingo")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

after_id = window.after(3000, show_meaning)


#Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=front_card_img)
card_title = canvas.create_text(400, 140, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


#Labels
progress_label = Label(text="", font=("Arial", 16), bg=BACKGROUND_COLOR)
progress_label.grid(row=1, column=0, columnspan=2)


#Buttons
wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=lambda: next_card("buttonW"))
wrong_button.grid(row=2, column=0)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, highlightthickness=0, command=lambda: next_card("buttonR"))
right_button.grid(row=2, column=1)

reset_button = Button(text="Reset", command=reset_progress, bg="white", fg="red")
reset_button.grid(row=3, column=0, columnspan=2, pady=10)

next_card("buttonW")
window.mainloop()
