Простой парсер

Собирает данные с новостных сайтов

В Таблице resource указанны поля:  
1. RESOURCE_ID - Это поле автоматически генерирует уникальный номер для ресурса в таблице.
2. RESOURCE_NAME - Это поле содержит краткое название ресурса.
3. RESOURCE_URL - Это поле содержит ссылку на ресурс где парсер забирает новости.
4. top_tag - Это поле содержит структуру для взятие ссылок на новости.( селектор html тега)
5. bottom_tag - Это поле содержит структуру для взятия текстового контента новости. ( селектор html тега)  
6. title_cut - Это поле содержит структуру для взятия заголовка новости. ( селектор html тега)  
7. date_cut - Это поле содержит структуру для взятия  даты и времени новости. ( селектор html тега)


В таблице items

1. id - Это поле автоматически генерирует уникальный номер для новости в таблице.  
2. res_id -  это поле resource_id из таблицы resource.  
3. link - это поле содержит ссылку на новость.  
4. title - это поле содержит заголовок новости.  
5. content - это поле содержит текстовый контент новости.  
6. nd_date - это поле содержит дату и время новости в формате Unix time.  
7. s_date - это поле содержит дату и время попадания новости в саму таблицу items в формате Unix time.  
8. not_date - это поле содержит дату новости в формате Год-Месяц-День.  


В папке last_pages хранятся файлы с номером страницы с которой парсер собрал ссылки.  
В случае обрыва начнет там где закончил.

