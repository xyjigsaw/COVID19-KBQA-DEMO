import questionSearch
import questionSparql

if __name__ == '__main__':
    sparql = questionSearch.sparqlConnect()
    # 初始化 并加载外部词典
    q2s = questionSparql.QuestionSparql([u'./data/extendWords.txt'])

    while True:
        question = input("-----------\n你想说什么？（q 退出）\n试一试：\n李文亮医生是谁？\n苍术有什么副作用？\n老年人预防措施？\nInput:")
        if question == 'q':
            break
        query = q2s.get_sparql(question)
        if query is not None:
            result = sparql.get_sparql_result(query)
            values = sparql.get_sparql_result_value(result)

            if len(values):
                print("、".join(values))
            else:
                print("Sorry!")
        else:
            print("Developing in process!")
