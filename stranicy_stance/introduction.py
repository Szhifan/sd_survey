import streamlit as st 

st.title("Introduction")
st.header("Task Description",divider="red")
st.write("**Stance Detection**")
st.write("""
Stance Detection (SD) is the task of determining the attitude expressed in a text towards a target. The most important components of a SD dataset are the target and the stance. The target is the entity towards which the attitude is expressed, and the stance is the attitude itself.
In our study, we focus on the stance detection of social media posts towards refugee crisis and Brexit from 2014 to 2019. Our dataset is different from the existing stance detection datasets in two aspects:
\n1: The targets are further divided into **fine-grained targets**. For instance, the target "migrants" is further divided into "refugees", "asylum seekers", "economic migrants", and "illegal migrants".
\n2: The targets are annotated by a large language model (LLM) instead of human annotators and/or direct matching from the text. In addition to the stance, you will also be asked to determine the relevance of the targets and fine-grained targets with respect to the post.
""")
st.write("**What is the task about?**")
st.write("""
In this study, you will be presented with a post and the target - fine-grained target pairs of the post annotated by the LLM. Note that for some posts, only the broad target is available; in this case, the target and fine-grained target will be the same.
Your task is to:
\n1: Choose how relevant the target and the fine-grained target are with respect to the post respectively. You may choose: :red[{irrelevant, somehow relevant, relevant}]. For targets that are directly visible in the text, you should choose "relevant". For targets that are not directly visible but can be inferred from the context, you should choose "somehow relevant". Otherwise, choose "irrelevant".\n
\n2: If the targets are relevant, you should annotate the stance of the post towards the targets. The available stances are: :red[{positive, negative, neutral}]. Neutral is selected when the post does not take a clear stance towards the target, e.g. news report. 

""")


st.header("Background Information & Terminology Explanation",divider="red")
st.write("""The targets we are interested in concern some highly specialized concepts in political science. Below we will demonstrate all targets and their fine-grained targets with their definitions and how they can be identified in the posts. And how the stances towards these targets can be determined.""")
st.subheader("Migrants",divider="red")

ex_illegal_migrants = """
:blue[**Illegal migrants**]: a person who enters or resides in a country without legal authorization, either by crossing borders without permission or by overstaying a visa or permit. 
:red[This target can be identified through a direct mention or keywords like “illegal”, or inferred from the context,] e.g. people crossing the border without permission.
"""
ex_refugee = """
:blue[**Refugees**]: People who flee their home country due to war, prosecution and other harms. 
:red[This target can be selected when the word "refugee" is mentioned. However, it can also be inferred from the context, e.g. people from Syria fleeing the war.]
"""
ex_asylum_seekers = """
:blue[**Asylum seekers**]: also people fleeing from their country due to the same reasons as the refugees. The key difference between asylum seekers and refugees
is that refugees have already been granted legal recognition of their status under international law, 
while asylum seekers are in the process of having their claims evaluated.
:red[This target can be identified through direct mentioning of people seeking asylum]. 
"""
ex_eco_migrants = """
:blue[**Economic migrants**]: Those who leave their home country for better economic/job opportunities. In our dataset, economic migrants often involve, but not limited to :red[EU migrants working in the UK].
"""
stance_migrants = """
\n:green[**positive stance**]: The text expresses a welcoming attitude towards migrants, e.g. by emphasizing their positive contribution (e.g. economic, cultural) to the host country. Or showing empathy towards their situation during the refugee crisis.
\n:red[**negative stance**]: The text expresses a hostile attitude towards migrants, e.g. by emphasizing the negative impact (e.g. economic, cultural) of migrants on the host country. Or showing a lack of empathy towards their situation during the refugee crisis.
"""
st.write("**Fine-grained targets**")
st.write(ex_illegal_migrants)
st.write(ex_refugee)
st.write(ex_asylum_seekers)
st.write(ex_eco_migrants)
st.write("**Stance**")
st.write(stance_migrants)

st.subheader("European Union Institutions",divider="red")
st.write("In the posts, the mention of this target is often signaled by the word “EU”. However, EU institutions should be identified as targets when it is interpreted as :red[a governmental agency that is involved in policy making or law enacting, not merely as a place name.] The following fine-grained targets of EU institutions could be identified as targets only if they are :red[directly mentioned:] ")

ex_eu_commission = """
:blue[**European Commission**]
"""

ex_eu_parliament = """
:blue[**European Parliament**]
"""

ex_eu_council = """
:blue[**European Council**] 
"""

ex_frontex = """
:blue[**Frontex**]: European Border and Coast Guard Agency
"""

ex_echo = """
:blue[**ECHO**]: European Civil Protection and Humanitarian Aid Operations
"""
stance_eu = """
\n:green[**positive stance**]: The text expresses a welcoming attitude towards the EU institutions, e.g. by emphasizing their positive contribution to the EU or positive role in the refugee crisis.
\n:red[**negative stance**]: The text expresses a hostile attitude towards the EU institutions, e.g. by emphasizing their negative impact on the EU or negative role in the refugee crisis.
"""
st.write("**Fine-grained targets**")
st.write(ex_eu_commission)
st.write(ex_eu_parliament)
st.write(ex_eu_council)
st.write(ex_frontex)
st.write(ex_echo)
st.write("**Stance**")
st.write(stance_eu)


st.subheader("Migration Policies",divider="red")
ex_tur_agreement = """
:blue[**EU-Turkey refugee return agreement**]: Turkey agreed to significantly increase border security at its shores and take back all future irregular entrants into Greece (and thereby the EU) from Turkey to the EU. Click this [link](https://www.rescue.org/eu/article/what-eu-turkey-deal) for more information. 
This target is usually identified through direct mention of :red["Turkey", "turkish government" or "Erdogan".]
"""
ex_dublin_regulation = """
:blue[**Dublin Regulation**]: The Country in which the asylum seeker first applies for asylum is responsible for either accepting or rejecting the claim.  Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information. 
This target is usually identified :red[through direct mention]. 
"""
ex_refugee_quotas = """
:blue[**Refugee quotas**]: a plan to relocate 120,000 asylum seekers over two years from the 'frontline' states Italy, Greece and Hungary to all other EU countries.
:red[This target can be identified through the word "quota" or the discussion about the distribution of the refugees among EU countries.]  Click this [link](https://www.bbc.com/news/world-europe-34329825) for more information.
"""
ex_open_end_question = """
:blue[**Policies of a political entity (party, country/government or politician) or 'concrete policy name' (e.g. Brexit)**]: 
Other than the predefined targets, the post might discuss the migration policies of a political entity (party, country or politician) or a concrete policy name (e.g. Brexit).
:red[This target can be identified through direct mention of the political entity or policy name.]
"""
stance_migration_policies = """
\n:green[**positive stance**]: The text expresses a welcoming attitude towards the migration policies, e.g. by emphasizing their positive contribution to the host country or positive role in the refugee crisis.
\n:red[**negative stance**]: The text expresses a hostile attitude towards the migration policies, e.g. by emphasizing their negative impact on the host country or negative role in the refugee crisis.
***
"""
st.write("**Fine-grained targets**")
st.write(ex_tur_agreement)
st.write(ex_dublin_regulation)
st.write(ex_refugee_quotas)
st.write(ex_open_end_question)
st.write("**Stance**")
st.write(stance_migration_policies)

st.subheader("Refugee pathways",divider="red")
ex_boat_sinking = """
:blue[**Boat sinking**]: The tragic event where refugees’ boats sink in the Mediterranean sea. 
"""
ex_mediteranean_crossing = """
:blue[**Mediterranean crossing**]: The dangerous journey that refugees take to cross the Mediterranean sea to reach Europe (mainly Italy, Spain and Greece). 
"""
ex_smuggling = """
:blue[**Smuggling**]: The illegal act of transporting/smuggling of people across the border. 
"""
stance_rp = """
\n:green[**positive stance**]: Due to the negative nature of the events, it is unlikely that the post will have a positive stance towards these events.
\n:red[**negative stance**]: The post either emphasizes the suffering of the refugees during these events (from pro-migrant perspective) or criticizes that foreigners are coming to the country illegally through these events (from anti-migrant perspective).
"""
st.write("This includes phenomena occurring during refugees' journey, or the ways they land in the host country.")
st.write("**Fine-grained targets**")
st.write(ex_boat_sinking)
st.write(ex_mediteranean_crossing)
st.write(ex_smuggling)
st.write("**Stance**")
st.write(stance_rp)

st.subheader("Reception of refugees",divider="red")
st.write("This is the way asylum seekers/refugees are being received and treated in the receiving country.")
ex_refugee_camps = """
:blue[**Refugee camps**]: Temporary shelters for refugees. This can be identified through direct mention or words like :red[“detention camps”.]
"""
ex_refugee_status = """
:blue[**Refugee status**]: The legal status of refugees, which might include the right to work in the receiving country. This can be identified through direct mention or words like :red[“asylum status”].
"""
stance_reception = """
\n:green[**positive stance**]: The text emphasizes the necessity of providing shelters and granting refugee status to the asylum seekers.
\n:red[**negative stance**]: The text emphasizes the poor conditions of the refugee camps or the lack of rights given to the refugees (from pro-migrant perspective). Or it opposes the idea of hosting refugees, providing them with shelters or granting them asylum status. (from anti-migrant perspective).
"""
st.write(ex_refugee_camps)
st.write(ex_refugee_status)
st.write("**Stance**")
st.write(stance_reception)

st.subheader("Asylum Procedure",divider="red")
st.write("This target concerns the legal procedures and concepts related to asylum applications. They could be identified through direct mention.")
ex_protection = """
:blue[**Protection (of refugees)**]: The post talks about the protection of refugees. 
"""
ex_legal_rights = """
:blue[**Legal rights (of refugees)**]: The post may refer to what rights the incoming refugees are awarded by the host states (the right to work or its absence, the right to move freely, or encampment)
"""
ex_compensation = """
:blue[**Compensation (of refugees)**]: The post may refer to financial compensation given to refugees or asylum seekers by the host states (a daily allowance or refugee hotel for example).
"""
stance_ap = """
\n:green[**positive stance**]: The text emphasizes the necessity of providing protection, legal rights, and compensation to the asylum seekers. Or praises the effectiveness of the asylum procedure.
\n:red[**negative stance**]: The text emphasizes the lack of protection, legal rights, or compensation given to the asylum seekers, or the inefficiency of the asylum procedure. (from pro-migrant perspective). Or it opposes the idea of providing protection, legal rights, or compensation to the asylum seekers. Or that the current asylum procedure facilitates the influx of refugees into the country.
(from anti-migrant perspective).
"""
st.write("**Fine-grained targets**")
st.write(ex_protection)
st.write(ex_legal_rights)
st.write(ex_compensation)
st.write("**Stance**")
st.write(stance_ap)
