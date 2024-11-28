from fastapi import FastAPI, Form, Request, HTTPException, Query, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from datetime import datetime, time
import uuid
repo = []
notafications= []
app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Orders:
    def __init__(self,id,date,orgtech,model,problemdeskription,bioclient,numberphone,status,otvetsvenye,comments,enddate):
        self.id =id
        self.date =date
        self.orgtech=orgtech
        self.model=model
        self.problemdeskription=problemdeskription
        self.bioclient=bioclient
        self.numberphone=numberphone
        self.status=status
        self.otvetsvenye=otvetsvenye
        self.comments= comments
        self.enddate=enddate



@app.get("/", response_class=HTMLResponse)
def base(request: Request): 
    return  templates.TemplateResponse("repo.html", {"request": request,"inside_data": repo,"dddd":notafications})


@app.get("/add", response_class=HTMLResponse)
def base(request: Request): 
    return  templates.TemplateResponse("add.html", {"request": request,"inside_data": repo})

@app.post("/create-api") 
def postdata(id: str = Form(),
             date: str = Form(),
    orgtech: str = Form(), 
            model: str =Form(),
            problemdeskription: str =Form(),
            bioclient: str =Form(),
            numberphone: str =Form(),
            status: str =Form(),
            ):
    print(date)
    repo.append(Orders(uuid.uuid4(), datetime.strptime(date, '%Y-%m-%d').timestamp(),orgtech=orgtech,model=model,problemdeskription=problemdeskription,bioclient=bioclient,numberphone=numberphone,status=status,otvetsvenye="nil",comments="nil",enddate="nil"))
    return HTMLResponse(content="<a href='/'>на главную</a>", status_code=200)




@app.post("/update-api") 
def update(id:str=Form(),
    status: str = Form(default= "nul"),
           description: str = Form(default= "nul"),
           otvetsvenye: str = Form(default= "nul"),
           comments: str = Form(default= "nul"),):
    print(status,description,otvetsvenye)
    for i in range(len(repo)):
        if str(repo[i].id) == id :
            newell = repo[i]
            if status!= "nul":
                newell.status= status
                if status == "close":
                    newell.enddate =  datetime.now().timestamp()
                    notafications.append(f"заявка с id:{str(repo[i].id)} обновлена")
            if  description!="nul":
                newell.problemdeskription= description
            if status!= "nul":
                newell.otvetsvenye=otvetsvenye  
            if comments!= "nul":
                newell.comments=comments        
            repo[i]= newell
            return  HTMLResponse(content="<a href='/'>на главную</a>", status_code=200)
        
    pass


@app.get("/update", response_class=HTMLResponse)
def base(request: Request): 
    return  templates.TemplateResponse("update.html", {"request": request,"inside_data": repo})



@app.get("/search", response_class=HTMLResponse)
def base(request: Request): 
    return  templates.TemplateResponse("search.html", {"request": request,"inside_data": repo})



@app.post("/search-api",response_class=HTMLResponse) 
def getbyid(request: Request,id: str = Form()):
    print(id,repo)
    for i in repo:
        if str(i.id) == id:
            return templates.TemplateResponse("repo.html", {"request": request,"inside_data": [i],"dddd":[]})
    pass


@app.get("/stats-api",response_class=HTMLResponse) 
def stats(request: Request): 
    closed = [i for i in repo if i.status=="close"]
    avgt= [(datetime.fromtimestamp(int(i.enddate)) - datetime.fromtimestamp(int(i.date))).seconds  for i in closed]
    return templates.TemplateResponse("stats.html", {"request": request,"ready": len([i for i in repo if i.status=="close"]),"avh":(sum(avgt) / len(avgt))/60/60})
pass


import uvicorn
if __name__ == "__main__":
    # add default data 
    repo.append(Orders("1",1686038096,orgtech="Компьютер",model="DEXP Aquilon O286",problemdeskription="Перестал работать",bioclient="bioclient",numberphone="numberphone",status="status",otvetsvenye="nil",comments="Интересно...",enddate="nill"))
    repo.append(Orders(2,1683273296,orgtech="Компьютер",model="DEXP Atlas H388",problemdeskription="Перестал работать",bioclient="bioclient",numberphone="numberphone",status="status",otvetsvenye="nil",comments="Будем разбираться!",enddate="nill"))
    repo.append(Orders(3,1688716496,orgtech="Ноутбук",model="MSI GF76 Katana 11UC-879XRU черный",problemdeskription="Выключается",bioclient="bioclient",numberphone="numberphone",status="close",otvetsvenye="nil",comments="Сделаем всё на высшем уровне!",enddate="1672559696"))
    repo.append(Orders(4,1690962896,orgtech="Ноутбук",model="MSI Modern 15 B12M-211RU черный",problemdeskription="Выключается",bioclient="bioclient",numberphone="numberphone",status="status",otvetsvenye="nil",comments="nil",enddate="nill"))
    repo.append(Orders(5,1690962896,orgtech="Принтер",model="HP LaserJet Pro M404dn",problemdeskription="Перестала включаться",bioclient="bioclient",numberphone="numberphone",status="status",otvetsvenye="nil",comments="nil",enddate="nill"))

    uvicorn.run(app, host="127.0.0.1", port=8000)
