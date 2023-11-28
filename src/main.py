import gradio as gr

def predict(message, history):

    yield .run(message)

gr.ChatInterface(predict, title="Sales Assistant backed by GPT").queue().launch(share=True)