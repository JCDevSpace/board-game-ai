from Game.Remote.message import Message, MsgType


class TCPProxyPlayer:
    """
    A TCPProxyPlayer is a combination of:
    -socket.connection():
        a tcp socket connection for communicating with the external player
    -str:
        a string of at most 12 alphanumeric chars for the name of the player
    -id:
        a int that unqiuely identifies the player in the system

    A remote player is a proxy for external players to interaction with the server through a specified plug & play protocal. This allows the referee and tournament manager from the internal server to interaction with players implemented external as if it was an in house player over a network connection.

    A RemotePlayer implements and IPlayer interface.
    """

    def __init__(self, name, unique_id, reader, writer):
        self.conn = conn
        self.name = name
        self.id = unique_id

    def ge_id(self):
        return self.id

    def get_name(self):
        return self.name

    async def game_start_update(self, game_state):
        """Updates the observer on the start of a board game by consuming the given starting players and the game state.

        Args:
            game_state (IState): a game state object
        """
        message = Message.state2msg(MsgType.G_START, game_state)
        self.writer.write(message.encode())
        await self.writer.drain()

    async def game_action_update(self, action):
        """Updates the observer on an action progress of a board game.

        Args:
            action (Action): an action
        """
        message = Message.action2msg(MsgType.G_ACTION, action)
        self.writer.write(message.encode())
        await self.writer.drain()

    async def game_kick_update(self, player):
        """Updates the observer on a player kick from the board game.

        Args:
            player (str): a color string representing a player
        """
        if self.color == player:
            self.writer.close()
            await self.writer.wait_closed()
        else:
            message = Message.color2msg(MsgType.G_KICK, player)
            self.writer.write(message.encode())
            await self.writer.drain()
    
    async def tournament_start_update(self, players):
        """Updatest the observer on the start of a board game tournament with the initial contestents.

        Args:
            players (list(str)): a list of string representing player names
        """
        message = Message.names2msg(MsgType.T_START, players)
        self.writer.write(message.encode())
        await self.writer.drain()

    async def tournament_progress_update(self, advanced, knocked):
        """Updates the observer on the progress of a board game tournament by consuming the given players who advanced to the next round and the players who got knocked out.

        Args:
            advanced (list(str)): a list of player names
            knocked (list(str)): a list of player names
        """
        message = Message.names2msg(MsgType.T_PROGRESS, advanced, knocked)
        self.writer.write(message.encode())
        await self.writer.drain()

    async def tournament_end_update(self, winners):
        """Updates the observer on the final winners of the board game tournament, the finals winners include the top three players, with first player in the winners list as first place and the last one as thrid place. 

        Args:
            winners (list(str)): a list of player names
        """
        message = Message.names2msg(MsgType.T_END, winners)
        self.writer.write(message.encode())
        await self.writer.drain()

        self.writer.close()
        await self.writer.wait_closed()

    async def playing_as(self, color):
        """Updates the player the color that it's playing as in a board game.

        Args:
            color (str): a color string
        """
        self.color = color

        message = Message.color2msg(MsgType.PLAYING_AS, color)
        self.writer.write(message.encode())
        await self.writer.drain()

    async def get_action(self, game_state):
        """Finds the action to take in a board game by consuming the given game state, the player also recieves all action and player kick updates due to being an observer, thus a stateful implementation is also viable.

        Args:
            game_state (IState): a game state object

        Returns:
            Action: an action to take
        """
        message = Message.state2msg(Message.T_ACTION, color)
        self.writer.write(message.encode())
        await self.writer.drain()

        response = await self.reader.read()

        return Message.msg2action(response)