class InfoMessage:
    """Информационное сообщение о тренировке."""
 
    def __init__(self, training_type: str,
                duration: float,
                distance: float,
                speed: float,
                calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
 
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
 
 
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65 # длина шага карлика
    M_IN_KM = 1000
    TRAINING_TYPE = ''
 
    def __init__(self,
                action: int, # количество совершённых действий
                duration: float, # длительность тренировки
                weight: float # вес спортсмена
                ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
 
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
 
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed
 
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
 
    def show_training_info(self) -> InfoMessage:
        output = InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories())
        return output
 
    """Вернуть информационное сообщение о выполненной тренировке."""
 
 
class Running(Training):
    COEFF_RUN_1 = 18
    COEFF_RUN_2 = 20
    TRAINING_TYPE = 'RUN'
    """Тренировка: бег."""
 
    def get_spent_calories(self) -> float:
        calories1 = self.COEFF_RUN_1 * self.get_mean_speed() - self.COEFF_RUN_2
        calories2 = calories1 * self.weight
        calories_out = calories2 / self.M_IN_KM * self.duration * 60
 
        return calories_out
 
 
class SportsWalking(Training):
    COEFF_WALK_1 = 0.035
    COEFF_WALK_2 = 2
    COEFF_WALK_3 = 0.029
    TRAINING_TYPE = 'WLK'
 
    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
 
    def get_spent_calories(self) -> float:
        calories = (self.COEFF_WALK_1 * self.weight + (
                    self.get_mean_speed() ** self.COEFF_WALK_2
                    // self.height) * self.COEFF_WALK_3 * self.weight)
        calories_out = calories * self.duration * 60
        return calories_out
 
    """Тренировка: спортивная ходьба."""
 
 
class Swimming(Training):
    COEFF_SWIM_1 = 1.1
    COEFF_SWIM_2 = 2
    LEN_STEP = 1.38
    TRAINING_TYPE = 'SWM'
    """Тренировка: плавание."""
 
    def __init__(self,
                action: int,
                duration: float,
                weight: float,
                length_pool: int,
                count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
 
    def get_mean_speed(self) -> float:
        speed = self.length_pool * self.count_pool
        speed_out = speed / super().M_IN_KM / self.duration
 
        return speed_out
 
    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + self.COEFF_SWIM_1)
        calories_out = calories * self.COEFF_SWIM_2 * self.weight
        return calories_out
 
 
def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages_db = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return packages_db[workout_type](*data)
 
 
def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())
 
 
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
 
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
