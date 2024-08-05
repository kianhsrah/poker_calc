from treys import Deck, Evaluator, Card
from collections import defaultdict

def classify_hand(evaluator, board, hand):
    score = evaluator.evaluate(board, hand)
    hand_class = evaluator.get_rank_class(score)
    if hand_class == 1:
        return 'straight_flush'
    elif hand_class == 2:
        return 'four_of_a_kind'
    elif hand_class == 3:
        return 'full_house'
    elif hand_class == 4:
        return 'flush'
    elif hand_class == 5:
        return 'straight'
    elif hand_class == 6:
        return 'three_of_a_kind'
    elif hand_class == 7:
        return 'two_pair'
    elif hand_class == 8:
        return 'one_pair'
    else:
        return 'high_card'

def get_hand_probabilities(evaluator, hand, board, num_players, is_final_round=False):
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
        deck.shuffle()
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

    if is_final_round:
        final_user_hand_type = classify_hand(evaluator, board, hand)
        user_probabilities = {hand_type: (1.0 if hand_type == final_user_hand_type else 0.0) for hand_type in hand_order}
        tie_probability = 1.0 if user_score == best_opponent_score else 0.0
    
    return user_probabilities, opponent_probabilities, win_probability, tie_probability