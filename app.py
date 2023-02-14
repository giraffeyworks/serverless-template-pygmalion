from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Init is ran on server startup
# Load your model to GPU as a global variable here.
def init():
    global model
    global tokenizer

    print("loading to CPU...")
    model = AutoModelForCausalLM.from_pretrained("PygmalionAI/pygmalion-350m")
    print("done")

    # conditionally load to GPU
    if device == "cuda:0":
        print("loading to GPU...")
        model.cuda()
        print("done")

    tokenizer = AutoTokenizer.from_pretrained("PygmalionAI/pygmalion-350m")


# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model
    global tokenizer

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    max_new = model_inputs.get('max_new_tokens', 10)
    if prompt == None:
        return {'message': "No prompt provided"}
    
    # Tokenize inputs
    input_tokens = tokenizer.encode(prompt, return_tensors="pt").to(device)

    # Run the model, and set `pad_token_id` to `eos_token_id`:50256 for open-end generation
    output = model.generate(input_tokens, max_new_tokens=max_new, pad_token_id=50256)

    # Decode output tokens
    output_text = tokenizer.batch_decode(output, skip_special_tokens = True)[0]

    result = {"output": output_text}

    # Return the results as a dictionary
    return result
