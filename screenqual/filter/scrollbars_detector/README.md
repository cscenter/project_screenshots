## Основная идея алгоритма
Находить вертикальные и горизонтальные полосы прокруток любых типов на краях страницы.
## Границы применимости
Хорошо работает для поиска аномалий на десктопных  и мобильных скриншотах. Наблюдаются проблемы с подокументными скриншотами, где есть прокручивающиеся элементы и стрелка для их прокрутки. Это происходит из-за того, что на стрелке есть линия и она вместе с границей всего скриншота детектится как вертикальная прокрутка. 
## Описание алгоритма
Приведем описание для нахождения вертикальных прокруток, горизонтальные работают аналогично:
* Находим все линии на изображений с помощью HoughLinesP 
* Отбираем среди всех найденных линий вертикальные линии(x1 == x2) и проверяем, что эти линии достаточно длинные(больше половины скриншота по длине).
* Оставляем только такие вертикальные линии, которые лежат у правой границы(по x координате)
* Сортируем линии по x 
* Проверяем массив из линии, чтобы найти есть ли в нем хотя бы две такие, которые находятся на приемлемом расстоянии друг от друга, т.е. не слишком близко(это избавляет нас от случаев, когда HoughLinesP находит несколько линий в окрестностях одной и той же прямой на скриншоте) и не слишком далеко(чтобы не детектить прямоугольники и другие детали верстки как прокрутки)
