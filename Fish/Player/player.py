
import sys
sys.path.append('..')

from Fish.Common.state import GameState
from Fish.Common.game_tree import GameTree
from Fish.Common.message import Message

# A GamePlayer is a (Strategy, State, Color, GamePhase)
# The client will use this object to store information about the game state
# from the server. As it polls the data the client will check if it is the
# players turn. If so it will then send the server the players move or placement
# depending on the game phase.

DEFAULT_DEPTH = 2
class Player:


    # Initializes a player object with the strategy that they will be using
    # Strategy, Age -> Player
    def __init__(self, strategy, age, id, depth=DEFAULT_DEPTH):
        self.strategy = strategy
        self.age = age
        self.id = id
        self.depth = depth

        self.state = None
        self.color = None
        
        self.in_tournament = False
        self.kicked = False
        self.won = False

    # Returns the age of the player
    # Void -> Int
    def get_age(self):
        return self.age

    # Returns the id of the player
    # Void -> Str
    def get_id(self):
        return self.id

    # Updates the player of the initial state of the game
    # returns True if the update was successfully processed
    # else False
    # GameState -> Boolean
    def inital_state_update(self, state):
        self.state = GameState.generate_game_state(*state)
        return True

    # Updates the player on it's color assignment in the game
    # returns True if the update was successfully processed
    # else False
    # Color -> Boolean
    def color_assignment_update(self, color):
        self.color = color
        return True

    # Updates the player of a placement action in the game
    # returns True if the update was successfully processed
    # else False
    # Placement -> Boolean
    def placement_update(self, placement):
        self.state.place_penguin(*placement)
        return True

    # Updates the player of a movement action in the game
    # returns True if the update was successfully processed
    # else False
    # Move -> Boolean
    def movement_update(self, movement):
        self.state.apply_move(movement)
        return True

    # Updates the player of a player kick in the game
    # returns True if the update was successfully processed
    # else False
    # Color -> Boolean
    def player_kick_update(self, color):
        if color == self.color:
            self.kicked = True
        self.state.remove_player(color)
        return True

    # Gets a placement action from the player
    # Void -> Placement
    def get_placement(self):
        return (self.color, self.strategy.get_placement(self.state))

    # Gets a movement action from the player
    # Void -> Move
    def get_move(self):
        return self.strategy.get_move(GameTree(self.state), self.depth)

    # Updates the player on the start of a tournament
    # returns True if the update was successfully processed
    # else False
    # Any -> Boolean
    def update_tournamnent_start(self, content):
        self.in_tournament = True
        self.kicked = False
        return True

    # Updates the player whether they have won the tournament
    # returns True if the update was successfully processed
    # else False
    # Boolean -> Boolean
    def inform_tournamnent_result(self, won):
        self.won = won
        self.in_tournament = False
        return True
        
    # Updates a players internal state based on the message from a referee
    # returns false if the player failed to recieve the message
    # Message -> Boolean
    # def send_message(self, message):
    #     handler_table = {
    #         Message.COLOR_ASSIGNMENT: self.set_color,
    #         Message.PLACEMENT: self.perform_placement,
    #         Message.INITIAL_STATE: self.set_state,
    #         Message.MOVEMENT: self.perform_movement,
    #         Message.PLAYER_KICK: self.kick_player,
    #         Message.TOURNAMENT_START: self.tournamnent_started,
    #         Message.TOURNAMENT_RESULT: self.recieve_results
    #     }

    #     if message['type'] in handler_table:
    #         handler = handler_table[message['type']]
    #     else:
    #         return False

    #     try:
    #         result = handler(message['content'])
    #         return result
    #     except expression as identifier:
    #         return False
