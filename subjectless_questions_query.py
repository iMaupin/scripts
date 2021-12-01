from psycopg2 import connect
from pandas import DataFrame, ExcelWriter
from queries import noSubjects, questionsWithMultipleSubjects
from getQuestionBanks import banks
from dataLists import dentalNames, paNames, medNames


def main():
    # connect to production follower
    db = connect()

    cur = db.cursor()

    medical = filter(lambda bank: bank['name'] in medNames, banks)
    naplex = filter(lambda bank: bank['name'] == 'NAPLEX', banks)
    dental = filter(lambda bank: bank['name'] in dentalNames, banks)
    pa = filter(lambda bank: bank['name'] in paNames, banks)
    categories = {'medical': list(medical), 'NAPLEX': list(
        naplex), 'dental': list(dental), 'PA': list(pa)}

    for index, category in enumerate(categories):
        print(f'Running {category} queries and exporting data to excel.')
        allBanksQuery(categories[category], noSubjects, 'exports/number_of_subjectless_questions_per_bank.xlsx',
                      ['Question Banks', 'Number of Subjectless Questions'], cur, f'{category}', index)

        allBanksQuery(categories[category], questionsWithMultipleSubjects, 'exports/questions_with_multiple_subjects_per_bank.xlsx',
                      ['Question Banks', 'Questions with multiple subjects'], cur, f'{category}', index)

    print("All queries complete and exported to excel documents.")


def allBanksQuery(banks, query, docname, columnNames, cursor, sheet_name, categoryIndex):
    output = []
    for index, questionBank in enumerate(banks):
        cursor.execute(query, {'qbank_id': questionBank['id']})
        res = cursor.fetchone()
        output.append((questionBank["name"], res[0]))
        df = DataFrame.from_dict(output)
        mode = 'w' if (index == 0 and categoryIndex == 0) else 'a'
        exists = 'replace' if mode == 'a' else None
        with ExcelWriter(docname, mode=mode, if_sheet_exists=exists) as writer:
            df.to_excel(writer, sheet_name=sheet_name,
                        index=False, header=columnNames)


if __name__ == '__main__':
    main()
