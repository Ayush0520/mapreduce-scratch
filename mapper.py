import asyncio
import grpc
import MapReduce_pb2
import MapReduce_pb2_grpc
import math
import os

class Mapper(MapReduce_pb2_grpc.MapperServiceServicer):

    def __init__(self, mapper_id):
        self.id = mapper_id
        self.centroid_point_list = None

    def calculate_nearest_centroid(self, data_point, centroids):
        # Initialize variables for tracking the nearest centroid and its distance
        nearest_centroid_id = None
        min_distance = float('inf')  # Initialize with infinity to ensure any distance will be smaller

        # Iterate over each centroid
        for centroid in centroids:
            # Calculate Euclidean distance between data_point and the current centroid
            distance = self.euclidean_distance(data_point, centroid)

            # Update nearest centroid if the current centroid is closer
            if distance < min_distance:
                min_distance = distance
                nearest_centroid_id = centroid.id  # Assuming centroid has an 'id' attribute

        return nearest_centroid_id

    def euclidean_distance(self, point1, point2):
        point1 = point1.split(",")  # Split the string by commas
        point1 = [float(point.strip()) for point in point1]

        # Assuming point1 and point2 are tuples/lists of coordinates (x, y)
        distance = math.sqrt((point1[0] - point2.x) ** 2 + (point1[1] - point2.y) ** 2)
        return distance

    def read_data_points(self, start_index, end_index):
        data_points = []
        file_path = "Data/Input/input.txt"
        with open(file_path, "r") as file:
            for _ in range(start_index):
                next(file)  # Skip lines until reaching the start index
            for index, line in enumerate(file, start=start_index):
                if index > end_index:
                    break  # Stop reading if reached the end index
                data_point = line.strip()  # Assuming each line represents a data point
                data_points.append(data_point)
        return data_points
    


    async def perform_map(self, request, context):

        # Empty the Centroid Point List
        self.centroid_point_list = []

        # Extracting Parameters
        start_index = request.start_index
        end_index = request.end_index
        centroids = request.centroids
        num_reducers = request.num_reducers
        

        # Read data points from the file
        data_points = self.read_data_points(start_index, end_index)


        # Iterate over data points
        for index, data_point in enumerate(data_points):
            # Calculate the nearest centroid for the current data point
            nearest_centroid_id = self.calculate_nearest_centroid(data_point, centroids)
            self.centroid_point_list.append((nearest_centroid_id, data_point))

        # Perform Partition
        self.perform_partition(start_index, end_index, num_reducers)

        return MapReduce_pb2.MapperResponse(status="Success")

    def perform_partition(self, start_index, end_index, num_reducers):
        for reducer_id in range(num_reducers):
            partition_file = f"Data/Mappers/M{self.id}/partition_{reducer_id+1}.txt"
            print
            if os.path.exists(partition_file):
                os.remove(partition_file)

        for centroid, point in self.centroid_point_list:
            # Extract the index of the point from Data/Input/input.txt
            index = self.find_point_index(point, start_index, end_index)
            if index is not None:
                # Calculate the partition number by taking modulo with num_reducers
                partition_number = index % num_reducers
                # Construct the path to the partition file
                partition_file = f"Data/Mappers/M{self.id}/partition_{partition_number+1}.txt"
                # Save the tuple (centroid, point) to the partition file
                self.save_to_partition(partition_file, (centroid, point))

    def find_point_index(self, point, start_index, end_index):
        # Open the input file and search for the index of the point
        input_file = "Data/Input/input.txt"
        with open(input_file, "r") as file:
            for index, line in enumerate(file):
                if start_index <= index <= end_index and line.strip() == point:
                    return index
        return None

    def save_to_partition(self, partition_file, data):
        # Create the partition file if it doesn't exist
        os.makedirs(os.path.dirname(partition_file), exist_ok=True)
        # Append the tuple (centroid, point) to the partition file
        with open(partition_file, "a") as file:
            file.write(f"{data}\n")

    async def send_data_to_reducer(self, request, context):

        # Extracting Parameters
        data_request = request.data_request
        reducer_id = request.reducer_id

        partition_file = f"Data/Mappers/M{self.id}/partition_{reducer_id}.txt"

        return MapReduce_pb2.ReducerResponse(data_points=self.construct_parameters_for_reducer(partition_file))
    
    def construct_parameters_for_reducer(self, partition_file):
        data_points = []

        with open(partition_file, 'r') as file:
            for line in file:
                centroid_id = line[2:15]
                coordinates = line[19:-3].split(",")
                coordinates = [point.strip() for point in coordinates]
                data_points.append({'centroid_id': centroid_id, 'x': coordinates[0], 'y': coordinates[1]})

        return data_points


async def serve(server_id):
    server = grpc.aio.server()
    MapReduce_pb2_grpc.add_MapperServiceServicer_to_server(Mapper(server_id), server)
    server.add_insecure_port(f"localhost:{50000 + server_id - 1}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    server_id = int(input("Enter the Mapper server ID(Numeric): "))
    asyncio.run(serve(server_id))


