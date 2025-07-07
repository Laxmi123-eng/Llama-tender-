import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

@st.cache_resource
def load_model():
    model_id = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return tokenizer, model

st.title("📄 Tender Requirements Generator")
st.markdown("This app uses a LLaMA 2 model to generate tender specifications based on your answers.")

# Load model
tokenizer, model = load_model()

# Input box
user_input = st.text_area("Enter your tender clarification answers here:")

# Generate button
if st.button("Generate Requirements Section"):
    if user_input.strip() == "":
        st.warning("Please enter some input.")
    else:
        with st.spinner("Generating..."):
            prompt = f"""
You are a public procurement expert. Based on the following user clarification answers, write a professional tender 'Requirements and Specifications' section (800–1000 words).

--- USER CLARIFICATIONS ---
{user_input}
"""

            inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

            outputs = model.generate(
                **inputs,
                max_new_tokens=700,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1
            )

            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            st.subheader("📝 Generated Tender Section")
            st.write(result)
