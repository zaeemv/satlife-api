from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models.tables import (Inventory, User)
from app.schemas import schemas
from app.services.create_entity import New_entity
from app.services.create_entitystatusHistory import create_status_history
from app.services.update_entity import update_entity_status
from app.config.entities import ENTITY_CONFIG
from app.routers.auth import require_permission

entity_config = ENTITY_CONFIG.get("project")

router = APIRouter()



# ===================== INVENTORY ENDPOINTS =====================
@router.post("/inventory/", response_model=schemas.InventoryRead, tags=["inventory"])
def create_inventory(inventory: schemas.InventoryCreate, session: Session = Depends(get_session), current_user: User = Depends(require_permission("create_inventory"))):
    db_inventory = Inventory(**inventory.model_dump())
    session.add(db_inventory)
    session.flush()

# Create
#    1.  Entity status
#    2.  Entity Status History
# --------------------------------------------------------------------------------------------------------------------------------------------
    New_entity(session=session, entity=db_inventory, entity_name = entity_config["display_name"], changed_by_user= current_user.id)
# --------------------------------------------------------------------------------------------------------------------------------------------

    session.commit()
    session.refresh(db_inventory)
    return db_inventory

@router.get("/inventory/", response_model=List[schemas.InventoryRead], tags=["inventory"])
def list_inventory(
    skip: int = 0, 
    limit: int = 100, 
    inventory_type: str = Query(None, description="Filter by inventory type (system, subsystem, module, unit, component)"),
    session: Session = Depends(get_session), 
    current_user: User = Depends(require_permission("view_inventory"))
):
    query = select(Inventory).offset(skip).limit(limit)
    if inventory_type:
        query = query.where(Inventory.inventory_type == inventory_type)
    return session.exec(query).all()

@router.get("/inventory/by-type/{inventory_type}/", response_model=List[schemas.InventoryRead], tags=["inventory"])
def list_inventory_by_type(
    inventory_type: str, 
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(require_permission("view_inventory"))
):
    """Get all inventory items of a specific type (system, subsystem, module, unit, component)."""
    query = select(Inventory).where(Inventory.inventory_type == inventory_type).offset(skip).limit(limit)
    return session.exec(query).all()

@router.get("/inventory/by-entity/{entity_id}/", response_model=List[schemas.InventoryRead], tags=["inventory"])
def list_inventory_by_entity(
    entity_id: int, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(require_permission("view_inventory"))
):
    """Get all inventory items associated with a specific entity."""
    query = select(Inventory).where(Inventory.entity_id == entity_id)
    return session.exec(query).all()

@router.get("/inventory/{inventory_id}/", response_model=schemas.InventoryRead, tags=["inventory"])
def get_inventory(inventory_id: int, session: Session = Depends(get_session), current_user: User = Depends(require_permission("view_inventory"))):
    inventory = session.get(Inventory, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@router.put("/inventory/{inventory_id}/", response_model=schemas.InventoryRead, tags=["inventory"])
def update_inventory(inventory_id: int, inventory: schemas.InventoryUpdate, session: Session = Depends(get_session), current_user: User = Depends(require_permission("edit_inventory"))):
    db_inventory = session.get(Inventory, inventory_id)
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    for k, v in inventory.model_dump(exclude_unset=True).items():
        setattr(db_inventory, k, v)
    session.add(db_inventory)
    session.commit()
    session.refresh(db_inventory)
    return db_inventory

@router.delete("/inventory/{inventory_id}/", tags=["inventory"])
def delete_inventory(inventory_id: int, session: Session = Depends(get_session), current_user: User = Depends(require_permission("delete_inventory"))):
    inventory = session.get(Inventory, inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    session.delete(inventory)
    session.commit()
    return {"ok": True}
