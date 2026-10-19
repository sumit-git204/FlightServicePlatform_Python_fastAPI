class AppException(Exception):
    status_code = 400

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BookingNotFoundError(AppException):
    status_code = 404


class UserNotFoundError(AppException):
    status_code = 404   


class FlightNotFoundError(AppException):
    status_code = 404


class SeatNotAvailableError(AppException):
    status_code = 400


class BookingAlreadyCancelledError(AppException):
    status_code = 400


class BookingAlreadyConfirmedError(AppException):
    status_code = 400

