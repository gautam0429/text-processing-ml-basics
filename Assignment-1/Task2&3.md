# Task 2: Basic Machine Learning Concept

Edxso wants to categorize incoming support tickets from schools into three categories:

- Technical Issue
- Billing
- General Inquiry

This is a text classification problem because the input is a text-based support ticket and the output is one of the predefined categories.

## How I Would Build the Model

I would first collect a dataset of previous support tickets where each ticket already has a correct category.

My basic approach would be:

1. Collect and label the support ticket data.
2. Clean and preprocess the text by converting it to lowercase and removing unnecessary punctuation and stop words.
3. Convert the text into numerical features using TF-IDF.
4. Split the dataset into training and testing data.
5. Train a classification model using the training data.
6. Use the trained model to predict the categories of new support tickets.
7. Evaluate the model using suitable performance metrics.

The overall workflow would look like this:

Support Ticket Data
        ↓
Text Preprocessing
        ↓
TF-IDF Feature Extraction
        ↓
Train / Test Split
        ↓
Logistic Regression
        ↓
Predict Category
        ↓
Evaluate Performance



# Task 3: Conversational AI Concepts

## Intent Classification

Intent Classification is the process of identifying what the user is trying to do or what they want from the chatbot.

For example, if a student says:

> "I forgot my password and want to reset it."

The chatbot can identify the intent as:

Intent: Password Reset