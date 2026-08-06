from app.config import settings
from datetime import timedelta

print(timedelta(hours=settings.JWT_EXPIRY_HOURS))
