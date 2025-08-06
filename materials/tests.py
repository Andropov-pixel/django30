from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    """Тестирование курса."""

    def setUp(self):
        """Прописываем тестовые данные курса."""
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(
            name="Тестовый курс", description="Тестовое описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Тестовое описание урока",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):  # OK
        """Тест на получение курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)


class LessonTestCase(APITestCase):
    """Тестирование урока."""

    def setUp(self):
        """Прописываем тестовые данные урока."""
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(
            name="Тестовый курс", description="Тестовое описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Тестовое описание урока",
            video_link="https://youtube.com/test",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):  # OK
        """Тест на получение урока."""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):  # NOK
        """Тест на создание урока."""
        url = reverse("materials:lessons_create")
        data = {
            "title": "newtest",
            "description": "newdescription",
            "video_link": "https://youtube.com/test",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title="newtest").exists())

    def test_lesson_update(self):  # OK
        """Тест на обновление урока."""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "update test"}
        response = self.client.patch(url, data)
        # print(response.json())
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "update test")

    def test_lesson_delete(self):  # OK
        """Тест на удаление урока."""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_subscription(self):  # OK
        """Тест на получение подписки."""
        url = reverse("materials:subscribe")  # Замените на Ваш URL
        data = {"course_id": self.course.pk}

        # Подписка на курс
        response = self.client.post(url, data, format="json")
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        # Удаление подписки
        response = self.client.post(url, data, format="json")
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")

    def test_lesson_list(self):  # OK
        """Тест на просмотр урока."""
        url = reverse("materials:lessons_list")

        response = self.client.get(url)
        # print(response.json())
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": self.lesson.video_link,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
