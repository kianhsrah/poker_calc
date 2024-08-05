from treys import Deck, Evaluator, Card
from collections import defaultdict

def classify_hand(evaluator, board, hand):
    score = evaluator.evaluate(board, hand)
    if score <= 10:
        return 'royal_flush'
    elif score <= 166:
        return 'straight_flush'
    elif score <= 322:
        return 'four_of_a_kind'
    elif score <= 1599:
        return 'full_house'
    elif score <= 1609:
        return 'flush'
    elif score <= 2467:
        return 'straight'
    elif score <= 3325:
        return 'three_of_a_kind'
    elif score <= 6185:
        return 'two_pair'
    elif score <= 7462:
        return 'one_pair'
    else:
        return 'high_card'

def get_hand_probabilities(evaluator, hand, board, num_players):
    deck = Deck()
    
    # Remove already known cards from the deck
    for card in hand + board:
        deck.cards.remove(card)
    
    user_hand_counts = defaultdict(int)
    opponent_hand_counts = defaultdict(int)
    win_count = 0
    tie_count = 0
    total_simulations = 10000
    
    for _ in range(total_simulations):  # Simulate 10,000 games
        # Reset the deck and remove known cards for each simulation
        deck = Deck()
        for card in hand + board:
            deck.cards.remove(card)
        
        remaining_board = deck.draw(5 - len(board))  # Draw the remaining board cards
        opponent_hands = [deck.draw(2) for _ in range(num_players - 1)]  # Draw opponent hands
        
        user_score = evaluator.evaluate(board + remaining_board, hand)
        user_hand_type = classify_hand(evaluator, board + remaining_board, hand)
        user_hand_counts[user_hand_type] += 1
        
        opponent_scores = [evaluator.evaluate(board + remaining_board, opponent_hand) for opponent_hand in opponent_hands]
        best_opponent_score = min(opponent_scores)
        
        if user_score < best_opponent_score:
            win_count += 1
        elif user_score == best_opponent_score:
            tie_count += 1
        
        for opponent_score, opponent_hand in zip(opponent_scores, opponent_hands):
            opponent_hand_type = classify_hand(evaluator, board + remaining_board, opponent_hand)
            opponent_hand_counts[opponent_hand_type] += 1
    
    user_probabilities = {hand_type: count / total_simulations for hand_type, count in user_hand_counts.items()}
    opponent_probabilities = {hand_type: count / (total_simulations * (num_players - 1)) for hand_type, count in opponent_hand_counts.items()}
    win_probability = win_count / total_simulations
    tie_probability = tie_count / total_simulations
    lose_probability = 1 - win_probability - tie_probability
    
    return user_probabilities, opponent_probabilities, win_probability, tie_probability, lose_probability
