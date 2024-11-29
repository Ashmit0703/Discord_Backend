from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    """
    Create a default admin user if no admin exists after database migration.
    """
    User = get_user_model()
    
    # Check if any admin users exist
    if not User.objects.filter(role='admin').exists():
        # Create admin user from environment variables or with default credentials
        admin_username = getattr(settings, 'DEFAULT_ADMIN_USERNAME', 'admin')
        admin_email = getattr(settings, 'DEFAULT_ADMIN_EMAIL', 'admin@example.com')
        admin_password = getattr(settings, 'DEFAULT_ADMIN_PASSWORD', 'adminpassword123')
        
        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            role='admin'
        )
        print(f"Default admin user '{admin_username}' created.")