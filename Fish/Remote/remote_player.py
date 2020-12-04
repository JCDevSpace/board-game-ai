import pathlib
import sys
scriptPath = pathlib.Path(__file__).parent.absolute()

from Fish.Remote.messages import Messages

# A Remote Player that can be given to the Referee,
# which communicates with the client
class RemotePlayer:

    def __init__(self, name, age, con, timeout, buff_size):
        self.name = name
        self.age = age
        self.con = con
        self.buff_size = buff_size
        self.con.settimeout(timeout)

        self.state = None
        self.color = None

        self.actions = []


    # Returns the age of the player
    # Void -> Int
    def get_age(self):
        return self.age

    # Returns the id of the player
    # Void -> Str
    def get_id(self):
        return self.name

    # Returns the color that the player got assigned with in a game
    # Void -> Str
    def assigned_color(self):
        return self.color

    # Updates the player on it's color assignment in the game
    # returns True if the update was successfully processed
    # else False
    # Color -> Boolean
    def color_assignment_update(self, color):
        self.color = color
        encoded_message = Messages.encode(Messages.PLAYING_AS, [color])

        self.con.sendall(encoded_message)
        return self.process_response()

    # Updates the player of the initial state of the game
    # returns True if the update was successfully processed
    # else False
    # GameState -> Boolean
    def inital_state_update(self, state):
        player_colors = state[1]

        self.state = GameState.generate_game_state(*state)

        encoded_message = Messages.encode(Messages.PLAYING_WITH, [state[1]])

        self.con.sendall(encoded_message)
        return self.process_response()

    # Updates the player of a placement action in the game
    # returns True if the update was successfully processed
    # else False
    # Placement -> Boolean
    def placement_update(self, placement):
        self.state.place_penguin(*placement)

    # Updates the player of a movement action in the game
    # returns True if the update was successfully processed
    # else False
    # Move -> Boolean
    def movement_update(self, movement):
        self.state.apply_move(movement)
        self.actions.append(movement)

    # Updates the player of a player kick in the game
    # returns True if the update was successfully processed
    # else False
    # Kick -> Boolean
    def player_kick_update(self, kick):
        self.state.remove_player(kick[0])

    # Gets a placement action from the player
    # Void -> Placement
    def get_placement(self):
        converted_state = Messages.convert_state(self.state.get_game_state())
        encoded_message = Messages.encode(Messages.SETUP, [converted_state])
        
        self.con.sendall(encoded_message)

        return self.process_response()

    # Gets a movement action from the player
    # Void -> Move
    def get_move(self):
        encoded_message = json_encode(self.state.get_game_state(), self.actions)
        self.actions = []

        self.con.sendall(encoded_message)

        return self.process_response()

    # Updates the player on the start of a tournament
    # returns True if the update was successfully processed
    # else False
    # Any -> Boolean
    def tournamnent_start_update(self):
        encoded_message = json_encode(True)

        self.con.sendall(encoded_message)

        return self.process_response()

    # Updates the player whether they have won the tournament
    # returns True if the update was successfully processed
    # else False
    # Boolean -> Boolean
    def tournamnent_result_update(self, won):
        encoded_message = json_encode(False)

        self.con.sendall(encoded_message)

        return self.process_response()

    # Processes the response from the client to something
    # that the referee can understand, if the response is
    # an invalid message, returns False
    def process_response(self):
        with self.con.recv(self.buff_size) as resp_msg:
            converted_response = Messages.convert_message(resp_msg)

            if converted_response:
                resp_type = Messages.response_type(converted_response)
                if resp_type == Messages.VOID:
                    return
                elif resp_type == Messages.POSITION:
                    return tuple(response)
                elif resp_type == Messages.ACTION:
                    return (self.color, response[0], response[1])
        return False
