import pygame
import os
from pprint import pprint, pformat


from constants import CARD_FACES_DIR, Players
from client_game_state import GameState
from client_ui_game_state import UIGameState, CardToMove

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui_cards", level=DebugLevel.client_ui_cards.value)


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
    
    def get_card_face_sprite(self, card:str) -> pygame.Surface:
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
        
    def get_card_back_sprite(self, card:str) -> pygame.Surface:
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
            card_graphic = self.get_card_face_sprite(card)
        else:
            card_graphic = self.get_card_back_sprite(card)
            
        return card_graphic
    
    def get_stack_name_with_prefix(self, stack:str, this_player:int) -> str:
        """Return the stack to be used for this card"""
        player:int = self._game_state.player_id.value        
        stack_prefix = "player_" if this_player == player else "opponent_"
        
        return stack_prefix + stack
    
    def card_orientate(self, card:pygame.Surface, vertical:bool) -> pygame.Surface:
        """
        Rotate the card as needed for the target stack
        
        Args:
            card (pygame.Surface): the card to be rotated
            vertical (int): the orientation (vertical = True)
        
        Returns:
            The rotated card if needed rotating
        """
        
        return card if vertical else pygame.transform.rotate(card.copy(), 90)


    # def where_to_place_card_initially(self, this_player: int, stack:str) -> tuple[tuple[int, int], bool]:
    #     """
    #     Calculate the position where the card should be placed
        
    #     Args:
    #         this_player (int): the player whose turn it is
    #         stack (str): the stack where the card should go
            
    #     Returns:
    #         The top left position of the card on the window
    #     """
        
    #     stack_name = self.get_stack_name(stack, this_player)
    #     # player: int = self._game_state.player_id.value        
    #     # stack_prefix = "player_" if this_player == player else "opponent_"

    #     ((x, y, w, h), vertical) = self._ui_game_state.stacks_positions[stack_name]
        
    #     return (x, y), vertical
        
    # def place_card(self, this_player: int, stack: str, card: str) -> None:
    #     """
    #     Place a card on the screen, at initialisation time

    #     Args:
    #         screen (pygame.surface): the main display area for the game
    #         player (int): the player whose turn it is
    #         stack (str): the stack where the card is located
    #         card (str): the card to be placed
    #     """

    #     # Get the card graphic, either face or back
    #     card_graphic = self.get_card_graphic(card)
        
    #     # Get the card placement for the stack. Also get the vertical orientation information
    #     card_placement, vertical = self.where_to_place_card_initially(this_player, stack)
        
    #     # Orientate the card for the stack
    #     card_graphic = self.card_orientate(card_graphic, vertical) 
        
    #     # render the graphic on the window
    #     self._ui_game_state.window.blit(card_graphic, card_placement)
    
    # def place_on_stack_initially(self, this_player: int, stack: str,  cards_list: list[str]) -> None:
        
    #     card_placement, vertical = self.where_to_place_card_initially(this_player, stack)
        
    #     cards_blits: list[pygame.Surface] = []
        
    #     # Get all the cards for this stack
    #     for card in cards_list:
    #         card_graphic: pygame.Surface = self.get_card_graphic(card)    
    #         card_graphic = self.card_orientate(card_graphic, vertical)
            
    #         cards_blits.append(card_graphic)
        
    #     for card_blit in cards_blits:
    #         # Render the card on the display
    #         self._ui_game_state.window.blit(card_blit, card_placement )
            
    #         if "tableau" in stack:
    #             shift: int = self._ui_game_state.tableau_cards_shift
    #             # If the card belongs to player
    #             if this_player == self._game_state.player_id.value:
    #                 # shift right the position for the next card to be placed down
    #                 next_card_position = (card_placement[0] + shift, card_placement[1])
    #             else:
    #                 # shift left
    #                 next_card_position = (card_placement[0] - shift, card_placement[1])
    #             card_placement = next_card_position

    #         # stack_name = self.get_stack_name(stack, this_player)
            
    #         # # record that the card was placed on the stack
    #         # self._ui_game_state.stacks_locations[stack_name] = (card_placement[0], card_placement[1], vertical)
            
    # def place_stacks_cards_initially(self) -> None:
    #     stacks: dict[str, dict[str, list[str]]] = self._game_state.stacks_cards
    #     player = self._game_state.player_id.value
    #     opponent = 1 - player

    #     # our cards
    #     for stack_name, card_stack in stacks[Players(player).name].items():
    #         self.place_on_stack_initially(player, stack_name, card_stack)
       
    #     # #opponent cards
    #     for stack_name, card_stack in stacks[Players(opponent).name].items():
    #         self.place_on_stack_initially(opponent, stack_name, card_stack)


    def place_card_on_window(self, stack: str, card: tuple[pygame.Rect, int, str]) -> None:
        """Place a card on the table on a stack
        1. from the card name get the graphics (front or back) - from _card_faces
        2. from the stack, get the orentiation - from stacks_positions
        3. from the card, get the coordinate - from cards_positions

        Args:
            stack (str): _description_
            card (tuple[pygame.Rect, int, str]): Card position on the table, card position on the stack, card name (4/5 digits)
        """
        # Get the appropriate graphic (front face or back)
        card_graphic: pygame.Surface = self.get_card_graphic(card[2])

        # TODO: Define a "is_vertical" method
        if stack != "moving_cards":
            self.card_orientate(card_graphic, self._ui_game_state.stacks_positions[stack][1])

        card_position: tuple[int, int] = (card[0].x, card[0].y)

        # Render on the window
        self._ui_game_state.window.blit(card_graphic, card_position)

    def place_cards(self) -> None:
        """Go through all the stacks and display each card on the window
        1. Update the _cards_positions list from the various stacks
        2. Update the _cards_positions list with the cards that are currently moving (by the mouse)
        3. Go through the _cards_positions list and send each card to the correct position
        """

        stacked_cards_list: dict[str, list[tuple[pygame.Rect, int, str]]] = self.fill_stacked_card_positions()
        moving_cards_list: dict[str, list[tuple[pygame.Rect, int, str]]] = self.fill_moving_card_positions()

        # for stack, cards_list in self._ui_game_state.cards_positions.items():
        #     for card in cards_list:
        #         if card[2] != "": # does the card slot in cards_position have a card_name? if yes, there is a card
        #             self.place_card_on_window(stack, card)
        
        # for moving_stack, moving_cards in moving_cards_list.items():
        #     for moving_card in moving_cards:
        #         for stacked_card in stacked_cards_list[moving_stack]:
        #             if stacked_card[2] == moving_card[2]:
        #                 stacked_cards_list[moving_stack].remove(stacked_card)
        
        
        for stack, cards_list in stacked_cards_list.items():
            for card in cards_list:
                # if card[2] != "": # does the card slot in cards_position have a card_name? if yes, there is a card
                    self.place_card_on_window(stack, card)
                    
        for stack, cards_list in moving_cards_list.items():
            for card in cards_list:
                self.place_card_on_window(stack, card)
                
    def fill_stacked_card_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
        """ Make up the _cards_position list of cards per stack
        1. Get the information from the cards list received from the server (_stacks_cards)
        2. Process the cards list player by player.
        3. Process separately the non-tableau stacks from the tableau stacks, because the tableau stacks shift the cards so several can be picked
        4. 

        Fill the tableau and non-tableau card locations with the correct card values
        """               
        
        stacked_cards_list: dict[str, list[tuple[pygame.Rect, int, str]]] = {}
        
        # go player after player:
        for player_name, player_stacks in self._game_state.stacks_cards.items():
            
            # As the list of cards from the server 
            if Players[player_name] == self._game_state.player_id:
                stack_prefix = "player_"
            else:
                stack_prefix = "opponent_"
                
            # the stack after stack for that player
            for stack in player_stacks:
                
                temp_updated_stack: list[tuple[pygame.Rect, int, str]] = []
                
                        # # if the stack coming from the server is empty, reset the default entry
                        # if len(self._game_state.stacks_cards[self._game_state.player_id.name][stack]) == 0:
                        #     card_rect, card_num, card_name = self._ui_game_state.cards_positions[stack_prefix + stack][0]
                        #     self._ui_game_state.cards_positions[stack_prefix + stack][0] = (card_rect, -1, "")
                        #     continue

                # if the stack coming from the server is empty of cards, 
                # make the _cards_position for this stack emtpy
                if len(self._game_state.stacks_cards[self._game_state.player_id.name][stack]) == 0:
                    temp_updated_stack = []

                
                # if the stack is a tableau stack, 
                # process separately to take care of the card shift position 
                        # taken separately because there is a max of 13 and the card_rect is different per card
                        # so all placeholders have been pre-allocated
                elif "tableau" in stack:
                    
                    # enumerate through the cards
                    for i in range(len(self._game_state.stacks_cards[self._game_state.player_id.name][stack])):
                        
                        # Get the card name that was provided by the server
                        stack_card_name = self._game_state.stacks_cards[self._game_state.player_id.name][stack][i]
                        
                        # Get the stack position from the dict containing the info
                        card_rect = self._ui_game_state.stacks_positions[stack_prefix + stack][0]

                        # Get the tuple for the tableau_card_positions dictionary 
                        # card_rect, card_num, card_name = self._ui_game_state.tableau_cards_positions[stack_prefix + stack][i]
                        # card_rect, card_num, card_name = self._ui_game_state.cards_positions[stack_prefix + stack][i]
                        
                        # update the tuple with the correct card number and card name
                        # self._ui_game_state.tableau_cards_positions[stack_prefix + stack][i] = card_rect, i, stack_card_name
                        # self._ui_game_state.cards_positions[stack_prefix + stack][i] = card_rect, i, stack_card_name
                        temp_updated_stack.append((card_rect, i, stack_card_name))
                    self._ui_game_state.cards_positions[stack_prefix + stack] = temp_updated_stack
                    
                    # Add to the stacked cards list
                    stacked_cards_list[stack_prefix + stack] = temp_updated_stack

                    # Remmove any element that was from a previous stack and above the current stack quantity
                    
                          
                    # while len(self._ui_game_state.cards_positions[stack_prefix + stack]) > len(stack):
                    #         self._ui_game_state.cards_positions[stack_prefix + stack].pop()
                    # while len(self._ui_game_state.tableau_cards_positions[stack_prefix + stack]) > len(stack):
                    #         self._ui_game_state.tableau_cards_positions[stack_prefix + stack].pop()
                    
                else:
                    
                    # enumerate through the cards
                    for i in range(len(self._game_state.stacks_cards[self._game_state.player_id.name][stack])):
                        # Get the card name that was provided by the server
                        stack_card_name = self._game_state.stacks_cards[self._game_state.player_id.name][stack][i]
                        
                        # Get the stack position from the dict containing the info
                        card_rect = self._ui_game_state.stacks_positions[stack_prefix + stack][0]
                        
                        # Get the tuple for the non_tableau_card_positions dictionary 
                        # card_rect, card_num, card_name = self._ui_game_state.cards_positions[stack_prefix + stack][0]
                        # card_rect, card_num, card_name = self._ui_game_state.non_tableau_cards_positions[stack_prefix + stack][0]
                        
                        # update the tuple with the correct card number and card name       
                        # temp_updated_stack.append((card_rect, card_num, stack_card_name)) 
                        temp_updated_stack.append((card_rect, i, stack_card_name)) 
                    self._ui_game_state.cards_positions[stack_prefix + stack] = temp_updated_stack         
                    
                    stacked_cards_list[stack_prefix + stack] = temp_updated_stack      
                    
        return stacked_cards_list 

    def fill_moving_card_positions(self) -> dict[str, list[tuple[pygame.Rect, int, str]]]:
        
        moving_cards_list:dict[str, list[tuple[pygame.Rect, int, str]]] = {}
        
        temp_updated_stack:list[tuple[pygame.Rect, int, str]] = []

        for card in self._ui_game_state.moving_cards:
            temp_updated_stack.append((card["card_rect_on_window"], card["card_pos_on_stack"], card["card_name"]))

        self._ui_game_state.cards_positions["moving_cards"] = temp_updated_stack
        
        moving_cards_list["moving_cards"] = temp_updated_stack
        
        return moving_cards_list

    def switch_cards_to_move_from_stack_to_moving_stack(self) -> None:

        client_logger.debug("switching cards to moving stack")

        client_logger.debug(f"0 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        client_logger.debug(f"0 - {pformat(self._ui_game_state.cards_positions["moving_cards"])}")

        from_stack:str = str(self._ui_game_state.card_to_move["stack"])
        stack_pos:int = int(self._ui_game_state.card_to_move["card_pos_on_stack"])
        # stack_size = len(self._ui_game_state.cards_positions[from_stack]) 
        stack_size = len([card for card in self._ui_game_state.cards_positions[from_stack] if card[2] != ""]) 
        temp_stack:list[CardToMove] = []

        if "tableau" in from_stack:
            for card in range(stack_size -1, stack_pos - 1, -1):
                # temp_stack.append({
                #         "stack": from_stack, 
                #         "card_pos_on_stack": stack_pos, 
                #         "card_rect_on_window": self._ui_game_state.card_to_move["card_rect_on_window"], 
                #         "card_name": self._ui_game_state.card_to_move["card_na>me"]})
                temp_stack.append(CardToMove(
                        stack = from_stack, 
                        card_pos_on_stack = stack_pos, 
                        card_rect_on_window = self._ui_game_state.card_to_move["card_rect_on_window"], 
                        card_name = self._ui_game_state.card_to_move["card_name"]))
                
                self._ui_game_state.cards_positions[from_stack][card] = (\
                    self._ui_game_state.cards_positions[from_stack][card][0], \
                    -1, \
                    "")
            client_logger.debug(f"{pformat(temp_stack)}")
            self._ui_game_state.moving_cards = temp_stack
        else:
            temp_stack.append({
                    "stack": from_stack, 
                    "card_pos_on_stack": stack_pos, 
                    "card_rect_on_window": self._ui_game_state.card_to_move["card_rect_on_window"].copy(), 
                    "card_name":self._ui_game_state.card_to_move["card_name"]})
            self._ui_game_state.moving_cards = temp_stack

            # self._ui_game_state.cards_positions[from_stack][stack_pos] = pygame.Rect((0,0,0,0)), -1, ""
            self._ui_game_state.cards_positions[from_stack][stack_pos] = (\
                    self._ui_game_state.cards_positions[from_stack][stack_pos][0], \
                    -1, \
                    "")

        # pprint(f"1 {self._ui_game_state.cards_positions}")
        client_logger.debug(f"0.5 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        self.fill_moving_card_positions()

        client_logger.debug(f"1 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        client_logger.debug(f"1 - {pformat(self._ui_game_state.cards_positions["moving_cards"])}")

    def switch_cards_to_move_from_moving_stack_to_stack(self) -> None:

        client_logger.debug("switching cards back")

        # client_logger.debug(f"{self._ui_game_state.cards_positions}")
        # pprint("")
        # pprint(f"2 {self._ui_game_state.cards_positions}")

        # input()
        client_logger.debug(f"2 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        client_logger.debug(f"2 - {pformat(self._ui_game_state.cards_positions["moving_cards"])}")



        to_stack: str = self._ui_game_state.moving_cards[0]["stack"]
        to_stack_pos: int = self._ui_game_state.moving_cards[0]["card_pos_on_stack"]
        # to_stack_pos = len([card for card in self._ui_game_state.cards_positions[from_stack] if  card[2] != ""]) 
        moving_stack_size = len([card for card in self._ui_game_state.moving_cards if card["card_name"] != ""]) 
        # stack_size = len(self._ui_game_state.cards_positions[from_stack]) 
        # temp_stack = []

        if "tableau" in to_stack:
            for card in range(to_stack_pos, to_stack_pos + moving_stack_size):
                self._ui_game_state.cards_positions[to_stack][card] = (\
                        self._ui_game_state.cards_positions[to_stack][card][0], \
                        self._ui_game_state.moving_cards[card]["card_pos_on_stack"], \
                        self._ui_game_state.moving_cards[card]["card_name"])
                        # self._ui_game_state.stacks_positions[to_stack][0] + self._ui_game_state, 
                        # self._ui_game_state.moving_cards[card]["card_rect_on_window"], 

        else:
            self._ui_game_state.cards_positions[to_stack][to_stack_pos] = (\
                    self._ui_game_state.cards_positions[to_stack][to_stack_pos][0], \
                    self._ui_game_state.moving_cards[0]["card_pos_on_stack"], \
                    self._ui_game_state.moving_cards[0]["card_name"])


        # pprint(f"3 {self._ui_game_state.cards_positions}")
        client_logger.debug(f"3 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        client_logger.debug(f"3 - {pformat(self._ui_game_state.cards_positions["moving_cards"])}")
        # input()


        self._ui_game_state.reset_moving_cards()
        client_logger.debug(f"4 - {pformat(self._ui_game_state.cards_positions["player_tableau3"])}")
        client_logger.debug(f"4 - {pformat(self._ui_game_state.cards_positions["moving_cards"])}")
        # self.fill_card_positions()