import pytest
from django.urls import reverse
from django.utils import timezone

from rest_framework import status


@pytest.mark.django_db
class TestRoomCreation:

    @pytest.fixture
    def rooms_endpoint(self):
        return reverse('api:room-list')

    @pytest.fixture
    def payload_room_creation(self):
        return {
            "name": "Sala Brasil",
            "slug": "sala-brasil",
            "description": "sala com televisão para até 5 pessoas",
            "color": "green",
        }

    def test_should_create_room(self, rooms_endpoint, public_client, payload_room_creation):
        response = public_client.post(
            rooms_endpoint, data=payload_room_creation, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRoomPayload:

    @pytest.fixture
    def rooms_endpoint(self):
        return reverse('api:room-list')

    @pytest.fixture
    def payload_room_list(self, room_one):
        return [
            {
                "id": 1,
                "name": "São Paulo",
                "slug": "sao-paulo",
                "description": "Sala para até 10 pessoas",
                "color": "red",
            }
        ]

    def test_should_return_right_payload(self, rooms_endpoint, public_client, payload_room_list):
        response = public_client.get(rooms_endpoint)
        json_response = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert json_response == payload_room_list


@pytest.mark.django_db
class TestMeetingCreation:

    @pytest.fixture
    def meeting_endpoint(self):
        return reverse('api:meeting-list')

    @pytest.fixture
    def payload_meeting_creation(self):
        return {
            "name": "Apresentação de projeto",
            "room": 1,
            "description": "apresentação do projeto para o cliente",
            "status": "scheduled",
            "date": "25/12/2018",
            "start": timezone.now().time(),
            "end": (timezone.now() + timezone.timedelta(minutes=120)).time()
        }

    def test_should_create_meeting(
            self, meeting_endpoint, public_client, payload_meeting_creation, room_one
    ):
        response = public_client.post(
            meeting_endpoint, data=payload_meeting_creation, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
