from tkinter import *
from random_word import RandomWords
import random


# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND = "#B1DDC6"
WHITE = 'white'

# ---------------------------- VARIABLES ------------------------------- #

showed_words = []
user_words = []
display = ""
wpm_count = 0

# ---------------------------- UI SETUP ------------------------------- #
class TypingSpeed:

    def __init__(self):

        self.r = RandomWords()
        self.raw_data = self.r.get_random_words(hasDictionaryDef="true", includePartOfSpeech="noun,verb",
                                                minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1,
                                                maxDictionaryCount=10, minLength=5, maxLength=10, sortBy="alpha",
                                                sortOrder="asc", limit=15)
        try:
            self.words_data = [i.title() for i in self.raw_data]
        except TypeError:
            self.raw_data = self.r.get_random_words(hasDictionaryDef="true", includePartOfSpeech="noun,verb",
                                                    minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1,
                                                    maxDictionaryCount=10, minLength=5, maxLength=10, sortBy="alpha",
                                                    sortOrder="asc", limit=15)

        self.wpm_count = 0

        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.config(padx=50, pady=50, bg=BACKGROUND)
        self.window.after_id = None
        self.canvas = Canvas(self.window, width=400, height=263, bg=BACKGROUND, highlightthickness=0)

        self.word_card_img = PhotoImage(file="images/card.png")
        self.canvas.create_image(200,132, image=self.word_card_img)
        self.word_show = self.canvas.create_text(200, 132, text="Press space bar after each word\n You Don't need to care about upper case\n\n-press enter to start-", font=("Courier", 14, "bold"), fill="white", justify="center", width=250)

        self.canvas.grid(column=1, row=2, columnspan=5, pady=10)



        self.wpm_label = Label(text="WPM: ", font=("Arial", 12), bg=BACKGROUND)
        self.wpm_label.grid(row=1, column=2)
        self.wpm_value = Label(text="?", font=("Arial", 12), bg=WHITE)
        self.wpm_value.grid(row=1, column=3)

        self.timer_label = Label(text="time left: ", font=("Arial", 12), bg=BACKGROUND)
        self.timer_label.grid(row=1, column=4)
        self.timer_text = Label(text="90", font=("Arial", 12), bg=BACKGROUND)
        self.timer_text.grid(row=1, column=5)

        self.entry_box = Entry(self.window, bg=WHITE, bd=0, font=("Arial", 12), justify="center", width=30)
        self.entry_box.focus()
        self.entry_box.grid(row=3, column=1, columnspan=6)
        self.window.bind("<space>", self.user_input)
        self.window.bind("<Return>", self.start)

        self.restart_btn_img = PhotoImage(file="images/reload.png")
        self.restart_button = Button(image=self.restart_btn_img, bd=0, relief="flat",
                                highlightthickness=0, bg=BACKGROUND, command=self.start)
        self.restart_button.grid(row=4, column=3, columnspan=2, padx=10, pady=10, sticky="W")

        self.window.mainloop()

    # ---------------------------- FUNCTIONS ------------------------------- #

    def start(self, *event):
        self.showed_words = []
        self.user_words = []
        self.wpm_count = 0
        self.wpm_value.config(text=self.wpm_count)
        self.entry_box.config(state="normal")
        self.start_timer()
        self.random_words()

        self.window.unbind("<Return>")

    def start_timer(self):
        if self.window.after_id is not None:
            self.window.after_cancel(self.window.after_id)
        self.count_down(90)

    def count_down(self,count):
        if count > 0:
            self.window.after_id = self.window.after(1000, self.count_down, count - 1)
        else:
            self.window.after_id = None
        if count < 10:
            count = f"0{count}"
        if count == "00":
            self.compare()
            self.restart_button["state"] = "normal"
            self.window.bind("<Return>", self.start)
        self.timer_text.config(text=f"{count}")


    def random_words(self):
        global display
        display = ""
        for i in range(8):
            display_word = random.choice(self.words_data)
            showed_words.append(display_word)
            display += (display_word + ' ')
        self.canvas.itemconfig(self.word_show, text=display)

    def compare(self):
        # count WPM
        global wpm_count
        self.entry_box.config(state="disabled")
        for i in user_words:
            if i in showed_words:
                wpm_count += 1
        self.wpm_value.config(text=wpm_count)
        print(f"user_input: {user_words}")
        print(f"display_words: {showed_words}")

    def user_input(self, event):
        user_words.append(self.entry_box.get().title().strip())
        self.entry_box.delete(0, "end")
        if len(user_words) % 8 == 0:
            self.random_words()

app = TypingSpeed()