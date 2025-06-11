import pygame

class UIGameState:
    _surface: pygame.Surface
    _stacks_locations: dict[str, tuple[int, int, bool]] # (x, y, V(True)/H)
    _cards_faces: dict[str, pygame.Surface]
    _is_moving: bool
    
    
    def __init__(self) -> None:
        self._is_moving = False
        self._stacks_locations = {}
        self._cards_faces = {}
        
    @property
    def stacks_locations(self) -> dict[str, tuple[int, int, bool]]:
        return self._stacks_locations
        
    @stacks_locations.setter
    def stacks_locations(self, stacks_locations: dict[str, tuple[int, int, bool]]) -> None:
        self._stacks_locations = stacks_locations
                
    @property
    def surface(self) -> pygame.Surface:
        return self._surface
    
    @surface.setter
    def surface(self, surface: pygame.Surface) -> None:
        self._surface = surface