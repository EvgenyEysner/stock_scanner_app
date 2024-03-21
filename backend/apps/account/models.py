from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .permissions import set_group_permissions


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Nutzer:in")
        verbose_name_plural = _("Nutzer:innen")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email


class Employee(models.Model):
    class PermissionGroup(models.IntegerChoices):
        INSTALLER = 1, _("Monteur")
        TEAM_MANAGEMENT = 2, _("Teamleitung")
        STOCK_MANAGEMENT = 3, _("Lagerleitung")
        BACKOFFICE = 4, _("Backoffice")

    user = models.OneToOneField(
        User,
        verbose_name=User._meta.verbose_name,
        on_delete=models.CASCADE,
        related_name="employee",
    )

    # stock = models.ForeignKey(
    #     Stock,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Mitarbeiter im Lager"),
    #     related_name="employees",
    # )

    created_on = models.DateField(_("Erstellt am"), auto_now_add=True, editable=False)

    first_name = models.CharField(_("Vorname"), max_length=255)
    last_name = models.CharField(_("Nachname"), max_length=255)

    street = models.CharField(_("Straße"), max_length=255)
    street_no = models.CharField(_("Hausnummer"), max_length=255, blank=True)
    zip_code = models.CharField(_("PLZ"), max_length=5)
    city = models.CharField(_("Ort"), max_length=255)

    permission_group = models.PositiveSmallIntegerField(
        _("Berechtigungsgruppe"),
        choices=PermissionGroup.choices,
        default=PermissionGroup.BACKOFFICE,
    )

    phone_mobile = models.CharField(_("Handy"), max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(_("Geburtsdatum"))
    date_of_joining = models.DateField(_("Eintrittsdatum"), null=True, blank=True)
    date_of_leaving = models.DateField(_("Austrittsdatum"), null=True, blank=True)

    is_qualified = models.BooleanField(_("Qualifiziert?"))
    date_of_qualification = models.DateField(
        _("Zeitpunkt der Qualifizierung"), null=True, blank=True
    )

    # target_hours = models.PositiveSmallIntegerField(_("Sollstunden"))
    # hourly_wage = models.DecimalField(_("Stundenlohn"), max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["last_name"]
        verbose_name = _("Mitarbeiter")
        verbose_name_plural = _("Mitarbeiter")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

post_save.connect(set_group_permissions, sender=Employee)
