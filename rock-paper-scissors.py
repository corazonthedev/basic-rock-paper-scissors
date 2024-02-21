import tkinter as tk
from tkinter import messagebox
import random

rps_list = ["rock", "paper", "scissors"]

def rps():
    # Scores
    player_win = 0
    ai_win = 0
    
    def check_winner(player_choice, ai_choice):
        nonlocal player_win, ai_win
        if (player_choice == "rock" and ai_choice == "scissors") or \
           (player_choice == "paper" and ai_choice == "rock") or \
           (player_choice == "scissors" and ai_choice == "paper"):
            player_win += 1
            return "Player wins!"
        elif (ai_choice == "rock" and player_choice == "scissors") or \
             (ai_choice == "paper" and player_choice == "rock") or \
             (ai_choice == "scissors" and player_choice == "paper"):
            ai_win += 1
            return "AI wins!"
        else:
            return "Equal!"

    def play_round(player_choice):
        ai_choice = random.choice(rps_list) #random AI
        result = check_winner(player_choice, ai_choice) #check
        result_label.config(text=result)
        ai_choice_label.config(text=f"AI's choice: {ai_choice}")
        player_choice_label.config(text=f"Player's choice: {player_choice}")
        scores_label.config(text=f"Ai: {ai_win} | Player: {player_win}")
        if ai_win >= 2:
            messagebox.showinfo("Result", "AI won!")
            root.destroy()
        elif player_win >= 2:
            messagebox.showinfo("Result", "Player won!")
            root.destroy()

    root = tk.Tk()
    root.title("Rock Paper Scissors")

    # Function for player's choice
    def set_choice(choice):
        play_round(choice)

    # Player options buttons
    rock_btn = tk.Button(root, text="Rock", command=lambda: set_choice("rock"))
    rock_btn.grid(row=0, column=0)
    paper_btn = tk.Button(root, text="Paper", command=lambda: set_choice("paper"))
    paper_btn.grid(row=0, column=1)
    scissors_btn = tk.Button(root, text="Scissors", command=lambda: set_choice("scissors"))
    scissors_btn.grid(row=0, column=2)

    # Labels for result, AI choice, player choice, and scores
    result_label = tk.Label(root, text="")
    result_label.grid(row=1, column=1)
    ai_choice_label = tk.Label(root, text="")
    ai_choice_label.grid(row=2, column=1)
    player_choice_label = tk.Label(root, text="")
    player_choice_label.grid(row=3, column=1)
    scores_label = tk.Label(root, text="")
    scores_label.grid(row=4, column=1)

    root.mainloop()

def main():
    rps()

main()
