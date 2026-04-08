import gradio as gr

def chat(message, history):
    message_length = len(message)
    word_count = len(message.split())
    response = f"(Agent Response): Message length of {message_length}, words: {word_count}"
    return response

gr.ChatInterface(
    fn=chat,
    title="Agent 1",
    description="Ask me a question about the documents.",
    examples=[
        "Why the sky is blue?",
        "Why the light is white?"
    ],
    textbox=gr.Textbox(placeholder="Type your message ...")
).launch(share=True)