from queue import Queue


class Task:
    def __init__(
        self, task_id, release_time, endpoint_pickup, endpoint_delivery, world
    ):
        self.id = task_id
        self.assigned_agent = None
        self.release_time = release_time
        self.pickup_endpoint = world.endpoints[endpoint_pickup]
        self.delivery_endpoint = world.endpoints[endpoint_delivery]


class TaskDict(dict):
    def __init__(self, task_file_path, world):
        self.load_file(task_file_path, world)

    def load_file(self, task_file_path, world):
        file = open(task_file_path, "r")
        if not file.mode == "r":
            print("Could not open " + task_file_path)
        else:
            print("Loading task file")
            task_data = file.readlines()
            task_id = 0
            for line in task_data:
                if line.find("\t") < 1:
                    data = line.split(" ")
                else:
                    data = line.split("\t")
                release_time = int(data[0])
                endpoint_pickup = int(data[1])
                endpoint_delivery = int(data[2])
                self[task_id] = Task(
                    task_id, release_time, endpoint_pickup, endpoint_delivery, world
                )
                task_id += 1


class TourDict(dict):
    def __init__(self, tour_file_path, agent_count, tasks_dict):
        self.load_file(tour_file_path, agent_count, tasks_dict)

    def load_file(self, tour_file_path, agent_count, tasks_dict):
        file = open(tour_file_path, "r")
        if not file.mode == "r":
            print("Could not open " + tour_file_path)
        else:
            print("Loading tour file")
            tour_data = file.readlines()
            tour_section = False
            agent_sequence = None
            agent_number = 1
            for line in tour_data:
                if "-1" in line:
                    if agent_sequence.qsize():
                        self[agent_number] = agent_sequence
                        tour_section = False
                if tour_section:
                    line_val = int(line)
                    if line_val <= agent_count:
                        if agent_sequence.qsize():
                            self[agent_number] = agent_sequence
                            agent_sequence = Queue()
                            agent_number = line_val
                    else:
                        task_id = line_val - agent_count - 1
                        agent_sequence.put(tasks_dict[task_id])
                        tasks_dict[task_id].seq_id = agent_number
                if "TOUR_SECTION" in line:
                    tour_section = True
                    agent_sequence = Queue()
