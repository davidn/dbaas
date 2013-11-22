from __future__ import unicode_literals
from logging import getLogger
from django.db import models
from .. import rules
from .user import User

logger = getLogger(__name__)


class Rule(models.Model):
    condition = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    completed = models.ManyToManyField(User, related_name='completed_rules')

    class Meta:
        app_label = "api"

    def run(self, user):
        if getattr(rules.conditions, self.condition)(user):
            logger.debug("Condition '%s' triggered for user '%s'. Running action '%s'",
                         self.condition, user.email, self.action)
            getattr(rules.actions, self.action)(user)
            self.completed.add(user)
            self.save()

    @classmethod
    def process_user(cls, user):
        for rule in cls.objects.exclude(completed=user):
            rule.run(user)

    @classmethod
    def process(cls):
        # The query below would fetch every rule, user pair we need, but I can't find a way to get django to make
        # pairs of instances from a query :(
        #   select api_user.id, api_rule.id from api_rule, api_user left join
        #   api_rule_completed on api_rule_completed.rule_id=api_rule.id and api_rule_completed.user_id=api_User.id
        #   where api_rule_completed.id is not null;
        for user in User.objects.all():
            cls.process_user(user)
