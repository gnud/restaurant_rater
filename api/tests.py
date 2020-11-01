from constance import config
from django.contrib.auth import get_user_model
from faker import Faker

from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api import models

fake = Faker()

# Constants
TOTAL_USERS = 5
TOTAL_RESTAURANTS = 3

# basename endpoints
RESTAURANT_LIST_URL = "restaurant-list"
RESTAURANT_DETAIL_URL = "restaurant-detail"
RESTAURANT_VOTE_URL = "api-v2-restaurant-vote-list"


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


class VotingTests(APITestCase):

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

    def test_vote(self):
        random_obj = models.Restaurant.objects.first()
        url = reverse(RESTAURANT_VOTE_URL, args=(random_obj.pk,))
        self.client.force_login(get_user_model().objects.first())

        print(f'Voting time [Normal]:')
        for i in range(1, config.DAILY_VOTES + 1):
            response = self.client.post(url)

            is_last = i == (config.DAILY_VOTES + 1)
            print(f'Try: {i}, is_over: \t{is_last}\t, i: {i} code: {response.status_code}')

            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vote_403(self):
        random_obj = models.Restaurant.objects.first()
        url = reverse(RESTAURANT_VOTE_URL, args=(random_obj.pk,))

        print(f'Voting time [Normal]:')
        for i in range(1, config.DAILY_VOTES + 1):
            response = self.client.post(url)

            is_last = i == (config.DAILY_VOTES + 1)
            print(f'Try: {i}, is_over: \t{is_last}\t, i: {i} code: {response.status_code}')

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_overvote(self):
        random_obj = models.Restaurant.objects.first()
        url = reverse(RESTAURANT_VOTE_URL, args=(random_obj.pk,))
        self.client.force_login(get_user_model().objects.first())

        total_allowed_votes = (config.DAILY_VOTES + 1) + 1  # +1 will over vote

        print(f'Voting time[Over vote]:')

        for i in range(1, total_allowed_votes):
            response = self.client.post(url)

            is_over = i == (config.DAILY_VOTES + 1)
            print(f'Try: {i}, is_over: \t{is_over}\t, i: {i} code: {response.status_code}')

            if not is_over:
                self.assertEqual(response.status_code, status.HTTP_200_OK)

            if is_over:
                self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
