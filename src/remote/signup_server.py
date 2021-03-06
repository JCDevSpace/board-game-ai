from src.remote.tcp_proxy_player import TCPProxyPlayer as Player
from src.admin.manager import Manager
from src.remote.message import MsgType
import src.remote.message as Message

from src.common.util import load_config, generate_players
from asyncio import start_server, create_task, sleep
from queue import Queue

import traceback


class SignUpServer:
    """
    A SignUpServer is a combination of:
    -dict:
        a dictionary of configuration parameters loaded on startup
    -Queue:
        a queue to keep track of players who have signed up for a tournament

    A SignUpServer is a server that accepts signups to board game tournaments. A match maker is started once anyone signed up for a tournament waiting for the configured match make length for new players to join, once that match maker length is over, a tournament manager is create and runs a tournament with all the players in the queue filling any open slots with inhouse AI players if less than the minimum players signed up.
    """

    def __init__(self):
        """Initializes a signup server, ready to start accepting signup and scheduling tournaments either once enough players signed up for a tournament of after a period of time
        """
        self.config = load_config("default_signup.yaml")
        self.player_queue = Queue()

    async def start(self):
        """Starts the signup server, processing tournament signups.
        """
        self.server = await start_server(self.process_signup_cb, self.config["host"], self.config["port"])

        async with self.server:
            await self.server.serve_forever()

    async def process_signup_cb(self, reader, writer):
        """Processes a signup request, recieving a name from the client to signup in a tournament with, starts a match maker if the signed up player is the first.

        Args:
            reader (Streams.StreamReader): a reader stream to recieve messages from the client
            writer (Streams.StreamWriter): a writer stream to sent message to the client
        """
        try:
            msg = await reader.read(self.config["read"])
            msg_type, name = Message.decode(msg)
            if msg_type == MsgType.SIGNUP and self.valid_name(name):
                self.player_queue.put(Player(name, 100, reader, writer))

                if self.player_queue.qsize() == 1:
                    create_task(self.match_maker())
        except Exception:
            writer.close()
            await writer.wait_closed()
            print(traceback.format_exc()) 

    async def match_maker(self):
        """Performs match making by waiting for the match make length of seconds specified in the server configuration, then if after that wait start a tournament with the signed up players so far.
        """
        await sleep(self.config["match_make"])

        create_task(self.start_tournament())

    def valid_name(self, name):
        """Determin whether the given name is valid according to the server configuration requirements.

        Args:
            name (str): a name string

        Returns:
            bool: a boolean with true indicating it's valid
        """
        return len(name) > self.config["min_name"] \
                and len(name) < self.config["max_name"]

    async def start_tournament(self):
        """Starts a board game tournament, enrolling all players from the queue, if after everyone from the queue is enroll and there is still less than the minimum number of player required for a tournament, generates inhouse AI players to fill up the difference.
        """
        enrolled_players = []

        while self.player_queue.qsize() > 0:
            enrolled_players.append(self.player_queue.get())

        if len(enrolled_players) < self.config["min_players"]:
            enrolled_players.extend( \
                generate_players( \
                    self.config["min_players"] - len(enrolled_players), \
                    self.config["ai_depth"]
                )
            )

        tournament_manager = Manager(enrolled_players)

        results = await tournament_manager.run_tournament()
        
        self.output_results(results)

    def output_results(self, results):
        print("\n\nTournament Results")
        for i, category in enumerate(["Winners:", "Loser:", "Kicked:"]):
            print("")
            print(category)
            for player in results[i]:
                print(player.get_name())
        


