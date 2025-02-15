from cryptek.test_and_check.base_model_test import BaseModelTestCase
from log_recorder_app.factories.audit_log_factory import AuditLogFactory


class AuditLogTestCase(BaseModelTestCase):
    class Meta:
        factory = AuditLogFactory
