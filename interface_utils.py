ALL_TARGETS = {
"migration policies":{"fg_targets":["none","EU-Turkey refugee return agreement","Dublin Regulation","Refugee Quotas"]},
"European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"]},
"refugee pathways":{"fg_targets":["none","boat sinking","Mediterranean crossing","smuggling"]},
"reception":{"fg_targets":["none","refugee camps","refugee status"]},
"asylum procedures":{"fg_targets":["none","protection", "compensation", "legal rights"]},
"migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants"]}
} 
TARGETS_MAP = {
    "european union institutions": "European Union Institutions",
    "european parliament": "European Parliament",
    "european commission": "European Commission",
    "european council": "European Council",
    "dublin regulation": "Dublin Regulation",
    "turkey agreement": "EU-Turkey refugee return agreement",
    "reception": "reception of refugees",
    
}
RELEVANT_CHOICES = ["irrelevant","somehow relevant","relevant"]
STANCE_OPTIONS = ["positive","negative","neutral"]
ALL_FG_TARGETS = [item for target in ALL_TARGETS.values() for item in target["fg_targets"]]
EXAMPLES = [
    {
        "text": "Poland, Czech Republic, and Hungary, I advise you to resist the pressure of the EU to import migrants. If you need even more motivation, just look at Germany and Sweden.",
        "ans": [
            {
                "t": "migrants -> refugees",
                "s": "negative",
                "explanation": "The author of the post supports the hard-line asylum policies of Poland, Czechia and Hungary while hinting at the severe consequences of taking up migrants like Germany and Sweden. Although the post only mentions migrants, given the background knowledge of the 2014 refugee crisis the migrants here are the refugees from the Middle East. So the fine-grained target should be refugee."
            },
            {
                "t": "European Union Institutions -> none",
                "s": "negative",
                "explanation": "The phrase 'pressure of the EU' indicates, given enough background knowledge, that the EU pressured its member states to accommodate refugees during the refugee. In this case, 'EU' is not merely a place name but a political institution that enacts laws and makes political decisions. Since no specific EU institution name such as EU parliament is mentioned, a fine-grained target is not applicable in this case. Also, the author criticises EU for its policies."
            }
        ],
        "ans_stance": [
            {
                "t": "migrants -> refugees",
                "r": "relevant -> somehow relevant",
                "s": "negative",
                "explanation": "The post expresses a stance against refugees. Although the post does not directly mention refugees, we can infer that the migrants are the refugees from the Middle East."
            },
            {
                "t": "European Union Institutions -> European Union Institutions",
                "r": "relevant -> relevant",
                "s": "negative",
                "explanation": "The post criticizes the EU for its policies to force EU member states to take in refugees."
            }
            ]
    },
    {
        "text": "Salvini refuses to bend, I love it. Italy - Salvini Refuses To Let 177 Migrants Off Ship Till EU Agrees To Take Them (Video) news",
        "ans": [
            {
                "t": "migrants -> refugees",
                "s": "negative",
                "explanation": "Salvini is a right-wing Italian politician holding anti-migrant opinions. The post supports his hard-line policies against refugees thus the post is against the refugees."
            },
            {
                "t": "refugee pathways -> Mediterranean crossing",
                "s": "none",
                "explanation": "The mentions refugees coming to the EU by boat through the Mediterranean Sea, while no further stance is expressed."
            },
            {
                "t": "migration policies -> none",
                "s": "positive",
                "explanation": "The post strongly supports the migration policy of Salvini. (migration policies but not in predefined list)"
            }
        ],
        "ans_stance": [
            {
                "t": "migrants -> refugees",
                "r": "relevant -> relevant",
                "s": "negative",
                "explanation": "The post expresses a negative stance towards refugees by supporting Salvini's hard-line policies."
            },
            {
                "t": "refugee pathways -> Mediterranean crossing",
                "r": "relevant -> somehow relevant",
                "s": "neutral",
                "explanation": "The post indirectly mentions the Mediterranean crossing. However, it does not express a stance towards it."
            },
            {
                "t": "migration policies -> Salvini",
                "r": "relevant -> relevant",
                "s": "positive",
                "explanation": "The post supports the migration policy of Salvini"
            }
        ]
    },
    {
        "text": "The funny thing about Brexit is that even the racists will be disappointed by it. The UK is not going to expel 2 million EU workers otherwise economy collapses. & future immigration more likely to come from Africa/Asia as Europeans won’t want to come without guaranteed rights.",
        "ans": [
            {
                "t": "migrants -> economic migrants",
                "s": "positive",
                "explanation": "The post primarily mentions migrants and specifically concerns about the economic consequences of EU migrants leaving UK and acknowledges their contributions to the UK economy. Thus, the post talks about economic migrants from EU/Africa/Asia who come to the UK for career perspectives."
            },
            {
                "t": "migration policies -> Brexit",
                "s": "negative",
                "explanation": "The post criticizes the economic consequences of Brexit."
            }
        ],
        "ans_stance": [
            {"t": "migrants -> economic migrants",
            "r": "relevant -> relevant",
            "s": "positive",
            "explanation": "The post expresses a positive stance towards economic migrants by acknowledging their contributions to the UK economy."},
            {
            "t": "Asylum procedures -> Asylum procedures",
            "r": "irrelevant -> irrelevant",
            "explanation": "The post does not mention asylum procedures or refugees, plus the post only talks about economic migrants."
            }
        ] 
    },
    {
        "text": "(translated from German)RT @warum_nur74 @Beatrix_vStorch The EU (SPD HrTönnes) wants to do it that way too. Suspend Dublin and then if a refugee in Libya says that his relative is in Germany, he comes straight to Germany. He doesn't need papers. The word is enough. Sometimes I wish for other times.",
        "ans": [
            {
                "t": "migrants -> refugees",
                "s": "negative",
                "explanation": "The author wants a more tightened control of refugees, indicating an against stance toward refugees."
            },
            {
                "t": "migration policies -> Dublin Regulation",
                "s": "positive",
                "explanation": "The author of the post supports the Dublin Regulation that it regulates which refugee should be allocated to which EU country. Otherwise, the refugees will pick whatever country they like (especially wealthy EU country like Germany). (Migration Policies -> SPD -> against is an alternative answer.)"
            },
            {
                "t": "asylum procedures -> none",
                "s": "negative",
                "explanation": "The author talks about the way and procedures a refugee is allocated to the receiving country (either through the Dublin agreement or depending on their relatives in Germany). The author criticizes that this procedure can be easily abused by those who want to migrante to Germany."
            }
        ],
        "ans_stance": [
            {
                "t": "migrants -> refugees",
                "r": "relevant -> relevant",
                "s": "negative",
                "explanation": "The post expresses a stance against refugees by supporting a more tightened control of refugees."
            },
            {
                "t": "migration policies -> Dublin Regulation",
                "r": "relevant -> relevant",
                "s": "positive",
                "explanation": "The post expresses a stance in favor of the Dublin Regulation, according to which refugees should be allocated to the EU country where they first entered, not wherever they want to go."
            },
            {
                "t": "asylum procedures -> asylum procedures",
                "r": "relevant -> some how relevant",
                "s": "negative",
                "explanation": "The post talks about the way and procedures a refugee is allocated to the receiving country, and asylum procedures can be inferred from the context. The stance is against, because the author criticizes that this procedure can be easily abused."}]
    },
    {
        "text": "(translated from German)RT @Beatrix_vStorch Migrant distribution minister Seehofer is failing because of the EU states. Unlike the minister, they are still in their right minds. 110,000 asylum applications in Germany and he wants to take in even more. Dear CSU, send him into retirement at last. #AfD",
        "ans": [
            {
                "t": "migrants -> asylum seekers",
                "s": "negative",
                "explanation": "The author doesn’t want more asylum seekers in Germany."
            },
            {
                "t": "migration policies -> CSU",
                "s": "negative",
                "explanation": "The post criticizes the migration policy of CSU (AFD -> favor is also an acceptable answer)."
            }
        ],
        "ans_stance": [
            {
                "t": "migrants -> asylum seekers",
                "r": "relevant -> relevant",
                "s": "negative",
                "explanation": "The author of the post is against receiving more asylum seekers in Germany."
            },
            {
                "t": "migration policies -> CSU",
                "r": "relevant -> relevant",
                "s": "negative",
                "explanation": "The post explicitly criticizes the migration policy of CSU."
            }]
    }
]

COMPLETION_URL = "https://app.prolific.com/submissions/complete?cc=CHCBTBHM"
TASK_DESCRIPTION = """
                    Please determine if the following targets appear in the post, the :red[**question mark**] contains the fine-grained target of each broad target in case you have forgotten. 
                    Once you have selected a target, 
                    please determine its fine-grained target (choose **none** if only the broad target applies) and the stance.
                    You may choose :red[none] as the stance if the post does not express a stance towards the target. This typically occurs in a new-report-like post.
                    To cancel your selection, please click :red[**No**]. You can choose :red[**from one to three**] targets."""
TASK_DESCRIPTION_STANCE = """
                      Please determine how relevant are the demonstrated targets and its fine-grained targets in the post respectively. If the target and the fine-grained target are the same, you do not need to determine the relevance of the fine-grained target.
                      If the answer is relevant or somehow relevant, please determine the stance of the target in the post. 
"""
LANG2ID = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
TTL = 1200
TEXT_CSS = """
<style>
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: black;
            z-index: 999;
        }
        .fixed-header {
            background-color: black; /* Black background for dark mode */
            color: white; /* White text for dark mode */
            border-bottom: 1px solid black;
            font-size: 24px;
        }
    }
</style
"""

ATTENTION_TESTS = {
    "en": {
        "9e2e8d5be5bf82daca015182979de5ea":{
        "target":"migrants",
        "stance":"negative",
        "index":0
        },
        "fc1d3f0591eb6e9a232de8149397b8a0":
        {
        "target":"migrants",
        "stance":"negative",
        "index":1
        },
        "9e49fd91d1130b185e02d36ab56be615":
        {
        "target":"migrants",
        "stance":"negative",
        "index":2
        },
        "62bbe929d3354af8cb28004856189dd4":
        {
        "target":"migrants",
        "stance":"positive",
        "index":3
        },
        "4eddcf5e141baa7eba7b09d5cc25b7e0":
        {
        "target":"migrants",
        "stance":"negative",
        "index":4
        }
    },

    "de": {
        "ddd92e3180b6ecdb253ec7c95df055f1": {
            "target": "migrants",
            "stance": "positive",
            "index": 0
        },
        "20d10483ab9e7e0a70e26530f8c03052": {
            "target":"migrants",
            "stance":"negative",
            "index":1
        },
        "ca931346cb084f0f8a212f4f78734c59":{
        "target":"migrants",
        "stance":"negative",
        "index":2},
        "e2b3d0fff978d51ad9bfd1efa3a146be":{
        "target":"migrants",
        "stance":"negative",
        "index":3
        },
        "d6730e29c4947d1e7937743085ce4eaa":{
        "target":"migrants",
        "stance":"neutral",
        "index":4} 
    },
    "pl": {
        "5f60f7d43410669d2d8c38f5361ef6d9":{
        "target":"migrants",
        "stance":"negative",
        "index":0
        },
        "15ffad20c9fa69fcc7301e062a6abc09":{
            "target": "migrants",
            "stance": "negative",
            "index": 1
        },
        "61b067a075a6de55c8bce25b55f3c46f":{
        "target":"migrants",
        "stance":"negative",
        "index":2
        },
        "a24881757d15104690b0930ce8fd5b5a":{
        "target":"migrants",
        "stance":"negative",
        "index":3
        },
        "0403c4cf8a40b6c5fda60f8cd4236345":{
        "target":"migrants",
        "stance":"negative",
        "index":4
        }
        },
    "it": {
        "6e5cd55f920ae270ad14f5f93b9d7a4e":{
        "target":"migrants",
        "stance":"negative",
        "index":0
        },
        "6e5cd55f920ae270ad14f5f93b9d7a4e":{
            "target": "migrants",
            "stance": "negative",
            "index": 1},
        "d629c04fbc8bbdbe1d7441cce977de7e":{
            "target": "migrants",
            "stance": "positive",
            "index": 2
        },
        "b1a62b2d9fa75b8ac5103eaf7a832c9a":{
            "target": "migrants",
            "stance": "negative",
            "index": 3
        },
        "cc62cbedba736f70eba998611120449a":{
            "target": "migrants",
            "stance": "negative",
            "index": 4
        }
}} 

all_targets_match = {
    "migrants": ["migrants", "illegal migrants", "refugees", "asylum seekers", "economic migrants"],
    "european union institutions": ["european union institutions", "european parliament", "european commission", "european council", "frontex", "echo"],
    "migration policies": ["migration policies", "turkey agreement", "dublin regulation", "refugee quotas"],
    "refugee pathways": ["refugee pathways", "boat sinking", "mediterranean crossing", "smuggling"],
    "reception": ["reception", "refugee camps", "refugee status"],
    "asylum procedures": ["asylum procedures", "protection", "compensation", "legal rights"],  
}
all_targets = [item for sublist in all_targets_match.values() for item in sublist]