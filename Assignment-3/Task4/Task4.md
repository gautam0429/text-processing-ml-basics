# Task 4: Evaluation and Production Monitoring

## Question 1:-

List and briefly explain 3 key evaluation metrics for the Speech components (ASR/TTS) and 2 metrics for the NLP/Response generation component.

## Answer:-

### Speech Components

**1. Word Error Rate (WER) - ASR**

WER measures how accurately the ASR system converts speech into text. It considers substitutions, deletions, and insertions. A lower WER means better transcription accuracy.

**2. Mean Opinion Score (MOS) - TTS**

MOS measures the perceived quality and naturalness of generated speech. Human evaluators usually rate the speech on a scale from 1 to 5. A higher score indicates better speech quality.

**3. Real-Time Factor (RTF) - ASR/TTS**

RTF compares the processing time with the actual audio duration. An RTF below 1 means the system can process audio faster than real time, which is important for a conversational voice agent.

### NLP / Response Generation

**4. Response Relevance**

This measures whether the generated response actually answers the user's question. For example, a question about an assignment deadline should receive an answer related to that deadline.

**5. Faithfulness / Groundedness**

This measures whether the generated response is supported by the information retrieved from the knowledge base. A higher groundedness means fewer unsupported or invented statements.

---

## Question 2:-

How would you automatically monitor and detect "hallucinations" (factually incorrect or out-of-context statements)?

## Answer:-

Since the voice agent uses RAG, I would compare the generated response with the retrieved knowledge before sending it to the user.

The basic flow would be:

User Query
    ↓
RAG Retrieval
    ↓
Retrieved Context
    ↓
LLM Response
    ↓
Groundedness Check
    ↓
Pass → Send Response
Fail → Retry / Safe Fallback

I would use a groundedness or NLI-based check to determine whether the response is supported by the retrieved context.

I would also check the retrieval similarity score. If the retrieved information is not relevant enough, the system should avoid generating an answer and instead ask the user to clarify the question.

For example:

"I don't have enough information to answer that accurately. Could you please clarify your question?"

In production, I would monitor retrieval scores, groundedness scores, fallback rate, response latency, and user feedback. A sudden increase in low-groundedness responses or fallbacks could indicate a problem with the model, prompt, or knowledge base.

## Final Approach

I would use WER, MOS, and RTF to evaluate the speech components, and response relevance and groundedness for the NLP component.

For hallucination detection, I would validate generated answers against the retrieved knowledge and use a safe fallback whenever the response cannot be sufficiently supported.