from PIL import Image
import numpy as np
import math
import sys

def get_gradated_brightness(original):
	for gradation in gradations:
		if original < gradation:
			return gradation
	return gradations[len(gradations)-1]

def get_calculated_cell(i, j):
	summ = 0
	for n in range(i, i + mosaic_size):
			for n1 in range(j, j + mosaic_size):
				try:
					# Получаем цвет
					r,g,b = arr[n][n1][0], arr[n][n1][1], arr[n][n1][2]
					# Складываем в сумму ячейки среднее по пикселю
					summ += (int(r) + int(g) + int(b)) // 3
				except:
					pass
	return summ

def get_averange_brightness_from_cell(summ):
	return int(summ // (mosaic_size**2))

def get_gradations(steps):
	# Получаем лист градаций (неэффективно)
	gradations = [0]
	step = 255.0 / (gradations_steps-1)
	for i in range(gradations_steps-1):
		gradations.append(gradations[i]+step)
	for i in range(gradations_steps-1):
		gradations[i] = math.floor(gradations[i])
	return gradations

try:
	img = Image.open(sys.argv[1])
except:
	print('Ошибка загрузки картинки: файл не найден')
	input()
arr = np.array(img)

image_width= len(arr)
image_height = len(arr[1])

mosaic_size = int(input("Введите размер сетки (в пикс.): "))
gradations_steps = int(input("Введите кол-во градаций серого: "))+1

gradations = get_gradations(gradations_steps)

i = 0
while i < image_width:
	j = 0
	while j < image_height:
		# Вычисляем среднее по ячейке
		averenge_summ = get_averange_brightness_from_cell(get_calculated_cell(i, j))

		# Обновляем значения
		for n in range(i, i + mosaic_size):
			for n1 in range(j, j + mosaic_size):
				brightness = get_gradated_brightness(averenge_summ)
				try:
					arr[n][n1][0], arr[n][n1][1], arr[n][n1][2] = brightness, brightness, brightness
				except:
					pass

		j = j + mosaic_size
	i = i + mosaic_size

res = Image.fromarray(arr)
res.save('res.jpg')
