from .register import router as register_router
from .control import router as control_router
from .schedule import router as schedule_router
from .notifications import router as notifications_router
from .state import router as state_router
from .analytics import router as analytics_router
from .reference import router as reference_router
from ai.handlers import router as ai_router
from .graphs import router as graphs_router


routers = [
    register_router,
    control_router,
    schedule_router,
    notifications_router,
    state_router,
    analytics_router,
    reference_router,
    ai_router,
    graphs_router
]
