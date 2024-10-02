from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from keri.core import serdering
from signify.app.clienting import SignifyClient
from time import sleep

import requests
from keri import kering
from keri.app import signing
from keri.app.keeping import Algos
from keri.core import coring, eventing, serdering
from keri.core.coring import Tiers
from keri.help import helping

from signify.app.clienting import SignifyClient

app = FastAPI()


# 定义接收的请求体数据模型
class AidRequest(BaseModel):
    # client:str
    name: str
    bran1: str
    bran2: str


# 将 create_aid 函数封装为 FastAPI 接口
@app.post("/wallet/create_aid")
def create_aid_endpoint(aid_request: AidRequest):
    try:
        # client = create_agent(b'Dmopaoe5tANSD8A5rwIhW',
        #                    "EGTZsyZyREvrD-swB4US5n-1r7h-40sVPIrmS14ixuoJ",
        #                    "EPkVulMF7So04EJqUDmmHu6SkllpbOt-KJOnSwckmXwz")
        client = create_agent(aid_request.bran1.encode())
        # client = SignifyClient(passcode=b'Dmopaoe5tANSD8A5rwIhW', tier=Tiers.low)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create client: {str(e)}")

    try:
        identifiers = client.identifiers()
        (_, _, op) = identifiers.create(aid_request.name, bran=aid_request.bran2)
        icp = op["response"]
        serder = serdering.SerderKERI(sad=icp)
        # assert serder.pre == aid_request.expected, f"Not {serder.pre}"
        return {"message": f"AID Created: {serder.pre}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating AID: {str(e)}")


# def create_agent(bran, controller, agent):
def create_agent(bran):
    url = "http://localhost:3901"
    tier = Tiers.low
    client = SignifyClient(passcode=bran, tier=tier)
    # assert client.controller == controller, f"not {client.controller}"

    evt, siger = client.ctrl.event()

    res = requests.post(url="http://localhost:3903/boot",
                        json=dict(
                            icp=evt.ked,
                            sig=siger.qb64,
                            stem=client.ctrl.stem,
                            pidx=1,
                            tier=client.ctrl.tier))

    if res.status_code != requests.codes.accepted:
        raise kering.AuthNError(f"unable to initialize cloud agent connection, {res.status_code}, {res.text}")

    client.connect(url=url, )
    # assert client.agent is not None
    # print("Agent created:")
    # print(f"    Agent: {client.agent.pre}    Controller: {client.agent.delpre}")
    # assert client.agent.pre == agent, f"not {client.agent.pre}"
    # assert client.agent.delpre == controller
    return client


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("create aid:app", host="127.0.0.1", port=8001, reload=True)
