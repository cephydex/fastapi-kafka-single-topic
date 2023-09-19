from fastapi import APIRouter, status
from utils.responses import gen_response

router = APIRouter(
            prefix='/api/v1/worker',
            tags=['Worker'],
            responses={status.HTTP_422_UNPROCESSABLE_ENTITY: {"message": "Request failed"}}
         )


@router.get('/')
def index_request():
    # return {"message": "consumer-worker is alive"}
    return gen_response("consumer-worker is alive", [], True)