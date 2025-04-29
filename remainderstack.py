from cardstack import CardStack
from card import Card
from deck import Deck

class RemainderStack(CardStack):
    _stack_name: str = "Remainder"
    _cards: list[Card]
    _player_num: int

    def __init__(self, deck: Deck, player_num: int):
        self._player_num = player_num
        self._cards = []
        self._cards = deck.draw_remaining_cards()
        if len(self._cards) != 52 - 13 - 4:
            raise ValueError(f"Error: The {self._stack_name} deck should have {52 - 13 - 4} cards, but it has {len(self._cards)} cards")

    # @property
    # def size(self) -> int:
    #     return len(self._cards)
    
    # @property
    # def top_card(self):
    #     return self._cards[len(self._cards) - 1]
    
    def reload_from_binstack(self, binstack_cards: list[Card]) -> bool:
        if self._cards:
            return False
        
        new_stack: list[Card] = binstack_cards
        new_stack.reverse()
        for card in new_stack:
            card.turn_face_down()
            self._cards.append(card)
        return True