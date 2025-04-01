from cryptek.qa_templates import ClassBaseViewTestCase


class LoginViewTestCase(ClassBaseViewTestCase):
    endpoint_name = "login"
    is_authenticated = True
