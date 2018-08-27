from django.http import Http404


class GroupRequiredMixin(object):

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        else:
            user_groups = [
                group for group in request.user.groups.values_list(
                    'name', flat=True
                )
            ]
            print(user_groups)

            # Expand the group_required variable by the company group
            self.group_required.append(
                "company_" + self.kwargs["pk"]
            )
            print(self.group_required)
            for permission in self.group_required:
                if permission not in user_groups:
                    raise Http404
            # Potencjalnie tutaj zrobić reset grup do stanu z klasy
        return super(GroupRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )