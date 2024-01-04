from django.test import TestCase

# Create your tests here.


print(
     [x if x % 2 == 0 else x * 2 for x in range(10)]
 )