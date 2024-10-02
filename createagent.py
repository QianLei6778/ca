from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import requests
import pytest
from keri import kering
from keri.core.coring import Tiers
from signify.app.clienting import SignifyClient

app = FastAPI()


# 定义输入数据模型，接收用户传入的 bran 参数
class AgentRequest(BaseModel):
    bran: str


# FastAPI 路由，封装 create_agent 函数
@app.post("/wallet/create_agent")
def create_agent(agent_request: AgentRequest):
    url = "http://localhost:3901"
    bran = agent_request.bran.encode()  # 将字符串转换为字节
    tier = Tiers.med

    try:
        client = SignifyClient(passcode=bran, tier=tier)
        assert client.controller == "EOgQvKz8ziRn7FdR_ebwK9BkaVOnGeXQOJ87N6hMLrK0"

        # Raises configuration error because the started agent has a different controller AID
        with pytest.raises(kering.ConfigurationError):
            client.connect(url=url)

        tier = Tiers.low
        client = SignifyClient(passcode=bran, tier=tier)
        assert client.controller == "ELI7pg979AdhmvrjDeam2eAO2SR5niCgnjAJXJHtJose"

        evt, siger = client.ctrl.event()

        res = requests.post(url="http://localhost:3903/boot",
                            json=dict(
                                icp=evt.ked,
                                sig=siger.qb64,
                                stem=client.ctrl.stem,
                                pidx=1,
                                tier=client.ctrl.tier))
        if res.status_code != requests.codes.accepted:
            raise kering.AuthNError(f"Unable to initialize cloud agent connection, {res.status_code}, {res.text}")

        client.connect(url=url)
        assert client.agent is not None
        assert client.agent.pre == "EEXekkGu9IAzav6pZVJhkLnjtjM5v3AcyA-pdKUcaGei"
        assert client.agent.delpre == "ELI7pg979AdhmvrjDeam2eAO2SR5niCgnjAJXJHtJose"

        return {"message": "Person agent created", "agent_pre": client.agent.pre, "agent_delpre": client.agent.delpre}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("create agent:app", host="127.0.0.1", port=8001, reload=True)
