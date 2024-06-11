from typing import Annotated
from fastapi import FastAPI, Path, Query
from quant import quantification

app = FastAPI()

@app.get("/quant")
async def root(minInc: Annotated[int, Query(ge=0)],
               maxInc: Annotated[int, Query(gt=0)],
               minLoss: Annotated[float, Query(ge=0)],
               maxLoss: Annotated[float, Query(gt=0)],
               confInc: Annotated[float, Query(gt=0, le=1)],
               confLoss: Annotated[float, Query(gt=0, le=1)]):
  jsondump = quantification(minInc, maxInc, minLoss, maxLoss, confInc, confLoss)
  print('dump received')
  print(jsondump)
  return jsondump
