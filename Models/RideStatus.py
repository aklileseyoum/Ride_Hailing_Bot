from enum import Enum

class RideStatus(Enum):
    ACCEPTED = 'accepted'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    REQUESTED = 'requested'
    IN_PROGRESS = 'in_progress'