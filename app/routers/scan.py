from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/scan",
    tags=['scan']
)


@router.get('/get', tags=['get'])
def get():
    return {'res': "all"}


@router.get('/{id}', tags=['getById'])
def get_by_id(id:int):
    return {'id': id, 'data': list(range(id, id+5))}


@router.get('/range', tags=['getRange'])
def get_range(start: int = Query(alias='from'), end: int = Query(alias='to')):
    return list(range(start, end))