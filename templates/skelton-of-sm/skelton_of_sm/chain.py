from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from langchain.schema.runnable import RunnablePassthrough
from skelton_of_sm.utils import create_list_elements
from langchain.pydantic_v1 import BaseModel

class ChainInput(BaseModel):
    question: str

#####################

skeleton_generator_template = """[User:] You’re an organizer responsible for only giving the skeleton (not the full content) for answering the question.
Provide the skeleton in a list of points (numbered 1., 2., 3., etc.) to answer the question. Instead of writing a full sentence,
each skeleton point should be very short with only 3∼5 words. Generally, the skeleton should have 3∼10 points. Now,
please provide the skeleton for the following question.
{question}
Skeleton:
[Assistant:] 1"""

skeleton_generator_prompt = ChatPromptTemplate.from_template(skeleton_generator_template)

skeleton_generator_chain = skeleton_generator_prompt | ChatOpenAI() | StrOutputParser() | (lambda x: "1. " + x)

#####################

point_expander_template = """[User:] You’re responsible for continuing the writing of one and only one point in the overall answer to the following question.
{question}
The skeleton of the answer is
{skeleton}
Continue and only continue the writing of point {point_index}. Write it **very shortly** in 1∼2 sentence and do not continue with other points!
[Assistant:] {point_index}. {point_skeleton}"""

point_expander_prompt = ChatPromptTemplate.from_template(point_expander_template)

point_expander_chain = RunnablePassthrough.assign(
    continuation=point_expander_prompt | ChatOpenAI() | StrOutputParser()
) | (lambda x: x['point_skeleton'] + " " + x['continuation'])

def get_final_answer(result):
    final_answer_str = "Here is the final answer:\n\n"
    for i, el in enumerate(result):
        stripped_el = el.split(". ", 1)
        if len(stripped_el) == 2:
            stripped_el = stripped_el[1]
        else:
            stripped_el = el
        final_answer_str += f"{i+1}. {el}\n"
    return final_answer_str

chain = (RunnablePassthrough.assign(
    skeleton=skeleton_generator_chain
) | create_list_elements | point_expander_chain.map() | get_final_answer).with_types(input_type=ChainInput)


if __name__ == "__main__":
    print(chain.invoke(
        {
            "question": "What are the most effective strategies for conflict resolution in the workplace?",
        }
    ))