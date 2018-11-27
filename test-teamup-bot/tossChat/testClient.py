
import grpc
import tossChatData_pb2
import tossChatData_pb2_grpc


channel = grpc.insecure_channel('localhost:50052')
stub = tossChatData_pb2_grpc.tossChatStub(channel)
chatData = tossChatData_pb2.ChatData(team_index=12357,room_index=514334,chat="Hello")
response = stub.tossChatData(chatData)

print(response.data)