import random


class Party:
    def __init__(self, number_of_members, members, bill):
        self.number_of_members = number_of_members
        self.members = members
        self.bill = bill
        self.dictionary = dict()

    def get_members(self, make_lucky):
        if make_lucky:
            lucky = self.members[random.randint(0, self.number_of_members - 1)]
            print(f"\n{lucky} is the lucky one!\n")
            average = self.get_average_bill(int(1))
            for elem in self.members:
                if elem != lucky:
                    self.dictionary[elem] = average
                else:
                    self.dictionary[elem] = 0
        else:
            self.dictionary = {i: self.get_average_bill(int(0)) for i in self.members}
        return self.dictionary

    def get_average_bill(self, minus):
        average = self.bill / (self.number_of_members - minus)
        if int(str(average).split(".")[1]) != 0:
            return float("{:.2f}".format(average))
        else:
            return int(average)


if __name__ == "__main__":
    print("Enter the number of friends joining (including you):")
    number_of_members = int(input())
    print()
    if number_of_members > 0:
        print("Enter the name of every friend (including you), each on a new line:")
        members = [input() for i in range(number_of_members)]
        print()
        print("Enter the total bill value:")
        bill = int(input())
        print()

        party = Party(number_of_members, members, bill)

        print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
        if input().lower() == "yes":
            print(party.get_members(True))
        else:
            print("No one is going to be lucky")
            print(party.get_members(False))
    else:
        print("No one is joining for the party")
