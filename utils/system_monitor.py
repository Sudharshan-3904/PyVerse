import psutil
import platform
try:
    import GPUtil
except ImportError:
    GPUtil = None

# Cache WMI instance
_wmi_instance = None

def get_system_stats():
    global _wmi_instance
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    gpu = 0.0
    gpu_temp = 0.0
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0].load * 100
            gpu_temp = gpus[0].temperature

    cpu_temp = 0.0
    if platform.system() == "Windows":
        try:
            if _wmi_instance is None:
                import wmi
                _wmi_instance = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            temperature_infos = _wmi_instance.Sensor()
            for sensor in temperature_infos:
                if sensor.SensorType == 'Temperature' and 'CPU Core' in sensor.Name:
                    cpu_temp = sensor.Value
                    break
        except Exception:
            pass
    else:
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps and len(temps['coretemp']) > 0:
                cpu_temp = temps['coretemp'][0].current
        except Exception:
            pass

    return {
        "cpu": cpu,
        "ram": ram,
        "gpu": gpu,
        "cpu_temp": cpu_temp,
        "gpu_temp": gpu_temp
    }
