from transformers import AutoModel, AutoTokenizer


# Download the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf") 
model = AutoModel.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# Save the model locally if needed
model.save_pretrained("/Users/irinejuliet/Desktop/llama/Llama-2-7b-model")
tokenizer.save_pretrained("/Users/irinejuliet/Desktop/llama/Llama-2-7b-tokenizer")

print("Model and tokenizer successfully downloaded!")

#Reload your files offline
tokenizer = AutoTokenizer.from_pretrained("./models/hf-frompretrained-download/Llama-2-7b-chat-hf")
model = AutoModel.from_pretrained("./models/hf-frompretrained-download/Llama-2-7b-chat-hf")