import os, json 
from dotenv import load_dotenv
from Account_APIs import DTAccount

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
    
    account.set_default_permissions(group_name)


if __name__ == "__main__":
    load_dotenv()

    account_num = os.getenv("account_num")
    client_id= os.getenv("client_id")
    client_secret= os.getenv("client_secret")
    my_account = DTAccount(account_num, client_id, client_secret)
    print(my_account)


    while True:
        commands={"set_perms": set_permissions, "get_perms": get_permissions}
        print(f"Available Commands: {commands.keys()}, exit")
        command = input("Enter a command: ")
        if command == 'exit':
            break
        elif command in commands:
            commands[command](my_account)
        else:
            print("Invalid Command")
