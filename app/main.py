from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.rooms import router as rooms_router
from app.api.bookings import router as booking_router
from app.api.time_slots import router as time_slot_router
from app.api.exceptions import (invalid_credentials_handler, user_already_exists_handler, forbidden_operation_handler,
                                user_not_found_handler, room_not_found_handler, room_already_exists_handler,
                                invalid_room_time_slot_handler, slot_already_booked_handler, booking_not_found_handler,
                                invalid_booking_date_handler, time_slot_overlap_handler, invalid_time_slot_handler)
from app.services.exceptions import (InvalidCredentialsError, UserAlreadyExistsError, ForbiddenOperationError,
                                     UserNotFoundError, RoomNotFoundError, RoomAlreadyExistsError,
                                     InvalidRoomTimeSlotError, SlotAlreadyBookedError, BookingNotFoundError,
                                     InvalidBookingDateError, TimeSlotOverlapError, InvalidTimeSlotError)


app = FastAPI(title="BookRoom")
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(booking_router)
app.include_router(time_slot_router)

app.add_exception_handler(InvalidCredentialsError, invalid_credentials_handler)
app.add_exception_handler(ForbiddenOperationError, forbidden_operation_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
app.add_exception_handler(RoomNotFoundError, room_not_found_handler)
app.add_exception_handler(RoomAlreadyExistsError, room_already_exists_handler)
app.add_exception_handler(InvalidRoomTimeSlotError, invalid_room_time_slot_handler)
app.add_exception_handler(SlotAlreadyBookedError, slot_already_booked_handler)
app.add_exception_handler(BookingNotFoundError, booking_not_found_handler)
app.add_exception_handler(InvalidBookingDateError, invalid_booking_date_handler)
app.add_exception_handler(TimeSlotOverlapError, time_slot_overlap_handler)
app.add_exception_handler(InvalidTimeSlotError, invalid_time_slot_handler)


@app.get("/")
def root():
    return RedirectResponse("/docs")