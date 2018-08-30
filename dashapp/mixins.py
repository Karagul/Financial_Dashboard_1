from django.http import Http404


# class GroupRequiredMixin(object):
#
#     group_required = None
#
#     def dispatch(self, request, *args, **kwargs):
#
#         if not request.user.is_authenticated:
#             raise Http404
#         else:
#             user_groups = [
#                 group for group in request.user.groups.values_list(
#                     'name', flat=True
#                 )
#             ]
#
#             for permission in self.group_required:
#                 if permission not in user_groups:
#                     raise Http404
#
#         return super(GroupRequiredMixin, self).dispatch(
#             request, *args, **kwargs
#         )

# ToDo: Create a mixin for group permission dispatches, use field for providing
# info on which settings to use
