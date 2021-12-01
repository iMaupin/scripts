from getQuestionBanks import banks
nonmedNames = [
                'PANRE',
                'PANCE',
                'NCLEX-RN',
                'NCLEX-PN',
                'INBDE',
                'NAPLEX',
                'AANP Family Nurse Practitioner',
                'NBDE Part I',
                'NBDE Part II',
                'Pediatric Primary Care Nurse Practitioner',
                'Psychiatric-Mental Health Nurse Practitioner',
                'AACN Adult-Gerontology Acute Care NP',
                'Critical Care Nursing',
                'NBDHE',
                'ANCC Family Nurse Practitioner',
                'Adult-Gerontology Primary Care NP',
                'ANCC Adult-Gerontology Acute Care NP',
                'Learning System 3.0 NCLEX-RN',
                'Learning System 3.0 NCLEX-PN',
                'BoardVitals Team Training',
                'Certified Nurse Midwife',
                'Certified Pediatric Nurse ',
                'TEAS',
                'ARRT Radiography',
                'ARRT Mock Exam',
                'NPLEX Part 1',
                'NPLEX Part 2',
                'Surgical Technologist',
                'CST Mock Exam',
                'COVID-19: A New Virus and New Challenges',
                'Opioid Prescribing, Substance Abuse, and Pain Management'
                ]

medical = filter(lambda bank: bank['name'] not in nonmedNames, banks)
medNames = list(map(lambda item: item['name'], medical))

dentalNames = ['INBDE', 'NBDHE']

paNames = ['PANRE', 'PANCE']
