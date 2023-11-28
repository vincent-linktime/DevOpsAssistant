import gradio as gr
from qa_engine import QaEngine

qa_engine = QaEngine()
gr.ChatInterface(qa_engine.get_answer, title="AI assistant for DevOps backed by GPT").queue().launch(share=True)