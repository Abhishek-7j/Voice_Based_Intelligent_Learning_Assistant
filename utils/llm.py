import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_ai_response(user_text, history=[], mode="Teacher"):
    """
    Generates a professional, AI-companion style response.
    Modes: Teacher, Coach, Creative
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return "CONFIG_ERROR: It looks like your OpenAI API Key is missing. Please add it to the .env file to activate my brain!"

    try:
        client = OpenAI(api_key=api_key)
        
        system_prompts = {
            "Teacher": "You are a world-class educational assistant, similar to Google Gemini. You explain complex topics simply, use structured bullet points, and encourage the user to ask follow-up questions.",
            "Coach": "You are a motivational learning coach. You help the user set goals, break down tasks, and stay focused. Your tone is energetic and supportive.",
            "Creative": "You are a creative brainstorming partner. You help the user think outside the box, generate stories, and explore weird ideas. Your tone is imaginative and slightly informal."
        }

        messages = [
            {"role": "system", "content": system_prompts.get(mode, system_prompts["Teacher"])}
        ]
        
        # Add history
        for msg in history:
            messages.append(msg)
            
        messages.append({"role": "user", "content": user_text})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.7 if mode == "Creative" else 0.5
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in LLM: {e}")
        if "api_key" in str(e).lower():
            return "CONFIG_ERROR: Your API Key seems invalid. Please check it in the .env file."
        return "I'm having a bit of trouble processing that right now. Could you please try asking again?"
