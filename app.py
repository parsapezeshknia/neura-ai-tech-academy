from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-for-production")

LESSONS = [
    {
        "id": "ai-basics",
        "number": "01",
        "category": "FOUNDATIONS",
        "title": "What is Artificial Intelligence?",
        "description": "Understand what AI is, where it appears in daily life, and how AI systems make predictions.",
        "duration": "8 min",
        "level": "Beginner",
        "icon": "✦",
        "color": "violet",
        "content": [
            ("The big idea", "Artificial Intelligence (AI) is a field of computer science focused on building systems that perform tasks that usually require human intelligence, such as recognizing patterns, understanding language, or making recommendations."),
            ("AI is a broad field", "AI is the umbrella term. Machine learning is one approach within AI, and deep learning is a specialized approach within machine learning."),
            ("Everyday examples", "Recommendation systems, voice assistants, spam filters, translation tools, and image recognition are common examples of AI in use.")
        ],
        "takeaway": "AI is the broad idea of making computer systems perform tasks associated with human intelligence."
    },
    {
        "id": "machine-learning",
        "number": "02",
        "category": "CORE CONCEPTS",
        "title": "Machine Learning",
        "description": "Explore how computers learn patterns from examples instead of following only fixed rules.",
        "duration": "10 min",
        "level": "Beginner",
        "icon": "⌘",
        "color": "blue",
        "content": [
            ("Learning from data", "Machine learning (ML) is a branch of AI. An ML model uses data to find patterns and then applies those patterns to new examples."),
            ("Training and testing", "During training, a model adjusts its internal parameters using example data. Testing evaluates how well it performs on data it has not seen during training."),
            ("A simple example", "A model trained with many labeled pictures of cats and dogs may learn visual patterns that help it classify a new picture.")
        ],
        "takeaway": "Machine learning uses examples and data to learn patterns that can be applied to new situations."
    },
    {
        "id": "neural-networks",
        "number": "03",
        "category": "CORE CONCEPTS",
        "title": "Neural Networks",
        "description": "Discover layers, nodes, and how information moves through a simplified neural network.",
        "duration": "12 min",
        "level": "Intermediate",
        "icon": "◎",
        "color": "cyan",
        "content": [
            ("Connected layers", "A neural network is a machine-learning model made of connected computational units, often called neurons or nodes."),
            ("Forward pass", "Input information moves through one or more hidden layers. Each connection has a weight, and each node applies a mathematical operation."),
            ("Learning", "During training, the network compares its output with the expected answer and adjusts weights to reduce error.")
        ],
        "takeaway": "Neural networks transform inputs through connected layers and learn by adjusting connection weights."
    },
    {
        "id": "large-language-models",
        "number": "04",
        "category": "GENERATIVE AI",
        "title": "Large Language Models",
        "description": "Learn what LLMs do, how they generate text, and why their answers need checking.",
        "duration": "11 min",
        "level": "Intermediate",
        "icon": "✳",
        "color": "pink",
        "content": [
            ("What is an LLM?", "A Large Language Model (LLM) is a machine-learning model trained on large collections of text. It learns statistical patterns in language."),
            ("Generating text", "Given a prompt, an LLM generates a response by predicting likely next tokens, one step at a time."),
            ("Important limitation", "An LLM can produce fluent but inaccurate information. Check important claims against reliable sources and do not treat generated text as automatically correct.")
        ],
        "takeaway": "LLMs generate language from learned patterns; fluent output is not a guarantee of accuracy."
    },
    {
        "id": "prompt-engineering",
        "number": "05",
        "category": "PRACTICAL AI",
        "title": "Prompt Engineering",
        "description": "Practice writing clear prompts with context, task instructions, and output requirements.",
        "duration": "9 min",
        "level": "Beginner",
        "icon": "⌁",
        "color": "orange",
        "content": [
            ("Be specific", "A useful prompt clearly states the task. Add relevant context so the model understands the situation."),
            ("Set constraints", "Specify the audience, tone, length, format, and any limits that matter."),
            ("Improve in steps", "Review the first answer, identify what is missing, and refine the prompt. Prompting is often an iterative process.")
        ],
        "takeaway": "Good prompts combine a clear task, useful context, and explicit output requirements."
    },
    {
        "id": "responsible-ai",
        "number": "06",
        "category": "AI LITERACY",
        "title": "Responsible AI",
        "description": "Understand bias, privacy, transparency, and the importance of human judgment.",
        "duration": "10 min",
        "level": "Beginner",
        "icon": "◇",
        "color": "green",
        "content": [
            ("Bias and fairness", "AI systems can reflect patterns and biases in their training data. Testing across different groups can help reveal unequal performance."),
            ("Privacy", "Avoid entering passwords, private records, or sensitive personal information into tools unless you understand how the data will be handled."),
            ("Human oversight", "People should review important AI-assisted decisions, especially in areas such as education, health, finance, and law.")
        ],
        "takeaway": "Responsible AI requires attention to fairness, privacy, transparency, and human oversight."
    }
]

QUIZ = [
    {
        "question": "Which statement best describes Artificial Intelligence?",
        "options": [
            "A field focused on systems that perform tasks associated with human intelligence",
            "A type of computer hardware",
            "A programming language",
            "A database that stores images"
        ],
        "answer": 0,
        "explanation": "AI is the broad field of building systems that can perform tasks such as language understanding, pattern recognition, and decision support."
    },
    {
        "question": "What is the main idea behind machine learning?",
        "options": [
            "A computer follows only manually written rules",
            "A model learns patterns from data",
            "A computer becomes conscious",
            "A program never changes after installation"
        ],
        "answer": 1,
        "explanation": "Machine-learning models use data to learn patterns that can be applied to new examples."
    },
    {
        "question": "What does an LLM commonly predict when generating text?",
        "options": [
            "The user's password",
            "The next token in a sequence",
            "The computer's temperature",
            "The exact truth of every sentence"
        ],
        "answer": 1,
        "explanation": "LLMs generate text by repeatedly predicting likely next tokens based on the context."
    },
    {
        "question": "Which is a responsible way to use AI?",
        "options": [
            "Assume every answer is correct",
            "Share private information in every prompt",
            "Check important claims and protect sensitive data",
            "Use AI output without reviewing it"
        ],
        "answer": 2,
        "explanation": "AI output can be inaccurate, and prompts may contain sensitive information. Verification and privacy awareness are important."
    },
    {
        "question": "Which prompt is likely to produce a more useful answer?",
        "options": [
            "Tell me stuff",
            "Explain",
            "Write something",
            "Explain machine learning to a beginner in 5 bullet points with one example"
        ],
        "answer": 3,
        "explanation": "The final prompt gives a clear task, audience, format, length, and an example requirement."
    }
]

@app.route("/")
def home():
    return render_template("index.html", lessons=LESSONS)

@app.route("/api/lesson/<lesson_id>")
def lesson(lesson_id):
    item = next((lesson for lesson in LESSONS if lesson["id"] == lesson_id), None)
    if item is None:
        return jsonify({"error": "Lesson not found"}), 404
    return jsonify(item)

@app.route("/api/quiz")
def quiz():
    # Keep the answer key on the server; send only questions and options.
    questions = [
        {"question": q["question"], "options": q["options"]}
        for q in QUIZ
    ]
    return jsonify({"questions": questions})

@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", [])
    if not isinstance(answers, list):
        return jsonify({"error": "Answers must be a list."}), 400

    score = 0
    results = []
    for index, question in enumerate(QUIZ):
        selected = answers[index] if index < len(answers) else None
        correct = selected == question["answer"]
        score += int(correct)
        results.append({
            "correct": correct,
            "correct_answer": question["answer"],
            "explanation": question["explanation"]
        })
    return jsonify({
        "score": score,
        "total": len(QUIZ),
        "percentage": round(score / len(QUIZ) * 100),
        "results": results
    })

@app.route("/api/assistant", methods=["POST"])
def assistant():
    payload = request.get_json(silent=True) or {}
    prompt = str(payload.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "Please enter a question."}), 400
    if len(prompt) > 1000:
        return jsonify({"error": "Please keep your question under 1,000 characters."}), 400

    # This is a small educational demo, not a live LLM connection.
    p = prompt.lower()
    if any(word in p for word in ["llm", "large language", "language model"]):
        answer = "A Large Language Model (LLM) is a machine-learning model trained on large amounts of text. It generates language by predicting likely next tokens from the context. Its answers can sound confident while still being incorrect, so verify important information."
    elif "machine learning" in p or p.strip() == "ml":
        answer = "Machine learning is a branch of AI in which models learn patterns from data. A model is trained on examples, evaluated on data it has not seen, and then used to make predictions or generate outputs."
    elif "neural" in p:
        answer = "A neural network is a model made of connected computational units arranged in layers. Information passes through the layers, and training adjusts connection weights to reduce the difference between predicted and expected outputs."
    elif "prompt" in p:
        answer = "A strong prompt states the task, gives relevant context, and specifies the desired format or constraints. For example: 'Explain neural networks to a beginner in four bullet points and include one everyday analogy.'"
    elif "bias" in p or "responsible" in p or "privacy" in p:
        answer = "Responsible AI includes checking for bias, protecting personal information, explaining limitations, and keeping human oversight for important decisions. Do not assume an AI output is automatically fair or accurate."
    else:
        answer = "Good question. This classroom demo assistant uses a small set of prepared explanations rather than a live AI model. Try asking about AI, machine learning, neural networks, LLMs, prompt engineering, bias, or privacy."
    return jsonify({"answer": answer, "mode": "demo"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
