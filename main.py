from lxml import etree
from lxml.etree import ParseError
import csv

data_fields = [
'ClinVarAssertion/ClinVarAccession/@OrgID',
'ClinVarAssertion/ClinVarSubmissionID/@submitter',
'ClinVarAssertion/ClinVarSubmissionID/@submitterDate',
'ClinVarAssertion/ClinicalSignificance/ReviewStatus',
'ClinVarAssertion/ClinVarAccession/@Acc',
'ClinVarAssertion/ClinVarAccession/@Version',
'ReferenceClinVarAssertion/TraitSet/Trait/Name/ElementValue/@Type',
'ReferenceClinVarAssertion/TraitSet/Trait/Name/ElementValue',
'ClinVarAssertion/ObservedIn/Sample/Origin'
'ReferenceClinVarAssertion/MeasureSet/Measure/AttributeSet/XRef/@Type',
'ReferenceClinVarAssertion/MeasureSet/Measure/AttributeSet/XRef/@ID',
'ReferenceClinVarAssertion/MeasureSet/Measure/AttributeSet/XRef/@DB',
'ClinVarAssertion/MeasureSet/Measure/Name/ElementValue',
'ClinVarAssertion/MeasureSet/Measure/MeasureRelationship/Symbol/ElementValue',
]

def main():
    context = None
    field_headers = []
    try:
        wrote_header = False
        context = etree.iterparse("D:\\upwork\\clinvar\\ClinVarFullRelease_2020-02.xml", events=('start',), tag=('ClinVarSet'))

        for event, elem in context:
            try:
                row = []
                if event == 'start':
                    for d in data_fields:
                        try:
                            val = None
                            if '@' in d:
                                e = d[:d.rfind('/')]
                                a = d[d.rfind('/')+2:]
                                if wrote_header == False:
                                    field_headers.append(a)
                                ele = elem.find(e)
                                if ele != None:
                                    val = ele.attrib[a]
                            else:
                                if wrote_header == False:
                                    field_headers.append(d[d.rfind('/')+1:])
                                ele = elem.find(d)
                                if ele != None:
                                    val = ele.text
                            if val:
                                row.append(val)
                            else:
                                row.append('')
                        except ParseError as e:
                            print(e.__doc__)
                            print(e.args)
                            continue
            except ParseError as e:
                print(e.__doc__)
                print(e.args)
                continue

            with open('D:\\upwork\\clinvar\\data.csv', mode='a') as file:
                if wrote_header == False:
                    data_writer = csv.DictWriter(file, fieldnames=field_headers)
                    data_writer.writeheader()
                    wrote_header = True

                data_writer = csv.writer(file, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow(row)
            #elem.clear()
    except ParseError as e:
        print(e.__doc__)
        print(e.args)
        pass
    except Exception as e:
        print(e.__doc__)
        print(e.args)
    finally:
        context = None

if __name__ == '__main__':
    main()