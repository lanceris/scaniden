from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Scan, Identity


router = APIRouter(
    tags=['index']
)


@router.get('/',
            summary='Retrieve summary for scans and identities',
            )
def index(db: Session = Depends(get_db)):
    scan_data = db.query(
        func.min(Scan.id).label('scan_min_id'), 
        func.max(Scan.id).label('scan_max_id'),
        func.min(Scan.created_at).label('scan_min_date'),
        func.max(Scan.created_at).label('scan_max_date')
        ).first()
    scan_data = dict(scan_data)
    distinct_verdicts = db.query(Scan.verdict_value).distinct().all()
    distinct_verdicts = [x['verdict_value'] for x in distinct_verdicts]
    scan_data['scan_distinct_verdicts'] = distinct_verdicts

    id_data = db.query(
        func.min(Identity.id).label('identity_min_id'), 
        func.max(Identity.id).label('identity_max_id'),
        func.min(Identity.expires_at).label('identity_min_expiry'),
        func.max(Identity.expires_at).label('identity_max_expiry')
        ).first()
    id_data = dict(id_data)

    data = {'scans': scan_data, 'identities': id_data}
    return data