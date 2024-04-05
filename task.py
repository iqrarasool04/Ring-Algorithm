class Process:
    def __init__(self, id):
        self.id = id
        self.active = True

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

class RingAlgorithm:
    def __init__(self, num_processes):
        self.processes = [Process(i + 1) for i in range(num_processes)]
        self.coordinator = None

    def start_election(self, initiating_process_id):
        initiator = self.processes[initiating_process_id - 1]
        print(f"Process {initiating_process_id} initiates the election.")

        has_elected = False
        for i in range(1, len(self.processes) + 1):
            next_process_id = (initiating_process_id + i) % len(self.processes)
            next_process = self.processes[next_process_id]
            if next_process.is_active():
                print(f"Process {next_process.get_id()} is asked if it is alive.")
                if next_process.get_id() == initiating_process_id:
                    has_elected = True
                    break

        if has_elected:
            self.coordinator = initiator
            print(f"Process {self.coordinator.get_id()} becomes the coordinator.")
        else:
            print("No response from any higher priority process. Election failed.")

    def process_fails(self, failed_process_id):
        failed_process = self.processes[failed_process_id - 1]
        failed_process.set_active(False)
        print(f"Process {failed_process_id} fails.")

        if self.coordinator is not None and self.coordinator.get_id() == failed_process_id:
            self.coordinator = None
            print("Coordinator failed. Starting new election...")
            self.start_election(1)

if __name__ == "__main__":
    num_processes = 7
    algorithm = RingAlgorithm(num_processes)

    print("Initial state:")
    for p in algorithm.processes:
        print(f"Process {p.get_id()}: Active: {1 if p.is_active() else 0}")

    algorithm.start_election(3)

    print("\nAfter election:")
    for p in algorithm.processes:
        print(f"Process {p.get_id()}: Active: {1 if p.is_active() else 0}")

    algorithm.process_fails(algorithm.coordinator.get_id())

    print("\nAfter coordinator failure:")
    for p in algorithm.processes:
        print(f"Process {p.get_id()}: Active: {1 if p.is_active() else 0}")

    algorithm.start_election(1)

    print("\nAfter new election:")
    for p in algorithm.processes:
        print(f"Process {p.get_id()}: Active: {1 if p.is_active() else 0}")
