import sys
from card_utils import parse_card
from probability_calculator import get_hand_probabilities
from treys import Evaluator

hand_order = [
    'straight_flush',
    'four_of_a_kind',
    'full_house',
    'flush',
    'straight',
    'three_of_a_kind',
    'two_pair',
    'one_pair',
    'high_card'
]

def print_probabilities(round_name, user_probabilities, opponent_probabilities, win_probability, tie_probability):
    print(f"\n{round_name.capitalize()} probabilities of each hand type:")
    
    print("{:<20} {:<10} {:<10}".format("Hand Type", "You", "Others"))
    print("{:<20} {:<10} {:<10}".format("---------", "---", "------"))

    for hand_type in hand_order:
        user_prob = user_probabilities.get(hand_type, 0.0) * 100
        opponent_prob = opponent_probabilities.get(hand_type, 0.0) * 100
        hand_type_display = hand_type.replace('_', ' ').title()
        print("{:<20} {:<10.2f} {:<10.2f}".format(hand_type_display, user_prob, opponent_prob))
    
    print() 
    
    print("{:<20} {:<10} {:<10}".format("", "You", "Others"))
    print("{:<20} {:<10} {:<10}".format("", "---", "------"))
    print("{:<20} {:<10.2f} {:<10.2f}".format("Win", win_probability * 100, (100 - win_probability * 100 - tie_probability * 100)))
    print("{:<20} {:<10.2f} {:<10.2f}".format("Tie", tie_probability * 100, tie_probability * 100))
    print()  

def main():
    evaluator = Evaluator()
    
    while True:
        try:
            num_players = int(input("\nHow many players are playing? "))
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
        
        user_probabilities, opponent_probabilities, win_probability, tie_probability = get_hand_probabilities(evaluator, hand, [], num_players)
        print_probabilities("Pre-flop", user_probabilities, opponent_probabilities, win_probability, tie_probability)
        
        board = []
        for round_name in ["flop", "turn", "river"]:
            if round_name == "flop":
                prompt = "Enter the flop cards (e.g., 2h 3d 5s): "
            else:
                prompt = f"Enter the {round_name} card (e.g., 9c): "
            
            board_cards = input(prompt).split()
            if any(card.lower() == 'r' for card in board_cards):
                sys.exit()

            # Check for correct number of cards for each round
            if round_name == "flop" and len(board_cards) != 3:
                print("Error: Please enter exactly 3 cards for the flop.")
                continue
            elif round_name in ["turn", "river"] and len(board_cards) != 1:
                print(f"Error: Please enter exactly 1 card for the {round_name}.")
                continue

            try:
                board.extend([parse_card(card) for card in board_cards])
            except KeyError as e:
                print(f"Invalid card input: {e}. Please try again.")
                continue
            
            try:
                num_players = int(input("How many players are playing now? "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue
            
            is_final_round = round_name == "river"
            user_probabilities, opponent_probabilities, win_probability, tie_probability = get_hand_probabilities(evaluator, hand, board, num_players, is_final_round)
            print_probabilities(round_name, user_probabilities, opponent_probabilities, win_probability, tie_probability)

            if is_final_round:
                sys.exit()  # End the program after the river round

if __name__ == "__main__":
    main()