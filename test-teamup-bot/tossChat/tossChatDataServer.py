import grpc
from concurrent import futures
import time

# import the generated classes
import tossChatData_pb2
import tossChatData_pb2_grpc

# import the original calculator.py
import tossChatData

# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class tossChatServicer(tossChatData_pb2_grpc.tossChatServicer):

    def tossChatData(self, request, context):
        response = tossChatData_pb2.returnData()
        response.data = tossChatData.toss_Chat_Data(request.team_index, request.room_index, request.chat)
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
tossChatData_pb2_grpc.add_tossChatServicer_to_server(
        tossChatServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)