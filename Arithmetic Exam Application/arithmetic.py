import random


class Application:

    def __init__(self):
        self.difficulty_lever = 0
        self.correct_answers = 0
        self.simple = "simple operations with numbers 2-9"
        self.hard = "integral squares of 11-29"

    def run(self):
        self.__choice_difficulty_level()
        for _ in range(0, 5):
            expression = self.__task_generate()
            print(expression)
            while True:
                try:
                    answer = int(input())
                except ValueError:
                    print("Incorrect format.")
                else:
                    if (self.difficulty_lever == 1 and eval(expression) == answer) or\
                            (self.difficulty_lever == 2 and pow(int(expression), 2) == answer):
                        print("Right!")
                        self.correct_answers += 1
                    else:
                        print("Wrong!")
                    break

        print(f"Your mark is {self.correct_answers}/5. Would you like to save the result? Enter yes or no.")
        answer = input().lower()
        if answer[0] == "y" and (len(answer) == 3 or len(answer) == 1):
            self.__save()

    def __choice_difficulty_level(self):
        while True:
            print("""Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29""")
            try:
                self.difficulty_lever = int(input())
                if self.difficulty_lever in range(1, 3):
                    break
                else:
                    print("Incorrect format.")
            except ValueError:
                print("Incorrect format.")

    def __task_generate(self):
        if self.difficulty_lever == 1:
            return str(random.randint(2, 9)) + " " + \
                   random.choice(["+", "-", "*"]) + " " + \
                   str(random.randint(2, 9))
        else:
            return str(random.randint(11, 29))

    def __save(self):
        with open("results.txt", 'a') as file:
            print("What is your name?")
            file.write(f"{input()}: {self.correct_answers}/5 in level {self.difficulty_lever} "
                       f"({self.simple if self.difficulty_lever == 1 else self.hard}).")
            print('The results are saved in "results.txt".')


if __name__ == "__main__":
    Application().run()
