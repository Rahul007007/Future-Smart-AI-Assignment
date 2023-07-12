import openai
import os
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate

os.environ["OPENAI_API_KEY"] = ''


csv_path = "E:/Programs/NLP/Few-Shot-Prompting/TestPrThree.csv"
df = pd.read_csv(csv_path)

df.rename(columns={'  S.NO': 'S.NO',
                   '                                                                              REPORT': 'REPORT',
                   '                                         LABELS': 'LABELS',
                   }, inplace=True)

train_df, test_df = train_test_split(df, test_size=0.80, train_size=0.20, random_state=None, stratify=df['LABELS'])


examples = []
for index , rows in train_df.iterrows():
  eg = {'REPORT': rows['REPORT'], 'LABEL': rows['LABELS']}
  examples.append(eg)

openai_llm = OpenAI(verbose = True, temperature = 0.1)

examples[0].keys()

basic_prompt_template = PromptTemplate(input_variables = ["REPORT", "LABEL"],
                                          template= """
                                          REPORT: {REPORT}
                                          LABEL: {LABEL}""")

few_shot_template = FewShotPromptTemplate(
    examples = examples,
    example_prompt = basic_prompt_template,
    prefix = "You are given a set of REPORTS and their labels. Classify the REPORTS based on their labels. If you do not know the label correctly, return 'Invalid input'.\n\n",
    suffix= 'REPORT: {REPORT}\nLabel:',
    input_variables = ['REPORT'],
    example_separator = '\n'
)

chain = chain = LLMChain(llm = openai_llm, prompt = few_shot_template)

def predict(report):
  pred_label = chain.run(report)
  return pred_label


