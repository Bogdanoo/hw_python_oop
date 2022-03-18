class InfoMessage:
    def __init__(self,
        duration: float,
        speed: float,
        calories: float,
        distance: float,
        training_type: str) -> None:
            self.duration = duration,
            self.speed = speed,
            self.calories = calories,
            self.distance = distance,
            self.training_type = training_type

    def get_message(self):
        return(
            f'Тип тренировки:',
f'{self.training_type}; '
            f'Дительность:',
f'{self.duration:.3f} ч.; '
            f'Дистанция:',
f'{self.distance:.3f} км; '
            f'Средняя скорость:',
f'{self.speed:.3f} км/ч; '
            f'Потрачено ккал:',
f'{self.calories:.3f}.'
            )
    """Информационное сообщение о тренировке."""

class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * Training.LEN_STEP / Training.M_IN_KM
        """Получить дистанцию в км."""

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration
        """Получить среднюю скорость движения."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        return InfoMessage.get_message
        """Вернуть информационное сообщение о выполненной тренировке."""

class Running(Training):
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(
        self,
        action,
        duration,
        weight
            ):
        super().__init__(action, duration, weight)
        self.type = type

    def get_spent_calories(self) -> float:
        return ((Running.coeff_calorie_1 * self.get_mean_speed() - 
        Running.coeff_calorie_2 * self.weight / Training.M_IN_KM * 
        self.duration * 60))


class SportsWalking(Training):
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def __init__(
        self,
        action,
        duration,
        weight,
        height
            ):
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        ((SportsWalking.coeff_calorie_1 * self.weight + 
        (self.get_mean_speed()**2 // self.height) * 
        SportsWalking.coeff_calorie_2 * self.weight) * 
        self.duration * 60)

    """Тренировка: спортивная ходьба. Числовым коэффициентам тоже нужны имена, не забывайте про это."""


class Swimming(Training):
    LEN_STEP = 1.38

    def __init__(
        self,
        action,
        duration,
        weight,
        lenght_pool,
        count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool / 
            Training.M_IN_KM / self.duration)

        def get_spent_calories(self) -> float:
             return ((self.get_mean_speed() + 1.1) * 2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    training_type = {'WLK': SportsWalking, 'RUN': Running, 'SWM': Swimming}
    return (training_type[workout_type] (*data).get_spent_calories())
    """Прочитать данные полученные от датчиков."""


def main(training: Training) -> None:
    print(InfoMessage(*Training).get_message())
    if __name__ == '__main__':
        packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),]
        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)