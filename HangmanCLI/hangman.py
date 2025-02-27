import json
import os
import random
import time
import shutil


### LOAD DATA ###
def load_tasks():
    with open("hangmandata.json", "r") as file:
        return json.load(file)
        
def load_top_players():
    with open("hangman_leaderboard.json", "r") as file:
        return json.load(file)

### SAVE DATA ###
def save_data(items):
    with open("hangmandata.json", "w") as file:
        json.dump(items, file, indent=4)

### SOME GLOBAL VARIABLES ###
interface = ["Start","Leaderboards" ,"Quit"]
leaderboard = load_top_players()
leaderboard_interface = enumerate(leaderboard, start=1)
items = load_tasks()
score = 0
columns = shutil.get_terminal_size().columns


### OTHER FUNCTIONS ###
def difficulty():
    os.system('cls' if os.name == 'nt' else 'clear')
    data_set = json.load(open("categories_data.json", "r"))
    print('Difficulty'.center(columns))
    d = ['Elementary', 'Highschool', 'College']
    for pos, i in enumerate(d,start=1):
        print(f'{pos}. {i}\n')
    print("•Press Enter for General•\n")
    while True:
        chose = input("Select Dif: ")
        if chose== "":
            dif = "General"
            with open("hangmandata.json", "r") as file:
                data = json.load(file)
            break
        else:
            dif = d[int(chose)-1]
            data = data_set[dif]
            break
    return data, dif


def update_leaderboard(player_name, player_score):
    global leaderboard
    normalized_name = player_name.lower()
    for player in leaderboard:
        if player["name"].lower() == normalized_name:
            if player_score > player["score"]:
                player["score"] = player_score
            break
    else:
        leaderboard.append({"name": player_name, "score": player_score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    with open("hangman_leaderboard.json", "w") as file:
        json.dump(leaderboard, file, indent=4)


### MAIN GAME FUNCTION ###
def run(player, lvl, diff):
    global score
    clue, word = None, None    

    ### FOR FILTERING DATA ###
    valid_clues = {k: v for k, v in lvl.items() if k != "high_score"}
    if not valid_clues:
        print("No words available in the game data!")
        return

    clue = random.choice(list(valid_clues.keys()))
    word = valid_clues[clue].lower()
    user_guess = ['_' if char != ' ' else ' ' for char in word.lower()]
    life = 5
    high_score = items.get("high_score", 0)

    ### GAME LOOP ###
    while life > 0:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n", "Welcome to Hangman!".center(columns))
        print(f"Game Difficulty: {diff}")
        print(f'\nHere is Your Clue:\n\n{clue.center(columns)}\n')
        print(f"\nScore: {score}")
        print(f"\n❤: {life}")
        print(f"\nWord: {' '.join(user_guess)}")

        guess = input("\n\nYour Guess: ").strip().lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("\nInvalid input! Please enter a single letter.", end='\r')
            time.sleep(1)
            continue

        ### CORRECT GUESS ###
        if guess in word:
            print("Correct!".center(columns))
            time.sleep(1)
            for index, letter in enumerate(word):
                if letter == guess:
                    user_guess[index] = guess
        ### WRONG GUESS ###
        else:
            print("Wrong!😝".center(columns))
            time.sleep(1)
            life -= 1

        ### COMPLETED THE WORD ###
        if "_" not in user_guess:
            os.system("cls" if os.name == "nt" else "clear")
            print("\n", "You guessed the word!🥳".center(columns))
            print(f"The word is: {word}")
            score += 1
            time.sleep(1.5)
            break

    ### HIGH SCORE SAVER ###
    if score > high_score:
        print(f'New High Score! : {score}')
        items["high_score"] = score
        save_data(items)
    
    ### GAME OVER SCREEN ###
    if life == 0:
        os.system("cls" if os.name == "nt" else "clear")
        update_leaderboard(player, score)
        print("\n", "Game Over! You ran out of lives🙁".center(columns))
        print(f"High Score: {high_score}\nYour total score is: {score}")
        time.sleep(1.5)
        score = 0

    ### TRY AGAIN LOOP ###
    while True:
        try_again = input("\nWould you like to try again? Y/N: ").strip().lower()
        if try_again == "y":
            run(player, lvl, diff)
            break
        elif try_again == "n":
            update_leaderboard(player, score)
            print("Thanks for playing!")
            print(f"Your score is: {score}")
            time.sleep(2)
            score = 0
            break
        else:
            print("Enter a valid option (Y/N).")

### INTERFACE OR INTRO FUNCTION ###
def main():
    global leaderboard
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n", "Welcome to Hangman!".center(columns))
        for pos, i in enumerate(interface, start=1):
            print(f"{pos}. {i}\n")
        user_opt = input("Option: ").strip()

        if user_opt == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            player = input('Enter Your Name: ')
            data, dif = difficulty()
            lvl = data
            diff = dif
            run(player, lvl, diff)
            
        elif user_opt == "2":
            os.system('clear')
            print("\n", "Leaderboards".center(columns))
            leaderboard = sorted(leaderboard, key=lambda x: x["score"],reverse=True)
            for rank, player in enumerate(leaderboard, start=1):
                print(f"{rank}. {player['name']} - {player['score']} points\n")
            input("\nPress Enter to return to the menu.")
            
        elif user_opt == "3":
            print("Thanks for playing!")
            break
            
        else:
            print("Enter a Valid Option (1/2/3)...")
            time.sleep(2)

if __name__=="__main__":
    main()
    
