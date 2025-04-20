from django.db.models import TextChoices


class ObjectStatuses(TextChoices):
    IN_PROCESS = 'IN_PROCESS'
    FINISHED = 'FINISHED'


class ObjectRoomStatuses(TextChoices):
    SOLD = 'SOLD'
    NOT_SOLD = 'NOT_SOLD'


class ApplicationStatuses(TextChoices):
    NEW = 'NEW'
    OLD = 'OLD'


block_numbers = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
)

block_numbers_list = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15"
]
