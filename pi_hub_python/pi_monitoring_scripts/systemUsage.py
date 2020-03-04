from pub_data import publish
import psutil

cpu = psutil.cpu_percent()
print(cpu)

ram = psutil.virtual_memory().percent
print(ram)

disk = psutil.disk_usage('/').percent
print(disk)

data = {
    "cpu" : cpu,
    "ram" : ram,
    "disk": disk
    }

publish("systemUsage", data)
