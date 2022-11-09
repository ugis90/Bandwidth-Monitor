#record network bandwidth for 21 seconds
import matplotlib.pyplot as plt
import numpy
import re
import time
import psutil

last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

log_file = open("Bandwidth_Monitor.log", "w")

for i in range(0, 22):
    time.sleep(1)

    bytes_received = psutil.net_io_counters().bytes_recv
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_received + bytes_sent

    new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    mb_new_received = new_received / 1024
    mb_new_sent = new_sent / 1024
    mb_new_total = new_total / 1024

    print(f"{mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total")

    log_file.write(f"{mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total\n")

    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

log_file.close()


#read log data and generate a graph
pattern = r'\d+.\d+'
log_file = open("Bandwidth_Monitor.log", "r")

data = []
for line in log_file:
    data.append(re.findall(pattern, line))

data_total = [float(x[2]) for x in data]
data_downloaded = [float(x[0]) for x in data]
data_uploaded = [float(x[1]) for x in data]

plt.plot(range(0,22), data_total, '-b')
plt.plot(range(0,22), data_downloaded, '-r')
plt.plot(range(0,22), data_uploaded, '-g')
plt.legend(['Total', 'Downloaded', 'Uploaded'])
plt.title('Bandwidth in MBps')

plt.ylabel('MB')
plt.yticks(numpy.arange(0, max(data_total), 5))
plt.ylim(0, max(data_total))

plt.xlabel('Time (seconds)')
plt.xticks(numpy.arange(0, 22, 1))

plt.grid()

plt.show()