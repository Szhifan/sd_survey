import streamlit as st 

st.title("Introduction")
st.header("Task Description",divider="red")
st.write("""
In this study, you will annotate broad and fine-grained targets, along with their corresponding stance, for 100 tweets. For each tweet, you will need to:
         
1. Identify if one or multiple pre-defined broad targets exist.
2. If the answer for first question is yes, determine if a fine-grained target (from a predefined list) under this broad target exists. If no fine-grained target is mentioned, please choose 'none' (Except for the target 'migration policies', where you have to manually input the name of the political entity mentioned in the tweet).
3. Select the stance the post expresses toward the selected target.
 
""")

st.header("Background Information & Terminology Explanation",divider="red")
st.write("""The targets we are interested in concern some highly specialized concepts in political science. Below we will demonstrate all targets and their fine-grained targets with a brief introduction and instruction. """)
st.subheader("Migrants",divider="red")
ex_illegal_migrants = """
:green[**Illegal migrants**]: a person who enters or resides in a country without legal authorization, either by crossing borders without permission or by overstaying a visa or permit. 

This target can be identified through a direct mention or keywords like “illegal”.

"""
ex_refugee = """
:green[**Refugees**]: People who flee their home country due to war, prosecution and other harms. In our dataset, these mainly concern Syrian and Afghan refugees fleeing from their home country to Europe. 
Other than direct mention, this target can be identified through context. If “migrants” are mentioned, but you can infer from the context that the post actually talks about refugees. 

This target can be selected when the word "refugee", "people fleeing their home country", "people escaping war" or similar terms are mentioned.
Refugee can be seen both as a legal term (a person that has been granted the legal status of refugee) and as a common parlance term (for everyone who fled their home country because of a conflict, fear or persecution, etc.).
"""
ex_asylum_seekers = """
:green[**Asylum seekers**]: also people fleeing from their country due to the same reasons as the refugees. The key difference between asylum seekers and refugees
 is that refugees have already been granted legal recognition of their status under international law, 
 while asylum seekers are in the process of having their claims evaluated. If their asylum application is successful, 
 they may be granted refugee status or other forms of protection. However, in the actual online discussions, 
 people may use refugees for those who flee from their home countries regardless of their actual legal status.

This target can be identified through the direct mention of the word “asylum”. 
"""
ex_eco_migrants = """
:green[**Economic migrants**]: Those who leave their home country for better economic/job opportunities. 

In our dataset, economic migrants often involve EU migrants in the UK in the discussion about Brexit.

"""

st.write(ex_illegal_migrants)
st.write(ex_refugee)
st.write(ex_asylum_seekers)
st.write(ex_eco_migrants)


st.subheader("European Union Institutions",divider="red")
st.write("In the tweets, the mention of this target is often signaled by the word “EU”. However, EU institutions should be identified as targets when it is interpreted as a governmental agency, not merely as a place name. The following fine-grained targets of EU institutions could be identified as targets if they are directly mentioned: ")

ex_eu_commission = """
:green[**European Commission**]
"""

ex_eu_parliament = """
:green[**European Parliament**]
"""

ex_eu_council = """
:green[**European Council**] 
"""

ex_frontex = """
:green[**Frontex**]: European Border and Coast Guard Agency
"""

ex_echo = """
:green[**ECHO**]: European Civil Protection and Humanitarian Aid Operations
"""

st.write(ex_eu_commission)
st.write(ex_eu_parliament)
st.write(ex_eu_council)
st.write(ex_frontex)
st.write(ex_echo)

st.subheader("Migration Policies",divider="red")
ex_tur_agreement = """
:green[**EU-Turkey refugee return agreement**]: Turkey agreed to significantly increase border security at its shores and take back all future irregular entrants into Greece (and thereby the EU) from Turkey to the EU. Click this [link](https://www.rescue.org/eu/article/what-eu-turkey-deal) for more information. 
"""
ex_dublin_regulation = """
:green[**Dublin Regulation**]: The Country in which the asylum seeker first applies for asylum is responsible for either accepting or rejecting the claim.  Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information. 
This target is usually identified through direct mention
"""
ex_refugee_quotas = """
:green[**Refugee quotas**]: a plan to relocate 120,000 asylum seekers over two years from the 'frontline' states Italy, Greece and Hungary to all other EU countries. France and Germany received the most quotas, and Countries like the Czech Republic, Hungary and Slovakia were against it. Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information
"""
ex_open_end_question = """
:green[**Policies of a political entity (party, country or politician) or 'concrete policy name' (e.g. Brexit)**]: 
Other than the aforementioned fine-grained targets, many posts comment on the migration policies of their own country and those of other EU countries, or on specific politicians or parties. 
Sometimes, it also involves specific policy names like Brexit.
:red[For this target, you have to manually input an answer].
"""

st.write(ex_tur_agreement)
st.write(ex_dublin_regulation)
st.write(ex_refugee_quotas)
st.write(ex_open_end_question)

st.subheader("Refugee pathways",divider="red")
ex_boat_sinking = """
:green[**Boat sinking**]: A tragic event where refugees’ boats sink in the Mediterranean sea. 
"""
ex_mediteranean_crossing = """
:green[**Mediterranean crossing**]: The dangerous journey that refugees take to cross the Mediterranean sea to reach Europe (mainly Italy, Spain and Greece). 
"""
ex_smuggling = """
:green[**Smuggling**]: The illegal act of transporting people across the border. 
"""
st.write("This includes phenomena occurring during refugees' journey.")
st.write(ex_boat_sinking)
st.write(ex_mediteranean_crossing)
st.write(ex_smuggling)
st.write("""These targets can be identified through direct mention or words like ship or boat, depending on the context.""")

st.subheader("Reception of refugees",divider="red")
st.write("This is the way asylum seekers/refugees are being received and treated in the receiving country.")
ex_refugee_camps = """
:green[**Refugee camps**]: Temporary shelters for refugees. This can be identified through direct mention or words like “detention camps”.
"""
ex_refugee_status = """
:green[**Refugee status**]: The legal status of refugees, which might include the right to work in the receiving country. This can be identified through direct mention or words like “asylum status”.
"""

st.write(ex_refugee_camps)
st.write(ex_refugee_status)

st.subheader("Asylum Procedure",divider="red")
st.write("This target concerns the legal procedures and concepts related to asylum applications. They could be identified through direct mention.")
ex_protection = """
:green[**Protection**]: The tweet may refer to international legal documents like the Geneva convention or the Global Compact for Refugees or Migration.
"""
ex_legal_rights = """
:green[**Legal rights**]: The tweet may refer to what rights the incoming refugees are awarded by the host states (the right to work or its absence, the right to move freely, or encampment)
"""
ex_compensation = """
:green[**Compensation**]: The tweet may refer to financial compensation given to refugees or asylum seekers by the host states (a daily allowance for example).
"""

st.write(ex_protection)
st.write(ex_legal_rights)
st.write(ex_compensation)
