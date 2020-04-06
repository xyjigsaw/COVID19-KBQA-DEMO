from refo import finditer, Predicate, Star, Any    # 正则表达式库
import re

# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX medicalProperty: <http://www.openkg.cn/COVID-19/medical/property/>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        return self.action(matches), self.condition_num


# TODO 定义关键词
pos_characterName = "nr"
characterName_entity = (W(pos=pos_characterName))
characterName = (W("谁") | W("医生") | W(""))

pos_medicine = ["n", "ns"]
medicineName_entity = (W(pos="n") | W(pos="ns"))
medicineName = (W("什么"))
m_effectsName = (W("副作用"))

object_entity = (W(pos="n") | W(pos="nr") | W(pos="l"))
object = (W("是什么"))


class Question:
    def __init__(self):
        pass

    @staticmethod
    def general(word_objects):
        select = u"?o"
        sparql = None
        for w in word_objects:
            e = u"?label rdfs:label ?input. " \
                u"?label ?p ?o. " \
                u"FILTER (REGEX(str(?input), '" + w.token + "')). " \
                u"FILTER NOT EXISTS {?o rdfs:label ?o2}."
            sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                              select=select,
                                              expression=e)
            break
        return sparql

    @staticmethod
    def match_character(word_objects):
        select = u"?o2"
        sparql = None
        for w in word_objects:
            if w.pos == pos_characterName:
                e = u"?characterName rdfs:label '{characterName}'@zh." \
                    u"?characterName ns0:P2  ?sex.".format(characterName=w.token)

                e = "{ ?label rdfs:label '" + w.token + "'@zh. " \
                    "?label ?p ?o2. " \
                    "?p rdfs:label ?o." \
                    " FILTER NOT EXISTS {?o2 rdfs:label ?o3}.}" \
                    "union{?label rdfs:label '" + w.token + "'@zh. " \
                    "?label ?p ?o. " \
                    "?o rdfs:label ?o2.} "
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def match_medicine(word_objects):
        select = u"*"
        sparql = None
        for w in word_objects:
            if w.pos in pos_medicine:
                e = u"?label rdfs:label '" + w.token + "'@zh. " \
                    u"?label ?p ?o.  " \
                    u"FILTER NOT EXISTS {?o rdfs:label ?o2}."
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def match_medicine_effects(word_objects):
        select = u"?o2"
        sparql = None
        for w in word_objects:
            if w.pos in pos_medicine:
                e = u"?label rdfs:label '{inputx}'@zh." \
                    u"?label medicalProperty:P90 ?o." \
                    u"?o rdfs:label ?o2.".format(inputx=w.token)
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def match_character_property(word_objects):
        select = u"?o ?o2"
        sparql = None
        for w in word_objects:
            if w.pos in pos_medicine:
                e = u"?label rdfs:label '李文亮'@zh." \
                    u"?label ?p ?o2.?p rdfs:label " \
                    u"?o.FILTER NOT EXISTS {?o2 rdfs:label ?o3}." \
                    u"FILTER (REGEX(str(?o), '死亡时间'))"

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

rules = [
    Rule(condition_num=2, condition=(medicineName_entity + Star(Any(), greedy=False) + m_effectsName + Star(Any(), greedy=False)), action=Question.match_medicine_effects),
    Rule(condition_num=2, condition=((medicineName_entity + Star(Any(), greedy=False) + medicineName + Star(Any(), greedy=False))
                                     | (medicineName + Star(Any(), greedy=False) + medicineName_entity + Star(Any(), greedy=False))), action=Question.match_medicine),
    Rule(condition_num=2, condition=((characterName_entity + Star(Any(), greedy=False) + characterName + Star(Any(), greedy=False))
                                     | (characterName + Star(Any(), greedy=False) + characterName_entity + Star(Any(), greedy=False))), action=Question.match_character),
    Rule(condition_num=1, condition=(Star(Any(), greedy=False) + object_entity + Star(Any(), greedy=False)), action=Question.general),
    ]
