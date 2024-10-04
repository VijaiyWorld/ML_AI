from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd

# ensure ollama is running 
# calling Ollama Model
llmo = ChatOllama(
    model="llama3.2",
    temperature=0,
)

prompt_extract = PromptTemplate.from_template(
    """
    ### COMMENTS FROM SOURCE:
    "{comments_data}"
    ### INSTRUCTION:
    Your job is to extract the failure mode or type from the comment JSON format containing the 
	following keys: `Failure_reason_and_part` 
    Only return the valid JSON. and NO PREAMBLE
    ### VALID JSON (NO PREAMBLE):
    """
)

def getAnalysis(text,llm=llmo): 
    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={'comments_data':text.replace('\n','')})
    json_parser = JsonOutputParser()
    json_res = json_parser.parse(res.content)
    return json_res


cmt = pd.read_csv('comment.csv')

cmt['output'] = cmt['comments'].apply(getAnalysis)

cmt.to_excel('output.xlsx')