import psutil
try:
    import GPUtil
except ImportError:
    GPUtil = None

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    gpu = 0.0
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0].load * 100
    return {"cpu": cpu, "ram": ram, "gpu": gpu}
