import sys
from card_utils import parse_card
from probability_calculator import get_probability
from treys import Evaluator

def main():
    evaluator = Evaluator()
    
    while True:
        try:
            num_players = int(input("How many players are playing? "))
            if num_players < 2:
                raise ValueError("There must be at least 2 players.")
            break
        except ValueError as e:
            print(e)
    
    while True:
        pre_flop = input("Enter your pre-flop cards (e.g., As Kh): ").split()
        if any(card.lower() == 'r' for card in pre_flop):
            sys.exit()
        
        try:
            hand = [parse_card(card) for card in pre_flop]
        except KeyError as e:
            print(f"Invalid card input: {e}. Please try again.")
            continue
        
        probability = get_probability(evaluator, hand, [], num_players)
        print(f"Pre-flop probability of winning: {probability * 100:.2f}%")
        
        for round_name in ["flop", "turn", "river"]:
            if round_name == "flop":
                prompt = "Enter the flop cards (e.g., 2h 3d 5s): "
            else:
                prompt = f"Enter the {round_name} card (e.g., 9c): "
            
            board_cards = input(prompt).split()
            if any(card.lower() == 'r' for card in board_cards):
                sys.exit()
            
            try:
                board = [parse_card(card) for card in board_cards]
            except KeyError as e:
                print(f"Invalid card input: {e}. Please try again.")
                continue
            
            try:
                num_players = int(input("How many players are playing now? "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue
            
            probability = get_probability(evaluator, hand, board, num_players)
            print(f"{round_name.capitalize()} probability of winning: {probability * 100:.2f}%")

if __name__ == "__main__":
    main()
