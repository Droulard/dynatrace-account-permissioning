############################################################################################################################################################
# TITLE: Account Management
# AUTHOR: Kyle Droulard
# RELEASE: V1
# DATE: 09/17/21
############################################################################################################################################################

import requests, json, logging, os
import datetime

class dt_account:
    _headers = {'accept': 'application/json', 'Authorization': ""}
    _permissions_file = "default_permissions.json"

    def __init__(self, acc_num, client_id, client_sec):
        self._account_num    = acc_num
        self._client_id      = client_id
        self._client_sec     = client_sec
        self._groups         = None
        self._defaults       = None


        date=datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
        
        if not os.path.exists("./logs"):
            os.makedirs("./logs")
        
        logging.basicConfig(filename=f'./logs/permissions_{date}.log',level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

    def __repr__(self):
        return f"DT Account: {self._account_num}"

    def _bearer_token(self, scope=None):   
        """
        Purpose: Grab the bearer token with read and write permissions for the given account
        Inputs: Requires account number, client id and client secret
        Return: 
                Runtime Error if the api call fails
                String containing the bearer token if the call is successful
                None in any other case
        """ 
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        URL = "https://sso.dynatrace.com/sso/oauth2/token"
        data = {
            "resource": f"urn:dtaccount:{self._account_num}",
            "grant_type": "client_credentials",
            "client_id": f"{self._client_id}",
            "client_secret": f"{self._client_sec}",
        }
        
        if scope in ["read", "write"]:
            data["scope"]= f"account-idm-{scope}"
            
        else:
            data ["scope"]= "account-idm-read"

        res = requests.post(URL, data=data, headers=headers)
        
        if res:
            bearer_token= res.json()['access_token']
        else:
            raise RuntimeError("Failed to fetch token")
        
        return bearer_token

    def _load_defaults(self):
        """
        Purpose: Get the permissions and tenants from the default permissions file
        Inputs:  None
        Return:  Valid Permission Set
        """ 
        if self._defaults == None:
            with open (self._permissions_file) as permission_file:
                self._defaults = json.load(permission_file)

    def _set_groups(self):
        """
        Purpose: Set account groups locally
        Inputs: None
        Runtime Errors if the api call fails
        """ 

        if self._groups is None:
            URL = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups"
            bearer_token = self._bearer_token()
            self._headers['Authorization'] = f"Bearer {bearer_token}"

            res = requests.get(URL, headers=self._headers)
            groups = dict()
            
            if res:
                for group in res.json()['items']:
                    groups[group['name']]=group
                logging.info("Set Groups Locally")
            else:
                logging.error("Failed to fetch groups")
                raise RuntimeError("Failed to fetch groups")
        
            self._groups = groups

    def _get_group_permission(self, group_id):
        """
        Purpose: Get permissions for a group by using the Group ID
        Inputs:  group id
        Return:  permission set for a group id in the form of a dictionary
        """ 

        url = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups/{group_id}/permissions"
        bearer_token = self._bearer_token()
        self._headers['Authorization'] = f"Bearer {bearer_token}"
        res = requests.get(url, headers=self._headers)
        
        if res:
            permissions = res.json()
        else:
            logging.error("Failed to fetch group permission")
            logging.error(res.json())
            raise RuntimeError("Failed to fetch group permissions")
        
        return permissions

    def _delete_group_permission(self, groupinfo):
        """
        Purpose: Used for deleting a permission for a specific tenant for a specific group
        Input:  Dictionary with the following keys: 'group_id', 'tenant', 'permission', Boolean value to run function in silence
            Example: 
                groupinfo={
                    'group_id': '***', 
                    'tenant': '***', 
                    'permission': 'tenant-viewer'
                }

        Return: True/False based on output for deleting group permissions
        """

        self._set_groups()
        bearer_token = self._bearer_token('write')
        output = False
        req_params = ['group_id', 'tenant', 'permission']

        if list(groupinfo.keys()) != req_params:
            print(req_params)
            raise TypeError("Delete Permissions Requires a dictionary with the keys listed")

        url = f'https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups/{groupinfo["group_id"]}/permissions'
        
        params = {
            "scope": groupinfo['tenant'],
            "permission-name": groupinfo['permission'],
            "scope-type": "tenant"
        }

        headers = {
            'accept': '*/*',
            'Authorization': f'Bearer {bearer_token}'
        }

        res = requests.delete(url=url, params=params, headers=headers)

        if res:
            logging.info("Successfully deleted permission")
            output = True
        else:
            logging.error("Failed to delete permission")
            raise RuntimeError("Deleting Permissions Failed")
            
        return output

    def _set_group_permission(self, groupinfo):
        """
        Purpose: Set the permissions for a given group and tenant
        Inputs:  Dictionary containing the following:
            Example: 
                groupinfo={
                    'group_id': '***', 
                    'tenant': '***', 
                    'permissions': ['tenant-viewer']
                }

        Return: True/False based on output for setting group permissions 
        """

        self._set_groups()
        bearer_token=self._bearer_token("write")
        output = False

        req_params = ['group_id', 'tenant', 'permissions']

        if list(groupinfo.keys()) != req_params:
            print(req_params)
            raise TypeError("Set Permissions Requires a dictionary with the keys listed")

        url = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups/{groupinfo['group_id']}/permissions"
        
        headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
        data=[]
        for permission in groupinfo['permissions']:
            data.append({
                "permissionName": permission,
                "scope": groupinfo['tenant'],
                "scopeType": "tenant"
            })
        
        res= requests.post(url, headers=headers, data=json.dumps(data))
        if res: 
            logging.info("Set Permissions: Successful")
            output = True
        else:
            logging.error("Call failed!")
            raise RuntimeError("Setting Permissions Failed")
        
        return output
            

    def group_exists(self, team_name):
        """
        Purpose: Check if a group exists within the local dictionary of users
        Inputs:  Team Name
        Return:  True/False
        """ 
        exists = False
        self._set_groups()
        
        for name in self._groups.keys():
            if team_name in name:
                exists = True
        
        return exists

   
    def get_permissions(self, group_name):
        """
        Purpose: Get permissions set for both the Power User and Base User groups of a given group
        Inputs:  The name of a given group, also defined as an application team 
        Return:  array of two dictionaries, first is the permission set of the power users second is the permission set for the base users 
        """ 
        self._set_groups()
        group_names = [f"Dynatrace_{group_name}_PowerUsers", f"Dynatrace_{group_name}_Users"]
        output = None
        
        permissions = []

        for name in group_names:
            if self.group_exists(name):
                group_id = self._groups[name]['uuid']
                permissions.append(self._get_group_permission(group_id))
            else:
                logging.error("Tried fetching non existant group")
                raise NameError("Group does not exist")
        if len(permissions) !=0:
            logging.info("Obtaining Permissions Successful")
            output = permissions
    
        return output

    def set_default_permissions(self, group_name):
        """
        Purpose: Set default permissions for both the Power User and Base User groups of a given group
        Inputs:  Group Name
        Return:  True/False based on if a group's permissions were set successfully
        """ 
        self._set_groups()
        self._load_defaults()
        group_names = [f"Dynatrace_{group_name}_PowerUsers", f"Dynatrace_{group_name}_Users"]
        output=True
        
        for tenant in self._defaults['tenants']:
            for name in group_names:
                permissions = self._defaults[name.split('_')[-1]]['permissions']
                logging.info(f"Setting permissions for {name}:")
                if self.group_exists(name):
                    group_info={
                        'group_id': self._groups[name]['uuid'],
                        'tenant': tenant,
                        'permissions': permissions

                    }
                    res = self._set_group_permission(group_info)
                    if res: 
                        logging.info(f"\tSet {permissions} for tenant {tenant}")
                    else:
                        output=False
                        logging.error(f"\tFailed to Set {permissions} for tenant {tenant}")
                else:
                    logging.error(f"Unknown Group: {name}")
                    raise RuntimeError("Encountered An Unknown Group!")
        return output

    def clear_permissions(self, group_name, user_type):
        """
        Purpose: Set clear all permissions assigned to a given group
        Inputs:  Group Name
        Return:  True/False based on if a group's permissions were removed successfully
        """ 

        self._set_groups()
        self._load_defaults()
        output=True

        if user_type in ["PowerUsers", "Users"]:
            group_name = f"Dynatrace_{group_name}_{user_type}"
        else:
            logging.error("Required Paramaters group_name, user_type not provided")
            raise NameError("Incorrect User Type")

        if self.group_exists(group_name):    
            group_id = self._groups[group_name]['uuid']
            permissions = self._get_group_permission(group_id)['permissions']
        
            if len(permissions) > 0:
                logging.info(f"Removing Permssions for {group_name}:")
                for permission in permissions:
                    res = self._delete_group_permission({'group_id': group_id, 'tenant': permission['scope'], 'permission':permission['permissionName']})
                    if res:
                        logging.info(f"\tSUCCESSFUL: {permission['permissionName']} removed for tenant: {permission['scope']}")
                    else: 
                        logging.error(f"\tFAILED: {permission['permissionName']} could not be removed for tenant: {permission['scope']}")
                        print("SOMETHING WENT WRONG")   
                        output=False    
            else:
                logging.error(f"Group {group_name} does not have any permissions")
                raise EOFError("No permissions exist for this group")
        else: 
            logging.error("Group Does Not Exist")
        
        return output
