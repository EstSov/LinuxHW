import sys
import os
import time
import psutil


log_file = './file.log'
workers = []
G_PID=os.getpid()

def main():
    if len(sys.argv) < 7:
        print('script.py -m message, -p 2 -n 2')
        exit()
    message = sys.argv[sys.argv.index('-m')+1]
    processes = int(sys.argv[sys.argv.index('-p')+1])
    iterations = int(sys.argv[sys.argv.index('-n')+1])

    for i in range(processes):
        print(f'P {os.getpid()}: Forking {i}')
        worker_pid = os.fork()
        if not worker_pid:
            now = time.time()
            for j in range(iterations*(i+1)):
                with open(log_file, mode='a+') as file:
                    file.write(f'C {n}: {message} {j+1}\n')
                time.sleep(1)
                if not psutil.pid_exists(G_PID):
                    os.abort()
            os.abort()
        workers.append(worker_pid)

    for pid in workers:
        print(f'P: Waiting for {pid}')
        done = os.waitpid(pid, 0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        for i in workers:
            os.kill(i, 0)
