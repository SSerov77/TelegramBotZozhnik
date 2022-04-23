# from data import db_session
# from data.db_session import global_init
# from data.other_tables import Quot
#
from data import db_session
from data.db_session import global_init
from data.dishes import Dish


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_blob(name, photo, photo1):
        global_init("db/database.db")
        db_sess = db_session.create_session()

        photo = convert_to_binary_data(photo)
        photo1 = convert_to_binary_data(photo1)

        dish = Dish()
        dish.name = name
        dish.dish_photo = photo
        dish.photo_recipe = photo1

        db_sess.add(dish)
        db_sess.commit()


insert_blob("Салат из курицы с персиком и руколой", "1.jpg", "2.jpg")
insert_blob("Теплый салат со стручковой фасолью", "3.jpg", "4.jpg")
insert_blob("Салат из персиков-гриль", "5.jpg", "6.jpg")
insert_blob("Ореховый салат с сыром и свежим фенхелем", "7.jpg", "8.jpg")
insert_blob("Салат «Битые огурцы»", "9.jpg", "10.jpg")
insert_blob("Салат со свеклой и брынзой", "11.jpg", "12.jpg")
insert_blob("Салат фунчоза", "13.jpg", "14.jpg")
insert_blob("Салат «Фаворит»", "15.jpg", "16.jpg")
insert_blob("Салат из куриной грудки в тарталетках", "17.jpg", "18.jpg")
insert_blob("Оливье классический с цыпленком", "19.jpg", "20.jpg")



