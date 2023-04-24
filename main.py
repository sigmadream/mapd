import time
from src.ta.ta_world import *
from src.ta.ta_task import *
from src.ta.ta_astar import AStar
from queue import Queue
from itertools import combinations
import src.mesa.mesa_server as mesa_server

GLOBAL_MAX_AGENT_TIME = 1500


def load_files():
    world = World("instances//kiva-10-500-5.map", GLOBAL_MAX_AGENT_TIME)
    tasks = TaskDict("instances//kiva-1.task", world)
    agent_tour_dict = TourDict("instances//solver.tsp", len(world.agents), tasks)
    return world, tasks, agent_tour_dict
    # return world, tasks


def copy_queue(queue):
    result = Queue()
    for entry in queue.queue:
        result.put(entry)
    return result


def find_agent_path(world, agent, time_step, release_time=0, find_step=0):
    a_star = AStar(world)
    other_agent_paths = []
    parking_locations = []

    for agent_id in world.agents:
        if agent_id != agent.id:
            other_agent_paths.append(world.agents[agent_id].path)
            parking_locations.append(world.agents[agent_id].parking_location)
    start_location = agent.path[time_step]
    goal_location = agent.next_endpoint

    new_path = a_star.search(
        time_step,
        start_location,
        goal_location,
        other_agent_paths,
        world,
        parking_locations,
        agent,
        release_time,
        find_step,
    )

    if not new_path:
        return False

    for state in new_path:
        world.agents[agent.id].path[state.time] = state.location

    world.agents[agent.id].time_at_goal = time_step + len(new_path) - 1
    return world.agents[agent.id].time_at_goal


def test_paths(world):
    return True


def main():
    world, tasks, tsp_seqs = load_files()
    make_span = 0
    last_sim_step = 0
    closed_list = {}
    time_start = time.perf_counter()
    for next_agent in world.agents:
        time_agent_start = time.perf_counter()
        max_len = 0
        priority_id = -1
        print("Determining execution times", end="")
        for agent_id in world.agents:
            if agent_id not in closed_list:
                print(".", end="")
                time_step = 0
                new_start_step = -1
                while True:
                    new_start_step += 1
                    time_step = new_start_step
                    seq = copy_queue(tsp_seqs[agent_id])
                    path_failed = False
                    for seq_task in range(seq.qsize()):
                        task = seq.get()
                        world.agents[agent_id].next_endpoint = task.pickup_endpoint
                        time_step = find_agent_path(
                            world,
                            world.agents[agent_id],
                            time_step,
                            task.release_time,
                            1,
                        )
                        if not time_step:
                            path_failed = True
                            break
                        world.agents[agent_id].next_endpoint = task.delivery_endpoint
                        time_step = find_agent_path(
                            world, world.agents[agent_id], time_step, 0, 2
                        )
                        if not time_step:
                            path_failed = True
                            break
                    if not path_failed:
                        break
                for t_step in range(GLOBAL_MAX_AGENT_TIME):
                    world.agents[agent_id].path[t_step] = world.agents[
                        agent_id
                    ].parking_location
                if priority_id == -1 or (time_step > max_len):
                    max_len = time_step
                    priority_id = agent_id
        print("")
        closed_list[priority_id] = True
        new_start_step = -1
        while True:
            new_start_step += 1
            time_step = new_start_step
            seq = copy_queue(tsp_seqs[priority_id])
            path_failed = False
            for next_task in range(tsp_seqs[priority_id].qsize()):
                task = seq.get()
                world.agents[priority_id].next_endpoint = task.pickup_endpoint
                time_step = find_agent_path(
                    world, world.agents[priority_id], time_step, task.release_time, 3
                )
                if not time_step:
                    path_failed = True
                    break
                world.agents[priority_id].next_endpoint = task.delivery_endpoint
                time_step = find_agent_path(
                    world, world.agents[priority_id], time_step, 0, 4
                )
                if not time_step:
                    path_failed = True
                    break
            if not path_failed:
                break
        make_span = max(make_span, world.agents[priority_id].time_at_goal)
        time_agent_stop = time.perf_counter()
        print(
            "Agent #"
            + str(priority_id)
            + " execution time: "
            + str(world.agents[priority_id].time_at_goal)
            + " (calc :"
            + str(round(((time_agent_stop - time_agent_start) / 60), 1))
            + " mins)"
        )
        world.agents[priority_id].next_endpoint = world.agents[
            priority_id
        ].parking_location
        find_agent_path(world, world.agents[priority_id], time_step)
        last_sim_step = max(last_sim_step, world.agents[priority_id].time_at_goal)
    time_stop = time.perf_counter()
    # mesa_server.simulate_scenario(world, tsp_seqs, last_sim_step)


if __name__ == "__main__":
    main()
