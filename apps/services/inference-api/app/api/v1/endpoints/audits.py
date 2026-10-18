"""
VIF SmartShelf — Shelf Audit Persistence & History API
"""
from typing import List, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# In-memory storage with initial realistic audit records
_audit_store: List[Dict[str, Any]] = [
    {
        "audit_id": "audit_kirana_mumbai_01",
        "store_name": "Shree Ganesh Kirana & Provisions",
        "timestamp": "2026-10-17T12:30:00Z",
        "items_detected": 42,
        "unique_skus": 14,
        "occupancy_pct": 84.5,
        "compliance_score": 88.0,
        "void_gaps_count": 2,
        "dominant_brand": "Parle",
    },
    {
        "audit_id": "audit_supermarket_delhi_02",
        "store_name": "Apna Bazaar Supermarket",
        "timestamp": "2026-10-17T14:15:00Z",
        "items_detected": 68,
        "unique_skus": 22,
        "occupancy_pct": 91.2,
        "compliance_score": 94.5,
        "void_gaps_count": 1,
        "dominant_brand": "Amul",
    },
    {
        "audit_id": "audit_mart_bengaluru_03",
        "store_name": "Namaste Retail Mart",
        "timestamp": "2026-10-17T16:45:00Z",
        "items_detected": 35,
        "unique_skus": 11,
        "occupancy_pct": 72.0,
        "compliance_score": 75.0,
        "void_gaps_count": 3,
        "dominant_brand": "Maggi",
    },
]


class AuditRecord(BaseModel):
    audit_id: str
    store_name: str = "Neighborhood Kirana Store"
    timestamp: str
    items_detected: int
    unique_skus: int
    occupancy_pct: float
    compliance_score: float
    void_gaps_count: int
    dominant_brand: str


@router.get("/audits", response_model=List[Dict[str, Any]])
async def list_audits():
    """Retrieve history of past Kirana & Supermarket shelf scans."""
    return _audit_store


@router.post("/audits", response_model=Dict[str, Any])
async def save_audit(record: AuditRecord):
    """Save an audit report to history."""
    data = record.model_dump()
    _audit_store.insert(0, data)
    return {"status": "saved", "audit": data}
