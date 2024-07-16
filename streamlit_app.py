import paramiko, subprocess, platform, getpass, os, asyncio

user = input("User: ")
passwd = getpass.getpass()
port = "22"
network="172.16."


def show_menu():
    #os.system('cls')
    print("###############################")
    print("PYTHON AUTOMATE HAPROXY MANAGER")
    print("1. Listar todos os frontend")
    print("2. Listar backend")
    print("3. Ativar backend")
    print("4. Desativar backend")

    print("9. Sair")

def validate(val):
    if run_command:
        print("Comando executado com sucesso!")
    else:
        print("Um erro foi encontrado!")
    return val


def listall_frontend():
    command = "hostname ; echo 'show servers state' | socat /var/run/haproxy.sock stdio | grep "+network+" | awk '{print $2}'"
    return command


def list_backend():
    frontend = input("Digite o nome do frontend: ")
    print(frontend)

    if frontend:
        command = "hostname ; echo 'show servers state "+frontend+"' | socat /var/run/haproxy.sock stdio | grep "+frontend+" | awk '{print $4}'"
    else:
        command = "null"

    return command
    

def disable_backend():
    frontend = input("Digite o frontend: ")
    backend = input("Digite o backend: ")
    command = "echo 'disable server "+frontend+"/"+backend+"' | socat /var/run/haproxy.sock stdio"
    return command


def enable_backend():
    frontend = input("Digite o frontend: ")
    backend = input("Digite o backend: ")
    command = "echo 'enable server "+frontend+"/"+backend+"' | socat /var/run/haproxy.sock stdio"
    return command


def run_command(command, user, passwd, port):
    if command:
        index = command.find("rm -rf")

        if index != -1:
            print("Wrong command!")
            exit(0)

        os_name = platform.system()
        if os_name == "Windows":
            paramPing = "-n"
        elif os_name == "Linux":
            paramPing = "-c"
        elif os_name == "MacOS":
            paramPing = "-c"
        else:
            print("The operating system is not supported.")
            exit(0)

        # print(os_name)

        # pkey = paramiko.RSAKey.from_private_key_file("id_rsa")

        with open("ips.txt", "r") as f:
            for line in f:
                hostIP = line.rstrip('\n')

                try:
                    ping_result = subprocess.check_output(["ping", paramPing, "2", hostIP])

                    if ping_result:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(hostname=hostIP, port=port, username=user, password=passwd)
                        #client.connect(hostname=hostIP, port=port, username=user, pkey=pkey)

                        stdin, stdout, stderr = client.exec_command(command)

                        outputMsg = stdout.read()
                        print(outputMsg.decode('utf-8'))

                        client.close()
                    else:
                        print(hostIP + " else is down.")
                except:
                    print(hostIP + " except is down.")
    return command        


def main():
    while True:
        show_menu()
        
        option = int(input("Escolha uma opcao: "))
        
        if option == 1:
            run_command(listall_frontend(),user,passwd,port)
            validate(run_command)
        elif option == 2:
            run_command(list_backend(),user,passwd,port)
        elif option == 3:
            run_command(enable_backend(),user,passwd,port)
        elif option == 4:
            run_command(disable_backend(),user,passwd,port)
            validate(run_command)
        elif option == 9:
            exit()
        else:
            print("Opção inválida!")
            
            
if __name__ == "__main__":
    main()
