# Agent State Tracker
agent_id = "agent-v1-search"          # str
cycle_iterations = 5                   # int
confidence_score = 0.875              # float
is_running = True                     # bool
error_message = None                  # NoneType

# Check if the agent state is valid and operational
print("--- Initial Agent State ---")
print(f"Agent: {agent_id} (Type: {type(agent_id).__name__})")
print(f"Iterations: {cycle_iterations} (Type: {type(cycle_iterations).__name__})")
print(f"Confidence: {confidence_score * 100:.1f}% (Type: {type(confidence_score).__name__})")
print(f"Is Running: {is_running} (Type: {type(is_running).__name__})")
print(f"Error: {error_message} (Type: {type(error_message).__name__})")

# Type conversion: parsing external sensor/API strings
raw_timeout_string = "30"
timeout_seconds = int(raw_timeout_string)
total_max_time = timeout_seconds * cycle_iterations

print("\n--- Processed Metrics ---")
print(f"Calculated Max Runtime: {total_max_time} seconds")
print(f"Is error present? {bool(error_message)} (evaluated via truthiness)")