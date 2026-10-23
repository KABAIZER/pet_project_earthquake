{% docs col__event_id %}Уникальный идентификатор события в USGS.{% enddocs %}
{% docs col__event_at %}Время события (UTC).{% enddocs %}
{% docs col__event_date %}Дата события в UTC.{% enddocs %}
{% docs col__magnitude %}Магнитуда события.{% enddocs %}
{% docs col__mag_type %}Тип шкалы магнитуды (ml, mb, mw и др.).{% enddocs %}
{% docs col__place %}Текстовое описание места события, как его отдаёт USGS.{% enddocs %}
{% docs col__longitude %}Долгота эпицентра, градусы.{% enddocs %}
{% docs col__latitude %}Широта эпицентра, градусы.{% enddocs %}
{% docs col__depth_km %}Глубина очага, км.{% enddocs %}
{% docs col__is_tsunami_flagged %}Признак того, что USGS пометил событие флагом цунами. Это флаг оповещения, а не подтверждённое цунами.{% enddocs %}
{% docs col__url %}Ссылка на страницу события на сайте USGS.{% enddocs %}
{% docs col__updated_at %}Когда USGS последний раз обновлял запись (UTC).{% enddocs %}

{% docs col__region %}Регион: часть строки place после последней запятой (для «X, Alaska» это «Alaska»). Если запятой нет, берётся вся строка place.{% enddocs %}
{% docs col__magnitude_class %}Класс по магнитуде: micro (до 3), minor (3–4), light (4–5), moderate (5–6), strong (6–7), major (7 и выше).{% enddocs %}
{% docs col__depth_class %}Класс по глубине: shallow (до 70 км), intermediate (70–300 км), deep (300 км и глубже). Пусто, если глубина неизвестна.{% enddocs %}

{% docs col__day %}Дата (UTC), по которой агрегированы события.{% enddocs %}
{% docs col__events %}Количество событий.{% enddocs %}
{% docs col__avg_magnitude %}Средняя магнитуда, округлённая до двух знаков.{% enddocs %}
{% docs col__max_magnitude %}Максимальная магнитуда.{% enddocs %}
{% docs col__moderate_plus_events %}Количество событий магнитудой 5 и выше.{% enddocs %}
{% docs col__tsunami_flagged_events %}Количество событий с флагом цунами.{% enddocs %}
{% docs col__last_event_at %}Время самого последнего события в регионе (UTC).{% enddocs %}