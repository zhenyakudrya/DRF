from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class MaterialsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            email="test@mail.ru",
            phone="123qweasd",
            city="Saint_P",
        )
        self.course = Course.objects.create(
            id=2,
            course_name="Course_test",
            course_content="CourseDescription_test",
            user=self.user
        )
        self.lesson = Lesson.objects.create(
            id=3,
            lesson_name="Lesson_test",
            lesson_content="LessonDescription_test",
            link_video="test.youtube.com",
            course=self.course,
            user=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_list_lessons(self):
        """Тестирование вывода списка уроков"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('lesson_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.id,
                        'lesson_name': self.lesson.lesson_name,
                        'lesson_content': self.lesson.lesson_content,
                        'lesson_image': self.lesson.lesson_image,
                        'course': self.lesson.course.id,
                        'link_video': self.lesson.link_video,
                        'user': self.lesson.user.id
                    }
                ]
            }
        )

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            "lesson_name": "Lesson_test",
            "lesson_content": "LessonDescription_test",
            "link_video": "https://www.youtube.com",
            "course": self.course.id,
            "user": self.lesson.user.id
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('lesson_create'),
            data=data
        )

        # print(response.content)

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_update_lesson(self):
        """Тестирование обновления урока"""

        updated_data = {
            "lesson_name": "Updated Lesson Name",
            "lesson_content": "Updated Lesson Description",
            "link_video": "https://www.youtube.com",
            "course": self.course.id,
            "user": self.lesson.user.id
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse('lesson_update', kwargs={'pk': self.lesson.id}),
            data=updated_data
        )

        # print(response.content)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('lesson_delete', kwargs={'pk': self.lesson.id}),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            email="test@mail.ru",
            phone="123qweasd",
            city="Saint_P",
        )
        self.course = Course.objects.create(
            id=2,
            course_name="Course_test",
            course_content="CourseDescription_test",
            user=self.user
        )

        #self.client.force_authenticate(user=self.user)
        self.user.status = False

    def test_subscribe_to_course(self):
        """Тестирование подписки на курс"""

        data = {
            "course": self.course.id,
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('subscription'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {'message': 'Вы подписались на обновления курса'}
        )

    def test_unsubscribe_from_course(self):
        """Тестирование отписки от курса"""

        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
            status=True
        )

        subscription.refresh_from_db()

        data = {
            "course": self.course.id,
        }

        self.client.force_authenticate(user=self.user)

        response_subscribe = self.client.post(
            reverse('subscription'),
            data=data
        )

        self.assertEquals(
            response_subscribe.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response_subscribe.json(),
            {'message': 'Вы отписались от обновления курса'}
        )

        self.user.refresh_from_db()  # Обновляем данные пользователя из базы
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscribe_to_course_unauthorized(self):
        """Тестирование подписки на курс для неавторизованного пользователя"""

        data = {
            "course": self.course.id,
        }

        response = self.client.post(
            reverse('subscription'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertEquals(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )

    def test_subscribe_to_not_existing_course(self):
        """Тестирование подписки на несуществующий курс"""

        not_existing_course = 8899

        data = {
            "course": not_existing_course,
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('subscription'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEquals(
            response.json(),
            {'detail': 'Страница не найдена.'}
        )