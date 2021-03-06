from src.player.strategies.minimax_strategy import MinimaxStrategy
from src.player.i_player import IPlayer
from src.common.i_state import IState
from asyncio import get_running_loop


class MinimaxPlayer(IPlayer):
    """
    An MinimaxPlayer is a combination of:
    -str:
        a alphanumeric str that's less than 12 chars that represents a name
    -int:
        a non negative integer that uniquely identifies a player in the system
    -IStrategy:
        a strategy object that the player used to find the best action
    -IState:
        a game state of the board game

    An MinimaxPlayer represents a AI player developed internally for example purposes. This implementation is a stateful one leveraging the updates it gets for being an observer and uses the minimax strategy when finding best action to take.

    The MinimaxPlayer implements the IPlayer interface.
    """

    def __init__(self, name, unique_id, depth=2):
        """Initializes a AI player that uses the minimax strategy to find the best action in a board game.

        Args:
            name (str): a alphanumeric player name, less than 12 chars
            unique_id (int): a non negative integer uniquely identifies a player in the system
            depth (int, optional): a positive integer to set how deep to search with the minimax strategy. Defaults to 2.
        """
        self.name = name
        self.id = unique_id
        self.state = None
        self.strategy = self.generate_strategy(depth)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    async def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        self.state = game_state

    async def game_action_update(self, action):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
        """
        if self.state:
            self.state.apply_action(action)

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        if self.state:
            self.state.remove_player(player)

    async def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        self.color = color

    async def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        loop = get_running_loop()

        if self.state and self.state.serialize() == game_state.serialize():
            action = await loop.run_in_executor(None, self.strategy.get_action, self.state)
            return action
        
        self.state = game_state
        action = await loop.run_in_executor(None, self.strategy.get_action, game_state)
        return action

    def generate_strategy(self, depth):
        """Generate and returns a minimax strategy set to search at the given depth and uses the internal state evaluation function.

        Args:
            depth (int): a postive integer

        Returns:
            IStrategy: a strategy object
        """
        return MinimaxStrategy(self.evaluate_state, depth)

    def evaluate_state(self, player, game_state):
        """Evaluates the value of a state for the specified player.

        Args:
            player (str): a color string representing a player
            game_state (int): a non negative integer
        """
        score = game_state.game_score(player)
        if score:
            return score 
        return 0