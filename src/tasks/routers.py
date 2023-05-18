from fastapi import APIRouter, Depends

from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix='/reports')


@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        'status': 200,
        'data': 'Письмо отправлено',
        'details': None
    }


# '''Реализация без использования селери'''
# @router.get('/dashboard')
# def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
#     background_tasks.add_task(send_email_report_dashboard, user.username)
#     return {
#         'status': 200,
#         'data': 'Письмо отправлено',
#         'details': None
#     }
