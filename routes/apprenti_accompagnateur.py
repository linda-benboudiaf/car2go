from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import ApprentiAccompagnateur, User
from schemas.apprenti_accompagnateur import ApprentiAccompagnateurCreate, ApprentiAccompagnateurResponse
from routes.auth import get_current_user

router = APIRouter(
    prefix="/service",
    tags=["Apprenti & Accompagnateur"]
)

@router.post("/", response_model=ApprentiAccompagnateurResponse)
def create_apprenti_accompagnateur(
    assoc: ApprentiAccompagnateurCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier que l'utilisateur connecté est bien un apprenti ou un accompagnateur
    if current_user.role not in ["apprenti", "accompagnateur"]:
        raise HTTPException(status_code=403, detail="Seuls les apprentis et accompagnateurs peuvent créer une association.")

    # Déterminer qui est qui dans l'association
    if current_user.role == "apprenti":
        apprenti_id = current_user.id
        accompagnateur_id = assoc.accompagnateur_id
    elif current_user.role == "accompagnateur":
        apprenti_id = assoc.apprenti_id
        accompagnateur_id = current_user.id

    # Vérifier si l'autre utilisateur existe et a le bon rôle
    apprenti = db.query(User).filter(User.id == apprenti_id, User.role == "apprenti").first()
    accompagnateur = db.query(User).filter(User.id == accompagnateur_id, User.role == "accompagnateur").first()

    if not apprenti:
        raise HTTPException(status_code=400, detail="L'utilisateur spécifié comme apprenti n'a pas le rôle 'apprenti'.")
    if not accompagnateur:
        raise HTTPException(status_code=400, detail="L'utilisateur spécifié comme accompagnateur n'a pas le rôle 'accompagnateur'.")

    new_assoc = ApprentiAccompagnateur(
        apprenti_id=apprenti_id,
        accompagnateur_id=accompagnateur_id,
        lien=assoc.lien
    )

    db.add(new_assoc)
    db.commit()
    db.refresh(new_assoc)

    return new_assoc

@router.get("/{apprenti_id}", response_model=list[ApprentiAccompagnateurResponse])
def get_accompagnateurs_for_apprenti(
    apprenti_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier si l'utilisateur est bien l'apprenti ou un administrateur
    if current_user.id != apprenti_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit. Vous ne pouvez voir que vos propres accompagnateurs.")

    accompagnateurs = db.query(ApprentiAccompagnateur).filter(ApprentiAccompagnateur.apprenti_id == apprenti_id).all()
    if not accompagnateurs:
        raise HTTPException(status_code=404, detail="Aucun accompagnateur trouvé pour cet apprenti.")

    return accompagnateurs

@router.get("/{accompagnateur_id}", response_model=list[ApprentiAccompagnateurResponse])
def get_apprentis_for_accompagnateur(
    accompagnateur_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Vérifier si l'utilisateur est bien l'accompagnateur ou un administrateur
    if current_user.id != accompagnateur_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit. Vous ne pouvez voir que vos propres apprentis.")

    apprentis = db.query(ApprentiAccompagnateur).filter(
        ApprentiAccompagnateur.accompagnateur_id == accompagnateur_id
    ).all()

    if not apprentis:
        raise HTTPException(status_code=404, detail="Aucun apprenti trouvé pour cet accompagnateur.")

    return apprentis

@router.delete("/{id}")
def delete_apprenti_accompagnateur(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assoc = db.query(ApprentiAccompagnateur).filter(ApprentiAccompagnateur.id == id).first()

    if not assoc:
        raise HTTPException(status_code=404, detail="Association non trouvée.")

    # Vérifier que seul un administrateur ou un utilisateur concerné peut supprimer
    if current_user.id not in [assoc.apprenti_id, assoc.accompagnateur_id] and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit. Vous ne pouvez supprimer que vos propres relations.")

    db.delete(assoc)
    db.commit()

    return {"message": "Association supprimée avec succès"}