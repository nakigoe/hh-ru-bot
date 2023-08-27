# Автоматизация отправки резюме и сопроводительных писем на hh.ru Vesrion 1.0 alpha
Питон бот: автоматизация отправки резюме и сопроводительных писем на hh.ru


<b>отправка 200 резюме за 15 минут одним кликом</b>

<b>Важное обновление от 27 августа 2023:</b> добавлены `user agent`, `cookies` и `local storage` для быстрого логина без пароля, чтобы минимизировать детект автоматизации.

Добавлена пауза 10 секунд на экране первого логина на случай ввода капчи от руки.

## Инструкция

Разрешение экрана и ширина в экрана пикселях важны на HH.RU
<br> Скрипт проверен на ширине экрана 1280px и 1366px. Рабоает!

### Замените:
  
  •  чтобы уменьшить детект автоматизации, замените информацию о Вашем браузере и устройстве, с которого вы обычно посещаете HH.RU `user_agent`
   
Вы можете с лёгкостью найти информацию о своём user-agent введя в строке поиска Вашего повседневного браузера и устройства ***"What's my user-agent?"*** , это обычная строка символов.

  •  имя пользователя `username`
  
  •  пароль `password`
  
  •  поисковый критерий `job_search_query`
  
  •  фильтр результатов (что исключить из результатов поиска) `exclude`
  
  •  файл с сопроводительным письмом `cover‑letter‑ru.txt`
  
  •  файл со сносками на Ваши работы (для автоматического заполнения дополнительных анкет hh.ru) `links‑list.txt`

<b>В планах:</b> автоматизация заполнения сверх-сложных анкет. 

### Установите Python:

  •  https://www.python.org/downloads/

### Установите PIP, если он не установился с Python автоматически:

  •  https://pip.pypa.io/en/stable/installation/

### Установите библиотеки (откройте командную строку):

  •  Selenium `pip install selenium`
  
### Завалите их своими резюме! 

  •  двойной щелчок мыши по `start.bat`

Свежая версия всегда здесь: https://github.com/nakigoe/hh-ru-bot
<br> Пишите, если Вы хотите получить уроки программирования: nakigoetenshi@gmail.com
<br> $60 в час

<h2 style="margin: 0 auto" align="center">Ставьте звёзды и делитесь сноской на репозиторий со всеми, кто искал работу, ищет работу, планирует искать работу!</h2>

💲💲 Отправляйте пожертвования студенту! https://nakigoe.org/ru/donate

<br>
<p style="margin: 0 auto" align="center">Посетите:</p>
<h1><a href="https://nakigoe.org/ru/" style="background-color: black;" target="_blank">
  <img style="display: block; width: calc(100vw - (100vw - 100%));"
    src="https://nakigoe.org/_IMG/logo.png" 
    srcset="https://nakigoe.org/_IMG/logo.png 4800w,
      https://nakigoe.org/_SRC/logo-3840.png 3840w,
      https://nakigoe.org/_SRC/logo-2560.png 2560w,
      https://nakigoe.org/_SRC/logo-2400.png 2400w,
      https://nakigoe.org/_SRC/logo-2048.png 2048w,
      https://nakigoe.org/_SRC/logo-1920.png 1920w,
      https://nakigoe.org/_SRC/logo-1600.png 1600w,
      https://nakigoe.org/_SRC/logo-1440.png 1440w,
      https://nakigoe.org/_SRC/logo-1280.png 1280w,
      https://nakigoe.org/_SRC/logo-1200.png 1200w,
      https://nakigoe.org/_SRC/logo-1080.png 1080w,
      https://nakigoe.org/_SRC/logo-960.png 960w,
      https://nakigoe.org/_SRC/logo-720.png 720w,
      https://nakigoe.org/_SRC/logo-600.png 600w,
      https://nakigoe.org/_SRC/logo-480.png 480w,
      https://nakigoe.org/_SRC/logo-300.png 300w"
    alt="NAKIGOE.ORG">
<img class="blend" style="display: block; width: calc(100vw - (100vw - 100%));" 
  src="https://nakigoe.org/_IMG/nakigoe-academy-night.jpg" 
  srcset="https://nakigoe.org/_IMG/nakigoe-academy-night.jpg 2800w,
    https://nakigoe.org/_SRC/nakigoe-academy-night-2048.jpg 2048w"
  alt="Nakigoe Academy">
  <img class="blend" style="display: block; width: calc(100vw - (100vw - 100%)); padding-bottom: 0.05em;"
    src="https://nakigoe.org/_IMG/logo-hot-bevel.png" 
    srcset="https://nakigoe.org/_IMG/logo-hot-bevel.jpg 4800w,
      https://nakigoe.org/_SRC/logo-hot-bevel-3840.jpg 3840w,
      https://nakigoe.org/_SRC/logo-hot-bevel-2560.jpg 2560w,
      https://nakigoe.org/_SRC/logo-hot-bevel-2400.jpg 2400w,
      https://nakigoe.org/_SRC/logo-hot-bevel-2048.jpg 2048w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1920.jpg 1920w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1600.jpg 1600w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1440.jpg 1440w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1280.jpg 1280w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1200.jpg 1200w,
      https://nakigoe.org/_SRC/logo-hot-bevel-1080.jpg 1080w,
      https://nakigoe.org/_SRC/logo-hot-bevel-960.jpg 960w,
      https://nakigoe.org/_SRC/logo-hot-bevel-720.jpg 720w,
      https://nakigoe.org/_SRC/logo-hot-bevel-600.jpg 600w,
      https://nakigoe.org/_SRC/logo-hot-bevel-480.jpg 480w,
      https://nakigoe.org/_SRC/logo-hot-bevel-300.jpg 300w"
    alt="NAKIGOE.ORG">
</a></h1>

<p style="margin: 0 auto" align="center">© NAKIGOE.ORG</p> 

<p style="margin: 0 auto" align="center">All rights reserved and no permissions are granted.</p>

<p style="margin: 0 auto" align="center">Please add stars to the repositories!</p>