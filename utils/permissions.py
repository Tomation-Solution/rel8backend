from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from account.models import user as user_realted_models
from utils.custom_exceptions import CustomError



class BasePermissionMixin(BasePermission):
    """
    Base permission blueprints for users
    """

 

    def has_permission(self, request, view):
        """
        permissions method to be implemented
        :param request:
        :param view:
        :return:
        """
        
        pass

class Isfinancial(BasePermission):
    def has_permission(self, request, view):
        if  request.user.user_type != 'members':
            return True
        
        if request.user.memeber.is_financial==False:
            raise  CustomError({'is_inancial':'please pay your outstanding dues'})
        return True
class IsAdminOrSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be super_admin or admin"
        return request.user.user_type in ['super_admin','admin']

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be admin"
        return request.user.user_type in ['admin']


class IsMember(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be members"
        return request.user.user_type in ['members']
class IsMemberOrProspectiveMember(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be members"
        return request.user.user_type in ['members','prospective_members']

class IsProspectiveMember(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be members"
        return request.user.user_type in ['prospective_members']

class IsPropectiveMemberHasPaid(BasePermission):
    def has_permission(self, request, view):
        return request.user.manprospectivememberprofile.has_paid

class IsPropectiveMembersHasPaid_general(BasePermission):
    'use this for man'
    def has_permission(self, request, view):
        return request.user.prospectivememberprofile.has_paid

class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):
        "basically the user has to be super_admin"
        return request.user.user_type in ['super_admin']

class Normal_Admin_Must_BelongToACHapter(BasePermission):
    def has_permission(self, request, view):

        if request.user.user_type in ['admin'] and request.user.chapter is None:
            raise CustomError({"error":"You Must Belong To a Chapter Please Reach Out to a super admin for help"})
        return True


class CanUploadMin(BasePermission):
    def has_permission(self, request, view):

        member = user_realted_models.Memeber.objects.get(user=request.user)

        if user_realted_models.ExcoRole.objects.filter(member=member).exists():
            return member.excorole.can_upload_min#if he can uplaod min then why not let he create and upload

        return False

class IsExco(BasePermission):
    def has_permission(self, request, view):
        member = user_realted_models.Memeber.objects.get(user=request.user)


        return member.is_exco


class IsMemberOwing(BasePermission):

    def has_permission(self, request, view):
        member = user_realted_models.Memeber.objects.get(user=request.user)
        if member.amount_owing < 0:
            raise CustomError({'error':'Please Clear your out standing payment'})
        return True
