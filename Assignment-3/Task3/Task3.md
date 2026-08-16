# Task 3: Handling Edge Cases, Noise, and Interruptions

## Question 1:-

Explain how you would implement a "barge-in" feature, allowing the user to interrupt the agent while it is speaking. What architectural changes are needed?

## Answer:-

I would implement barge-in by continuously monitoring the user's microphone even while the agent is speaking.

The architecture would use a Voice Activity Detection (VAD) component such as Silero VAD to detect when the user starts speaking.

The flow would be:

Agent Speaking
      ↓
TTS / Audio Playback
      ↓
Microphone continues listening
      ↓
VAD detects user speech
      ↓
Stop TTS
      ↓
Cancel current response if still running
      ↓
Process new audio through ASR
      ↓
RAG / LLM
      ↓
New TTS Response

The audio input and output should work independently so that the system can listen for interruptions while the agent is speaking.

I would also use a persistent WebSocket connection for real-time audio streaming and to send interruption/cancellation events between the client and backend.

---

## Question 2:-

Describe the logic or fallback mechanism you would implement when the ASR output has very low confidence or the user's speech is unintelligible. How does the agent gracefully recover without frustrating the user?

## Answer:-

I would check the ASR output quality or confidence before sending the transcript to the LLM.

The basic flow would be:

User Speech
     ↓
VAD
     ↓
ASR
     ↓
Confidence Check
     ↓
High Confidence → Continue to Intent / RAG / LLM
     ↓
Low Confidence → Ask User to Repeat or Clarify

For low-confidence or unintelligible speech, the assistant should respond naturally instead of generating an answer from an unreliable transcript.

For example:

"I didn't quite catch that. Could you please repeat that?"

If the problem continues, I would provide a more helpful prompt such as:

"Could you tell me whether you need help with a course, assignment, or mentoring session?"

I would also handle common edge cases:

- **Background noise:** Apply suitable audio preprocessing and use VAD to focus on speech.
- **Empty or very short input:** Avoid sending it to the LLM and ask the user to try again.
- **Ambiguous question:** Ask a short clarification question instead of making assumptions.
- **Repeated failures:** Limit retries and provide an alternative support option instead of repeatedly asking the user to repeat.

For example, if the user says:

"Tell me about the deadline."

The assistant could ask:

"Sure. Which course or assignment are you asking about?"

## Final Approach

For barge-in, I would continuously monitor the microphone and stop the current TTS response as soon as user speech is detected.

For low-confidence ASR, I would validate the transcript before processing it, ask the user to repeat or clarify when necessary, and provide a safe fallback after repeated failures.

This helps prevent incorrect responses while keeping the conversation natural and user-friendly.