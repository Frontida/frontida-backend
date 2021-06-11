from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None):
        if email is None:
            raise TypeError("User should have a email")

        user = self.model(email=self.normalize_email(email), user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if email is None:
            raise TypeError("User should have a email")
        if password is None:
            raise TypeError("Password should not be none")
        user = self.create_user(email, "ADMIN", password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
