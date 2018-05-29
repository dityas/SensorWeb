import ipaddress
import argparse
import subprocess
import time

# GLOBAL DECLARATION.
GRAFANA_SERVER_IP=ipaddress.IPv4Address("192.168.1.2")

class Administrator:

    """
        Administrator object. Contains default methods for setting date and copying files to the cluster. Can also execute custom commands.
    """

    def __init__(self,user,ip_addresses):
        self.user=str(user)
        self.hosts=ip_addresses

    def update_time(self):
        """
            Updates the time on all BBs using debians 'date --set ' command.
            Returns dict of results in form {"output":message,"error":message}
        """
        now=str(time.ctime())
        command=["date","--set","'"+now+"'"]
        return self.execute(command)

    def check_uptime(self):
        """
            Runs `uptime` on all hosts in the cluster. Good for checking connectivity.
        """
        command=['uptime']
        return self.execute(command)

    def run_custom(self,command):
        command=command.split(" ")
        return self.execute(command)

    def __run_ssh_exec(self,host,command):
        """
            Run command using ssh.
        """

        out,err=subprocess.Popen(["ssh","-o","ConnectTimeout=5",self.user+"@"+str(host)]+command,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        res = {"ip":str(host),"output":out,"error":err}
        print(res)
        return res

    def __run_scp(self,lpath,rpath,host):
        """
            Copy files from lpath to rpath using scp
        """

        out,err=subprocess.Popen(["scp",lpath,f"{self.user}@{host}:{rpath}"]).communicate()
        return {"ip":str(host),"output":out,"error":err}

    def rcopy(self,lpath,rpath):
        result=[]

        for host in self.hosts:
            result.append(self.__run_scp(lpath,rpath,host))

        return result

    def execute(self,command):
        result=[]

        for host in self.hosts:
            print(f"Running on {host}")
            result.append(self.__run_ssh_exec(host,command))

        return result

def print_result(results):
    for result in results:
        print(result)

if __name__=="__main__":

    parser=argparse.ArgumentParser(description="""
    This script will execute the given command on all the nodes in a cluster.
    !!! INFO !!! This script requires key based authentication on all nodes in the cluster.
    If this is not done, first set it up.
    Create key pair using ssh-keygen
    Then install the public key on every node in the cluster using ssh-copy-id.
    """)

    parser.add_argument("-c","--command",action="store",type=str,help="Command to execute on all the machines in the cluster.")
    parser.add_argument("-s","--start",action="store",type=str,help="Starting IP of the cluster.")
    parser.add_argument("-n","--num_hosts",action="store",type=int,help="Number of hosts in the cluster.")
    parser.add_argument("-l","--local_path",action="store",type=str,help="Local path of the file to be copied.")
    parser.add_argument("-r","--remote_path",action="store",type=str,help="Remote path for file to be copied.")
    args=parser.parse_args()

    addresses=[]
    start=ipaddress.IPv4Address(args.start)
    for i in range(args.num_hosts):
        addresses.append(start+i)
    addresses.append(GRAFANA_SERVER_IP)

    admin=Administrator(user="root",ip_addresses=addresses)

    command=args.command
    if command == "beacon" or command=="uptime":
        result=admin.check_uptime()
        print_result(result)

    elif command=="set_date":
        result=admin.update_time()
        print_result(result)

    elif command=="copy":
        assert len(args.local_path)>0
        assert len(args.remote_path)>0
        result=admin.rcopy(args.local_path,args.remote_path)
        print_result(result)

    else:
        result=admin.run_custom(command)
        print_result(result)

    print("Finished executing.")
