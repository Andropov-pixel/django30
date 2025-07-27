from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson, Subscription
from users.models import CustomUser


class TrainingTestCase(APITestCase):

    def setUp(self):
        self.member = CustomUser.objects.create(email="user@example.com")
        self.training = Course.objects.create(
            title="Mathematics", description="Algebra and Geometry", owner=self.member
        )
        self.session = Lesson.objects.create(
            title="Algebra Basics",
            description="Introduction to algebraic concepts",
            course=self.training,
        )
        self.client.force_authenticate(user=self.member)

    def test_training_retrieve(self):
        url = reverse("materials:course-detail", args=(self.training.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.training.title)

    def test_training_create(self):
        self.assertEqual(Course.objects.all().count(), 1)

    def test_training_update(self):
        url = reverse("materials:course-detail", args=(self.training.pk,))
        data = {"title": "Advanced Mathematics"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Advanced Mathematics")

    def test_training_delete(self):
        url = reverse("materials:course-detail", args=(self.training.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_training_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        expected_result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.training.pk,
                    "lessons": [
                        {
                            "id": self.session.pk,
                            "title": self.session.title,
                            "description": self.session.description,
                            "preview_image": None,
                            "video_url": None,
                            "course": self.training.pk,
                            "owner": None,
                        }
                    ],
                    "title": self.training.title,
                    "preview_image": None,
                    "description": self.training.description,
                    "owner": self.member.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)


class SessionTestCase(APITestCase):

    def setUp(self):
        self.member = CustomUser.objects.create(email="user@example.com")
        self.training = Course.objects.create(
            title="Mathematics", description="Algebra and Geometry", owner=self.member
        )
        self.session = Lesson.objects.create(
            title="Algebra Basics",
            description="Introduction to algebraic concepts",
            course=self.training,
            owner=self.member,
        )
        self.client.force_authenticate(user=self.member)

    def test_session_retrieve(self):
        url = reverse("materials:lesson_detail", args=(self.session.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.session.title)

    def test_session_create(self):
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_session_update(self):
        url = reverse("materials:lesson_update", args=(self.session.pk,))
        data = {"title": "Advanced Algebra"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Advanced Algebra")

    def test_session_delete(self):
        url = reverse("materials:lesson_delete", args=(self.session.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_session_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        expected_result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.session.pk,
                    "title": self.session.title,
                    "description": self.session.description,
                    "preview_image": None,
                    "video_url": None,
                    "course": self.training.pk,
                    "owner": self.member.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_result)


class EnrollmentTestCase(APITestCase):
    def setUp(self):
        self.member = CustomUser.objects.create(email="user@example.com")
        self.training = Course.objects.create(
            title="Mathematics", description="Algebra and Geometry", owner=self.member
        )
        self.session = Lesson.objects.create(
            title="Algebra Basics",
            description="Introduction to algebraic concepts",
            course=self.training,
            owner=self.member,
        )
        self.client.force_authenticate(user=self.member)

    def test_enrollment_create(self):
        url = reverse("materials:course_subscription")
        data = {"user": self.member, "course": self.training.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "subscription added"})

    def test_enrollment_delete(self):
        self.enrollment = Subscription.objects.create(
            user=self.member, course=self.training
        )
        url = reverse("materials:course_subscription")
        data = {"user": self.member, "course": self.training.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "subscription removed"})