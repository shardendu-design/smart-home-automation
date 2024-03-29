# import subprocess

# # Global variables to hold references to subprocesses
# main_process = None
# app_process = None

# def run_main_and_app():
#     global main_process, app_process
#     main_process = subprocess.Popen(['python', 'main.py'])
#     app_process = subprocess.Popen(['python', 'app.py'])

# def terminate_subprocesses():
#     global main_process, app_process
#     if main_process and main_process.poll() is None:
#         main_process.terminate()
#     if app_process and app_process.poll() is None:
#         app_process.terminate()

# if __name__ == '__main__':
#     try:
#         # Run main.py and app.py together
#         run_main_and_app()

#         # Wait for Ctrl+C
#         while True:
#             pass

#     except KeyboardInterrupt:
#         print("\nCtrl+C pressed. Shutting down...")
#         terminate_subprocesses()

#     print("Launcher script completed.")

# import multiprocessing
# import os
# import signal
# import time

# def run_app(file_name):
#     os.system(f"python {file_name}")

# def stop_processes(processes):
#     for proc in processes:
#         if proc.is_alive():
#             os.kill(proc.pid, signal.SIGTERM)  # Send termination signal

# if __name__ == "__main__":
#     processes = []
#     files = ['main.py', 'app.py']

#     try:
#         for file in files:
#             proc = multiprocessing.Process(target=run_app, args=(file,))
#             proc.start()
#             processes.append(proc)

#         while True:  # Keep the script running
#             time.sleep(1)

#     except KeyboardInterrupt:
#         print("Stopping applications...")
#         stop_processes(processes)


import multiprocessing
import os
import signal
import time
import subprocess

def run_app(file_name):
    # Use subprocess.Popen instead of os.system
    proc = subprocess.Popen(["python", file_name])
    proc.wait()

def stop_processes(processes):
    for proc in processes:
        if proc.is_alive():
            # Terminate the process group
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

if __name__ == "__main__":
    # Set the start method for multiprocessing
    multiprocessing.set_start_method("spawn")

    processes = []
    files = ['main.py', 'app.py']

    try:
        for file in files:
            # Start each process in its own process group
            proc = multiprocessing.Process(target=run_app, args=(file,))
            proc.start()
            processes.append(proc)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping applications...")
        stop_processes(processes)
