# -*- coding: utf-8 -*-

from time import time

import grpc

from proto.builds.service_pb2 import Null, Ticket
from proto.builds.service_pb2_grpc import TestServiceStub


def main():
    with grpc.insecure_channel("localhost:3000") as channel:
        client = TestServiceStub(channel)
        client.Health(Null())
        start = time()

        for _ in range(3000):
            client.AddTicket(Ticket(
                name="SomeTicket",
                description="...",
                story_points=2
            ))

            # print(confirmation.expected_dateline)

        print(time() - start)


if __name__ == "__main__":
    main()
