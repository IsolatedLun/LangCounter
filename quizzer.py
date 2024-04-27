import os
import random

from lang_counter import LangCounter

class Quizzer:
    def __init__(self, max_questions = 12, max_num = 1_000_000) -> None:
        self.max_questions = max_questions
        self.max_num = max_num
        self.mistakes = 0

        self.language_list = [x.split('.')[0] for x in os.listdir("./languages")]
        self.selected_languages = []
        self.counters = {}

        print("-" * 48)
        print(">> Type 'exit' to leave")
        print("-" * 48)
        for i, lang in enumerate(self.language_list):
            print(f"{i + 1}) {lang.capitalize()}")
        print("-" * 48)
        
        inp = input("> Select languages [1,..]: ")
        if inp == "all":
            self.selected_languages = self.language_list
            for x in self.language_list:
                self.counters[x] = LangCounter(x)
        elif "exit" in inp:
            print(">> Exitting...")
            exit();
        else:
            for x in inp.split(","):
                idx = int(x.strip())
                selected_language = self.language_list[idx - 1]
                self.selected_languages.append(selected_language)

                self.counters[selected_language] = LangCounter(selected_language)

        i = 0
        while i < max_questions:
            rand_num = random.randint(1, self.max_num)
            rand_language = random.choice(self.selected_languages)
            self.question(i, rand_language, rand_num)

            i += 1

        print(f"Result: {i - self.mistakes}/{i} correct.")

    def question(self, i: int, language: str, n: str):
        counter: LangCounter = self.counters[language]
        print(f"> Question ({i + 1})[{language}]: {counter.wordify(n)}")
        
        try:
            user_guess = input("Guess: ")
            if counter.wordify(user_guess) == counter.wordify(n):
                print(">> Correct!")
            else:
                print(f">> Incorrect, the answer was: {n}")
                self.mistakes += 1
        except:
            print(f">> Incorrect, the answer was: {n}")
            self.mistakes += 1

quizzer = Quizzer()