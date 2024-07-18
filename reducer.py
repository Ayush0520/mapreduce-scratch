import grpc
import asyncio
import MapReduce_pb2
import MapReduce_pb2_grpc

class Reducer(MapReduce_pb2_grpc.ReducerServiceServicer):
    
    def __init__(self, reducer_id):
        self.id = reducer_id
        self.mapper_port_dict = None
        self.mapper_stubs = None
        self.data = None


    # Assign Mapper Port Nos. 
    def assign_port(self, num_mappers, base_port):
        port_dict = {}
        for i in range(0, num_mappers):
            port_dict[f"M{i+1}"] = base_port+i
        return port_dict
    
    # Creates Mapper Stubs
    def create_mapper_stubs(self):
        stubs = {}
        for mapper_id, mapper_port in self.mapper_port_dict.items():
            channel = grpc.aio.insecure_channel(f'localhost:{mapper_port}')
            stub = MapReduce_pb2_grpc.MapperServiceStub(channel)
            stubs[mapper_id] = stub
        return stubs

    async def invoke_reducer(self, request, context):

        # Extracting Parameters
        num_mappers = request.num_mappers
        num_centroids = request.num_centroids

        self.data = {}

        # Create Centroid Dictionary
        for centroid in range(num_centroids):
            self.data[f"centroid_id_{centroid}"] = []

        # Assigning Port No. to Mappers
        self.mapper_port_dict = self.assign_port(num_mappers, 50000)

        # Initialize gRPC channel and stubs for Mapper services
        self.mapper_stubs = self.create_mapper_stubs()

        mapper_parameters = []

        parameters = MapReduce_pb2.ReducerParameters(
            data_request='GET', 
            reducer_id=str(self.id)
        )

        # Prepare parameters for each Mapper
        for mapper_id, stub in self.mapper_stubs.items():
            mapper_parameters.append((mapper_id, parameters))

        # Send parameters to each Mapper asynchronously
        tasks = []
        for mapper_id, parameters in mapper_parameters:
            task = asyncio.create_task(self.send_parameters_to_mapper(mapper_id, parameters))
            tasks.append(task)

        # Wait for all Reducer tasks to complete
        await asyncio.gather(*tasks)

        # Continue with Shuffle and Sort, Reduce
        self.perform_shuffle_and_sort_reduce()

        return self.prepare_data()
    
    # Send Parameters to Mapper
    async def send_parameters_to_mapper(self, mapper_id, parameters):
        try:
            # Send parameters to Mapper asynchronously
            response = await self.mapper_stubs[mapper_id].send_data_to_reducer(parameters)
            # print(f"Received response from Mapper {mapper_id}: {response}")
            self.process_mapper_response(response)
        except Exception as e:
            print(f"Error sending parameters to Mapper {mapper_id}: {e}")

    def process_mapper_response(self, response):

        for entry in response.data_points:
            centroid_id = entry.centroid_id
            x = entry.x
            y = entry.y
            self.data[centroid_id].append((x,y))

        

    def perform_shuffle_and_sort_reduce(self):
        file_path = f"Data/Reducers/R{self.id}.txt"

        with open(file_path, "w") as file:
            for centroid_id, tuples_list in self.data.items():
                for tuple_ in tuples_list:
                    coordinates = ', '.join(map(str, tuple_))
                    file.write(f"Centroid ID: {centroid_id}, Coordinates: {coordinates}\n")

    def prepare_data(self):
        points_map = {}
        for centroid_id, points_list in self.data.items():
            points = MapReduce_pb2.Points()
            for point_tuple in points_list:
                point = MapReduce_pb2.Point(x=point_tuple[0], y=point_tuple[1])
                points.points.append(point)
            points_map[centroid_id] = points
        

        response = MapReduce_pb2.InvokeResponse()
        for centroid_id, points in points_map.items():
            response.data[centroid_id].CopyFrom(points)

        return response




async def serve(server_id):
    server = grpc.aio.server()
    MapReduce_pb2_grpc.add_ReducerServiceServicer_to_server(Reducer(server_id), server)
    server.add_insecure_port(f"localhost:{60000 + server_id - 1}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    server_id = int(input("Enter the Reducer server ID(Numeric): "))
    asyncio.run(serve(server_id))