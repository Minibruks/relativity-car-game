Проект для Яндекс.Лицей. 
Учимся работать с PyGame.

Игра для демонстрации следствий из специальной теории отностительности.

Изучив на уроках возможности работы с сетевым репозиторием github, а также изучив некоторые возможности проекта PyGame, я нашел на github пример игры и на основе ее кода сделал свою ветку данной игры, где при отображении предметов учитываеются преобразования Лоренца при скоростях близких к скорости света.

Первоначальная версия - это игра в машинки, где нужно обгонять и не врезаться.
Я изменил физическую модель игры таким образом чтобы учитывались линейные искажения размеров автомобилей при околосветовых скоростях.
А чтобы они были заметны невооруженным взглядом - установил константу скорости света в моей игре - 30 км/ч

Управление:
стрелки вправо и влево - объезд припятствий.
Стрелки вверх вниз - изменение скорости автомобиля.

В верхней части экрана видим текущую скорость автомобиля и максимально возможную скорость в моем виртуальном мире (скорость света).
В процессе игры можно наблюдать сокращение размеров движущихся относительно нашего автомобиля предметов.

Изменяя в коде значение переменной crash_flag (0 или 1) можно отключить режим завершения игры после столкновения, чтобы удобнее было наблюдать за демонстрацией изменения линейных размеров предметов.

P.S. Действия игры перенесены в космос а в качестве фоновой музыки звучит песня Space Oddity Дэвида Боуи. "Как тебе такое Илон Маск?" :)