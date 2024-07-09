from fastapi import APIRouter
from .user import router as userd
from .subvenciones import router as subv
from .empresas import router as empr
from .projects import router as proj
from .settings import router as sett
# from .ofertas import router as ofrt
# from .evaluaciones import router as evalua

router = APIRouter()
router.include_router(userd)
router.include_router(subv)
router.include_router(empr)
router.include_router(proj)
router.include_router(sett)
#router.include_router(ofrt)
#router.include_router(evalua)