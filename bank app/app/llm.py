# Instantiate a LLM

from pandasai.llm import OpenAI
llm = OpenAI(api_token="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")
from pandasai import SmartDataframe


def get_ans(df,que):
    print('----came here-----')
    print(df)
    print(que)
    sdf = SmartDataframe(df, config={"llm": llm})
    res=sdf.chat(que)
    return res