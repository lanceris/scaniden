from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/identity",
    tags=['identity']
)


@router.get('/get', tags=['get'])
def get():
    return 'all'


@router.get('/{id}', tags=['getById'])
def get_by_id(id:int):
    return id


@router.get('/range', tags=['getRange'])
def get_range(start: int = Query(alias='from'), end: int = Query(alias='to')):
    return list(range(start, end))