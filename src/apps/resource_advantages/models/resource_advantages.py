from django.db import models

class ResourceAdvantages(models.Model):

    CATEGORY_CHOICES = (
        ('MONTANT_FIXE','Montant Fixe'),
        ('PRET','Prêt'),
    )
    FREQUENCY = (
        ('PONCTUELLE','Ponctuelle'),
        ('JOURNALIERE','Journalière'),
        ('MENSUELLE','Mensuelle'),
        ('TRIMESTRIELLE','Trimestrielle'),
        ('SEMSTRIELLE','Semestrielle'),
        ('ANNUELLE','Annuelle'),
    )
    name = models.CharField(max_length=20, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0], max_length=20, null=True)
    frequency = models.CharField(choices=FREQUENCY, default=FREQUENCY[0][0], max_length=20, null=True)
    is_montant_fixe = models.BooleanField(default=False, null=True)
    load_rate = models.DecimalField(decimal_places=2, max_digits=2, null=True)
