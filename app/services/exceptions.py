class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class ForbiddenOperationError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class RoomNotFoundError(Exception):
    pass


class RoomAlreadyExistsError(Exception):
    pass


class BookingNotFoundError(Exception):
    pass


class SlotAlreadyBookedError(Exception):
    pass


class InvalidRoomTimeSlotError(Exception):
    pass


class InvalidBookingDateError(Exception):
    pass


class TimeSlotNotFoundError(Exception):
    pass


class TimeSlotOverlapError(Exception):
    pass


class InvalidTimeSlotError(Exception):
    pass
