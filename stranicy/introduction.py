import streamlit as st 

st.title("Introduction")
st.header("Task Description",divider="red")
st.write("""In this study, you will annotate the broad and fine-grained targets and their corresponding stance for 100 tweets (you can exit and re-enter the interface if you wish to pause, and your results will be saved). 
Given a tweet, you must identify 1) If one or multiple pre-defined broad targets exist. 2) If a fine-grained target (from a predefined list) of your previously chosen broad target exists, then 3) select the stance the post expresses toward your target. 
We design all our questions as simple multiple-choice questions except for the target “migration policies”. If you think “migration policies” are mentioned but don’t fit in with our predefined fine-grained target list, we will ask you which/whose migration policies (government, party, politicians, Brexit etc.) the post mentions and manually input the name of the relevant political entities/specific policies. 
Before proceeding to the actual annotation, we will test your ability by performing the SD annotation on a few simpler examples. You will proceed to the actual annotation if your performance is satisfactory.
 
""")

st.header("Background Information & Terminology Explanation",divider="red")
st.write("""The targets we are interested in concern some highly specialized concepts in political science. Below we will demonstrate all targets and fine-grained targets with a brief introduction and instruction. """)
st.subheader("Migrants",divider="red")
ex_illegal_migrants = """
**Illegal migrant**: a person who enters or resides in a country without legal authorization, either by crossing borders without permission or by overstaying a visa or permit. 
**This target can be identified through a direct mention or keywords like “illegal”.**

"""
ex_refugee = """
**Refugees**: People who flee their home country due to war, prosecution and other harms. In our dataset, these mainly concern Syrian and Afghan refugees fleeing from their home country to Europe. 
**Other than direct mention, this target can be identified through context. If “migrants” are mentioned, but you can infer from the context that the post actually talks about refugees, this target can be selected.**
"""
ex_asylum_seekers = """
**Asylum seekers**: also people fleeing from their country due to the same reasons as the refugees. The key difference between asylum seekers and refugees
 is that refugees have already been granted legal recognition of their status under international law, 
 while asylum seekers are in the process of having their claims evaluated. If their asylum application is successful, 
 they may be granted refugee status or other forms of protection. However, in the actual online discussions, 
 people may use refugees for those who flee from their home countries regardless of their actual legal status.
**This target can be identified through the direct mention of the word “asylum”.**
"""
ex_eco_migrants = """
**Economic migrants**: Those who leave their home country for better economic/job opportunities. 
**In our dataset, economic migrants often involve EU migrants in the UK in the discussion about Brexit.**

"""

st.write(ex_illegal_migrants)
st.write(ex_refugee)
st.write(ex_asylum_seekers)
st.write(ex_eco_migrants)


st.subheader("European Union Institutions",divider="red")
st.write("In the tweets, the mention of this target is often signaled by the word “EU”. However, EU institutions should be identified as targets when it is interpreted as a governmental agency, not merely as a place name. The following fine-grained targets of EU institutions could be identified as targets if they are directly mentioned: ")

ex_eu_commission = """
**European Commission**:
"""

ex_eu_parliament = """
**European Parliament**: 
"""

ex_eu_council = """
**European Council**: 
"""

ex_frontex = """
**Frontex**: European Border and Coast Guard Agency
"""

ex_echo = """
**ECHO**: European Civil Protection and Humanitarian Aid Operations
"""

st.write(ex_eu_commission)
st.write(ex_eu_parliament)
st.write(ex_eu_council)
st.write(ex_frontex)
st.write(ex_echo)

st.subheader("Migration Policies",divider="red")

ex_tur_agreement = """
**EU-Turkey refugee return agreement**: Turkey agreed to significantly increase border security at its shores and take back all future irregular entrants into Greece (and thereby the EU) from Turkey to the EU. Click this [link](https://www.rescue.org/eu/article/what-eu-turkey-deal) for more information. 
"""
ex_dublin_regulation = """
**Dublin Regulation**: The Country in which the asylum seeker first applies for asylum is responsible for either accepting or rejecting the claim.  Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information. 
This target is usually identified through direct mention
"""
ex_refugee_quotas = """
**Refugee quotas**: a plan to relocate 120,000 asylum seekers over two years from the 'frontline' states Italy, Greece and Hungary to all other EU countries. France and Germany received the most quotas, and Countries like the Czech Republic, Hungary and Slovakia were against it. Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information
"""
ex_open_end_question = """
**Policies of a political entity (party, country or politician) or 'concrete policy name' (e.g. Brexit)**: 
Other than the aforementioned fine-grained targets, many posts comment on the migration policies of their own country and those of our EU countries. This information also indicates the post’s stance toward migrants/refugees and the crisis. 

"""

st.write(ex_tur_agreement)
st.write(ex_dublin_regulation)
st.write(ex_refugee_quotas)
st.write(ex_open_end_question)

st.subheader("Refugee pathways",divider="red")
ex_boat_sinking = """
**Boat sinking**: A tragic events where refugees’ boats sink in the Mediterranean sea. 
"""
ex_mediteranean_crossing = """
**Mediterranean crossing**: The dangerous journey that refugees take to cross the Mediterranean sea to reach Europe (mainly Italy, Spain and Greece). 
"""
ex_smuggling = """
**Smuggling**: The illegal act of transporting people across the border. 
"""
st.write("This includes phenomena occurring during refugees' journey.")
st.write(ex_boat_sinking)
st.write(ex_mediteranean_crossing)
st.write(ex_smuggling)
st.write("""These targets can be identified through direct mention or words like shipt or boat, depending on the context.""")

st.subheader("Reception of refugees",divider="red")
st.write("This is the way asylum seekers/refugees are being received and treated in the receiving country.")
ex_refugee_camps = """
**Refugee camps**: Temporary shelters for refugees. This can be identified through direct mention or words like “ detention camps”.
"""
ex_refugee_status = """
**Refugee status**: The legal status of refugees, which might include the right to work in the receiving country. This can be identified through direct mention or words like “asylum status”.
"""

st.write(ex_refugee_camps)
st.write(ex_refugee_status)

st.subheader("Asylum Procuduere",divider="red")
st.write("This target concerns the legal procedures and concepts related to asylum applications.")
ex_protection = """
**Protection**: 
"""
ex_legal_rights = """
**Legal rights**:
"""
ex_compensation = """
**compensation**:
"""

st.write(ex_protection)
st.write(ex_legal_rights)
st.write(ex_compensation)
