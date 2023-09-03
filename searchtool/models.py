from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Tag(models.Model):
    tag_title = models.CharField(max_length=30, verbose_name="Tags")

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Database(models.Model):
    keyword = models.CharField(max_length=100, verbose_name="Keyword")
    description = models.CharField(max_length=300, verbose_name="Description")
    prob_quest = models.CharField(max_length=300, verbose_name="Probing questions")
    view_search = models.CharField(max_length=120, verbose_name="Search in view")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        tags = [i.tag_title for i in self.tags.all()]

        return "Keyword: {0} | Description: {1} | Probing questions: {2} | Search in view: {3} | Tags: {4}".format(self.keyword, self.description, self.prob_quest, self.view_search, tags)

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"

class UserManager(BaseUserManager):
    # Create user
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
            return user
    # vytvori admina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user

class User(AbstractBaseUser):

    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True