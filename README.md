# DT-Account-Permissioning
![Quality gate](./image/quality_gate.png?raw=true)


## About The Project
<i>"A python module for managing user access to Dynatrace."</i>


The overall goal of this project is to provide automation around DT Permissions so that when a team is added to Dynatrace, permissions can be set automatically based on the group type and the Dynatrace tenants a user should have access to. 

### Note: project makes use of the concept of Power Users and Base Users which each have a different default set of permissions

## Requires:
+ Dynatrace Account
+ Dynatrace OAuth Client
+ Project makes use of an .env file for storing the information from the OAuth token specifically:
    + Account Number
    + Client ID
    + Client Secret 
+ A default permission file for listing the permissions that should be granted to Power Users and Base Users and the tenants that users should have access to.

## Capabilities: 
+ Obtain permissions given to a specific teams Power Users and Base Users 
+ Check if a group exists
+ Add a permission to a group 
+ Add default permissions to a given team's PowerUsers and Base Users 
+ Add a list of permissions to a group
+ Remove a permission from a group 
+ Remove all permissions from a group
