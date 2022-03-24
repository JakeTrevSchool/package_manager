from django.test import TestCase
from manager.models import Package, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render

# Create your tests here.

class PackageMethodTests(TestCase):

	def test_package_tags_can_be_empty(self):
		# Checking if we can create a package without adding any tags.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		package = Package(author=profile, package_name='test67785', downloads=0, views=1)
		package.save()
		self.assertEqual((package.tags == ''), True)

	def test_package_is_private_by_default(self):
		# Checking if packages are private by default.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		package = Package(author=profile, package_name='test67785', downloads=0, views=1)
		package.save()
		self.assertEqual((package.public == 0), True)

class HomeTests(TestCase):

	def test_default_avatar_used_if_user_has_no_avatar(self):
		# Checking if the default avatar image is used if a user has not uploaded a profile image.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		response = self.client.get(reverse('manager:index'))
		self.assertContains(response, 'default_avatar.png')

	def test_3_packages(self):
		# Checking if home page displays the number of packages as 3.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		package = Package(author=profile, package_name='test67785', downloads=0, views=1)
		package.save()
		package = Package(author=profile, package_name='test103', downloads=0, views=1)
		package.save()
		package = Package(author=profile, package_name='test0284', downloads=0, views=1)
		package.save()
		response = self.client.get(reverse('manager:index'))
		number_of_packages = response.context['packages']
		self.assertEquals(number_of_packages, 3)

	def test_2_developers(self):
		# Checking if home page displays the number of developers as 2.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		self.user2 = User.objects.create_user(username='testuser5', email='user4351@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser5', password='e92SinZod4')
		profile = UserProfile(user=self.user2, avatar="")
		profile.save()
		response = self.client.get(reverse('manager:index'))
		number_of_developers = response.context['developers']
		self.assertEquals(number_of_developers, 2)

	def test_login_button_if_user_is_not_logged_in(self):
		# Checking for a log in button if no user is logged in.
		response = self.client.get(reverse('manager:index'))
		self.assertContains(response, 'Log In')

	def test_logout_button_if_user_is_logged_in(self):
		# Checking for a log out button if there is a user logged in.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		response = self.client.get(reverse('manager:index'))
		self.assertContains(response, 'Log Out')

class ExploreTests(TestCase):

	def test_explore_displays_my_packages(self):
		# Checking if the explore page displays my packages.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		package = Package(author=profile, package_name='MyNewPackage', downloads=0, views=1)
		package.save()
		response = self.client.get(reverse('manager:explore'))
		self.assertContains(response, 'MyNewPackage')

	def test_explore_displays_top_viewed_packages(self):
		# Checking if the explore page displays the top viewed packages on the first page.
		self.user = User.objects.create_user(username='testuser3', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='testuser3', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		package = Package(author=profile, package_name='MyNewPackage', downloads=0, views=2, public=1)
		package.save()
		package = Package(author=profile, package_name='MyNewPackage2', downloads=0, views=1, public=1)
		package.save()
		package = Package(author=profile, package_name='MyNewPackage3', downloads=0, views=5, public=1)
		package.save()
		package = Package(author=profile, package_name='MyNewPackage4', downloads=0, views=6, public=1)
		package.save()
		package = Package(author=profile, package_name='MyNewPackage5', downloads=0, views=7, public=1)
		package.save()
		package = Package(author=profile, package_name='MostViewedPackage', downloads=0, views=8, public=1)
		package.save()
		package = Package(author=profile, package_name='LeastViewedPackage', downloads=0, views=0, public=1)
		package.save()
		response = self.client.get(reverse('manager:explore'))
		# Checking if the most viewed package is displayed.
		self.assertContains(response, 'MostViewedPackage')
		# Checking if the least viewed package is not displayed.
		self.assertNotContains(response, 'LeastViewedPackage')

class ProfileTests(TestCase):

	def test_profile_username_is_correct(self):
		# Checking if the profile page displays the correct username of the logged in user.
		self.user = User.objects.create_user(username='ThisIsTheUsername', email='user4352@gmail.com', password='e92SinZod4')
		login = self.client.login(username='ThisIsTheUsername', password='e92SinZod4')
		profile = UserProfile(user=self.user, avatar="")
		profile.save()
		request = ''
		response = self.client.get('/profile/ThisIsTheUsername')
		self.assertContains(response, 'ThisIsTheUsername')


