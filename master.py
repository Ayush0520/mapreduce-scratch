import random
import os
import grpc
import asyncio
import MapReduce_pb2
import MapReduce_pb2_grpc

class Master:

    def __init__(self, num_mappers, num_reducers, num_centroids, num_iterations):
        self.num_mappers = num_mappers
        self.num_reducers = num_reducers
        self.num_centroids = num_centroids
        self.num_iterations = num_iterations
        self.master_port = 49152
        self.base_port_mapper = 50000
        self.base_port_reducer = 60000
        self.mapper_port_dict = self.assign_port(self.num_mappers, self.base_port_mapper, True)
        self.reducer_port_dict = self.assign_port(self.num_reducers, self.base_port_reducer, False)
        self.centroid_dict = None

        # Print Mapper/Reducer Port Mapping
        self.print_port_mapping()

        # Intializing Centroids for K-Means
        self.generate_random_centroids("Data/centroids.txt", self.num_centroids, 2)

        # Adding to Data Directory Structure
        self.add_to__directory_structure()

        # Initialize gRPC channel and stubs for mapper and reducer services
        self.mapper_stubs = self.create_mapper_stubs()
        self.reducer_stubs = self.create_reducer_stubs()



    # Runs K-Means Clustering Algorithm
    async def run_kmeans(self):
        for iterations in range(self.num_iterations):
            self.centroid_dict = {}
            for id in range(self.num_centroids):
                self.centroid_dict[f"centroid_id_{id}"] = []
            mapper_parameters = []
            indices = self.assign_indices()
            centroids = self.read_centroids_file()
            self.append_to_dump(str(centroids))

            # Prepare parameters for each Mapper
            for mapper_id, stub in self.mapper_stubs.items():
                parameters = self.construct_parameters_for_mapper(mapper_id, indices, centroids)
                mapper_parameters.append((mapper_id, parameters))

            # Send parameters to each Mapper asynchronously
            tasks = []
            for mapper_id, parameters in mapper_parameters:
                task = asyncio.create_task(self.send_parameters_to_mapper(mapper_id, parameters))
                tasks.append(task)

            # Wait for all Mapper tasks to complete
            await asyncio.gather(*tasks)

            parameters = MapReduce_pb2.InvokeParameters(
                num_mappers=int(self.num_mappers),
                num_centroids=int(self.num_centroids)
            )

            # Continue with Reducer Task
            task = []
            for reducer_id in self.reducer_port_dict:
                task = asyncio.create_task(self.send_parameters_to_reducer_invoke(reducer_id, parameters))
                tasks.append(task)

            # Wait for all Mapper tasks to complete
            await asyncio.gather(*tasks)

            new_centroids = self.get_new_centroid()

            # Checks Convergence
            if self.check_convergence(new_centroids):
                break

        

    # Checks K-Means Algorithm Convergence
    def check_convergence(self, new_centroids):
        old_centroids = self.read_centroids_file()
        old_centroids_dict = {}

        for id in range(self.num_centroids):
            old_centroids_dict[f"centroid_id_{id}"] = (old_centroids[id][0], old_centroids[id][1])

        flag = True
        for mapper_id in old_centroids_dict:
            old_coordinates = old_centroids_dict[mapper_id]
            new_coordiates = new_centroids[mapper_id]

            if new_coordiates != old_coordinates or new_coordiates == None:
                flag = False

        # Define the path to the file
        file_path = "Data/centroids.txt"

        # Iterate through the dictionary and write coordinates to the file
        count = 0
        with open(file_path, "w") as file:
            for centroid_id, coordinates in new_centroids.items():
                # Write coordinates to the file
                if coordinates == None:
                    continue
                file.write("{},{}\n".format(coordinates[0], coordinates[1]))
                count += 1
        self.num_centroids = count

        self.append_to_dump(str(new_centroids))
        return flag

    def calculate_average(self, points):
        if len(points)==0:
            return None
        total_x = 0
        total_y = 0
        for point in points:
            total_x += float(point[0])
            total_y += float(point[1])
        avg_x = total_x / len(points)
        avg_y = total_y / len(points)
        return (avg_x, avg_y)

    def get_new_centroid(self):
        centroid_avg_dict = {}

        for centroid_id, points in self.centroid_dict.items():
            centroid_avg_dict[centroid_id] = self.calculate_average(points)

        return centroid_avg_dict
    
    def process_response(self, response):
        for id, Points in response.data.items():
            for point in Points.points:
                self.centroid_dict[id].append((point.x, point.y))
            
    

    

    # Send Parameters to Mapper
    async def send_parameters_to_mapper(self, mapper_id, parameters):
        try:
            # Send parameters to Mapper asynchronously
            response = await self.mapper_stubs[mapper_id].perform_map(parameters)
            self.append_to_dump("Calling rpc perform_map from Master - Mapper")
            print(f"Received response from Mapper {mapper_id}: {response}")
        except Exception as e:
            print(f"Error sending parameters to Mapper {mapper_id}: {e}")

    async def send_parameters_to_reducer_invoke(self, reducer_id, parameters):
        try:
            # Send parameters to Mapper asynchronously
            response = await self.reducer_stubs[reducer_id].invoke_reducer(parameters)
            self.append_to_dump("Calling rpc invoke_reducer from mapper - reducer")
            # print(f"Received response from Reducer {reducer_id}: {response}")
            self.process_response(response)
        except Exception as e:
            print(f"Error sending parameters to Reducer {reducer_id}: {e}")

    # Construct parameters for Mapper
    def construct_parameters_for_mapper(self, mapper_id, indices, centroids_list):

        centroid_messages = [
            MapReduce_pb2.Centroid(id=centroid[0], x=centroid[1], y=centroid[2])
            for centroid in centroids_list
        ]


        parameters = MapReduce_pb2.MapperParameters(
            mapper_id=mapper_id,
            start_index=indices[int(mapper_id[-1])-1][0],
            end_index=indices[int(mapper_id[-1])-1][1],
            centroids=centroid_messages,
            num_reducers=self.num_reducers
        )


        return parameters 

    # Creates Mapper Stubs
    def create_mapper_stubs(self):
        stubs = {}
        for mapper_id, mapper_port in self.mapper_port_dict.items():
            channel = grpc.aio.insecure_channel(f'localhost:{mapper_port}')
            stub = MapReduce_pb2_grpc.MapperServiceStub(channel)
            stubs[mapper_id] = stub
        return stubs
    
    # Creates Reducer Stubs
    def create_reducer_stubs(self):
        stubs = {}
        for reducer_id, reducer_port in self.reducer_port_dict.items():
            channel = grpc.aio.insecure_channel(f'localhost:{reducer_port}')
            stub = MapReduce_pb2_grpc.ReducerServiceStub(channel)
            stubs[reducer_id] = stub
        return stubs


    # Assign Indices to Mappers.
    def assign_indices(self):
        total_lines = 0
        file_path = os.path.join('Data', 'Input', 'input.txt')

        with open(file_path, 'r') as file:
            total_lines = sum(1 for line in file)

        lines_per_mapper = total_lines // self.num_mappers
        indices = []
        for i in range(self.num_mappers):
            start_index = i * lines_per_mapper
            end_index = (i + 1) * lines_per_mapper if i < self.num_mappers - 1 else total_lines
            end_index -= 1
            indices.append((start_index, end_index))

        return indices
    
    # Read Centroid Files 
    def read_centroids_file(self):
        centroids_file = "Data/centroids.txt"
        centroids = []
        with open(centroids_file, "r") as f:
            for index, line in enumerate(f):
                centroid = line.strip().split(",")
                centroid_id = f"centroid_id_{index}"  # Create ID with index prefix
                x = float(centroid[0])
                y = float(centroid[1])
                centroids.append((centroid_id, x, y))  # Add ID, x, and y to the list
        return centroids


    # Maps Mapper/Reducer Port Number.
    def assign_port(self, num_process, base_port, isMapper):
        port_dict = {}
        for i in range(0, num_process):
            if isMapper:
                port_dict[f"M{i+1}"] = base_port + i
            else:
                port_dict[f"R{i+1}"] = base_port + i
        return port_dict
    
    # Print Mapper/Reducer Port Mapping:
    def print_port_mapping(self):
        print("-------------------------------------------------------")
        print("Mapper/Reducer Port Mapping: ")
        print(self.mapper_port_dict)
        print(self.reducer_port_dict)



    # Generates random Centroids for K-Means Clustering
    def generate_random_centroids(self, file_path, num_centroids, dimension):
        centroids = []
        with open(file_path, 'w') as file:
            for _ in range(num_centroids):
                centroid = [random.uniform(-100, 100) for _ in range(dimension)]  # Adjust range as needed
                centroids.append(centroid)
                file.write(','.join(map(str, centroid)) + '\n')
        return centroids
    
    def append_to_dump(self, text):
        # Define the path to the file
        file_path = "Data/dump.txt"
        
        # Open the file in append mode and write the text
        with open(file_path, "a") as file:
            file.write(text + "\n")
    

    def add_to__directory_structure(self):
        # Create the main Data directory if it doesn't exist
        data_dir = 'Data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Create subdirectories for mappers
        mappers_dir = os.path.join(data_dir, 'Mappers')
        if not os.path.exists(mappers_dir):
            os.makedirs(mappers_dir)
        
        for i in range(1, self.num_mappers + 1):
            mapper_dir = os.path.join(mappers_dir, f'M{i}')
            if not os.path.exists(mapper_dir):
                os.makedirs(mapper_dir)

            # Create partition files for each mapper
            for j in range(1, self.num_reducers + 1):
                partition_file = os.path.join(mapper_dir, f'partition_{j}.txt')
                if not os.path.exists(partition_file):
                    open(partition_file, 'a').close()
        
        # Create files for reducers
        reducers_dir = os.path.join(data_dir, 'Reducers')
        if not os.path.exists(reducers_dir):
            os.makedirs(reducers_dir)
        
        for i in range(1, self.num_reducers + 1):
            reducer_file = os.path.join(reducers_dir, f'R{i}.txt')
            if not os.path.exists(reducer_file):
                open(reducer_file, 'a').close()  # Create an empty file


    
#############################################################################################################################

# Creates initial Data-Directory Structure
def create_directory_structure():
    # Create the main Data directory if it doesn't exist
    data_dir = 'Data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Create subdirectories within the Data directory
    subdirectories = ['Mappers', 'Reducers']
    for subdir in subdirectories:
        subdir_path = os.path.join(data_dir, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)
    
    # Create centroids.txt file
    centroids_file = os.path.join(data_dir, 'centroids.txt')
    if not os.path.exists(centroids_file):
        open(centroids_file, 'a').close()  # Create an empty file
    
    # Create dump.txt file
    dump_file = os.path.join(data_dir, 'dump.txt')
    if not os.path.exists(dump_file):
        open(dump_file, 'a').close()  # Create an empty file
    

async def main(num_mappers, num_reducers, num_centroids, num_iterations):

    # Initialize Master
    master = Master(num_mappers, num_reducers, num_centroids, num_iterations)

    # Run K-Means algorithm
    await master.run_kmeans()

if __name__ == "__main__":
    print("Staring Master Server!")
    num_mappers = int(input("Enter the number of Mappers: "))
    num_reducers = int(input("Enter the number of Reducers: "))
    num_centroids = int(input("Enter number of Centroids: "))
    num_iterations = int(input("Enter the number of Iterarions: "))

    # Creating directory structure
    create_directory_structure()

    # Input to execute K-Means Clustering
    start_input = input("Press Enter to start K-Means Clustering Algorithm")

    asyncio.run(main(num_mappers, num_reducers, num_centroids, num_iterations))



    


