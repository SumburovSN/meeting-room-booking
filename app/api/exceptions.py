from fastapi import Request
from fastapi.responses import JSONResponse
from app.services.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    ForbiddenOperationError,
    InvalidCredentialsError,
    RoomNotFoundError,
    RoomAlreadyExistsError,
    InvalidRoomTimeSlotError,
    SlotAlreadyBookedError,
    BookingNotFoundError,
    InvalidBookingDateError,
    TimeSlotNotFoundError,
    TimeSlotOverlapError,
    InvalidTimeSlotError,
)


async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "User already exists"
        },
    )


async def forbidden_operation_handler(request: Request, exc: ForbiddenOperationError):
    return JSONResponse(
        status_code=403,
        content={
            "detail": "Forbidden"
        },
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "User not found"
        },
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid credentials"
        },
    )


async def room_not_found_handler(request: Request, exc: RoomNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Room not found"
        },
    )


async def room_already_exists_handler(request: Request, exc: RoomAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Room already exists"
        },
    )


async def invalid_room_time_slot_handler(request: Request, exc: InvalidRoomTimeSlotError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Time slot not found"
        },
    )


async def slot_already_booked_handler(request: Request, exc: SlotAlreadyBookedError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Time slot already booked"
        },
    )


async def booking_not_found_handler(request: Request, exc: BookingNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Booking not found"
        },
    )


async def invalid_booking_date_handler(request: Request, exc: InvalidBookingDateError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Booking date cannot be in the past"
        },
    )


async def time_slot_not_found_handler(request: Request, exc: TimeSlotNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Time slot not found"
        },
    )


async def time_slot_overlap_handler(request: Request, exc: TimeSlotOverlapError):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Time slot overlaps with existing slot"
        },
    )


async def invalid_time_slot_handler(request: Request, exc: InvalidTimeSlotError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Start time must be before end time"
        },
    )
