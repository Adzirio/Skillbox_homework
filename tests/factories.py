from faker import Faker

fake = Faker()

def client_factory():
    """ClientFactory как функция"""
    return {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "credit_card": fake.credit_card_number() if fake.boolean(chance_of_getting_true=80) else None,
        "car_number": fake.license_plate(),
    }


def parking_factory():
    """ParkingFactory как функция"""
    count_places = fake.pyint(min_value=5, max_value=100)
    return {
        "address": fake.address(),
        "opened": fake.boolean(chance_of_getting_true=70),
        "count_places": count_places,
        "count_available_places": max(0, count_places - fake.pyint(min_value=0, max_value=count_places // 2)),
    }