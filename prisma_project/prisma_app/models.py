from django.db import models
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    internal_id = models.IntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    hashed_password = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=50, default="USER")
    is_super_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    preferred_locale = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    address_line_1 = models.TextField(null=True, blank=True)
    address_house_number = models.TextField(null=True, blank=True)
    address_line_2 = models.TextField(null=True, blank=True)
    address_city = models.CharField(max_length=255, null=True, blank=True)
    address_post_code = models.CharField(max_length=20, null=True, blank=True)
    address_country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handle = models.CharField(max_length=255, unique=True)
    hashed_session_token = models.TextField(null=True, blank=True)
    anti_csrf_token = models.TextField(null=True, blank=True)
    public_data = models.TextField(null=True, blank=True)
    private_data = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hashed_token = models.TextField()
    token_type = models.CharField(max_length=255)
    note = models.TextField(null=True, blank=True)
    disabled = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    sent_to = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ApiAccessLog(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.ForeignKey(Token, on_delete=models.RESTRICT)
    action = models.CharField(max_length=255)
    success = models.BooleanField()
    comment = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    event_type_choices = [
        ('SamplePickupRequested', _('Sample Pickup Requested')),
        ('SubjectSubmitted', _('Subject Submitted')),
        ('CegatSampleRegistrationRequest', _('Cegat Sample Registration Request')),
        ('SampleBillingChanged', _('Sample Billing Changed')),
        ('SamplingMethodChanged', _('Sampling Method Changed')),
        ('SamplePurposeChanged', _('Sample Purpose Changed')),
        ('SampleTestTypeChanged', _('Sample Test Type Changed')),
        ('SampleWetLabChanged', _('Sample Wet Lab Changed')),
    ]
    type = models.CharField(max_length=255, choices=event_type_choices)
    event_time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    subject_id = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='organisations')

class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new_report_available = models.CharField(max_length=50, default='Email')
    new_sample_event = models.CharField(max_length=50, default='Email')
    subject_file_upload = models.CharField(max_length=50, default='Email')



class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    internal_id = models.IntegerField(unique=True)
    version_number = models.IntegerField(default=1)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='subjects')
    office_unit = models.ForeignKey('OfficeUnit', null=True, on_delete=models.SET_NULL)
    status_choices = [
        ('Draft', 'Draft'),
        ('Declared', 'Declared'),
        ('Submitted', 'Submitted'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Draft')
    wizard_step_choices = [
        ('PersonalInfo', 'Personal Info'),
        ('FamilyHistory', 'Family History'),
        ('ClinicalInfo', 'Clinical Info'),
        ('PhysicalInfo', 'Physical Info'),
        ('Summary', 'Summary'),
        ('Completed', 'Completed'),
    ]
    wizard_step = models.CharField(max_length=50, choices=wizard_step_choices, default='PersonalInfo')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name or str(self.id)


class SubjectFile(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='files')
    is_pedigree = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)  # This remains the primary key
    arcensus_order_id = models.IntegerField(unique=True)  # Change from AutoField to IntegerField
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.arcensus_order_id}"


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    device_id = models.CharField(max_length=255, unique=True)
    subject = models.ForeignKey('Subject', null=True, on_delete=models.SET_NULL, related_name='samples')
    test_type_choices = [
        ('WholeGenomeSequencing', 'Whole Genome Sequencing'),
        ('WholeExomeSequencing', 'Whole Exome Sequencing'),
        ('SangerOnHold', 'Sanger On Hold'),
    ]
    test_type = models.CharField(max_length=50, choices=test_type_choices, default='SangerOnHold')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.device_id



class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    type_choices = [
        ('myLifeHeart', 'My Life Heart'),
        ('myLifeGenome', 'My Life Genome'),
        ('myLifeCancer', 'My Life Cancer'),
        ('myLifeExome', 'My Life Exome'),
        ('sangerSequencing', 'Sanger Sequencing'),
        ('sangerOnHold', 'Sanger On Hold'),
        ('researchWES', 'Research WES'),
        ('researchWGS', 'Research WGS'),
    ]
    type = models.CharField(max_length=50, choices=type_choices)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.type}"


class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='reports')
    uploader = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='uploaded_reports')
    order = models.ForeignKey('Order', null=True, on_delete=models.RESTRICT, related_name='reports')
    report_type_choices = [
        ('Diagnostics', 'Diagnostics'),
        ('Update', 'Update'),
        ('Correction', 'Correction'),
        ('FailedAnalysis', 'Failed Analysis'),
        ('NegativeFollowUp', 'Negative Follow Up'),
        ('RawData', 'Raw Data'),
        ('DataAnalysis', 'Data Analysis'),
        ('Research', 'Research'),
    ]
    report_type = models.CharField(max_length=50, choices=report_type_choices, null=True, blank=True)
    test_type_choices = [
        ('WholeGenomeSequencing', 'Whole Genome Sequencing'),
        ('WholeExomeSequencing', 'Whole Exome Sequencing'),
        ('SangerOnHold', 'Sanger On Hold'),
    ]
    test_type = models.CharField(max_length=50, choices=test_type_choices, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    file_type_choices = [
        ('PDF', 'PDF'),
        ('JSON', 'JSON'),
    ]
    file_type = models.CharField(max_length=50, choices=file_type_choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report {self.file_name}"


class SubjectShare(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='shared_subjects')
    access_type_choices = [
        ('Read', 'Read'),
        ('ReadWrite', 'Read & Write'),
    ]
    access_type = models.CharField(max_length=50, choices=access_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subject Share {self.id}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    subject = models.ForeignKey('Subject', null=True, on_delete=models.SET_NULL, related_name='payments')
    status_choices = [
        ('Initiated', 'Initiated'),
        ('Failed', 'Failed'),
        ('OK', 'OK'),
    ]
    status = models.CharField(max_length=50, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"


class FinanceSetting(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    version_number = models.IntegerField(default=1)
    test_type_choices = [
        ('WholeGenomeSequencing', 'Whole Genome Sequencing'),
        ('WholeExomeSequencing', 'Whole Exome Sequencing'),
        ('SangerOnHold', 'Sanger On Hold'),
    ]
    test_type = models.CharField(max_length=50, choices=test_type_choices)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='finance_settings')
    test_available = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)  # Price in smallest currency unit (e.g., cents for EUR)
    currency_choices = [
        ('EUR', 'Euro'),
        ('USD', 'US Dollar'),
    ]
    currency = models.CharField(max_length=50, choices=currency_choices)
    samples = models.ManyToManyField('Sample', related_name='finance_settings')
    creator = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='created_finance_settings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Finance Setting {self.id} - {self.test_type}"


class OfficeUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    name = models.CharField(max_length=255)
    address_line_1 = models.TextField()
    address_house_number = models.TextField(null=True, blank=True)
    address_line_2 = models.TextField(null=True, blank=True)
    address_city = models.CharField(max_length=255)
    address_post_code = models.CharField(max_length=20)
    address_country = models.CharField(max_length=100)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, related_name='office_units')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
