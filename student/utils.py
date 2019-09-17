# import string
# import secrets
# import random
# from django.utils.text import slugify

# def streamgenerate(self):
#     pass
# def coursegenerate(self):
#     pass

# def batchgenerate(self):
#     pass
    
# def random_string_generator(size=20, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


# def unique_key_generator(instance):
#     """
#     This is for a Django project with an key field
#     """
#     size = random.randint(30, 45)
#     key = random_string_generator(size=size)

#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(key=key).exists()
#     if qs_exists:
#         return unique_slug_generator(instance)
#     return key


# def unique_enrollment_number_generator(instance):
#     """
#     This is for a Django project with an order_id field
#     """
#     order_enrollment_number = random_string_generator()

#     Klass = instance.__class__
#     order_enrollment_number = random_string_generator()
#     qs_exists = Klass.objects.filter(enrollment_number=order_enrollment_number).exists()
#     if qs_exists:
#         return unique_slug_generator(instance)
#     order_enrollment_number = random_string_generator()
#     return order_enrollment_number





# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance 
#     has a model with a slug field and a title character (char) field.
#     """
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.title)

#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#                     slug=slug,
#                     randstr=random_string_generator(size=4)
#                 )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug