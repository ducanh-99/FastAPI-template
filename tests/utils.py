from sqlalchemy.orm import Session

from app.db.provider import Provider
from app.helpers.fcm_utils import FcmAbstract
from app.i18n.lang import MultiLanguage
from app.repositories.areas_repo import AreaRepository
from app.repositories.booking_repo import BookingRepository
from app.repositories.device_repo import DeviceRepository
from app.repositories.grade_repo import GradeRepository
from app.repositories.notification_repo import NotificationRepository
from app.repositories.otp_repo import OTPRepository
from app.repositories.parent_repo import ParentRepository
from app.repositories.studen_parent_repo import StudentParentRepository
from app.repositories.student_repo import StudentRepository
from app.repositories.subject_repo import SubjectRepository
from app.repositories.tutor_repo import TutorRepository
from app.repositories.tutor_subject_repo import TutorSubjectRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.fcm_service import FcmService
from app.services.notification_service import NotificationService


def create_auth_service(db_session: Session):
    return AuthService(
        MultiLanguage(),
        Provider(db_session, MultiLanguage()),
        UserRepository(db_session),
        OTPRepository(db_session),
        TutorRepository(db_session),
        TutorSubjectRepository(db_session),
        StudentRepository(db_session),
        ParentRepository(db_session),
        StudentParentRepository(db_session),
        GradeRepository(db_session),
        AreaRepository(db_session),
        SubjectRepository(db_session),
        BookingRepository(db_session),
    )


def create_notification_service_test(db_session: Session):
    notification_service = NotificationService(
        lang=MultiLanguage(),
        provider=Provider(db_session, MultiLanguage()),
        notification_repo=NotificationRepository(db_session),
        booking_repo=BookingRepository(db_session),
        fcm_service=FcmService(DeviceRepository(db_session), FcmAbstract())
    )
    return notification_service
