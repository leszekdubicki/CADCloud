# http://stackoverflow.com/questions/2940858/kill-process-by-name-in-python
import psutil
 
PROCNAME = "SLDWORKS.exe"
#PROCNAME = "notepad.exe"
 
def kill_chromedriver():
    for proc in psutil.process_iter():
        #print proc.name() == PROCNAME
        print proc.name()
        if str(proc.name()) == PROCNAME:
           print "kill kill"
           proc.kill()

if __name__ == "__main__":
    kill_chromedriver()
