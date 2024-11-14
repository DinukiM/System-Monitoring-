import itertools
import psutil
import random
import time

# List of servers with their CPU thresholds
servers = [
    {"name": "server1.company.com", "cpu_threshold": 85},
    {"name": "server2.company.com", "cpu_threshold": 85},
    {"name": "server3.company.com", "cpu_threshold": 85}
]

# Create a round-robin iterator
server_pool = itertools.cycle(servers)

# Function to simulate getting CPU load for a server
def get_server_cpu_load(server):
    # Simulate getting the server's CPU load (replace with actual load fetching in real use)
    return random.randint(50, 100)  # Simulating a load between 50-100%

# Function to distribute traffic based on server load
def distribute_request(request_id):
    for _ in range(len(servers)):
        # Pick the next server in round-robin order
        server = next(server_pool)
        
        # Check the server's CPU load
        server_cpu_load = get_server_cpu_load(server)
        print(f"Checking {server['name']} - CPU Load: {server_cpu_load}%")
        
        # If the server's CPU is below the threshold, assign the request
        if server_cpu_load < server["cpu_threshold"]:
            print(f"Request {request_id} is handled by {server['name']} (CPU Load: {server_cpu_load}%)\n")
            return
        
    print(f"All servers are at high load; request {request_id} is queued.\n")

# Simulate multiple incoming requests
for request_id in range(1, 11):  # Simulate 10 requests
    distribute_request(request_id)
    time.sleep(1)  # Wait a second before the next request for demonstration

