# Here I want to create an interface for communication and planet exploration
# Meant to make the life of our teammates working on the odometry easier
# and in end effect our main method cleaner
# and also to make sure that the respective methods are called in the right order
# (so that for example pathSelect message couldn't be sent without sending the path or ready messages prior)
# This way, we also make sure that the values entering the database are indeed those validated by the server
import CommunicationFactory
from ExplorationManager import ExplorationManager
from CommunicationFactory import CommunicationFactory


class CommunicationExplorationInterface:

    # This dream didn't come true
    # My goal was to make this class iterable
    # so that, after the first vertex
    # the team can iterate over the exploration more or less in such a way:

    # while exploration.hasNext():
    # odometry.turn_and_follow_line(exploration.next())
    # exploration.push_scanning_results(odometry.get_scanned_nodes())

    # and these classes would manage all the rest, including the messaging, target setting, exploration etc
    # and, after the target has been reached or the exploration completed,
    # the hasNext() method would return false

    def __init__(self, client, logger):
        self.explorer = ExplorationManager()
        self.communication = CommunicationFactory.getInstance(client, logger, self.explorer)

    def first_vertex_arrival(self):
        pass

    def arrived_at_vertex(self, estimated_x, estimated_y, estimated_direction):
        pass

    # we will call the get_directions function twice at every vertex
    # once with path_select_check set to False for sending the path_select message
    # and then with the above check set to True for getting the real, server-updated (or not) direction
    def get_directions(self, path_select_check=False):
        return self.explorer.get_directions() if not path_select_check else self.__get_path_select()

    def __get_path_select(self) -> int:
        if self.explorer.path_select_set:
            self.explorer.path_select_set = False
            return self.explorer.path_select_dir
        else:
            return self.explorer.last_direction

