import subprocess
import main
import app

# Run file1.py in a separate process
process1 = subprocess.Popen(['python', 'main.py'])

# Run file2.py in a separate process
process2 = subprocess.Popen(['python', 'app.py'])

# Wait for both processes to finish
process1.wait()
process2.wait()

print("Both file executions completed")
