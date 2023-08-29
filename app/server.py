# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import grpc

from proto.builds.service_pb2_grpc import TestServiceServicer, add_TestServiceServicer_to_server
from proto.builds.service_pb2 import Confirmation


class Service(TestServiceServicer):
    def Health(self, request, context):
        return request

    def AddTicket(self, request, context):
        expected_dateline = datetime.utcnow() + timedelta(days=request.story_points)
        return Confirmation(expected_dateline=expected_dateline.strftime("%Y-%m-%d %H:%M:%S"))



def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_TestServiceServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:3000")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()
