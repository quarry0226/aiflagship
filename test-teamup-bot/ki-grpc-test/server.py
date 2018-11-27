import grpc
from concurrent import futures
import time

# import the generated classes
import conversation_pb2
import conversation_pb2_grpc

# import the original calculator.py
import make_chat

# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class ConversationServicer(conversation_pb2_grpc.ConversationServicer):

    def makeChat(self, request, context):
        response = conversation_pb2.ChatData()
        response.chat = make_chat.make_chat(request.team_index, request.room_index, request.chat)
        response.team_index = request.team_index
        response.room_index = request.room_index
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
conversation_pb2_grpc.add_ConversationServicer_to_server(
        ConversationServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)