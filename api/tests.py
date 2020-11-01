from django.contrib.auth import get_user_model
from faker import Faker

from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

fake = Faker()

# Constants
TOTAL_USERS = 5
TOTAL_RESTAURANTS = 3

# basename endpoints
RESTAURANT_LIST_URL = "restaurant-list"
RESTAURANT_DETAIL_URL = "restaurant-detail"


class RestaurantTests(APITestCase):

    def setUp(self) -> None:
        super().setUp()

        baker.make_recipe(
            'api.userTemplate',
            _quantity=TOTAL_USERS,
        )
        baker.make_recipe(
            'api.restaurantTemplate',
            _quantity=TOTAL_RESTAURANTS,
        )

    def test_check_user_size(self):
        users_cnt = get_user_model().objects.all().count()

        self.assertEqual(users_cnt, TOTAL_USERS)

    def test_user_login(self):
        url = reverse(RESTAURANT_LIST_URL)
        self.client.force_login(get_user_model().objects.first())

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_fail(self):
        url = reverse(RESTAURANT_LIST_URL)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_list(self):
        url = reverse(RESTAURANT_LIST_URL)
        self.client.force_login(get_user_model().objects.first())

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), TOTAL_RESTAURANTS)

    def test_restaurant_list_403(self):
        url = reverse(RESTAURANT_LIST_URL)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_create(self):
        data = {
            'name': fake.text(160),
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_LIST_URL)
        self.client.force_login(get_user_model().objects.first())

        response = self.client.post(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurant_create_400(self):
        target_missing_field = 'name'

        data = {
            # target_missing_field: 'None',
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_LIST_URL)
        self.client.force_login(get_user_model().objects.first())

        response = self.client.post(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get(target_missing_field)[0], 'This field is required.')

    def test_restaurant_create_403(self):
        data = {
            'name': fake.text(160),
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_LIST_URL)

        response = self.client.post(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_update(self):
        random_obj = baker.make_recipe('api.restaurantTemplate')

        data = {
            'name': fake.text(160),
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_DETAIL_URL, args=(random_obj.pk,))
        self.client.force_login(get_user_model().objects.first())

        response = self.client.put(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurant_update_400(self):
        random_obj = baker.make_recipe('api.restaurantTemplate')

        data = {
            # 'name': fake.text(160),
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_DETAIL_URL, args=(random_obj.pk,))
        self.client.force_login(get_user_model().objects.first())

        response = self.client.put(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_restaurant_update_403(self):
        random_obj = baker.make_recipe('api.restaurantTemplate')

        data = {
            'name': fake.text(160),
            'description': fake.text(200),
            'address': fake.text(35),
            'cover': open('test_data/sample.jpg', 'rb')
        }

        url = reverse(RESTAURANT_DETAIL_URL, args=(random_obj.pk,))

        response = self.client.put(
            url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_restaurant_delete(self):
        random_obj = baker.make_recipe('api.restaurantTemplate')

        url = reverse(RESTAURANT_DETAIL_URL, args=(random_obj.pk,))
        self.client.force_login(get_user_model().objects.first())

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_restaurant_delete_404(self):
        # random_obj = baker.make_recipe(
        #     'api.restaurantTemplate',
        # )

        url = reverse(RESTAURANT_DETAIL_URL, args=(-1,))
        self.client.force_login(get_user_model().objects.first())

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_restaurant_delete_403(self):
        random_obj = baker.make_recipe('api.restaurantTemplate')

        url = reverse(RESTAURANT_DETAIL_URL, args=(random_obj.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
