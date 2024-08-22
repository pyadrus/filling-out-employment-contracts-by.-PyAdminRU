# -*- coding: utf-8 -*-
from datetime import datetime

import openpyxl as op
from docxtpl import DocxTemplate
from loguru import logger

from parsing_comparison_file import parsing_document_1, compare_and_rewrite_professions

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы


def open_list_gup():
    file = 'list_gup/Списочный_состав.xlsx'
    wb = op.load_workbook(file)  # открываем файл
    ws = wb.active  # открываем активную таблицу
    list_gup = []  # создаем список
    for row in ws.iter_rows(min_row=6, max_row=1077, min_col=0, max_col=36):  # перебираем строки
        row_data = [cell.value for cell in row]  # создаем список
        list_gup.append(row_data)  # добавляем в список
    return list_gup  # возвращаем список


def filling_data_hourly_rate(row, formatted_date, ending, file_dog):
    doc = DocxTemplate(file_dog)
    context = {
        'name_surname': f" {row[6]} ",  # Ф.И.О. (Иванов Иван Иванович)
        'name_surname_completely': f" {row[7]} ",  # Ф.И.О. (Иванов И. И.)
        'date_admission': f" {formatted_date} ",  # Дата поступления
        'ending': f"{ending}",  # Окончание ый или ая
        'post': f" {row[3]} ",  # Должность
        'district': f" {row[1]} ",  # Участок
        'salary': f" {row[11]} ",  # Часовая тарифная ставка или оклад
        'series_number': f'{row[17]}',  # Номер паспорта
        'phone': f'{row[15]}',  # Телефон
        'address': f'{row[16]}',  # Адрес
        'issue_date': f'{row[18]}',  # Дата выдачи
        'issued_by': f'{row[19]}',  # Кем выдан
        'code': f'{row[20]}',  # Код подразделения
        'official_salary': 'часовая тарифная ставка',
        'official_salary_termination': 'часовой тарифной ставки',
        'month_or_hour': 'в час',
        'district_pro': f" {row[22]} ",  # Участок
    }
    doc.render(context)
    doc.save(f"готовые договора/{row[0]}_{row[5]}_{row[6]}.docx")


def record_data_salary(row, formatted_date, ending, file_dog):
    logger.info(f"Табельный номер: {row[5]}, Ф.И.О.: {row[6]}")  # форматирование даты
    doc = DocxTemplate(file_dog)
    date = row[34]
    day, month, year = date.split('.')  # Разделение даты, если в Excell файле стоит формат ячейки дата, то будет вызываться ошибка программы
    context = {
        'name_surname': f" {row[6]} ",  # Ф.И.О. (Иванов Иван Иванович)
        'name_surname_completely': f" {row[7]} ",  # Ф.И.О. (Иванов И. И.)
        'date_admission': f" {formatted_date} ",  # Дата поступления
        'ending': f"{ending}",  # Окончание ый или ая
        'post': f" {row[3]} ",  # Должность
        'district': f" {row[1]} ",  # Участок
        'salary': f" {row[11]} ",  # Часовая тарифная ставка или оклад
        'series_number': f'{row[17]}',  # Номер паспорта
        'phone': f'{row[15]}',  # Телефон
        'address': f'{row[16]}',  # Адрес
        'issue_date': f'{row[18]}',  # Дата выдачи
        'issued_by': f'{row[19]}',  # Кем выдан
        'code': f'{row[20]}',  # Код подразделения
        'official_salary': 'должностной оклад',
        'official_salary_termination': 'должностного оклада',
        'month_or_hour': 'в месяц',
        'district_pro': f" {row[22]} ",  # Участок
        'employment_contract_number': f' {row[28]}',  # Номер трудового договора
        'day': f'{day}',  # День
        'month': f'{month}',  # Месяц
        'year': f'{year}',  # Год
    }

    doc.render(context)
    doc.save(f"готовые договора/{row[0]}_{row[5]}_{row[6]}.docx")


def creation_contracts(row, formatted_date, ending):
    if row[11] > 1000:
        if row[21] == 7:  # 7 часов
            record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_7_часов.docx")
        elif row[21] == 8:  # 8 часов
            if row[2] == 'Рук.пр.гр.подз':
                record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР.docx")
            elif row[2] == 'Спец.пром.подз':
                record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР.docx")
            elif row[2] == 'Всп.раб.поверх':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            elif row[2] == 'Спец.пром.пов.':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            elif row[2] == 'Рук.пр.гр.пов.':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            elif row[2] == 'Рабоч.непр.гр.':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            elif row[2] == 'Руковод.непром':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            elif row[2] == 'Служащие пром.':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
            else:
                record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
        elif row[21] == 12:  # 12 часов
            record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор_12_часов.docx")

        elif row[21] == 24:  # 24 часов
            if row[2] == 'Всп.раб.поверх':
                if row[13] == 4:
                    record_data_salary(row, formatted_date, ending,
                                       "template/Шаблон_трудовой_договор_8_часов_ИТР_без_вредности.docx")
                else:
                    record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
        else:
            record_data_salary(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")
    elif row[11] < 1000:
        if row[21] == 6:  # 6 часов
            filling_data_hourly_rate(row, formatted_date, ending, "template/Шаблон_трудовой_договор_6_часов.docx")
        else:
            filling_data_hourly_rate(row, formatted_date, ending, "template/Шаблон_трудовой_договор.docx")


def format_date(date):
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    date = datetime.strptime(date, "%d.%m.%Y")
    return '" {:02d} " {} {} г.'.format(date.day, months[date.month], date.year)


if __name__ == '__main__':
    # TODO: Вынести в отдельную функцию
    print("Парсинг документа Exell\n1 - Парсинг документа Exell\n2 - Заполнение договоров\n3 - Сравнивание и заполнение данных в Exell\n\nВыберите значение:")
    user_input = int(input())
    if user_input == 1:
        parsing_document_1(min_row=6, max_row=1084, column=5, column_1=8)
    elif user_input == 2:

        start = datetime.now()  # фиксируем и выводим время старта работы кода
        logger.info('Время старта: ' + str(start))

        parsed_data = open_list_gup()
        for row in parsed_data:
            if row[14] == "Мужчина":
                ending = "ый"
                creation_contracts(row, format_date(row[8]), ending)
            elif row[14] == "Женщина":
                ending = "ая"
                creation_contracts(row, format_date(row[8]), ending)

        finish = datetime.now()  # фиксируем и выводим время окончания работы кода
        logger.info('Время окончания: ' + str(finish))
        logger.info('Время работы: ' + str(finish - start))  # вычитаем время старта из времени окончания

    elif user_input == 3:
        compare_and_rewrite_professions()
