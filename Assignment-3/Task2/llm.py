def generate_response(prompt: str) -> str:
    """Mock an LLM response using the RAG prompt."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    return (
        "Mentoring sessions can be scheduled through the mentoring "
        "section of the Edxso platform, based on the available "
        "time slots shown there."
    )


if __name__ == "__main__":
    test_prompt = "How can I schedule a mentoring session?"

    response = generate_response(test_prompt)

    print("Mock LLM Response:")
    print(response)