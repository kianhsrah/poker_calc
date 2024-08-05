from treys import Deck, Evaluator

def get_probability(evaluator, hand, board, num_players):
    deck = Deck()
    
    # Remove already known cards from the deck
    for card in hand + board:
        deck.cards.remove(card)
    
    wins = 0
    total = 0
    
    for _ in range(10000):  # Simulate 10,000 games
        # Reset the deck and remove known cards for each simulation
        deck = Deck()
        for card in hand + board:
            deck.cards.remove(card)
        
        remaining_board = deck.draw(5 - len(board))  # Draw the remaining board cards
        opponent_hands = [deck.draw(2) for _ in range(num_players - 1)]  # Draw opponent hands
        
        all_hands = [hand] + opponent_hands
        scores = [evaluator.evaluate(board + remaining_board, h) for h in all_hands]
        
        if scores[0] == min(scores):
            wins += 1
        
        total += 1
    
    return wins / total
