from django.db import models

class Coupon(models.Model):

    class Types(models.TextChoices):
        '''
        Coupon Types
        '''
        FLAT = "FLAT", "Flat"
        PERCENTAGE = "PERCENTAGE", "Percentage"

    class Status(models.TextChoices):
        """
        Coupon Status
        """
        APPROVED = "APPROVED", "Approved"
        PENDING = "PENDING", "Pending"

    base_type = Types.FLAT
    base_status = Status.PENDING

    coupon_code = models.CharField(
        verbose_name="Coupon Code", max_length=50, null=False, blank=False)

    expiry_date = models.DateTimeField(
        verbose_name="Expires Date Time", null=True, blank=True)
    type = models.CharField(
        verbose_name="Type", max_length=50, choices=Types.choices, default=base_type)

    offer_value = models.FloatField(verbose_name="Offer Value", default=0)
    coupon_description = models.TextField(verbose_name="Description", null=True, blank=True)

    status = models.CharField(
        verbose_name="Status", max_length=50, choices=Status.choices, default=base_status)

    class Meta:
        db_table = 'coupon'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-offer_value']

    def __str__(self):
        return str(self.coupon_code + "  " +"(" + self.status + ")")