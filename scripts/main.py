import os, json 
from dotenv import load_dotenv
from Account_APIs import DTAccount

def get_permissions(account, group_name=None):
    if group_name == None:
        team_name = input("Enter a team name: ")
    else:
        team_name = group_name

    for group in account.get_permissions(team_name):
        print(f"group_name: {group['name']}")
        print(f"Group ID: {group['uuid']}")
        print(f"Permissions: {(json.dumps(group['permissions'], indent=4, sort_keys=True))}")
    

if __name__ == "__main__":
    load_dotenv()

    account_num = os.getenv("account_num")
    client_id= os.getenv("client_id")
    client_secret= os.getenv("client_secret")
    my_account = DTAccount(account_num, client_id, client_secret)
    print(my_account)

    get_permissions(my_account, '***')

    groupinfo={
                    'group_type': 'Users',
                    'group_name': '***', 
                    'tenant': '***', 
                    'permission': '***'
                }
    print("Deleting the permission")
    input("Hit enter to continue")
    my_account.delete_group_permission(groupinfo)
    get_permissions(my_account, '***')
    print("Setting the permission")
    input("Hit enter to continue")
    my_account.set_group_permission(groupinfo)
    get_permissions(my_account, '***')


