from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        """ Заполняем базу данных """

        self.user = User.objects.create(email='TEST@mail.ru')
        self.course = Course.objects.create(title='JAVA+', description="Лучший курс")
        self.lesson = Lesson.objects.create(title='Основы JAVA', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """ Тестируем детальную информацию по уроку """

        url = reverse('course:lessons_retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        """ Тестируем создание урока """

        url = reverse('course:lessons_create')
        data = {
            'title': 'Продолжение по JAVA+',
            'video': 'youtube.com'
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)  # Проверяем статус-код

        self.assertEqual(
            Lesson.objects.all().count(), 2)  # Проверяем кол-во уроков в БД

    def test_lesson_update(self):
        """ Тестируем обновление информации по уроку """

        url = reverse('course:lessons_update', args=(self.lesson.pk,))

        data = {
            'title': 'Продолжение по JAVA+ и C++',

        }

        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            response.status_code, status.HTTP_200_OK  # Проверяем статус-код
        )
        self.assertEqual(
            data.get('title'), 'Продолжение по JAVA+ и C++'  # Проверяем внесенные изменения
        )

    def test_lesson_delete(self):
        """ Тестируем удаление урока """

        url = reverse('course:lessons_delete', args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT  # Проверяем статус-код
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """ Тестируем удаление урока """

        url = reverse('course:lessons_list')

        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK  # Проверяем статус-код
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1)  # Проверяем кол-во уроков в БД

        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'video': '', 'title': 'Основы JAVA', 'description': None, 'image': None,
             'course': self.course.pk,
             'owner': self.user.pk}]}

        self.assertEqual(
            response.json(), result  # Проверяем результат
        )

    def test_check_subscription(self):
        """ Тестируем добавление подписки """

        url = reverse('users:subscription-list')
        data = {
            'owner': self.user.pk,
            'course': self.course.pk
        }

        response = self.client.post(url, data)
        print(response.json())

        self.assertEqual(
            response.status_code, status.HTTP_200_OK)  # Проверяем статус-код

        self.assertEqual(
            response.json().get('message'), 'Подписка добавлена')  # Проверяем кол-во уроков в БД

        self.assertEqual(
            Subscription.objects.filter(user=self.user.pk).exists(), True)  # Проверяем наличие подписки у USER