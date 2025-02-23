from django.test import TestCase
from .models import Tovar, Country, Categories, Cabine, Trbody, Engine, Entype, Wheelbase
from .models import Ticket, CustomUser, Status
from django.contrib.auth import get_user_model


class TovarModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(country="Северная Америка")
        self.category = Categories.objects.create(catgname="Магистральные перевозки")
        self.cabine = Cabine.objects.create(cabtype="VNL - Ночная")
        self.trbody = Trbody.objects.create(bodytype="Тягач")
        self.engine = Engine.objects.create(engine="Дизель")
        self.entype = Entype.objects.create(entype="VNL - D16")
        self.wheelbase = Wheelbase.objects.create(wbase="6x4")

        self.tovar = Tovar.objects.create(
            tovarname="Volvo VNL",
            tovarprice=25700000,
            country=self.country,
            cabine=self.cabine,
            trbody=self.trbody,
            yeardate=2020,
            engine=self.engine,
            entype=self.entype,
            transmisson="I-Shift (12)",
            weight=25000,
            power=500,
            tovardescrpt="Грузовик для магистральных перевозок",
            wheelbase=self.wheelbase,
        )
        self.tovar.category.add(self.category)

    def test_tovar_creation(self):
        self.assertEqual(self.tovar.tovarname, "Volvo VNL")
        self.assertEqual(self.tovar.tovarprice, 25700000)
        self.assertEqual(self.tovar.country.country, "Северная Америка")
        self.assertEqual(self.tovar.cabine.cabtype, "VNL - Ночная")
        self.assertEqual(self.tovar.trbody.bodytype, "Тягач")
        self.assertEqual(self.tovar.yeardate, 2020)
        self.assertEqual(self.tovar.engine.engine, "Дизель")
        self.assertEqual(self.tovar.entype.entype, "VNL - D16")
        self.assertEqual(self.tovar.transmisson, "I-Shift (12)")
        self.assertEqual(self.tovar.weight, 25000)
        self.assertEqual(self.tovar.power, 500)
        self.assertEqual(self.tovar.tovardescrpt, "Грузовик для магистральных перевозок")
        self.assertEqual(self.tovar.wheelbase.wbase, "6x4")
        self.assertEqual(self.tovar.category.first().catgname, "Магистральные перевозки")


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            third_name="Test",
            phone="1234567890",
            password="testpass123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "TestUser")
        self.assertEqual(self.user.third_name, "Test")
        self.assertEqual(self.user.phone, "1234567890")


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="TestUser",
            third_name="Test",
            phone="1234567890",
            password="testpass123"
        )
        self.status = Status.objects.create(title="Новое заявление 1")
        self.ticket = Ticket.objects.create(
            creator=self.user,
            number="TestUser",
            email2="Test@test.com",
            phone2="1234567890",
            status=self.status
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.creator.username, "TestUser")
        self.assertEqual(self.ticket.number, "TestUser")
        self.assertEqual(self.ticket.email2, "Test@test.com")
        self.assertEqual(self.ticket.phone2, "1234567890")
        self.assertEqual(self.ticket.status.title, "Новое заявление 1")