import threading
import time
from omega.node.Message import Message
from omega.node.BlockchainUtils import BlockchainUtils


"""
Runs a thread for each node and looks for other nodes initiating connections.
"""
class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node

    """
    Initiates a thread for both status and discovery.
    """
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    """
    Status thread just prints current connections every 5s.
    """
    def status(self):
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(5)

    """
    Discovery thread broadcasts handshake message.
    """
    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    """
    Handshake sebds handshake message.
    """
    def handshake(self, connected_node):
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connected_node, handshakeMessage)


    """
    Message sent to all connected nodes.
    """    
    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    """
    Handles discovery message and connects peers not yet conencted.
    """
    def handleMessage(self, message):
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer:
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(
                    peersPeer.ip, peersPeer.port)
