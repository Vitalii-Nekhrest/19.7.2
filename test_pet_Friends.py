from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Пушок', animal_type='Теренозавр',
                                     age='5000001', pet_photo='images/Puhok.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=500005):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

"""Тест для Недостающий метод добавления новой фотки питомцу"""
def test_add_new_pfoto_pet(pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_new_pfoto_pet(auth_key, pet_id, pet_photo)

    assert status == 200

"""Тест для Недостающий метод добавления нового питомца без фотки питомца"""
def test_add_create_pet_simple(name='Телепузик', animal_type='Теренозавр',
                                     age='5000005'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

"""Негативный тест №1"""
"""Метод api.key с несуществующим email"""
def test_get_api_key_for_valid_user(email="nekhres.vitalii@gmail.com", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

"""Негативный тест №2"""
"""Метод api.key с несуществующим password"""
def test_get_api_key_for_valid_user(email=valid_email, password="valid_password"):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

"""Негативный тест №3"""
"""Метод add_new_pet_with_valid_data с указанием отрицательного возраста """
def test_add_new_pet_with_valid_data(name='Пушок', animal_type='Теренозавр',
                                     age='-4545', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name

"""Негативный тест №4"""
"""Метод add_new_pet_with_valid_data с указанием набора букв вмето возраста"""
def test_add_new_pet_with_valid_data(name='Пушок', animal_type='Теренозавр',
                                     age='апврп', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name

"""Негативный тест №5"""
"""Метод add_new_pet_with_valid_data с указанием неверного auth_key"""
def test_add_new_pet_with_valid_data(name='Пушок', animal_type='Теренозавр',
                                     age='апврп', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet("5df5615fc3ff95192cdbf77c8cbedd618fea76f22eaeec4e130b85f9", name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

"""Негативный тест №6"""
"""Метод add_new_pet_with_valid_data с указанием имени питомца с пробелами на разных роскладках клавиатуры"""
def test_add_new_pet_with_valid_data(name='Пушокshdgjsfhvljsf gdfohbo dfbl jdfjbdfb jdfbnljd fn bld', animal_type='Теренозавр',
                                     age='апврп', pet_photo='images/cat.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name

"""Негативный тест №7"""
"""Метод successful_delete_self_pet попытка удалить питомка с номером выходящим за список питомцев"""
def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][344]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

"""Негативный тест №8"""
"""Метод successful_update_self_pet_info попытка поменять данные питомца номер которого выходящим за список питомцев"""
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=500005):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][3444]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

"""Негативный тест №9"""
"""Метод test_successful_update_self_pet_info с пустой переменной name и animal_type"""
def test_successful_update_self_pet_info(name='', animal_type='', age=500005):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

"""Негативный тест №10"""
"""Метод asuccessful_update_self_pet_info с указанием отрицательного возраста и словаря в переменной name"""
def test_successful_update_self_pet_info(name={'er': 'wer'}, animal_type='sgw', age=-500005):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")