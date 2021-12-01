questionBanksIDandName = "SELECT name, id FROM question_banks WHERE state = 'active' ORDER BY id asc"

noSubjects = """With internal_medicine as (
     WITH all_internal_medicine_question_subjects as (
    SELECT questions_subjects.question_id, questions_subjects.subject_id, subjects.name
    FROM questions_subjects
    JOIN
        question_banks_subjects ON question_banks_subjects.subject_id = questions_subjects.subject_id AND question_banks_subjects.question_bank_id = %(qbank_id)s
    JOIN
        subjects on subjects.id = questions_subjects.subject_id
)
    SELECT
        questions.id as id, string_agg(all_internal_medicine_question_subjects.name, ', ') as all_subjects
    FROM
        questions
    JOIN
        question_banks_questions qbqs ON qbqs.question_id = questions.id AND qbqs.question_bank_id = %(qbank_id)s
    LEFT OUTER JOIN
        all_internal_medicine_question_subjects ON all_internal_medicine_question_subjects.question_id = questions.id
WHERE
    questions.state = 'active'
GROUP BY
    questions.id
ORDER BY questions.id ASC),
internal_medicine_no_vc_or_ie as (SELECT
    distinct explanations.question_id as id,
    string_agg(subjects.name, ', ') as Subject_name
FROM
    explanations
JOIN
    question_banks_questions qbq on explanations.question_id = qbq.question_id
JOIN
    question_banks qb on qb.id = qbq.question_bank_id
JOIN
    questions on questions.id = qbq.question_id
JOIN
    questions_subjects on questions_subjects.question_id = questions.id
JOIN
    subjects on subjects.id = questions_subjects.subject_id
WHERE
    questions.state = 'active'
    and qb.id = %(qbank_id)s
GROUP BY
    explanations.question_id
ORDER BY
    explanations.question_id asc)
select
count(id)
FROM
    internal_medicine
WHERE
    all_subjects is null"""

questionsWithMultipleSubjects = """ WITH all_internal_medicine_question_subjects as (
SELECT questions_subjects.question_id, questions_subjects.subject_id, subjects.name
FROM questions_subjects
JOIN
    question_banks_subjects ON question_banks_subjects.subject_id = questions_subjects.subject_id AND question_banks_subjects.question_bank_id = %(qbank_id)s
JOIN
    subjects on subjects.id = questions_subjects.subject_id
), question_bank_question_subjects as (
SELECT
    questions.id as id,
    string_agg(all_internal_medicine_question_subjects.name, ', ') as all_subjects
FROM
    questions
JOIN
    question_banks_questions qbqs ON qbqs.question_id = questions.id AND qbqs.question_bank_id = %(qbank_id)s
LEFT OUTER JOIN
    all_internal_medicine_question_subjects ON all_internal_medicine_question_subjects.question_id = questions.id
WHERE
questions.state = 'active'
GROUP BY
questions.id
ORDER BY questions.id ASC)
SELECT
count(question_bank_question_subjects.id)
from question_bank_question_subjects
WHERE
question_bank_question_subjects.all_subjects ilike '%%,%%' """

noVitalConcept = '''select
    distinct explanations.question_id as qid,
    string_agg(question_banks.name, ',') as bank_names
    from
    explanations
    join questions on questions.id = explanations.question_id
    join question_banks_questions qbq on questions.id = qbq.question_id
    join question_banks on qbq.question_bank_id = question_banks.id
    where
    NOT explanations.name ilike '%%vital concept%%'
    AND questions.state = 'active'
    group by
    qid
    order by
    qid asc'''

noIncorrectAnswer = '''select
        distinct explanations.question_id as qid,
        string_agg(question_banks.name, ',') as bank_names
        from
        explanations
        join questions on questions.id = explanations.question_id
        join question_banks_questions qbq on questions.id = qbq.question_id
        join question_banks on qbq.question_bank_id = question_banks.id
        where
        NOT explanations.name ilike '%%incorrect answer%%'
        AND questions.state = 'active'
        group by
        qid
        order by
        qid asc'''

noRefernceLink = '''
select
    distinct questions.id as qid,
    string_agg(question_banks.name, ',') as bank_names
    from
    questions
    join question_banks_questions qbq on questions.id = qbq.question_id
    join question_banks on qbq.question_bank_id = question_banks.id
    where
    NOT questions.reference ilike '%href%'
    AND questions.state = 'active'
    group by
    qid
    order by
    qid asc
'''

allQuestionsQuestionBanks = '''
select
    distinct questions.id as qid,
    string_agg(question_banks.name, ',') as bank_names
    from
    questions
    join question_banks_questions qbq on questions.id = qbq.question_id
    join question_banks on qbq.question_bank_id = question_banks.id
    group by
    qid
    order by
    qid asc
'''
