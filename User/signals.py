from User.models import *
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.is_staff==True:
            StaffUser.objects.create(user=instance)
        if instance.is_partner==True:
            Partner.objects.create(user=instance)
        if instance.is_customer==True:
            Customer.objects.create(user=instance)    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    if instance.is_staff==True:
        instance.staffuser.save()
    if instance.is_partner==True:
        instance.partner.save()
    if instance.is_customer==True:
        instance.customer.save()