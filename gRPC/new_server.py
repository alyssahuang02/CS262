import grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources

class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        