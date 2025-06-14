import pygame

from client_ui_game_state import UIGameState

from game_logger import GameLogger, DebugLevel
client_logger: GameLogger = GameLogger("client_ui_stacks_layout", level=DebugLevel.client_ui_stacks_layout.value)


class StacksLayoutUI:
    _ui_game_state: UIGameState

    
    def __init__(self, ui_game_state: UIGameState) -> None:
        """
        Initialise the stacks layout
        Calculate the positions of the stacks
        Store the positions in the _positions attribute
        """
        
        self._ui_game_state = ui_game_state
        
    def render_empty_stacks(self) -> None:
        """
        Display the stacks positions using an empty card. 

        Args:
            surface (pygame.Surface): The surface to display on
            cards (Cards): the set of card graphics to use
        """
        stacks_locations = self._ui_game_state._stacks_positions
        
        card_face: str = "EC"
        # card_face = "HQ"
        
        card_graphics = self._ui_game_state.card_face(card_face)

        for stack in stacks_locations:
            ((x, y, w, h), vertical) = stacks_locations[stack]
            blank_blit = card_graphics if vertical else pygame.transform.rotate(card_graphics.copy(), 90)
            
            if card_face == "EC":
                blank_blit.set_colorkey(blank_blit.get_at((3,3)))
            
            self._ui_game_state.window.blit(blank_blit, (x, y) )

            
    def render_stacks_locations(self) -> None:
        for stack in self._ui_game_state.stacks_positions:
            if "crapette" in stack:
                pygame.draw.rect(self._ui_game_state.window, (128, 50, 0), self._ui_game_state.stacks_positions[stack][0], 5)
            else:    
                pygame.draw.rect(self._ui_game_state.window, (128, 128, 128), self._ui_game_state.stacks_positions[stack][0], 1)

            
    def render_cards_positions(self) -> None:

        for stack in self._ui_game_state.cards_positions:
            for card_rect, card_num, card_name in self._ui_game_state.cards_positions[stack]:
                pygame.draw.rect(self._ui_game_state.window, ( 255, 255, 0), card_rect, 2)


            