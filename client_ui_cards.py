import pygame
import os

from constants import CARD_FACES_DIR, Players
# , GAME_HEIGHT, CARD_IMG_HEIGHT, CARD_IMG_WIDTH
from client_game_state import GameState
from client_ui_game_state import UIGameState

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui_cards", level=DebugLevel.client_ui_cards.value)

# from game_logger import GameLogger

# client_logger: GameLogger


class CardsUI:
    _game_state: GameState
    _ui_game_state: UIGameState

    
    def __init__(self, client_game_state: GameState, client_game_ui_state: UIGameState) -> None:
        
        # associate the game state with the class
        self._game_state = client_game_state
                
        # associate the ui game state with the class
        self._ui_game_state = client_game_ui_state
        
        # self._ui_game_state._cards_faces = {}
        self._load_cards_faces()

        client_logger.info("initial cards scaling done")
    
    def _load_cards_faces(self) -> None:
        """
        Load the card faces into the cards_faces dictionary
        The cards_faces dictionary is used to store the card faces as self._originally_loaded_cards_faces
        The rescaling will always come from this dictionary to ensure consistent quality

        Raises:
            ValueError: If a svg file (card face) is missing
            ValueError: If a png file (card back or blank) is missing
            ValueError: If a svg file was not loaded correctly
            ValueError: If a png file was not loaded correctlty
            ValueError: If the dictonary ends up with the incorrect number of card faces
        """
        
        # dictionary to store the card faces
        cards_faces: dict[str, pygame.Surface] = {}
        
        # list of the card faces to load
        play_cards_list: list[str] = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                                      "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK",
                                      "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK",
                                      "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]
        other_cards_list: list[str] = ["BB", "BR", "EC"]
        
        # Get the list of all SVG files in the directory
        # Currently the card faces only are in SVG format
        svg_files: list[str] = [f for f in os.listdir(CARD_FACES_DIR) if f.endswith('.svg')]
        
        # check that all the card faces files can be found.  (at least as filenames)
        for card in play_cards_list:
            if card + ".svg" not in svg_files:
                raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
        
        # Get the list of all PNG files in the directory
        # Currently the card backs and empty card only are in PNG format
        png_files: list[str] = [f for f in os.listdir(CARD_FACES_DIR) if f.endswith('.png')]
        
        # check that all the card faces files can be found.  (at least as filenames)
        for card in other_cards_list:
            if card + ".png" not in png_files:
                raise ValueError(f"Card {card} not found in {CARD_FACES_DIR}")
        
        # For each card in the play_cards_list...
        for card in play_cards_list:
            
            # Load the card graphics into the card_faces dictionary
            try: 
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.svg"))
            except pygame.error as e:
                raise ValueError(f"Card {card} not loaded: {e}")

        # for the cards in the other_cards_list
        for card in other_cards_list:
            
            # Load the card graphics into the card_faces dictionary
            try:
                cards_faces[card] = pygame.image.load(os.path.join(CARD_FACES_DIR, f"{card}.png"))
            except pygame.error as e:
                raise ValueError(f"Card BB, BR or EC not loaded: {e}")
            
        # Double check that all cards have a graphics associated
        if len(cards_faces) != len(play_cards_list) + len(other_cards_list):
            raise ValueError(f"card images problem: only {len(cards_faces)} cards loaded, expected {len(play_cards_list) + len(other_cards_list)}")

        # Convert each card face to a pygame surface
        for card in cards_faces:
            cards_faces[card] = cards_faces[card].convert()

        # Store this as the original dictionary to ensure consistent quality
        self._ui_game_state.originally_loaded_cards_faces = cards_faces.copy()
        
        
        # self._ui_game_state.scale_cards_faces()
        
        # print(self._ui_game_state._cards_faces["EC"].get_rect())
        # self._ui_game_state.cards_faces = cards_faces.copy()
        
        # self.scale_cards_faces()
        # This is not stored in the _ui_game_state - only the rescaled sprites are stored there
    
    
    def get_card_face(self, card: str) -> pygame.Surface:
        """
        Return the card face for the given card
        
        Args:
            card (str): the card to get the face for
            
        Returns:
            pygame.Surface: the card face for the given card
        """
        # "Cards" contains Suit [1 char] Rank [1 or 2 char] face_up [1 char] playerOwner [1 char]
        card_face: str = card[:-2]
        card_graphic = self._ui_game_state._cards_faces[card_face]
        
        return card_graphic
        
    def get_card_back(self, card:str) -> pygame.Surface:
        """
        Return the card back for the given card

        Args:
            card (str): the card to get the back for

        Returns:
            pygame.Surface: the card back for the given card
        """
        card_back = "BB" if Players(int(card[-1])) == self._game_state.player_id else "BR"
        card_graphic = self._ui_game_state._cards_faces[card_back] 
        
        return card_graphic
    
    def get_card_graphic(self, card:str) -> pygame.Surface:
        """
        Return the card graphic for the given card
        
        Args:
            card (str): the card to get the graphic for

        Returns:
            pygame.Surface: the card graphic for the given card
        """
        # "Cards" contains SR(R)u/dP:
        #   Suit [1 char]           CDHS
        #   Rank [1 or 2 char]      1-10, J, Q, K
        #   face_up [1 char]        u or d
        #   playerOwner [1 char]    0 or 1
        
        if card[-2] == 'u':
            card_graphic = self.get_card_face(card)
        else:
            card_graphic = self.get_card_back(card)
            
        return card_graphic
    
    def where_to_place_card_initially(self, this_player: int, stack:str) -> tuple[tuple[int, int], bool]:
        """
        Calculate the position where the card should be placed
        
        Args:
            this_player (int): the player whose turn it is
            stack (str): the stack where the card should go
            
        Returns:
            The top left position of the card on the window
        """
        
        player: int = self._game_state.player_id.value        
        stack_prefix = "player_" if this_player == player else "opponent_"

        ((x, y, w, h), vertical) = self._ui_game_state.stacks_locations[stack_prefix + stack]
        
        return (x, y), vertical
        
    def card_orientate(self, card: pygame.Surface, vertical: bool) -> pygame.Surface:
        """
        Rotate the card as needed for the target stack
        
        Args:
            card (pygame.Surface): the card to be rotated
            vertical (int): the orientation (vertical = True)
        
        Returns:
            The rotated card if needed rotating
        """
        
        return card if vertical else pygame.transform.rotate(card.copy(), 90)
        
    def place_card(self, this_player: int, stack: str, card: str) -> None:
        """
        Place a card on the screen, at initialisation time

        Args:
            screen (pygame.surface): the main display area for the game
            player (int): the player whose turn it is
            stack (str): the stack where the card is located
            card (str): the card to be placed
        """

        # Get the card graphic, either face or back
        card_graphic = self.get_card_graphic(card)
        
        # Get the card placement for the stack. Also get the vertical orientation information
        card_placement, vertical = self.where_to_place_card_initially(this_player, stack)
        
        # Orientate the card for the stack
        card_graphic = self.card_orientate(card_graphic, vertical) 
        
        self._ui_game_state.window.blit(card_graphic, card_placement)
        
        # card_face: str = card[:-2]
        
        # Calculate the position of the card on the screen
        # player: int = self._game_state.player_id.value        
        # stack_prefix = "player_" if this_player == player else "opponent_"

        # ((x, y, w, h), vertical) = self._ui_game_state.stacks_locations[stack_prefix + stack]
        

        # if card[-2] == 'u':  # face up or down. this is the second to last char.
        #     card_graphic = self._ui_game_state._cards_faces[card_face]
        # else:
        #     card_back = "BB" if Players(card[-1]) == self._game_state.player_id else "BR"
        #     card_graphic = self._ui_game_state._cards_faces[card_back] 
    
        # blit_card = self._ui_game_state._cards_faces[card_face] if vertical \
        #             else pygame.transform.rotate(self._ui_game_state._cards_faces[card_face].copy(), 90)
            
        # blit_card = card_graphic if vertical else pygame.transform.rotate(card_graphic.copy(), 90)
        
        # self._ui_game_state._window.blit(blit_card, (x, y) )
        
    def place_on_stack_initially(self, this_player: int, stack: str,  cards_list: list[str]) -> None:
        
        
        # Calculate the position of the card on the screen
        # player: int = self._game_state.player_id.value   
             
        # stack_prefix = "player_" if this_player == player else "opponent_"
        # ((x, y, w, h), vertical) = self._ui_game_state.stacks_locations[stack_prefix + stack_name]
        
        card_placement, vertical = self.where_to_place_card_initially(this_player, stack)
        
        shift: int = self._ui_game_state.tableau_cards_shift
        # shift: int = self.width // 4
        
        cards_blits = []
        
        for card in cards_list:
        #     # cards contains Suit [1 char] Rank [1 or 2 char] face_up [1 char] 
        #     card_face: str = card[:-1]

        #     # client_logger.debug(f"{player=} {this_player=}")
            
        #     if card[-1] == 'u':  # face up
        #         card_graphic = self._ui_game_state._cards_faces[card_face]
        #     else:
        #         card_graphic = self._ui_game_state._cards_faces["BB" if this_player == player else "BR"] # self._ui_game_state._cards_faces["BR"] 
        # # if this_player == 1 else "BR"]
        #     # blit_card = self._ui_game_state._cards_faces[card_face] if vertical \
        #     #             else pygame.transform.rotate(self._ui_game_state._cards_faces[card_face].copy(), 90)
            card_graphic = self.get_card_graphic(card)    
            card_graphic = self.card_orientate(card_graphic, vertical)
            
                
            # cards_blits.append(card_graphic if vertical else pygame.transform.rotate(card_graphic.copy(), 90))
            cards_blits.append(card_graphic)
        
        for card_blit in cards_blits:
            self._ui_game_state.window.blit(card_blit, card_placement )
            
            if "tableau" in stack:
                if this_player == self._game_state.player_id.value:
                    next_card_position = (card_placement[0] + shift, card_placement[1])
                else:
                    next_card_position = (card_placement[0] - shift, card_placement[1])
                card_placement = next_card_position

                    

                
            # self._ui_game_state._window.blit(card_blit, (x, y) )
            
            # if stack_name[:-1] == "tableau" and this_player == player:
            #     x += shift
                
            # if stack_name[:-1] == "tableau" and this_player != player:
            #     x -= shift
                
            # if stack_name == "crapette" and this_player == player:
            #     x -= shift
                
            # if stack_name == "crapette" and this_player != player:
            #     x += shift
                
    def place_stacks_cards_initially(self) -> None:
        stacks: dict[str, dict[str, list[str]]] = self._game_state.stacks_cards
        player = self._game_state.player_id.value
        opponent = 1 - player

        # our cards
        for stack_name, card_stack in stacks[Players(player).name].items():
            self.place_on_stack_initially(player, stack_name, card_stack)
       
        # #opponent cards
        for stack_name, card_stack in stacks[Players(opponent).name].items():
            self.place_on_stack_initially(opponent, stack_name, card_stack)
