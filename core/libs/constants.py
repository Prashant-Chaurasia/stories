from enum import Enum

default_duration = 86400

class State(Enum):
  UPLOADED = "UPLOADED"
  PROCESSED = "PROCESSED"