import grpc
from concurrent import futures
import mychatbot_pb2, mychatbot_pb2_grpc

# Import your sync wrapper around the Replicate stream
from mybot.mybot_template import call_model_sync

class SimpleChatbotServicer(simplechatbot_pb2_grpc.simplechatbotServicer):
    def predict(self, request, context):
        # request.input1 is the user message
        user_msg = request.input1
        try:
            # call_model_sync should return your model’s reply as a string
            reply = call_model_sync(user_msg)
            return mychatbot_pb2.predict_resp(output1=reply)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return mychatbot_pb2.predict_resp(output1="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    mychatbot_pb2_grpc.add_mychatbot_to_server(
        mychatbotServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on port 50051…")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
