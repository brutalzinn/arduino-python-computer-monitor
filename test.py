import psutil
import GPUtil

gpu = GPUtil.getGPUs()[0]
gpu_util = int(gpu.load * 100)
gpu_temp = int(gpu.temperature)
#print(gpu_temp)
cpuTemps = psutil.sensors_temperatures()['coretemp']
for item in cpuTemps:
    if 'Package' in item.label:
        print(item.current)