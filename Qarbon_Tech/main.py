from fastapi import FastAPI,HTTPException,Query
from schema import Request_Body,User,Emp,Resp
import json
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uuid
from starlette import status
from typing import Optional,Union

app = FastAPI()

path = "C:/Users/YBravish/Desktop/Assessment_1/Response/response.json"
path2 = "C:/Users/YBravish/Desktop/Assessment_1/Response/response2.json"

def create_response_json(unique_id, data_dict, file_location):
    """
    Method to write responses to json file
    """
    try:
        with open(file_location, 'r') as file:
            existing_data = json.load(file)
    except Exception:
        existing_data = {}
    existing_data[unique_id] = data_dict
    try:
        with open(file_location, 'w') as file:
            json.dump(existing_data, file, indent=4)
        print(f"Data for unique ID {unique_id} has been written to {file_location}")
    except Exception as e:
        print(f"An error occurred while writing to {file_location}: {e}")
    print("hi")
    return existing_data


@app.post("/create-user-details/",tags=["User"],response_model=Resp)
async def create_user_details(details : Request_Body):
    data = jsonable_encoder(details)
    data["ID"] = str(uuid.uuid4())[0:5]
    if data["source"] == "seller":
        raise HTTPException(status_code=422,detail="source cannot be set to 'seller' ")
    else:
        create_response_json(data["ID"],data,path)
    return data

@app.get("/get-by-ID/{item_id}",tags=["User"])
async def get_by_id(item_id : str):
    try:
        with open(path,"r") as file:
            data = json.load(file)
            if item_id in data:
                return data[item_id]
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")

@app.get("/get-by-list/",tags=["User"])
async def get_by_list(name:Optional[str]=Query(default=None,description="name of the item"),
                issue:Optional[str]=Query(default=None),
                offset:Optional[int]=Query(default=None),limit:Optional[int]=Query(default=10)):
    if offset is not None and offset<0:
        raise HTTPException(status_code=400,detail="offset cannot be negative")
    if limit is not None and limit<0:
        raise HTTPException(status_code=400,detail="limit cannot be negative")
    if offset is None:
        offset=0
    if limit is None:
        limit=0
    try:
        with open(path,"r") as file:
            data=json.load(file)
    except Exception:
        raise HTTPException(status_code=404,detail="file not found")
    exc_data=[]
    for _,item_info in data.items():
        json_name=item_info.get("name")
        for i in range(len(item_info.get("item_name"))):
            json_issue=item_info.get("item_name")[i]["issue_date"]
        print(json_issue)
        
        if (name==json_name or name==None) and (issue==json_issue or issue==None):
            extracted={
                "name":item_info.get("name"),
                "email":item_info.get("email"),
                "contact":item_info.get("contact"),
                "source":item_info.get("source"),
                "item_name":item_info.get("item_name"),
                "Id":item_info.get("ID")
            }
            exc_data.append(extracted)
    response=exc_data[offset:offset+limit]
    if not response or not exc_data:
        raise HTTPException(status_code=404,detail="no matching record found")
    return response


@app.patch("/update/{item_id}",tags=["User"])
async def update_items(item_id : str,details : Request_Body):
    try:
        with open(path,"r") as file:
            data = json.load(file)
            if item_id in data:
                conv = jsonable_encoder(details)
                conv['ID']=item_id
                jname = data[item_id]["name"]
                jemail = data[item_id]["email"]
                # jcon = data[item_id]["contact"]
                jsource = data[item_id]["source"]
               

                data[item_id] = conv
                if data[item_id]["name"] == None:
                    data[item_id]["name"] = jname
                if data[item_id]["email"] == None:
                    data[item_id]["email"] = jemail
                # if data[item_id]["contact"] == None:
                #     data[item_id]["contact"] = jcon
                if data[item_id]["source"] == None:
                    data[item_id]["source"] = jsource
                with open(path,"w") as f1:
                    json.dump(data,f1,indent=4)
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
        return data[item_id]
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")




                    

@app.delete("/delete-by-ID/{item_id}",tags=["User"])
async def delete_by_id(item_id:str):
    try:
        with open(path,"r") as file:
            data = json.load(file)
            if item_id in data:
                data.pop(item_id)
                with open(path,"w") as f:
                    json.dump(data,f,indent=4)
                return {"item":"Removed Successfully"}
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")
        


# Employee Details
@app.post("/create-emp",tags=["Emp"])
async def create_emp_details(emp : Emp):
    data = jsonable_encoder(emp)
    data["ID"] = str(uuid.uuid4())[0:5]
    create_response_json(data["ID"],data,path2)
    return data

@app.get("/get-emp-by-ID/{emp_id}",tags=["Emp"])
async def get_emp_by_id(emp_id : str):
    try:
        with open(path2,"r") as file:
            data = json.load(file)
            if emp_id in data:
                return data[emp_id]
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")
    

# @app.get("/get-emp-by-list",tags=["Emp"])
# async def get_emp_by_list(sal_id : str, emp_tax : Union[float,None]=None):
#     try:
#         with open(path2,"r") as file:
#             data = json.load(file) 
#             if data[]


@app.patch("/update_emp/{emp_id}",tags=["Emp"])
async def update_emp_items(emp_id : str,emp : Emp):
    conv = jsonable_encoder(emp)
    try:
        with open(path2,"r") as file:
            data = json.load(file)
            if emp_id in data:
                data[emp_id] = conv
                with open(path2,"w") as f1:
                    json.dump(data,f1,indent=4)
            else:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content="ID not found")
        return data[emp_id]
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")


@app.delete("/delete-emp-by-ID/{item_id}",tags=["Emp"])
async def delete_emp_by_id(item_id:str):
    try:
        with open(path,"r") as file:
            data = json.load(file)
            if item_id in data:
                data.pop(item_id)
                with open(path2,"w") as f:
                    json.dump(data,f,indent=4)
                return {"item":"Removed Successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID doesn't exist")
    except Exception:
        raise HTTPException(status_code=404,detail="File not Found")
    

