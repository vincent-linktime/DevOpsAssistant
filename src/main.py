import gradio as gr
from qa_engine import QaEngine
import yaml


with open("config.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)

title = "AI assistant for DevOps backed by GPT"
if config["language"] == "cn":
    title = "GPT支持的DevOps智能助手"
    
qa_engine = QaEngine()
gr.ChatInterface(qa_engine.get_answer, title=title).queue().launch(share=True)