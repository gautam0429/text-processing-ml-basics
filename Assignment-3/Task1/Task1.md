# Task 1: System Design & Architecture for Real-Time Voice Agent

## Scenario

Edxso is building an intelligent voice-based virtual assistant to help students navigate their courses, answer questions about their curriculum, and schedule mentoring sessions.

## Answer

I would design the voice agent as a real-time pipeline where audio is processed in small streams instead of waiting for the complete conversation turn.

The high-level flow would be:

Student Microphone
        ↓
Audio Streaming
        ↓
Voice Activity Detection
        ↓
Speech-to-Text
        ↓
Intent / Query Understanding
        ↓
Knowledge Retrieval
        ↓
LLM Response Generation
        ↓
Text-to-Speech
        ↓
Student Speaker

## 1. ASR - Automatic Speech Recognition

For speech recognition, I would use `faster-whisper`, which is an optimized implementation of the Whisper model and is suitable when faster inference is required.

I would use Silero VAD (Voice Activity Detection) before ASR to identify when the student is actually speaking and to reduce unnecessary processing of silence.

The flow would be:

Live Audio
    ↓
Silero VAD
    ↓
Short Audio Segments
    ↓
faster-whisper
    ↓
Transcript

For a real-time system, I would process short audio segments and update the transcript incrementally instead of waiting for the entire recording.

## 2. NLU and Intent Understanding

After ASR produces the transcript, the system needs to understand what the student is asking.

Some possible intents are:

- Course Information
- Course Progress
- Assignment Question
- Assignment Deadline
- Mentoring Session
- Technical Support
- General Inquiry

For common and well-defined intents, I would use a lightweight intent classifier to keep the response path fast.

For more complex or open-ended questions, the system can pass the query to an instruction-tuned LLM.

This gives a simple routing approach:

User Query
    ↓
Intent Detection
    ↓
 ┌───────────────────────┐
 │                       │
Known Intent        Complex Query
 │                       │
 ↓                       ↓
Specific Action       RAG + LLM
 │                       │
 └───────────┬───────────┘
             ↓
          Response

## 3. Knowledge Retrieval using RAG

For course information, curriculum details, FAQs, and mentoring information, I would use Retrieval-Augmented Generation (RAG).

Instead of relying only on the LLM's existing knowledge, the system would first search the Edxso knowledge base and provide the relevant information to the model.

The retrieval flow would be:

Student Query
      ↓
Embedding Model
      ↓
Vector Search
      ↓
Relevant Documents
      ↓
Retrieved Context
      ↓
LLM

For embeddings, I would use an open-source model from Sentence Transformers.

For the initial implementation, FAISS would be suitable for vector similarity search. It is lightweight and works well when the knowledge base is not extremely large.

## 4. LLM - Response Generation

For response generation, I would use an instruction-tuned open-source model such as a Llama-family model.

The LLM would receive:

- System instructions
- Current user question
- Relevant conversation history
- Retrieved knowledge from the RAG pipeline

The prompt structure would be:

System Instructions
        +
Conversation Context
        +
Retrieved Knowledge
        +
Current Question
        ↓
       LLM
        ↓
Contextual Response

I would instruct the model to use the retrieved information when answering knowledge-based questions and avoid inventing information when the required information is not available.

## 5. TTS - Text-to-Speech

For text-to-speech, I would use an open-source solution such as Piper.

The important part for a real-time system is that TTS should not wait for the complete LLM response.

As soon as a meaningful response segment is available, it can be passed to TTS.

The flow would be:

LLM Response Chunks
        ↓
Piper TTS
        ↓
Audio Chunks
        ↓
Student Speaker

This reduces the time between the user's question and the beginning of the spoken response.

## 6. Reducing Latency

For a natural voice conversation, I would focus on reducing the time-to-first-response rather than only optimizing the total processing time.

I would use:

1. WebSocket audio streaming so audio can be continuously sent between the client and backend.

2. VAD to detect speech boundaries and avoid processing unnecessary silence.

3. Small audio segments so the system does not have to wait for a complete recording.

4. Incremental ASR processing so partial transcription can become available while the user is speaking.

5. Early retrieval where possible, so knowledge retrieval can start as soon as enough information is available.

6. Streaming LLM output so the first response tokens are available before the entire response is generated.

7. Streaming or incremental TTS so speech synthesis can begin with the first response segment.

8. Keeping frequently used models loaded in memory instead of loading them for every request.

9. Using GPU inference where available for models that benefit from GPU acceleration.

The interaction would therefore look like:

Student Starts Speaking
        ↓
Audio Streaming
        ↓
VAD
        ↓
Incremental ASR
        ↓
Partial / Final Transcript
        ↓
Intent + Retrieval
        ↓
LLM Starts Generating
        ↓
First Response Segment
        ↓
TTS
        ↓
Student Hears Response

This approach reduces the perceived delay because different stages can begin processing as soon as their required input is available.

## 7. Conversational Memory and Multi-Turn Context

I would maintain a separate session for each active student using a unique session ID.

The session would contain recent conversation history and important state related to the current interaction.

For example:

Student:
"What is the deadline for my Python course?"

Assistant:
"The deadline is Friday."

Student:
"Can I get an extension?"

The second question does not mention the Python course again, but the previous conversation provides the required context.

For normal conversations, I would send the recent messages along with the current question.

The context would be:

System Instructions
        +
Recent Conversation History
        +
Retrieved Knowledge
        +
Current Question
        ↓
       LLM

I would avoid sending the complete conversation every time because it increases token usage and can increase latency.

For longer conversations, I would use:

- Recent conversation turns
- A short summary of older conversation
- Important session information
- Relevant information retrieved from the knowledge base

For example:

Session ID
    ↓
Recent Messages
    ↓
Conversation Summary
    ↓
Current Question
    ↓
RAG Context
    ↓
LLM

Any information that needs to persist across sessions should be stored carefully with appropriate privacy and data-retention rules.

## 8. Overall Architecture

The complete architecture would be:

                         STUDENT
                            │
                            ▼
                    Microphone / Audio
                            │
                            ▼
                  WebSocket Audio Stream
                            │
                            ▼
                       Silero VAD
                            │
                            ▼
                    faster-whisper
                            │
                            ▼
                        Transcript
                            │
                            ▼
                 Intent / Query Understanding
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
            Intent Router        RAG Retrieval
                  │                   │
                  │          Sentence Transformers
                  │                   │
                  │                 FAISS
                  │                   │
                  └─────────┬─────────┘
                            ▼
                   Conversation Context
                            │
                            ▼
                    Llama-family LLM
                            │
                            ▼
                    Response Streaming
                            │
                            ▼
                       Piper TTS
                            │
                            ▼
                    Audio Streaming
                            │
                            ▼
                         STUDENT

## 9. Proposed Technology Stack

ASR                  → faster-whisper

Voice Activity       → Silero VAD

NLU / Intent         → Lightweight intent classifier + LLM

LLM                  → Llama-family instruction-tuned model

Embeddings           → Sentence Transformers

Vector Search        → FAISS

TTS                  → Piper

Backend              → Python + FastAPI

Real-time Transport  → WebSocket

## Conclusion

I would build the voice agent using faster-whisper for ASR, Silero VAD for speech detection, a lightweight intent layer for common requests, an instruction-tuned Llama-family model for complex responses, Sentence Transformers with FAISS for knowledge retrieval, and Piper for TTS.

The main latency strategy would be to stream audio and responses, process short audio segments, keep models loaded, and start each stage as soon as its required input is available.

For multi-turn conversations, I would maintain session-based recent history and summarize older messages when the conversation becomes long. This provides enough context for the LLM without repeatedly sending the entire conversation.