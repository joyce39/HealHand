


from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "jpacifico/Chocolatine-3B-Instruct-DPO-v1.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Message history with example (primer)
messages = [
    {
        "role": "system",
        "content": "You are a rehabilitation assistant AI."
    },
    {
        "role": "user",
        "content": "Given joint-level analysis in this format:\n\n{\n  \"index_tip\": {\n    \"avg_position_offset_m\": 0.025,\n    \"max_position_offset_m\": 0.031,\n    \"position_offset_stddev_m\": 0.0027,\n    \"max_velocity_difference_mps\": 0.12\n  },\n  \"wrist\": {\n    \"avg_position_offset_m\": 0.005,\n    \"max_position_offset_m\": 0.007,\n    \"position_offset_stddev_m\": 0.0011,\n    \"max_velocity_difference_mps\": 0.0072\n  }\n}\n\nPlease return a JSON summary structured like this:\n\n{\n  \"gesture_name\": \"grab\",\n  \"summary\": {\n    \"index_tip\": {\n      \"avg_position_offset_m\": 0.025,\n      \"max_velocity_spike_mps\": 0.12,\n      \"rotation_deviation\": \"moderate\"\n    },\n    \"wrist\": {\n      \"avg_position_offset_m\": 0.005,\n      \"rotation_deviation\": \"slight\"\n    }\n  },\n  \"comments\": [\n    \"Index was too high (2.5 cm). Try relaxing the fingertip and aligning it with your thumb.\",\n    \"you moved a bit too fast, maintain a smoother, more controlled gesture.\",\n    \"Wrist showed slight deviation. You’re close — just keep your wrist more neutral during the movement.\",\n    \"Great effort! With small adjustments, you’ll have a perfect gesture soon.\"\n  ]\n}\n\nYour output should include:\n1. A gesture name (default: \"grab\")\n2. A summary per joint with numerical metrics and a rotation deviation field (inferred if needed). Do not refer to specific frames unless frame numbers are explicitly included in the input.\n3. A list of comments that:\n   - Provide clear, practical advice for improvement\n   - Use encouraging and supportive tone\n   - Use short, simple, human-friendly sentences\n   - Are phrased as if speaking to a patient\nOnly return the JSON."
    }
]


# Start chat loop
while True:
    user_input = input("\nEnter new joint analysis:\n")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Append new joint data
    messages.append({"role": "user", "content": user_input})

    # Format full prompt
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

    # Generate reply
    response = generator(prompt, max_length=5120, do_sample=True, temperature=0.7)[0]['generated_text']

    # Extract model reply
    reply = response.split(prompt)[-1].strip()

    # Append reply to history
    messages.append({"role": "assistant", "content": reply})

    print(f"\nAssistant:\n{reply}")
