from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Common model for all table
class CommonModel(models.Model):
    # A timestamp representing when this object was created.
    created_date = models.DateTimeField(auto_now_add=True)
    # A timestamp reprensenting when this object was last updated.
    updated_date = models.DateTimeField(auto_now=True)

    created_by = models.CharField(max_length=50, blank=True)
    updated_by = models.CharField(max_length=50, blank=True)
    class Meta:
        abstract = True

        # By default, any model that inherits from `CommonModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-updated_date', '-created_date']

# Create your models here.
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password,
                    created_by='', updated_by='', user_type='', first_name='', last_name=''):
        user = self.model(username=username,
                          email=self.normalize_email(email),
                          user_type=user_type,
                          created_by=created_by,
                          updated_by=updated_by,
                          first_name=first_name,
                          last_name=last_name
                          )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password,
                        created_by='', updated_by='', user_type = ''):
      """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password, created_by='admin', updated_by='admin', user_type='Admin', first_name=username, last_name=username)
      user.is_superuser = True
      user.status = True
      # user.user_type = "Admin"
      user.save()

      return user

    # def create_user(self, username, email, password=None):
    #     """Create and return a `User` with an email, username and password."""
    #     if username is None:
    #         raise TypeError('Users must have a username.')
    #
    #     if email is None:
    #         raise TypeError('Users must have an email address.')
    #
    #     user = self.model(username=username, email=self.normalize_email(email))
    #     user.set_password(password)
    #     user.save()
    #
    #     return user
    #
    # def create_superuser(self, username, email, password):
    #     """
    #     Create and return a `User` with superuser powers.
    #
    #     Superuser powers means that this use is an admin that can do anything
    #     they want.
    #     """
    #     if password is None:
    #         raise TypeError('Superusers must have a password.')
    #
    #     user = self.create_user(username, email, password)
    #     user.is_superuser = True
    #     user.is_staff = True
    #     user.save()
    #
    #     return user


#Create your models here.
class User(AbstractUser, CommonModel):
    ADMIN = 'Admin'
    HR = 'HR'
    EMPLOYEE = 'Employee'
    MANAGEMENT = 'Management'
    TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (HR, 'HR'),
        (EMPLOYEE, 'Employee'),
        (MANAGEMENT, 'Management')
    )

    user_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=EMPLOYEE,
    )
    email = models.EmailField(db_index=True, unique=True)
    objects = UserManager()
    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.first_name + "-" +self.username