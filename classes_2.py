import numpy as np


class Manipulator(object):
    def __init__(self, m_time):
        self.time = m_time
        self.arm_pos1 = 0
        self.arm_pos2 = 0
        self.arm1_fin = []
        self.arm2_fin = []
        self.arm_vel1 = 0
        self.arm_vel2 = 0
        self.const1 = 0
        self.const2 = 0
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.count = 0

    def arm1_fin_calculation(self):
        t = 0
        while t <= self.time:
            arm1_fin = self.arm_pos1 + self.arm_vel1 * t
            self.arm1_fin.append(arm1_fin)
            t += 5
        return self.arm1_fin

    def arm2_fin_calculation(self):
        t = 0
        while t <= self.time:
            arm2_fin = self.arm_pos2 + self.arm_vel2 * t
            self.arm2_fin.append(arm2_fin)
            t += 5
        return self.arm2_fin

    def end_values_calculation(self):
        for i in self.arm1_fin:
            for j in self.arm2_fin:
                self.count += 1
                """ Работа с уравнениями для x и y """
                self.x = i + j
                self.y = i - j
                """ Работа с уравнениями для x_vel и y_vel """
                self.x_vel = i * j
                self.y_vel = i * (j + 1)
                print('%(count)d) x [%(x).3f], y [%(y).3f], x_vel [%(x_vel).2f], y_vel [%(y_vel).2f]' % {"count": self.count, "x": self.x, "y": self.y, "x_vel": self.x_vel, "y_vel": self.y_vel})


class Rotating(Manipulator):
    def __init__(self, m_time):
        super().__init__(m_time)
        self.const1 = float(input('Введите параметр l1 в см: '))
        self.const2 = float(input('Введите параметр l2 в см: '))
        self.arm_pos1 = np.radians(float(input('Введите начальное значение {}1 в градусах: '.format(chr(966)))))
        self.arm_pos2 = np.radians(float(input('Введите начальное значение {}2 в градусах: '.format(chr(966)))))
        self.arm_vel1 = np.radians(float(input('Введите угловую скорость {}1_vel в град/сек: '.format(chr(966)))))
        self.arm_vel2 = np.radians(float(input('Введите угловую скорость {}2_vel в град/сек: '.format(chr(966)))))

    def end_values_calculation(self):
        for i in self.arm1_fin:
            for j in self.arm2_fin:
                self.count += 1
                self.x = self.const1 * np.cos(i) + self.const2 * np.cos(i + j)
                self.y = self.const1 * np.sin(i) + self.const2 * np.sin(i + j)
                self.x_vel = -self.const1 * self.arm_vel1 * np.sin(i) - self.const2 * (self.arm_vel1 + self.arm_vel2) * np.sin(i + j)
                self.y_vel = self.const1 * self.arm_vel1 * np.cos(i) - self.const2 * (self.arm_vel1 + self.arm_vel2) * np.cos(i + j)
                print('%(count)d) x [%(x).3f], y [%(y).3f], x_vel [%(x_vel).2f], y_vel [%(y_vel).2f]' % {"count": self.count, "x": self.x, "y": self.y, "x_vel": self.x_vel, "y_vel": self.y_vel})


class Orthogonal(Manipulator):
    def __init__(self, m_time):
        super().__init__(m_time)
        self.const1 = float(input('Введите параметр L в см: '))
        self.const2 = float(input('Введите параметр H в см: '))
        self.arm_pos1 = np.radians(float(input('Введите начальное значение {}1 в градусах: '.format(chr(966)))))
        self.arm_pos2 = float(input('Введите значение параметра s в см: '))
        self.arm_vel1 = np.radians(float(input('Введите угловую скорость {}1_vel в град/сек: '.format(chr(966)))))
        self.arm_vel2 = float(input('Введите скорость по оси s в см/сек: '.format(chr(966))))

    def arm2_fin_calculation(self):
        t = 0
        while t < self.time:
            arm2_fin = self.arm_pos2 - self.arm_vel2 * t
            if arm2_fin > 0:
                self.arm2_fin.append(arm2_fin)
            t += 5
        return self.arm2_fin

    def end_values_calculation(self):
        for i in self.arm1_fin:
            for j in self.arm2_fin:
                self.count += 1
                self.x = j * np.cos(i) + self.const1 * np.cos(i) + self.const2 * np.sin(i)
                self.y = j * np.sin(i) + self.const1 * np.sin(i) - self.const2 * np.cos(i)
                self.x_vel = (-j * np.sin(i) - self.const1 * np.sin(i) + self.const2 * np.cos(i)) * self.arm_vel1 + np.cos(i) * self.arm_vel2
                self.y_vel = (j * np.cos(i) + self.const1 * np.cos(i) + self.const2 * np.sin(i)) * self.arm_vel1 + np.sin(i) * self.arm_vel2
                print('%(count)d) x [%(x).3f], y [%(y).3f], x_vel [%(x_vel).2f], y_vel [%(y_vel).2f]' % {"count": self.count, "x": self.x, "y": self.y, "x_vel": self.x_vel, "y_vel": self.y_vel})


n = int(input('Выберите схему робота:\n 1. Поворотный\n 2. Прямолинейный\n '))
while n != 1 and n != 2:
    print('Вы ввели неправильный номер. Выберите один из предложенных номеров схемы.')
    n = int(input('Выберите схему робота:\n 1. Поворотный\n 2. Прямолинейный\n '))
else:
    time = float(input('Введите время работы в сек: '))
    if n == 1:
        robot1 = Rotating(time)
        robot1.arm1_fin_calculation()
        robot1.arm2_fin_calculation()
        robot1.end_values_calculation()
    else:
        robot2 = Orthogonal(time)
        robot2.arm1_fin_calculation()
        robot2.arm2_fin_calculation()
        robot2.end_values_calculation()
