# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DueappDeactivatingdue(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=355)
    is_for_excos = models.BooleanField()
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    starttime = models.TimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    month = models.IntegerField()
    chapters = models.ForeignKey('AccountChapters', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dueapp_deactivatingdue'


class DueappDeactivatingdueUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_overdue = models.BooleanField()
    is_paid = models.BooleanField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_key = models.TextField()
    deactivatingdue = models.ForeignKey(DueappDeactivatingdue, models.DO_NOTHING)
    user = models.ForeignKey('AccountUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dueapp_deactivatingdue_user'


class DueappDue(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=355)  # Field name made lowercase.
    re_occuring = models.BooleanField()
    is_for_excos = models.BooleanField()
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    startdate = models.DateField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    starttime = models.TimeField(db_column='startTime', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    scheduletype = models.CharField(max_length=200)
    schedule = models.JSONField(blank=True, null=True)
    alumni_year = models.DateField(blank=True, null=True)
    is_on_create = models.BooleanField()
    chapters = models.ForeignKey('AccountChapters', models.DO_NOTHING, blank=True, null=True)
    dues_for_membership_grade = models.ForeignKey('AccountMembershipgrade', models.DO_NOTHING, blank=True, null=True)
    endtime = models.TimeField(db_column='endTime', blank=True, null=True)  # Field name made lowercase.
    is_deactivate_users = models.BooleanField()
    exco = models.ForeignKey('AccountExcorole', models.DO_NOTHING, blank=True, null=True)
    item_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'Dueapp_due'


class DueappDueUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_overdue = models.BooleanField()
    is_paid = models.BooleanField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_key = models.TextField()
    due = models.ForeignKey(DueappDue, models.DO_NOTHING)
    user = models.ForeignKey('AccountUser', models.DO_NOTHING, blank=True, null=True)
    item_code = models.TextField()

    class Meta:
        managed = False
        db_table = 'Dueapp_due_user'


class Rel8TenantClient(models.Model):
    id = models.BigAutoField(primary_key=True)
    schema_name = models.CharField(unique=True, max_length=63)
    timezone = models.CharField(max_length=63)
    name = models.CharField(max_length=100)
    paystack_publickey = models.TextField()
    paystack_secret = models.TextField()
    paid_until = models.DateTimeField()
    on_trial = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    owner = models.CharField(max_length=254)
    payment_plan = models.CharField(max_length=25)
    flutterwave_publickey = models.TextField()
    flutterwave_secret = models.TextField()

    class Meta:
        managed = False
        db_table = 'Rel8Tenant_client'


class Rel8TenantDomain(models.Model):
    id = models.BigAutoField(primary_key=True)
    domain = models.CharField(unique=True, max_length=253)
    is_primary = models.BooleanField()
    tenant = models.ForeignKey(Rel8TenantClient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Rel8Tenant_domain'


class Rel8TenantFinancialAndNonfinancialmembersrecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    file = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=400)
    for_financial = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Rel8Tenant_financial_and_nonfinancialmembersrecord'


class Rel8TenantPeriodictasktenantlink(models.Model):
    id = models.BigAutoField(primary_key=True)
    use_tenant_timezone = models.BooleanField()
    periodic_task = models.OneToOneField('DjangoCeleryBeatPeriodictask', models.DO_NOTHING)
    tenant = models.ForeignKey(Rel8TenantClient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Rel8Tenant_periodictasktenantlink'


class AccountAdmin(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    user = models.OneToOneField('AccountUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_admin'


class AccountChapters(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_chapters'


class AccountCommiteegroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    team_of_reference = models.CharField(max_length=100, blank=True, null=True)
    commitee_todo = models.JSONField(blank=True, null=True)
    commitee_duties = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_commiteegroup'


class AccountCommiteegroupMembers(models.Model):
    id = models.BigAutoField(primary_key=True)
    commiteegroup = models.ForeignKey(AccountCommiteegroup, models.DO_NOTHING)
    memeber = models.ForeignKey('AccountMemeber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_commiteegroup_members'
        unique_together = (('commiteegroup', 'memeber'),)


class AccountCommiteepostion(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_of_postion = models.CharField(unique=True, max_length=200)
    duties = models.JSONField()
    commitee_group = models.ForeignKey(AccountCommiteegroup, models.DO_NOTHING)
    member = models.ForeignKey('AccountMemeber', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_commiteepostion'


class AccountExcorole(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    about = models.TextField()
    can_upload_min = models.BooleanField()
    chapter = models.ForeignKey(AccountChapters, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_excorole'


class AccountExcoroleMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    excorole = models.ForeignKey(AccountExcorole, models.DO_NOTHING)
    memeber = models.ForeignKey('AccountMemeber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_excorole_member'
        unique_together = (('excorole', 'memeber'),)


class AccountMembereducation(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_of_institution = models.TextField()
    major = models.TextField()
    degree = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    reading = models.CharField(max_length=50)
    speaking = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    member = models.ForeignKey('AccountMemeber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_membereducation'


class AccountMemberemploymenthistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    postion_title = models.CharField(max_length=200)
    employment_from = models.DateField(blank=True, null=True)
    employment_to = models.DateField(blank=True, null=True)
    employer_name_and_addresse = models.CharField(max_length=200)
    member = models.ForeignKey('AccountMemeber', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_memberemploymenthistory'


class AccountMembershipgrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    chapter = models.ForeignKey(AccountChapters, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_membershipgrade'


class AccountMembershipgradeMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    membershipgrade = models.ForeignKey(AccountMembershipgrade, models.DO_NOTHING)
    memeber = models.ForeignKey('AccountMemeber', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_membershipgrade_member'
        unique_together = (('membershipgrade', 'memeber'),)


class AccountMemeber(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount_owing = models.DecimalField(max_digits=19, decimal_places=4)
    is_exco = models.BooleanField()
    is_financial = models.BooleanField()
    alumni_year = models.DateField()
    telephone_number = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField(blank=True, null=True)
    citizenship = models.CharField(max_length=24)
    user = models.OneToOneField('AccountUser', models.DO_NOTHING)
    bio = models.TextField()
    has_updated = models.BooleanField()
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    yog = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'account_memeber'


class AccountSecondleveldatabase(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_secondleveldatabase'


class AccountSuperAdmin(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    user = models.OneToOneField('AccountUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_super_admin'


class AccountUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=254)
    is_invited = models.BooleanField()
    is_active = models.BooleanField()
    photo = models.CharField(max_length=100, blank=True, null=True)
    is_member = models.BooleanField()
    is_staff = models.BooleanField()
    user_type = models.CharField(max_length=25)
    is_superuser = models.BooleanField()
    temp_password = models.TextField(blank=True, null=True)
    usersecret = models.TextField(db_column='userSecret')  # Field name made lowercase.
    username = models.TextField(db_column='userName')  # Field name made lowercase.
    chapter = models.ForeignKey(AccountChapters, models.DO_NOTHING, blank=True, null=True)
    is_prospective_member = models.BooleanField(db_column='is_prospective_Member')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account_user'


class AccountUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_groups'
        unique_together = (('user', 'group'),)


class AccountUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AccountUsermemberinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250, blank=True, null=True)
    member = models.ForeignKey(AccountMemeber, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_usermemberinfo'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AccountUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class ChatChat(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    chat_room = models.ForeignKey('ChatChatroom', models.DO_NOTHING)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_chat'


class ChatChatroom(models.Model):
    id = models.BigAutoField(primary_key=True)
    room_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'chat_chatroom'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.BooleanField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsChordcounter(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    sub_tasks = models.TextField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsGroupresult(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    date_created = models.DateTimeField()
    date_done = models.DateTimeField()
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_groupresult'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MeetingMeeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    details = models.TextField()
    date_for = models.DateTimeField(blank=True, null=True)
    addresse = models.TextField()
    event_date = models.DateTimeField(blank=True, null=True)
    organisername = models.CharField(db_column='organiserName', max_length=400)  # Field name made lowercase.
    organiserdetails = models.CharField(db_column='organiserDetails', max_length=400)  # Field name made lowercase.
    organiserimage = models.CharField(db_column='organiserImage', max_length=100, blank=True, null=True)  # Field name made lowercase.
    chapters = models.ForeignKey(AccountChapters, models.DO_NOTHING, blank=True, null=True)
    commitee = models.ForeignKey(AccountCommiteegroup, models.DO_NOTHING, blank=True, null=True)
    exco = models.ForeignKey(AccountExcorole, models.DO_NOTHING, blank=True, null=True)
    membership_grade = models.ForeignKey(AccountMembershipgrade, models.DO_NOTHING, blank=True, null=True)
    meeting_docs = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting_meeting'


class MeetingMeetingapology(models.Model):
    id = models.BigAutoField(primary_key=True)
    note = models.TextField()
    meeting = models.ForeignKey(MeetingMeeting, models.DO_NOTHING, blank=True, null=True)
    members = models.ForeignKey(AccountMemeber, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_meetingapology'


class MeetingMeetingattendies(models.Model):
    id = models.BigAutoField(primary_key=True)
    meeting = models.ForeignKey(MeetingMeeting, models.DO_NOTHING, blank=True, null=True)
    members = models.ForeignKey(AccountMemeber, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_meetingattendies'


class MeetingMeetingproxyattendies(models.Model):
    id = models.BigAutoField(primary_key=True)
    participants = models.JSONField()
    meeting = models.ForeignKey(MeetingMeeting, models.DO_NOTHING)
    member = models.ForeignKey(AccountMemeber, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_meetingproxyattendies'


class MeetingMeetingreshedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    request_reschedule_date = models.DateTimeField(blank=True, null=True)
    meeting = models.ForeignKey(MeetingMeeting, models.DO_NOTHING, blank=True, null=True)
    members = models.ForeignKey(AccountMemeber, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_meetingreshedule'


class NotificationsNotification(models.Model):
    level = models.CharField(max_length=20)
    unread = models.BooleanField()
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.BooleanField()
    action_object_content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    actor_content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    recipient = models.ForeignKey(AccountUser, models.DO_NOTHING)
    target_content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    deleted = models.BooleanField()
    emailed = models.BooleanField()
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications_notification'


class ProspectivememberAdminsetpropectivemembershiprule(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    propective_members_text_fields = models.JSONField(blank=True, null=True)
    propective_members_file_fields = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prospectivemember_adminsetpropectivemembershiprule'


class ProspectivememberManprospectivememberformone(models.Model):
    id = models.BigAutoField(primary_key=True)
    cac_registration_number = models.TextField()
    name_of_company = models.CharField(max_length=600)
    tax_identification_number = models.TextField()
    corporate_office_addresse = models.TextField()
    office_bus_stop = models.TextField()
    office_city = models.TextField()
    office_lga = models.TextField()
    office_state = models.CharField(max_length=300)
    postal_addresse = models.CharField(max_length=300)
    telephone = models.CharField(max_length=13)
    email_addresse = models.CharField(max_length=254)
    website = models.CharField(max_length=200)
    factoru_details = models.TextField()
    legal_status_of_company = models.CharField(max_length=100)
    number_of_female_expatriates = models.IntegerField()
    number_of_male_expatriates = models.IntegerField()
    local_share_capital = models.TextField()
    foreign_share_capital = models.TextField()
    ownership_structure_equity_local = models.TextField()
    ownership_structure_equity_foregin = models.TextField()
    total_value_of_land_asset = models.TextField()
    total_value_of_building_asset = models.TextField()
    total_value_of_other_asset = models.TextField()
    installed_capacity = models.TextField()
    current_sales_turnover = models.TextField()
    projected_sales_turnover = models.TextField()
    are_your_product_exported = models.TextField()
    company_contact_infomation = models.TextField()
    designation = models.TextField()
    name_of_md_or_ceo_of_company = models.TextField()
    selectdate_of_registration = models.DateField(blank=True, null=True)
    upload_signature = models.CharField(max_length=100, blank=True, null=True)
    prospective_member = models.OneToOneField('ProspectivememberManprospectivememberprofile', models.DO_NOTHING)
    all_raw_materials_used = models.JSONField()
    all_roduct_manufactured = models.JSONField()
    number_of_female_permanent_staff = models.IntegerField()
    number_of_male_permanent_staff = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prospectivemember_manprospectivememberformone'


class ProspectivememberManprospectivememberformtwo(models.Model):
    id = models.BigAutoField(primary_key=True)
    corporate_affairs_commision = models.CharField(max_length=100)
    letter_of_breakdown_of_payment_and_docs_attached = models.CharField(max_length=100)
    first_year_of_buisness_plan = models.CharField(max_length=100)
    second_year_of_buisness_plan = models.CharField(max_length=100)
    photocopy_of_your_reciept_issued_on_purchase_of_applicant_form = models.CharField(max_length=100)
    prospective_member = models.OneToOneField('ProspectivememberManprospectivememberprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prospectivemember_manprospectivememberformtwo'


class ProspectivememberManprospectivememberprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name_of_company = models.CharField(max_length=600)
    telephone_number = models.CharField(max_length=600)
    cac_registration_number = models.TextField()
    email = models.CharField(max_length=254)
    website = models.CharField(max_length=200)
    corporate_office_addresse = models.TextField()
    has_paid = models.BooleanField()
    paystack = models.CharField(max_length=300)
    application_status = models.CharField(max_length=100)
    user = models.OneToOneField(AccountUser, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'prospectivemember_manprospectivememberprofile'


class ProspectivememberProspectivememberformone(models.Model):
    id = models.BigAutoField(primary_key=True)
    info = models.JSONField()
    prospective_member = models.OneToOneField('ProspectivememberProspectivememberprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prospectivemember_prospectivememberformone'


class ProspectivememberProspectivememberformtwo(models.Model):
    id = models.BigAutoField(primary_key=True)
    prospective_member = models.OneToOneField('ProspectivememberProspectivememberprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prospectivemember_prospectivememberformtwo'


class ProspectivememberProspectivememberformtwofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    file = models.CharField(max_length=100)
    form_two = models.ForeignKey(ProspectivememberProspectivememberformtwo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prospectivemember_prospectivememberformtwofile'


class ProspectivememberProspectivememberprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=600)
    telephone_number = models.CharField(max_length=600)
    email = models.CharField(max_length=254)
    addresse = models.TextField()
    has_paid = models.BooleanField()
    paystack = models.CharField(max_length=300)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    application_status = models.CharField(max_length=100)
    user = models.OneToOneField(AccountUser, models.DO_NOTHING)
    paystack_key = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'prospectivemember_prospectivememberprofile'


class ProspectivememberRegistrationamountinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'prospectivemember_registrationamountinfo'
