from api.models import User
u = User.objects.get(username='admin')
u.set_password('admin123456')
u.save()
