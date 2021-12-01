from psycopg2 import connect
from pandas import DataFrame, ExcelWriter
from dataLists import dentalNames, medNames, paNames
from queries import noVitalConcept, noIncorrectAnswer, noRefernceLink, allQuestionsQuestionBanks


def main():
    # connect to production follower
    db = connect(dbname='d1uchr8lktdtps',
                 user='ucnfbftrefdbh7',
                 password='p04bb8279d315e59fc8bd98cf29bea29a9791eef4263938b67cbf4d57d9864f31',
                 host='ec2-3-223-71-97.compute-1.amazonaws.com',
                 port='5432',
                 sslmode='require')

    cur = db.cursor()
    crunchData(noVitalConcept, cur, 'exports/questions_with_no_vital_concepts.xlsx', [
               'QID', 'Banks'], allQuestions=False)
    crunchData(noIncorrectAnswer, cur, 'exports/questions_with_no_incorrect_answer.xlsx',
               ['QID', 'Banks'], allQuestions=False)
    crunchData(noRefernceLink, cur, 'exports/questions_with_no_reference_link.xlsx', [
               'QID', 'Banks'], allQuestions=False)
    crunchData(allQuestionsQuestionBanks, cur, 'exports/questions_with_multiple_questionBanks.xlsx',
               ['QID', 'Banks'], allQuestions=True)


def crunchData(query, cursor, file, columnNames, allQuestions):
    cursor.execute(query)
    res = cursor.fetchall()
    questions = []
    for item in res:
        question = {'id': item[0], 'banks': [item[1]]}
        questions.append(question)

    for question in questions:
        if ',' in question['banks'][0]:
            text = question['banks'][0]
            banksList = text.split(',')
            question['banks'] = banksList

    multiBankQuestions = list(
        filter(lambda question: len(question['banks']) > 1, questions))
    if not allQuestions:
        medicalQuestions = [
            q for q in questions
            if any(bank in medNames for bank in q['banks'])]
        print("total med questions", len(medicalQuestions))

        print(medicalQuestions[35])

        dentalQuestions = [
            q for q in questions
            if any(bank in dentalNames for bank in q['banks'])]
        print("total dental questions", len(dentalQuestions))

        naplexQuestions = [
            q for q in questions
            if q['banks'][0] == 'NAPLEX' and len(q['banks']) == 1]

        paQuestions = [
            q for q in questions
            if (len(q['banks']) == 1 and q['banks'][0] in paNames) or (len(q['banks']) == 2 and (q['banks'][0] in paNames and q['banks'][1] in paNames))]

        print("total naplex questions", len(naplexQuestions))
        writeToExcel(medicalQuestions, 'w', file,
                     'Medical', columnNames, 'Medical')
        writeToExcel(dentalQuestions, 'a', file,
                     'Dental', columnNames, 'Dental')
        writeToExcel(naplexQuestions, 'a', file,
                     'NAPLEX', columnNames, 'NAPLEX')
        writeToExcel(paQuestions, 'a', file, 'PA', columnNames, 'PA')
    else:
        writeToExcel(multiBankQuestions, 'w', file,
                     'Questions with Multiple Banks', columnNames, 'multiBankQuestions')


def writeToExcel(list, writeMode, file, sheet_name, columnNames, listName):
    if len(list) == 0:
        print(f'{listName} is empty exiting function.')
        return
    else:
        df = DataFrame.from_dict(list)
        with ExcelWriter(file, mode=writeMode) as writer:
            df.to_excel(writer, sheet_name=sheet_name,
                        index=False, header=columnNames)


if __name__ == '__main__':
    main()
