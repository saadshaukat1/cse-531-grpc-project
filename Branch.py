from concurrent import futures
import time

import grpc
from termcolor import colored

import branch_pb2_grpc
from branch_pb2 import MsgRequest, MsgResponse


class Branch(branch_pb2_grpc.BranchServicer):
    """
    Represents a branch in the banking system.

    Attributes:
        id (int): The ID of the branch.
        balance (float): The current balance of the branch.
        branches (list): The IDs of the other branches in the system.
        stubList (list): List of gRPC client stubs for communication with other branches.
        recvMsg (list): List of received messages.
    """

    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.recvMsg = list()
        self.local_cache = dict()  # For Read your Writes
        self.last_write_time = dict()  # For Monotonic Writes

    # Setup gRPC channel & client stub for each branch
    def createStubs(self):
        for branchId in self.branches:
            if branchId != self.id:
                port = str(50000 + branchId)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))

    # Incoming MsgRequest from Customer transaction
    def MsgDelivery(self, request, context):
        writeSet = request.writeSet
        return self.ProcessMsg(request, True)

    # Incoming MsgRequest from Branch propagation
    def MsgPropagation(self, request, context):
        writeSet = request.writeSet
        return self.ProcessMsg(request, False)

    # Handle received Msg, generate and return a MsgResponse
  
    def ProcessMsg(self, request, propagate):
        result = "success"

        if request.money < 0:
            result = "fail"
        elif request.interface == "query":
            # If there's a locally cached value for this process, return it
            if request.id in self.local_cache:
                return MsgResponse(interface=request.interface, result="success", money=self.local_cache[request.id])
        elif request.interface == "deposit" or request.interface == "withdraw":
            # Get the current time
            current_time = time.time()
            
            # Check if there was a previous write operation by the same process
            if request.id in self.last_write_time:
                # If the previous write operation has not completed, return an error
                if self.last_write_time[request.id] > current_time:
                    return MsgResponse(interface=request.interface, result="fail", money=self.balance)
            start_time = time.time()

            # Update the balance and the last write time
            if request.interface == "deposit":
                self.balance += request.money
            else:  # request.interface == "withdraw"
                if self.balance >= request.money:
                    self.balance -= request.money
                else:
                    return MsgResponse(interface=request.interface, result="fail", money=self.balance)

            # Record the end time and calculate WRITE_OPERATION_TIME
            end_time = time.time()
            WRITE_OPERATION_DURATION = end_time - start_time

            # Update the local cache and the last write time for this process
            self.local_cache[request.id] = self.balance
            self.last_write_time[request.id] = current_time + WRITE_OPERATION_DURATION

            if propagate == True:
                if request.interface == "deposit":
                    self.Propagate_Deposit(request)
                else:  # request.interface == "withdraw"
                    self.Propagate_Withdraw(request)
        else:
            result = "fail"

        return MsgResponse(interface=request.interface, result=result, money=self.balance)    
    # Propagate Customer withdraw to other Branches
    def Propagate_Withdraw(self, request):
        for stub in self.stubList:
            stub.MsgPropagation(MsgRequest(id=request.id, interface="withdraw", money=request.money, writeSet=request.writeSet))

    # Propagate Customer deposit to other Branches
    def Propagate_Deposit(self, request):
        for stub in self.stubList:
            stub.MsgPropagation(MsgRequest(id=request.id, interface="deposit", money=request.money, writeSet=request.writeSet))