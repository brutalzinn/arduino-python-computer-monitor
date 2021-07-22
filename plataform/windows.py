class Windows:
    def __init__(self, maxmem):
        self.maxmem = maxmem
        self.Li = 16
        self.Lii = 0
    def execute(self,mode):
        mem = psutil.virtual_memory()
        cpuTemps = psutil.sensors_temperatures()['coretemp']
        cpuPercent = psutil.cpu_percent()
        maxMemStatus = '1'
        memPercent = mem.percent
        if memPercent > self.maxMem:
            maxMemStatus = '1'
        else:
            maxMemStatus = '0'
        memTotal = mem.total /1024/1024/1024
        if hasattr(mem, 'active'):
            memUsed = mem.active /1024/1024/1024
        else:
            memUsed = mem.used /1024/1024/1024
        gpu = GPUtil.getGPUs()[0]
        gpu_util = int(gpu.load * 100)
        gpu_temp = int(gpu.temperature)
        cpuTemp = 0
        for item in cpuTemps:
            if 'Package' in item.label:
                cpuTemp = item.current
        memInfo = f'MEM: {memPercent}% {round(memUsed,1)}GB de {round(memTotal,1)}GB'
        gpuInfo = f'GPU: {gpu_util}% {gpu_temp}C'
        procInfo = f'CPU: {cpuPercent}% {cpuTemp}C'
        def modeWriter():
            global mode
            def scrollText(text):
                result = None
                StrProcess = "                " + text + "                "
                result = StrProcess[self.Lii: self.Li]
                self.Li = self.Li + 1
                self.Lii = self.Lii + 1
                if self.Li > len(StrProcess):
                    self.Li = 16
                    self.Lii = 0
                return result
            writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
            if self.mode == -1:
                writerResult = {"rowone":f"{memInfo}","rowtwo":f"{procInfo}"}
            if self.mode == 1:
                writerResult = {"rowone":f"{scrollText(memInfo)}","rowtwo":f"{procInfo}"}
            if self.mode == 3:
                writerResult = {"rowone":f"{gpuInfo}","rowtwo":f"{procInfo}"}
            writerResult['maxmem'] = maxMemStatus
            return writerResult