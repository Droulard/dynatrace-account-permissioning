############################################################################################################################################################
# TITLE: Account Management
# AUTHOR: Kyle Droulard
# RELEASE: V1
# DATE: 09/17/21
############################################################################################################################################################
import os, json 
from dotenv import load_dotenv
from Account_APIs import dt_account

def get_permissions(account, group_name=None):
    if group_name == None:
        group_name = input("Enter a team name: ")
    
    groups = account.get_permissions(group_name)
    if groups != None:
        for group in groups:
            print(f"group_name: {group['name']}")
            print(f"Group ID: {group['uuid']}")
            print(f"Permissions: {(json.dumps(group['permissions'], indent=4, sort_keys=True))}")
    else:
        print("Team haa not been added")

def set_permissions(account, group_name=None):
    if group_name == None:
        group_name = input("Enter a team name: ")
    
    res = account.set_default_permissions(group_name)
    if res:
        print(f"Permissions Set for {group_name}")
    else:
        print("An error Occurred!")


def verify_group(account, group_name=None):
    if group_name == None:
        group_name = input("Enter a team name: ")
    
    res = account.group_exists(group_name)
    
    if res:
        print(f"{group_name} exists")
    else:
        print(f"{group_name} is unknown!")

def read_from_file(account, file_name=None):
    if file_name == None:
        for file in os.listdir():
            print(file, end="\t")
        print("\n")

        file_name = input("Enter a Text File: ")
    with open(f"{file_name}.txt", "r") as group_file:
        for _ in group_file:
            team_name=group_file.readline().split("_")[1]
            set_permissions(account,team_name)


if __name__ == "__main__":
    load_dotenv()

    account_num = os.getenv("account_num")
    client_id= os.getenv("client_id")
    client_secret= os.getenv("client_secret")
    my_account = dt_account(account_num, client_id, client_secret)
    print(my_account)


    while True:
        commands={
            "set_perms": set_permissions, 
            "get_perms": get_permissions, 
            "read_file": read_from_file, 
            "verify": verify_group
            }
        print(f"Available Commands: {commands.keys()}, exit")
        command = input("Enter a command: ")
        if command == 'exit':
            break
        elif command in commands:
            commands[command](my_account)
        else:
            print("Invalid Command")
