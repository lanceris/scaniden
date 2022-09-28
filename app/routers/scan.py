from typing import List, Optional

from fastapi import APIRouter, Query, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Scan
from ..schemas import ScanOut


router = APIRouter(
    prefix="/scan",
    tags=['scan']
)


@router.get('/get',
            summary="Retrieve a list of scans",
            response_model=Page[ScanOut])
def get(db: Session = Depends(get_db)):
    return paginate(db.query(Scan))


@router.get('/range',
            summary='Retrieves a list of scans by ID range',
            response_model=List[ScanOut])
def get_range(
    db: Session = Depends(get_db),
    start: int = Query(alias='from', description='Scan unique identifier start'), 
    end: int =   Query(alias='to', description='Scan unique identifier end')
    ):
    """Retrieves a list of scans by ID range"""
    
    res = db.query(Scan).filter(Scan.id.between(start, end)).all()
    return res


@router.get('/{id}',
            summary="Retrieve a scan by its unique identifier",
            response_model=Optional[ScanOut])
def get_by_id(db: Session = Depends(get_db),
              id:int = Query(description='Scan unique identifier')):
    res = db.query(Scan).filter(Scan.id == id).first()
    return res