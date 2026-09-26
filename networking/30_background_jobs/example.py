import redis
import json
import time
import threading

def worker_process(worker_id):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    print(f"Worker {worker_id} started, waiting for jobs...")
    while True:
        # Blocks until an item is available in 'job_queue'
        # Returns a tuple (queue_name, popped_value)
        queue, job_data = r.brpop('job_queue', timeout=5)
        if not job_data:
            break # Exit after 5 seconds of inactivity
            
        job = json.loads(job_data)
        print(f"[Worker {worker_id}] Processing: {job['task']} for user {job['user_id']}")
        time.sleep(2) # Simulate heavy work
        print(f"[Worker {worker_id}] Finished: {job['task']}")

def producer_process():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    jobs = [
        {"task": "generate_report", "user_id": 101},
        {"task": "send_email", "user_id": 102},
        {"task": "process_image", "user_id": 103}
    ]
    
    for job in jobs:
        print(f"[Producer] Enqueueing job: {job['task']}")
        r.lpush('job_queue', json.dumps(job))
        time.sleep(0.5)

if __name__ == '__main__':
    # Start worker in a separate thread for demonstration
    worker_thread = threading.Thread(target=worker_process, args=(1,))
    worker_thread.start()
    
    # Run producer
    producer_process()
    
    worker_thread.join()
