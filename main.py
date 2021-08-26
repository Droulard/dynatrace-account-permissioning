import os, json 
from dotenv import load_dotenv
from Account_APIs import DTAccount

if __name__ == "__main__":
    load_dotenv()

    account_num = os.getenv("account_num")
    client_id= os.getenv("client_id")
    client_secret= os.getenv("client_secret")
    my_account = DTAccount(account_num, client_id, client_secret)
    print(my_account)


    team_name = input("Enter a team name: ")
    for group in my_account.get_permissions(team_name):
        print(f"group_name: {group['name']}")
        print(f"Group ID: {group['uuid']}")
        print(f"Permissions: {(json.dumps(group['permissions'], indent=4, sort_keys=True))}")
    