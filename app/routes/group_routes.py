from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import models,database,auth,schemas
from ..schemas import GroupCreate,GroupOut


router=APIRouter(
    prefix="/groups",
    tags=["Groups"]
)

@router.post("/",response_model=GroupOut)
def create_group(group:GroupCreate,db:Session=Depends(database.get_db),current_user:models.User=Depends(auth.get_current_user)):
    new_group=models.Group(name=group.name,owner_id=current_user.id)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)

    group_member=models.GroupMember(user_id=current_user.id,group_id=new_group.id,role="admin")
    db.add(group_member)
    db.commit()

    return new_group

@router.post("/{group_id}/add_member/{user_id}")
def add_member_to_group(group_id: int,user_id: int,db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)):
    
    membership = db.query(models.GroupMember).filter_by(group_id=group_id,user_id=current_user.id,role="admin").first()

    if not membership:
        raise HTTPException(status_code=403, detail="Only admins can add members")

    exists = db.query(models.GroupMember).filter_by(group_id=group_id,user_id=user_id).first()

    if exists:
        raise HTTPException(status_code=400, detail="User already in group")

    new_member = models.GroupMember(group_id=group_id,user_id=user_id,role="member")
    db.add(new_member)
    db.commit()
    return {"message": f"User {user_id} added to group {group_id}"}

@router.get("/", response_model=list[schemas.GroupOut])
def get_user_groups(db: Session = Depends(database.get_db),
                    current_user: models.User = Depends(auth.get_current_user)):
    # Get groups where user is a member
    group_ids = db.query(models.GroupMember.group_id).filter(
        models.GroupMember.user_id == current_user.id
    ).subquery()

    groups = db.query(models.Group).filter(models.Group.id.in_(group_ids)).all()
    return groups


@router.get("/{group_id}/members")
def list_group_members(
    group_id: int,
    db: Session = Depends(database.get_db),current_user: models.User = Depends(auth.get_current_user)):
    
    member_check = db.query(models.GroupMember).filter_by(group_id=group_id,user_id=current_user.id).first()

    if not member_check:
        raise HTTPException(status_code=403, detail="You are not a member of this group")

    members = db.query(models.GroupMember).filter_by(group_id=group_id).all()

    return [{"user_id": m.user_id, "role": m.role}for m in members]

@router.get("/{group_id}/expenses")
def group_expense_summary(group_id: int,db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)):
  
    member = db.query(models.GroupMember).filter_by(group_id=group_id,user_id=current_user.id).first()

    if not member:
        raise HTTPException(status_code=403, detail="Access denied")

    expenses = db.query(models.Expense).filter_by(group_id=group_id).all()
    return [{ "title": e.title,
              "amount": e.amount,
              "category": e.category,
              "timestamp": e.timestamp,
              "added_by": e.owner_id
            }for e in expenses]
