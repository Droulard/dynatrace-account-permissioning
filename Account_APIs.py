import requests

class DTAccount:
    _headers = {'accept': 'application/json', 'Authorization': ""}
    
    def __init__(self, acc_num, client_id, client_sec):
        self._account_num    = acc_num
        self._client_id      = client_id
        self._client_sec     = client_sec
        self._groups         = None

    def __repr__(self):
        return f"DT Account: {self._account_num}"

    def _bearerToken(self, scope=None):   
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
            print("success")
            bearer_token= res.json()['access_token']
        else:
            raise RuntimeError("Failed to fetch groups")
        
        return bearer_token

    def _getGroups(self):
        """
        Purpose: Grab the created groups for the given account
        Inputs: Requires account number, and bearer token
        Runtime Error if the api call fails

        """ 
        URL = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups"
        bearer_token = self._bearerToken()
        self._headers['Authorization'] = f"Bearer {bearer_token}"

        res = requests.get(URL, headers=self._headers)
        groups = dict()
        if res:
            print("Grabbing groups: success")
            for group in res.json()['items']:
                groups[group['name']]=group

        else:
            raise RuntimeError("Failed to fetch groups")
        
        return groups
    
    def _setGroups(self):
        """
        Purpose: Lazy load for DT groups
        Inputs:  None
        Return:  None
        """ 
        if self._groups is None:
            self._groups = self._getGroups()

    def _getGroupPermission(self, group_id):
        """
        Purpose: Get permissions for a group by using the Group ID
        Inputs:  group id
        Return:  permission set for a group id in the form of a dictionary
        """ 

        url = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups/{group_id}/permissions"
        bearer_token = self._bearerToken()
        self._headers['Authorization'] = f"Bearer {bearer_token}"
        res = requests.get(url, headers=self._headers)
        
        if res:
            print("Obtaining Permissions: successful")
            permissions = res.json()
        else:
            raise RuntimeError("Failed to fetch group permissions")
        
        return permissions

    def _setGroupPermission(self, **groupinfo):
        """
        Purpose: Lazy load for DT groups
        Inputs:  Dictionary containing the following:
                    * Group Type
                    * Group ID
                    * Tenant List: Array of tenants that the user needs permissions too
        Return:  Boolean based off of API response
        TODO:    Function is a template right now

        Template: 

            url = f"https://api.dynatrace.com/iam/v1/accounts/{self._account_num}/groups/{group_id}/permissions"
            bearer_token=self._bearerToken("write")
            headers = {
                "accept": "*/*",
                "Authorization": f"Bearer {bearer_token}",
                "Content-Type": "application/json"
                }
            
            TODO: Set the permission data Dynamically 
            data=  {
                    "permissionName": "tenant-viewer",
                    "scope": "***",
                    "scopeType": "tenant"
                }

            TODO: Return Boolean based on status code of the API request
            res= requests.post(url, headers=headers, data=data)
            if res: 
                print("Set Permissions: Successful")
            else:
                raise RuntimeError("Failed to Set Permissions")
            
        """
        print("Feature Not Implemented Yet!")
        return None
        
    def _getvalid_permissions(self):
        """
        Purpose: Get valid permissions for a Dynatrace Account
        Inputs:  None
        Return:  Valid Permission Set
        """ 
        url="https://api.dynatrace.com/ref/v1/account/permissions"
        bearer_token = self._bearerToken()
        self._headers['Authorization'] = f"Bearer {bearer_token}"
        res = requests.get(url, headers=self._headers)
        if res:
            print("Obtaining Permission Sets: successful")
            permissions = res.json()
        else:
            raise RuntimeError("Failed to fetch permissions")
        return permissions

    def _getTenants(self):
        """
        Purpose: Get valid tenants for a Dynatrace Account
        Inputs:  None
        Return:  Valid tenant set and management zones for the tenant
        TODO: Seperate tenants and management zones, method should only return valid tenants
        """ 
        url = f"https://api.dynatrace.com/env/v1/accounts/{self._account_num}/environments"
        bearer_token = self._bearerToken()
        self._headers['Authorization'] = f"Bearer {bearer_token}"
        res = requests.get(url, headers=self._headers)
        if res:
            print("Obtaining Tenants: successful")
            tenants = res.json()
        else:
            raise RuntimeError("Failed to fetch tenants")
 
        return tenants
    
    def get_permissions(self, group_name):
        """
        Purpose: Get permissions set for both the Power User and Base User groups of a given group
        Inputs:  The name of a given group, also defined as an application team 
        Return:  array of two dictionaries, first is the permission set of the power users second is the permission set for the base users 
        """ 
        self._setGroups()
        group_names = [f"Dynatrace_{group_name}_PowerUsers", f"Dynatrace_{group_name}_Users"]
        permissions = []
        for name in group_names:
            group_id = self._groups[name]['uuid']
            permissions.append(self._getGroupPermission(group_id))
        return permissions

    def set_permissions(self, group_name):
        """
        TODO: Implement this feature for setting permissions for a group
        """
        print("Feature Not Implemented Yet!")
        return None
