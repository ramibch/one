from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from djstripe.models import Event
from plans.models import PremiumPlan
from users.models import User, UserPremiumPlan
from utils.email import send_simple_email

EMAIL_BODY_THANKS = _(
    """Hi,

Thank you for your order!

If you have any questions or you require any technical support,
you can contact me directly to this email!

Best wishes!
Rami (nicecv.online)
"""
)


@receiver(post_save, sender=Event)
def process_stripe_event(sender, instance, created, **kwargs):
    proceed = (
        instance.type == "checkout.session.completed"
        and "plan_id"
        and "user_id" in instance.data["object"]["metadata"]
    )

    if not proceed:
        return

    plan_id = int(instance.data["object"]["metadata"]["plan_id"])
    user_id = int(instance.data["object"]["metadata"]["user_id"])

    try:
        user = User.objects.get(id=user_id)
        plan = PremiumPlan.objects.get(id=plan_id)
    except (User.DoesNotExist, PremiumPlan.DoesNotExist):
        return

    userplan = UserPremiumPlan.objects.create(plan=plan, user=user)

    subject = "Nice CV | " + _("Welcome")
    send_simple_email(subject=subject, body=EMAIL_BODY_THANKS, to=userplan.user.email)
