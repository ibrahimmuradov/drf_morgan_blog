import string
import random

chars = string.digits + string.ascii_letters

class CodeGenerator:
    @staticmethod
    def code_link_generator(size, chars=chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_activation_link_code(cls, size, model_):
        new_code = cls.code_link_generator(size=size)
        qs_exists = model_.objects.filter(slug=new_code).exists()
        return cls.create_activation_link_code(size, model_) if qs_exists else new_code
