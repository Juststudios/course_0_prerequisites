import redis
import time

def run_redis_demo():
    # Connecting to Redis. 
    # decode_responses=True automatically decodes byte responses to strings.
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    try:
        # Ping the server to ensure connection
        if r.ping():
            print("Successfully connected to Redis!")
    except redis.exceptions.ConnectionError:
        print("Could not connect to Redis. Is it running?")
        return

    # Basic SET and GET
    r.set('session:123', 'active')
    print("Session status:", r.get('session:123'))
    
    # TTL (Time to Live) Example
    r.setex('temp_key', 2, 'I will disappear in 2 seconds')
    print("temp_key value:", r.get('temp_key'))
    print("Waiting 3 seconds...")
    time.sleep(3)
    print("temp_key value now:", r.get('temp_key')) # Should be None
    
    # Using Lists as a Queue
    r.delete('task_queue') # Clear queue
    r.rpush('task_queue', 'task_1', 'task_2', 'task_3')
    print("Queue length:", r.llen('task_queue'))
    
    # Popping from Queue
    task = r.lpop('task_queue')
    print("Popped task:", task)

if __name__ == '__main__':
    run_redis_demo()
