import multiprocessing
import os
import platform
import socket
import ctypes
import subprocess
import psutil, shutil
import string
import wmi
from datetime import timedelta
from dataclasses import dataclass

@dataclass
class Report():

    def get_uptime(self):
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

    def get_cpus(self):
        """
        Get the number of CPUs and model/type
        """
        data = {}
        try:
            if platform.system() == 'Windows':
                output = subprocess.check_output(
                    'wmic cpu get name /format:csv', shell=True)
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

    def get_users(self):
        """
        Get the current logged in users
        """
        try:
            pipe = os.popen("who |" + "awk '{print $1, $2, $6}'")
            data = pipe.read().strip().split("\n")
            pipe.close()

            if data == [""]:
                data = None
            else:
                data = [i.split(None, 3) for i in data]

        except Exception as err:
            data = str(err)

        return data
    
    def get_ipaddress(self):
        """
        Get the IP Address and other information for all network interfaces
        """
        return socket.gethostbyname(socket.gethostname())
        #return socket.gethostbyname_ex(socket.gethostname())[-1]

    def get_traffic(self, request):
        """
        Get the traffic for the specified interface
        """
        data = {}
        try:
            if platform.system() == 'Windows':
                output = subprocess.check_output('netstat -e', shell=True)
                lines = output.decode().split('\r\n')
                for line in lines:
                    if request in line:
                        data['traffic_in'] = int(line.split()[1])
                        data['traffic_out'] = int(line.split()[4])
                        break
            else:  # Assuming Linux
                output = subprocess.check_output('cat /proc/net/dev', shell=True)
                lines = output.decode().split('\n')
                for line in lines:
                    if request in line:
                        data['traffic_in'] = int(line.split(':')[1].split()[0])
                        data['traffic_out'] = int(line.split(':')[1].split()[8])
                        break
        except subprocess.CalledProcessError as err:
            data = str(err)

        return data

    def get_platform(self):
        """
        Get the OS name, hostname and kernel
        """
        return platform.system()

    def get_disk(self):
        """
        Get disk usage
        """
        try:
            if platform.system() == 'Windows':
                drives = []
                for letter in string.ascii_uppercase:
                    if os.path.exists(letter + ":\\"):
                        drives.append(letter + ":\\")

                data = []
                for drive in drives:
                    total, used, free = shutil.disk_usage(drive)
                    percent = (used / total) * 100
                    disk_usage = {"drive": drive, "total": total,
                                "used": used, "free": free, "percent": percent}
                    data.append(disk_usage)
            else:
                pipe = os.popen(
                    "df -Ph | "
                    + "grep -v Filesystem | "
                    + "awk '{print $1, $2, $3, $4, $5, $6}'"
                )
                data = pipe.read().strip().split("\n")
                pipe.close()

                data = [i.split(None, 6) for i in data]

        except Exception as err:
            data = str(err)

        return data

    def get_disk_rw(self):
        """
        Get the disk reads and writes
        """
        try:
            if platform.system() == 'Windows':
                c = wmi.WMI()
                partitions = []
                for disk in c.Win32_LogicalDisk():
                    partitions.append({
                        'device': disk.DeviceID,
                        'mountpoint': disk.Caption,
                        'filesystem': disk.FileSystem,
                        'total_size': int(disk.Size),
                        'used': int(disk.Size) - int(disk.FreeSpace),
                        'free': int(disk.FreeSpace),
                        'percent_used': int(disk.Size - disk.FreeSpace) / int(disk.Size) * 100
                    })
            else:
                pipe = os.popen(
                    "cat /proc/partitions | grep -v 'major' | awk '{print $4}'")
                data = pipe.read().strip().split("\n")
                pipe.close()

                rws = []
                for i in data:
                    if i.isalpha():
                        pipe = os.popen(
                            "cat /proc/diskstats | grep -w '" +
                            i + "'|awk '{print $4, $8}'"
                        )
                        rw = pipe.read().strip().split()
                        pipe.close()

                        rws.append([i, rw[0], rw[1]])

                if not rws:
                    pipe = os.popen(
                        "cat /proc/diskstats | grep -w '" +
                        data[0] + "'|awk '{print $4, $8}'"
                    )
                    rw = pipe.read().strip().split()
                    pipe.close()

                    rws.append([data[0], rw[0], rw[1]])

                data = rws

        except Exception as err:
            data = str(err)

        return data

    def get_mem(self):
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

    def get_cpu_usage(self):
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

    def get_load(self):
        """
        Get load average
        """
        data = ""
        try:
            if platform.system() == 'Windows':
                data = psutil.cpu_percent()
            else:  # Assuming Linux
                with open('/proc/loadavg', 'r') as f:
                    data = f.read().strip().split()[0]
        except Exception as err:
            data = str(err)

        return data

    def get_netstat(self):
        """
        Get ports and applications
        """
        try:
            pipe = os.popen(
                "ss -tnp | grep ESTAB | awk '{print $4, $5}'| sed 's/::ffff://g' | awk -F: '{print $1, $2}' "
                "| awk 'NF > 0' | sort -n | uniq -c"
            )
            data = pipe.read().strip().split("\n")
            pipe.close()

            data = [i.split(None, 4) for i in data]

        except Exception as err:
            data = str(err)

        return data
