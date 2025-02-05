import streamlit as st
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.prompts import PromptTemplate
            
def llm_generator(subtitles, api_key):
    
    """Calling LLM and Generate Study Notes from the Subtitles"""
    
    llm = ChatNVIDIA(model="meta/llama-3.1-405b-instruct", nvidia_api_key=api_key)
    
    prompt = PromptTemplate(
        inputs=['subtitles'],
        template='''
        
        Here You have to make a study note from the below YouTube video subtitles. These subtitles mostly come in two languages: Hindi and English, and sometimes Hinglish.
        But you have to make notes in English only. The video subtitles are given below:

        {subtitles}
        '''
    )
    
    chain = prompt | llm
    
    try:
        
        response = chain.invoke(subtitles)
        
        return response.content
    
    except Exception as e:
        
        return f"Exception occoured at {e}"
    
