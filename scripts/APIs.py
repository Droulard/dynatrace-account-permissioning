from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
from Account_APIs import DTAccount
import uvicorn, os
load_dotenv()
account_num = os.getenv("account_num")
client_id= os.getenv("client_id")
client_secret= os.getenv("client_secret")
my_account = DTAccount(account_num, client_id, client_secret)


app = FastAPI()

@app.get("/permissions/{team_name}")
async def get_permissions(team_name):
    output ={}
    try:
        groups = my_account.get_permissions(team_name)
        output=groups
    except Exception as exception:
        raise HTTPException(status_code=404, detail=f"Failed: {exception}")
    return output

@app.post("/permissions/{team_name}")
async def set_permissions(team_name):
    output={}
    try:
        res = my_account.set_default_permissions(team_name)
        if res:
            output={"message": f"Permissions set for {team_name}"}
        else:
            raise HTTPException(status_code=500, detail="An Error Occurred")
    except Exception as exception:
        raise HTTPException(status_code=404, detail=f"Failed: {exception}")
    return output

@app.delete("/permissions/team/{team_name}/group_type/{group_type}")
async def delete_permissions(team_name, group_type):
    output={}
    try:
        res = my_account.clear_permissions(team_name, group_type)
        if res:
            output={"message": f"Permissions removed for {team_name}"}
        else:
            raise HTTPException(status_code=500, detail="An Error Occurred")
    except Exception as exception:
        raise HTTPException(status_code=404, detail=f"Failed: {exception}")
    return output


if __name__ == "__main__":
    uvicorn.run("APIs:app", host="localhost", port=5000, log_level="info")
