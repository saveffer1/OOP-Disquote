import os
import platform
import socket
import ctypes
import subprocess
import psutil
from dataclasses import dataclass

# cloned linux functions from pydash and fastdash
    # https://github.com/dgilland/pydash
    # https://github.com/psiace-archive/fastdash
    
# tested on windows 11
# untested on linux
@dataclass
class Report():

    def get_uptime(self) -> str:
        """
        Get uptime
        """
        data = ""
        try:
            if platform.system() == 'Windows':
                lib = ctypes.windll.kernel32
                t = lib.GetTickCount64()
                t = int(str(t)[:-3])
                mins, sec = divmod(t, 60)
                hour, mins = divmod(mins, 60)
                days, hour = divmod(hour, 24)
                data = (f"{days} days, {hour:02}:{mins:02}:{sec:02}")
            else:  # Assuming Linux
                data = os.popen('uptime -p').read()[:-1]
        except Exception as err:
            data = str(err)
        finally:
            return data

    def get_cpus(self) -> dict:
        """
        Get the number of CPUs and model/type
        """
        data = {}
        try:
            if platform.system() == 'Windows':
                output = subprocess.check_output('wmic cpu get name /format:csv', shell=True)
                lines = output.decode().strip().split('\r\r\n')
                # Count the number of rows in the CSV file
                data['type'] = lines[1].split(',')[1].strip()
                data['cpus'] = os.cpu_count()
            else:  # Assuming Linux
                pipe = subprocess.Popen(
                    ['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)
                output = subprocess.check_output(
                    ['grep', 'model name'], stdin=pipe.stdout)
                pipe.stdout.close()
                lines = output.decode().strip().split('\n')
                data['type'] = lines[0].split(':')[-1].strip()
                data['cpus'] = os.cpu_count()
        except subprocess.CalledProcessError as err:
            data = str(err)

        return data

    
    def get_ipaddress(self) -> str:
        """
        Get the IP Address and other information for all network interfaces
        """
        return socket.gethostbyname(socket.gethostname())
        #return socket.gethostbyname_ex(socket.gethostname())[-1]

    def get_platform(self) -> str:
        """
        Get the OS name, hostname and kernel
        """
        return platform.system()


    def get_mem(self) -> dict:
        """
        Get memory usage
        """
        data = dict()
        try:
            if platform.system() == 'Windows':
                mem = psutil.virtual_memory()
                allmem = mem.total
                freemem = round(mem.available / (1024**3), 2)
                usage = round(mem.used / (1024**3), 2)
                percent = mem.percent
                mem_usage = {
                    "usage": usage,
                    "free": freemem,
                    "percent": percent,
                }
                
                data = mem_usage
            else:
                pipe = os.popen("free -tm | " + "grep 'Mem' | " +
                                "awk '{print $2,$4,$6,$7}'")
                data = pipe.read().strip().split()
                pipe.close()

                allmem = int(data[0])
                freemem = int(data[1])
                buffers = int(data[2])
                cachedmem = int(data[3])

                # Memory in buffers + cached is actually available, so we count it
                # as free. See http://www.linuxatemyram.com/ for details
                freemem += round((buffers + cachedmem) / (1024**3), 2)

                percent = 100 - ((freemem * 100) / allmem)
                usage = round((allmem - freemem) / (1024**3), 2)

                mem_usage = {
                    "usage": usage,
                    "buffers": buffers,
                    "cached": cachedmem,
                    "free": freemem,
                    "percent": percent,
                }

                data = mem_usage

        except Exception as err:
            data = str(err)

        return data

    def get_cpu_usage(self) -> dict:
        """
        Get the CPU usage and running processes
        """
        data = {}
        try:
            if platform.system() == 'Windows':
                process_list = []
                for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                    try:
                        if process.info['name'] == 'systemd' or process.info['cpu_percent'] == 0.0:
                            continue
                        
                        if process.info['pid'] != 0:
                            process_list.append({
                                'pid': process.info['pid'],
                                'name': process.info['name'],
                                'cpu_percent': process.info['cpu_percent']
                            })
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                process_list = sorted(process_list, key=lambda x: x['cpu_percent'], reverse=True)

                # Get the total CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                num_cpus = psutil.cpu_count(logical=True)

                cpu_used = {
                    'free': 100 - cpu_percent,
                    'used': cpu_percent,
                    'all': process_list
                }

                data = cpu_used
            else:  # Assuming Linux
                pipe = os.popen("ps aux --sort -%cpu,-rss")
                data = pipe.read().strip().split("\n")
                pipe.close()

                usage = [i.split(None, 10) for i in data]
                del usage[0]

                
                total_usage = []

                for element in usage:
                    usage_cpu = element[2]
                    if usage_cpu == "-----": # Handle this special case in Linux implementation
                        continue
                    total_usage.append(float(usage_cpu))

                total_usage = sum(total_usage)

                total_free = (100 * int(self.get_cpus()["cpus"])) - total_usage

                cpu_used = {"free": total_free,
                            "used": total_usage, "all": usage}

            data = cpu_used

        except Exception as err:
            data = str(err)

        return data

