from fastapi import APIRouter, Depends

from src.presentation.api.dependencies import SetContextUser
from src.presentation.api.v1.general import router as General
from src.presentation.api.v1.upload import router as Upload

# router = APIRouter(prefix="", dependencies=[Depends(verify_auth)])
router = APIRouter(prefix="", dependencies=[Depends(SetContextUser())])
router.include_router(General)
router.include_router(Upload)
