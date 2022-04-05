from typing import Dict, List, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: str
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_RUN_1: int = 18
    COEFF_RUN_2: int = 20
    MIN_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        calories1 = self.COEFF_RUN_1 * self.get_mean_speed() - self.COEFF_RUN_2
        calories2 = calories1 * self.weight
        return calories2 / self.M_IN_KM * self.duration * self.MIN_IN_HOUR


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_WALK_1: float = 0.035
    COEFF_WALK_2: int = 2
    COEFF_WALK_3: float = 0.029
    MIN_IN_HOUR: int = 60

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
        return calories * self.duration * self.MIN_IN_HOUR


class Swimming(Training):
    """Тренировка: плавание."""
    COEFF_SWIM_1: float = 1.1
    COEFF_SWIM_2: int = 2
    LEN_STEP: float = 1.38

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
        return self.length_pool * self.count_pool / \
        Swimming.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.COEFF_SWIM_1) \
             * self.COEFF_SWIM_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in workout_types:
        raise ValueError('Укажите правильный вид тренировки: ' \
                    f'{workout_types.keys()}')
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
