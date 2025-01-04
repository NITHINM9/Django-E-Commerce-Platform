from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.db import transaction
from .models import UserActivity
import logging

class LogUserActivityMiddleware(MiddlewareMixin):
    logger = logging.getLogger(__name__)

    def process_request(self, request):
        if request.user.is_authenticated:
            self.logger.info(f"Processing login for {request.user.username}")
            existing_activity = UserActivity.objects.filter(
                user=request.user,
                logout_time=None  
            ).first()

            if existing_activity is None:
                activity = UserActivity(
                    user=request.user,
                    login_time=now(),
                    username=request.user.username
                )
                activity.save()
                self.logger.info(f"User {request.user.username} logged in at {activity.login_time}.")
    
    def process_response(self, request, response):
        self.logger.info(f"Processing response for user {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        return response


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger = logging.getLogger(__name__)
    
    print(f"Logout signal received for user {user.username}")

    with transaction.atomic():
        try:
            activity = UserActivity.objects.filter(
                user=user, 
                logout_time=None  
            ).latest('login_time')
            
            # Update the logout time
            activity.logout_time = now()
            activity.save()

            print(f"Logout time recorded for user {user.username} at {activity.logout_time}")
            logger.info(f"Logout time recorded for user {user.username} at {activity.logout_time}")

        except UserActivity.DoesNotExist:
            print(f"No active session found for user {user.username}")
            logger.warning(f"No active session found for user {user.username} during logout.")
        except Exception as e:
            print(f"Error logging out user {user.username}: {str(e)}")
            logger.error(f"An error occurred while logging out {user.username}: {str(e)}")
