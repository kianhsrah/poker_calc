from treys import Card

def parse_card(card_str):
    rank_dict = {'1': 'A', 'a': 'A', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': 'T', 'j': 'J', 'q': 'Q', 'k': 'K'}
    suit_dict = {'s': 's', 'h': 'h', 'd': 'd', 'c': 'c'}
    
    rank = rank_dict.get(card_str[:-1].lower())
    suit = suit_dict.get(card_str[-1].lower())
    
    if not rank or not suit:
        raise KeyError(f"Invalid card input: {card_str}")
    
    return Card.new(rank + suit)
