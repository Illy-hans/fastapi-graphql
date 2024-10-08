from .user_model import User
from .interest_model import Interest
from .user_interest import UserInterest
from .balance_model import Balance

# This ensures all models are imported and initialised
__all__ = ["User", "Interest", "UserInterest", "Balance"]

