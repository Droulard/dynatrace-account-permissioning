# DT-Account-Permissioning
A python module for managing user access to Dynatrace

## Requires:
+ Dynatrace Account
+ Dynatrace OAuth Client
+ Project makes use of an .env file for storing the information from the OAuth token specifically:
    + Account Number
    + Client ID
    + Client Secret 

## About The Project
The overall goal of this project is to provide automation around DT Permissioning so that when a team is added to Dynatrace permissions can be set automatically based on default permissions for a group type and the Dynatrace tenants a user should have access to. 

## Capabilities: 
+ Obtain permissions given to a specific teams Power Users and Base Users 

## TODO: 
+ The following needs to be added: 
    + Resource: JSON structure for hosting valid tenants, valid permissions, default permissions for Base and Power User Groups
    + Feature: Set user group permissions, based on group type, the default permissions for a user group and list of tenants that a user should have access to.
    + Feature: Verify user group permissions
    + Feature: Allow users to verify if a group exists in dynatrace 
+ The following should/could be added: 
    + Interface: fastAPI or otherwise
    + Mongo Datbase for storing information regarding valid tenants, valid permissions and default permission for both Dynatrace User Groups