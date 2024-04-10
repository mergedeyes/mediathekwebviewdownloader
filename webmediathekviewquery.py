try:
    from prompt_toolkit import prompt
    import requests
    import json
    import time
    import re
    import os
except ImportError:
    print("Module(s) not available. Please install the required module(s) using 'python3 -m pip install <module>'.")

def get_user_input():
    title = prompt("Title: ")
    channel = prompt("Channel: ")
    return title, channel

# Function to perform the API request and save the response
def query_api(title, channel):
    query = {
        "queries": [
            {
                "fields": ["title", "topic"],
                "query": title
            },
            {
                "fields": ["channel"],
                "query": channel
            }
        ],
        "sortBy": "timestamp",
        "sortOrder": "desc",
        "future": False,
        "offset": 0,
        "size": 50,
        "duration_min": 10,
        "duration_max": 1000000
    }

    # Convert the query to a JSON string
    query_string = json.dumps(query)

    # Set the appropriate header
    headers = {'Content-Type': 'text/plain'}

    # Make the POST request with the stringified JSON as plain text
    response = requests.post('https://mediathekviewweb.de/api/query', data=query_string, headers=headers)
    return response.json()

def choose_episode(data):
    results = data["result"]["results"]
    filtered_results = []

    # Regular expression to match "Episode" followed by a number
    episode_pattern = re.compile(r'Episode \d+', re.IGNORECASE)
    
    for result in results:
        title = result.get("title", "")
        if not episode_pattern.match(title):
            filtered_results.append(result)
            
    for index, item in enumerate(filtered_results, start=1):
        print(f"{index}. {item['title']}")
    
    choice = int(prompt("Select an episode by number: ")) - 1
    return results[choice]

def get_file_size(url):
    if url:  # Ensure the URL is not empty
        response = requests.head(url)  # Make a HEAD request to get headers
        size = response.headers.get('content-length', 0)  # Fetch content-length header
        return int(size)
    return 0

def choose_quality(episode):
    print("Available video qualities:")
    qualities = ["url_video", "url_video_low", "url_video_hd"]
    names = ["Standard", "Low", "HD"]
    for index, quality in enumerate(qualities, start=1):
        if episode[quality]:
            size_bytes = get_file_size(episode[quality])
            size_readable = human_readable_size(size_bytes)
            print(f"{index}. {names[index-1]} - {size_readable}")
    
    choice = int(prompt("Select a quality by number: ")) - 1
    return episode[qualities[choice]]

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0 or unit == 'TB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"
    
def download_video(url, default_filename):
    default_filename = default_filename.replace(":", " -")
    # Sanitize default_filename to remove characters that are not allowed in file names
    sanitized_filename = re.sub(r'[\\/*?:"<>|]', '_', default_filename)
    
    filename = prompt(f"Enter filename (without extension, default: {sanitized_filename}. For default press enter): ") or sanitized_filename
    extension = url.split('.')[-1]
    
    full_path = f"{filename}.{extension}"
    if os.path.exists(full_path):
        overwrite = prompt(f"File '{full_path}' already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            print("Download cancelled.")
            return
        
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:  # no content length header
        print("Downloading... (size unknown)")
        with open(f"{filename}.{extension}", "wb") as file:
            file.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        start_time = time.time()
        last_update_time = start_time

        with open(f"{filename}.{extension}", "wb") as file:
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                file.write(data)
                elapsed = time.time() - start_time
                if time.time() - last_update_time > 0.7:  # Update every X seconds
                    done = int(50 * dl / total_length)
                    speed = dl / elapsed
                    eta = (total_length - dl) / speed if speed > 0 else 0
                    print(f"\r[{'=' * done}{' ' * (50-done)}] {human_readable_size(dl)}/{human_readable_size(total_length)} - {human_readable_size(speed)}/s ETA: {eta:.2f} s", end='')
                    last_update_time = time.time()
        print(f"\nDownloaded {human_readable_size(total_length)} in {elapsed:.2f} seconds.")
    print(f"Download complete. File saved as '{filename}.{extension}'.")

def main():
    try:
        title, channel = get_user_input()
        response_data = query_api(title, channel)
        episode = choose_episode(response_data)
        video_url = choose_quality(episode)
        default_filename = episode['title']
        download_video(video_url, default_filename)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
