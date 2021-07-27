import subprocess

def obtener_procesos():
    p1 = subprocess.Popen(" sudo ps aux | awk '{print($2,$11,$3,$4)}'", stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (procesos, err) = p1.communicate()
    procesos = procesos.split('\n')
    return procesos

def kill_proc(pid):
    cmd="sudo kill -9 " + str(pid)
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    (procesos, err) = p1.communicate()
