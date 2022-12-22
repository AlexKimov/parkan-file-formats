# Описание
Форматы файлов серии игр **Parkan**.

#### Текущие планы:

**1.** Распаковка файлов внутри архива.

**2.** Запаковка архивов.

**3.** Плагины для просмотра и сохранения файлов.

### Шаблоны
| № | Формат | Прогресс  | Шаблон |  Описание   |
| :-- | :------- | :-- | :-- | :-- |
|  **1**  |  .lib  |  | [LIB.bt](https://github.com/AlexKimov/parkan-file-formats/blob/master/formats/LIB.bt)  | Архивы игры **Parkan: Хроники Империи** с файлами, часть файла зашифрована |

### Скрипты
| № | Название  | Скрипт |  Описание   |
| :-- | :------- | :-- | :-- | 
|  **1**  |  decodeLIB.1sc  |  [decodeLIB.1sc](https://github.com/AlexKimov/parkan-file-formats/blob/master/scripts/decodeLIB.1sc)  | Расшифровка таблицы со списком файлов внутри .lib (**Parkan: Хроники Империи**) для правильной работы шаблона **LIB.bt** |
|  **2**  |  lib.bms  |  [lib.bms](https://github.com/AlexKimov/parkan-file-formats/blob/master/scripts/lib.bms)  | Распаковка файлов из .lib (**Parkan: Хроники Империи**) архивов |
