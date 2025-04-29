from cardstack import CardStack
from deck import Deck
from card import Card

class TableauStack(CardStack):
    _stack_name: str = "Tableau"
    _cards: list[Card]
    _selected_cards: list[Card]
    _player_num: int

    def __init__(self, deck: Deck, player_num):
        self._player_num = player_num
        self._cards = []
        first_card: Card = deck.draw_n_cards(1)[0]
        first_card.turn_face_up()
        self._cards.append(first_card)


    # @property
    # def top_card(self) -> Card:
    #     return self._cards[len(self._cards) - 1]

    # @property
    # def is_empty(self) -> bool:
    #     return len(self._cards) == 0

    # @property
    # def size(self) -> int:
    #     return len(self._cards)

    def position_in_stack(self, card) -> int | None:
        if card in self._cards:
            position: int = self._cards.index(card)
            return position
        else:
            return None

    def can_be_added(self, card: Card, player_num: int) -> bool:
        if self.is_empty:
            return True
        if self.top_card.is_one_above(card) and not self.top_card.is_same_colour(card):
            return True
        return False

    # def add_card(self, card: Card) -> bool:
    #     if self.can_be_added(card):
    #         self._cards.append(card)
    #         return True
    #     return False

    def add_n_cards(self, cards_to_add: list[Card], player_num: int) -> bool:
        # ic(self.top_card)
        # ic(cards_to_add[0])
        # ic(self.can_be_added(cards_to_add[0]))
        if self.can_be_added(cards_to_add[0], player_num):
            for card in cards_to_add:
                # ic(card)
                self.add_card(card, player_num)
            return True
        return False


    # def force_add_card(self, card: Card) -> None:
    #     """add a card to the tableau without checking rule, used for debug

    #     Args:
    #         card (Card): the card to add
    #     """
    #     self._cards.append(card)


    # def remove_top_card(self) -> None:
    #     self._cards.pop()

    def select_cards(self, card: Card) -> list[Card]|None:
        """Selects all the cards from the card provided to the top of the stack
        It does not remove the cards from the stack

        Args:
            card (Card): The card from which to select

        Returns:
            list[Card]: the card from which to select until the top of the pile, None if the card is not in the stack
        """
        position = self.position_in_stack(card)

        if not position:
            return None
        
        # TODO: It might be useful to use a parent/child linking instead but this'll do for now
        self._selected_cards = []
        self._selected_cards = self._cards[position:]
        return self._selected_cards
    
    def deselect_cards(self) -> None:
        self._selected_cards = []

    def remove_selected_cards(self) -> bool:
        if len(self._selected_cards) == 0:
            return True
        
        inverted_selected_cards: list[Card] = self._selected_cards[::-1]
        for card in inverted_selected_cards:
            if card == self.top_card:
                # self._cards.pop()
                self.remove_top_card()
            else:
                print("Error removing the selected card from the Tableau stack")
                return False
        return True

    @property
    def get_selected_Cards(self) -> list[Card] | None:
        """Returns the selected cards
        Returns:
        list[Card]: the selected cards
        """
        return self._selected_cards if len(self._selected_cards) != 0 else None