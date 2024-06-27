from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager


# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(
        User, related_name="projects",
        on_delete=models.DO_NOTHING
    )
    name_project = models.CharField(max_length=50)
    descripton = models.CharField(max_length=1000)
    git_link = models.CharField(null=True, blank=True, max_length=200)
    project_image = models.ImageField(null=True, blank=True, upload_to="projectimages/")
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followed_by",
                                     symmetrical=False,
                                     blank=True,)
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    profile_image = models.ImageField(null=True, blank=True, upload_to="userimages/")
    git_link = models.CharField(null=True, blank=True, max_length=150)
    linledin_link = models.CharField(null=True, blank=True, max_length=150)

    def __str__(self):
        return self.user.username


# Create Profile when new user signs up
# @receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()
#         Have users follows themselfs
        user_profile.follows.set([instance.userprofile.id])
        user_profile.save()


post_save.connect(create_profiles, sender=User)

