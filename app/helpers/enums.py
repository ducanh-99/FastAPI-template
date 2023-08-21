from enum import Enum


class StateBookingRequest(Enum):
    pending = "pending"
    accept = "accept"
    cancel_by_parent = "cancel_by_parent"
    cancel_by_tutor = "cancel_by_tutor"
    all = "all"


class DayOfWeek(Enum):
    MONDAY = "Thứ 2"
    TUESDAY = "Thứ 3"
    WEDNESDAY = "Thứ 4"
    THURSDAY = "Thứ 5"
    FRIDAY = "Thứ 6"
    SATURDAY = "Thứ 7"
    SUNDAY = "Chủ Nhật"


class ClassEnum(Enum):
    LOP_1 = "Lớp 1"
    LOP_2 = "Lớp 2"
    LOP_3 = "Lớp 3"
    LOP_4 = "Lớp 4"
    LOP_5 = "Lớp 5"
    LOP_6 = "Lớp 6"
    LOP_7 = "Lớp 7"
    LOP_8 = "Lớp 8"
    LOP_9 = "Lớp 9"
    LOP_10 = "Lớp 10"
    LOP_11 = "Lớp 11"
    LOP_12 = "Lớp 12"
    Other = "Other"


class EventStatusUpdate(Enum):
    Confirmed = "Confirmed"
    Cancelled = "Cancelled"
    InProgress = "InProgress"
    Completed = "Completed"


class PaymentStatusRequest(Enum):
    Paid = "Paid"
    Unpaid = "Unpaid"


class TitleNotification(Enum):
    parent_booking_accept = "Gia sư đã xác nhận đặt lịch của bạn"
    tutor_booking_accept = "Bạn đã xác nhận đặt lịch"

    parent_booking_created = "Bạn đã tạo một lời mời gia sư"
    other_parent_booking_created = "Vợ/Chồng bạn đã tạo một lời mời gia sư"
    tutor_booking_created = "Bạn nhận được một lời mời từ phụ huynh"

    parent_booking_cancel_by_parent = "Bạn đã huỷ một lời mời gia sư"
    tutor_booking_cancel_by_parent = "Bạn đã bị huỷ một lời mời từ phụ huynh"

    parent_booking_cancel_by_tutor = "Gia sư đã huỷ một lời mời"
    tutor_booking_cancel_by_tutor = "Bạn đã huỷ một lời mời từ phụ huynh"

    parent_booking_start_event = "Buổi học của con đã được bắt đầu"
    tutor_booking_start_event = "Buổi dạy của bạn đã được bắt đầu"

    parent_booking_finish_event = "Buổi học của con đã kết thúc"
    tutor_booking_finis_event = "Buổi dạy của bạn đã kết thúc"

    parent_payment_order = "Gia sư đã tạo một yêu cầu thanh toán cho bạn"

    parent_payment_paid = "Bạn đã thanh toán một kỳ cho gia sư"
    tutor_payment_paid = "Bạn đã được thanh toán từ phụ huynh"

    event_booking_will_start = "Buổi học sắp bắt đầu"
    event_regular_will_start = "Một sự kiện của bạn sắp bắt đầu"


