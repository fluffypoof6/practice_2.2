import psutil
import os
import time

def bar(p): return '█' * int(p/4) + '░' * (25 - int(p/4))

try:
    disk = 'C:\\' if os.name == 'nt' else '/'
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*40)
        print("Системс моникторикс endfield ")
        print("="*40)
        
        cpu = psutil.cpu_percent()
        print(f"CPU: {cpu:5.1f}%\n{bar(cpu)}")
        
        ram = psutil.virtual_memory().percent
        print(f"RAM: {ram:5.1f}%\n{bar(ram)}")
        
        disk_usage = psutil.disk_usage(disk).percent
        print(f"DISK: {disk_usage:5.1f}%\n{bar(disk_usage)}")
        
        time.sleep(2)
except KeyboardInterrupt:
    print("\nБб")