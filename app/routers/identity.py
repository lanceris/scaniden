from typing import List, Optional

from fastapi import APIRouter, Query, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Identity
from ..schemas import IdentityOut

router = APIRouter(
    prefix="/identity",
    tags=['identity']
)


@router.get('/get',
            summary='Retrieve a list of identities',
            response_model=Page[IdentityOut])
def get(db: Session = Depends(get_db)):
    return paginate(db.query(Identity))


@router.get('/range',
            summary='Retrieve a list of identities by ID range',
            response_model=List[IdentityOut])
def get_range(
    db: Session = Depends(get_db),
    start: int = Query(alias='from', description='Identity unique identifier start'), 
    end: int =   Query(alias='to', description='Identity unique identifier end')
    ):

    res = db.query(Identity).filter(Identity.id.between(start, end)).all()
    return res


@router.get('/{id}',
            summary='Retrieve an identity by ID',
            response_model=Optional[IdentityOut])
def get_by_id(
    db: Session = Depends(get_db),
    id:int = Query(description='Identity unique identifier')
    ):

    res = db.query(Identity).filter(Identity.id == id).first()
    return res


