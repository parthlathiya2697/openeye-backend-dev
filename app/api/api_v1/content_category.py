from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from openeye_backend import crud
from openeye_backend.api import deps
from openeye_backend.api.api_v1.utils.common import is_new_user
from openeye_backend.schemas.content_category import ContentCategoryOutput

router = APIRouter(prefix="/content-category", tags=["Content Category"])


@router.get("/all", response_model=List[ContentCategoryOutput])
def read_categories(
    db: Session = Depends(deps.get_db), user_id: str = Depends(deps.get_user_id)
):
    subscription_product_access = crud.subscription_product_access.get_by_user_id(
        db, user_id=user_id
    )

    if not subscription_product_access:
        subscription = crud.subscription.get_by_owner_id(db, owner_id=user_id)
        user = crud.user.get_by_id(db, fb_id=user_id)
        if user and is_new_user(subscription_plan=subscription, user=user):
            if not subscription:
                subscription_product = crud.subscription_product.get_by_title(
                    db, title="Free Trial"
                )
                if subscription_product:
                    subscription_product_access = (
                        crud.subscription_product_access.get_by_product_id(
                            db, product_id=str(subscription_product.id)
                        )
                    )

    enabled_content_type_ids = (
        subscription_product_access.content_type_ids
        if subscription_product_access
        else None
    )
    return crud.content_category.get_all_(
        db, enabled_content_type_ids=enabled_content_type_ids
    )
