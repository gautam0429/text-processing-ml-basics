# Task 3: Troubleshooting and Debugging

## Scenario

A deployed conversational AI assistant was working fine, but recently it started classifying a large number of student queries as "Fallback/Unknown Intent", severely degrading the user experience.

### Question:-

As an AI Engineer, how would you troubleshoot and debug this issue? Mention at least 3 specific steps or areas you would investigate to find the root cause.

### Answer:-

I would troubleshoot the issue step by step and first try to identify what changed between the last working version and the current version.

### 1. Check Recent Changes and Deployments

I would first check whether there were any recent changes to the model, intent configuration, preprocessing logic, API, or application deployment. I would compare the current version with the last known working version and check recent Git commits and deployment logs.

### 2. Inspect the Queries Being Classified as Fallback

I would look at actual student queries that are being classified as `Fallback/Unknown Intent` and compare them with previously successful queries and the training data.

For example:

Previous query: "How do I reset my password?"

Recent query: "I cannot access my account anymore."

Both queries may have a similar meaning but different wording. This could indicate that the model does not have enough representative examples for the newer type of query.

### 3. Check Model Confidence and Fallback Threshold

I would check the confidence scores produced by the intent classifier. If the confidence scores have suddenly decreased, I would investigate whether the model configuration or fallback threshold has changed.

A threshold that is set too high could cause valid queries to be classified as `Fallback/Unknown Intent`.

### 4. Check the Preprocessing Pipeline

I would verify that the input preprocessing is still working correctly. I would check text normalization, tokenization, input formatting, and any recent changes to the tokenizer or preprocessing code.

A preprocessing issue could cause the model to receive incorrect or incomplete input and result in more fallback predictions.

### 5. Check for Data or Intent Drift

I would check whether students have started asking about new topics or using different language that was not present in the original training data.

If new types of queries are becoming common, I would collect and label representative examples and consider updating the training data and retraining or fine-tuning the model.

### 6. Check Logs and Monitoring

Finally, I would check application logs and monitoring data to identify when the fallback rate increased. I would compare the fallback rate before and after the issue and check whether the problem affects all intents or only specific categories.

After identifying the root cause, I would reproduce the issue in a test environment, apply the fix, and run regression tests using both previously failing and previously working queries before deploying the change to production.