"""Models"""

import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
# from django.contrib.auth.models import Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from sorl.thumbnail import ImageField
from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from universal.media_handlers import save_avatar

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    is_active = models.BooleanField(default=False) # activate by email
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "User - {}".format(self.email)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def prof(self):
        return self.siteuser.screen_name

class Role(TimeStampedModel):
    role = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['role']

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse('siteuser:role_index')

class SiteUser(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = AutoSlugField(set_using="screen_name")
    roles = models.ManyToManyField(Role)
    screen_name = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = ImageField(upload_to=save_avatar, null=True, blank=True)

    quota = models.IntegerField(default=100)
    used = models.IntegerField(default=0)
    key = models.CharField(max_length=50, default=uuid.uuid4, null=True, blank=True, unique=True)

    class Meta:
        ordering = ['screen_name']
        verbose_name_plural = 'siteusers'

    @property
    def remaining_quota(self):
        return self.quota - self.used

    def __str__(self):
        return self.screen_name

    def get_absolute_url(self):
        return reverse('siteuser:detail', args=[str(self.id), str(self.slug)])

    def get_user_success_url(self):
        return reverse()

    def get_user_creation_url(self):
        return reverse('siteuser:new_activation', args=[str(self.user.id), str(self.screen_name)])

    def get_all_roles(self):
        return ", ".join([role.role for role in self.roles.all()])

class SiteUserGroup(TimeStampedModel):
    name = models.CharField(max_length=30, blank=True, null=True)
    about_group = models.TextField()
    group_social = models.URLField(blank=True, null=True)
    members = models.ManyToManyField(SiteUser, through='GroupMembership')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('siteuser:group_detail', kwargs={'pk' : self.pk})

class GroupMembership(TimeStampedModel):
    siteuser = models.ForeignKey(SiteUser, blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(SiteUserGroup, blank=True, null=True, on_delete=models.SET_NULL)
    is_group_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name + " membership"

    def get_absolute_url(self):
        return reverse('siteuser:group_detail', kwargs={'pk' : self.group.pk})

class GroupJoinRequest(TimeStampedModel):
    requesting_user = models.ForeignKey(SiteUser, null=True, blank=True, on_delete=models.SET_NULL)
    group_of_interest = models.ForeignKey(SiteUserGroup, null=True, blank=True, on_delete=models.SET_NULL)

class Follow(TimeStampedModel):
    from_siteuser = models.ForeignKey(SiteUser, blank=True, null=True, on_delete=models.SET_NULL, related_name="from_siteuser_set")
    to_siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name="to_siteuser_set")
