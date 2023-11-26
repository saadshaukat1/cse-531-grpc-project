from time import sleep

import grpc
from termcolor import colored

import branch_pb2_grpc
from branch_pb2 import MsgRequest


class Customer:
    def __init__(self, id, events):
        self.id = id
        self.events = events
        self.writeSet = list()
        self.recvMsg = list()
        self.stub = None

    # Setup gRPC channel & client stub for branch
    def createStub(self):
        port = str(50000 + self.id)
        channel = grpc.insecure_channel("localhost:" + port)
        self.stub = branch_pb2_grpc.BranchStub(channel)

    # Send gRPC request for each event
    def executeEvents(self):
        for event in self.events:
             # Check if the 'money' key is in the event dictionary
            if 'money' not in event:
                # If not, add it with a default value
                event['money'] = 0
                
            # Sleep 3 seconds for 'query' events
            if event["interface"] == "query":
                sleep(3)

            # Add operation to writeSet for 'deposit' and 'withdraw' events
            if event["interface"] in ["deposit", "withdraw"]:
                self.writeSet.append(event)

            # Send request to Branch server
            response = self.stub.MsgDelivery(
                MsgRequest(id=event["id"], interface=event["interface"], money=event["money"])
            )

            # Create msg to be appended to self.recvMsg list
            msg = {"interface": response.interface, "result": response.result}

            # Add 'money' entry for 'query' events
            if response.interface == "query":
                msg["money"] = response.money

            self.recvMsg.append(msg)

    # Generate output msg
    def output(self):
        return {"id": self.id, "recv": self.recvMsg}
