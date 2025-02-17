MODEL_NAME='gpt-3.5-turbo'
DB_NAME = "expenses.db"
WATSON_PROMPT_LAB_URL="https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
WATSON_VISION_MODEL_ID="meta-llama/llama-3-2-11b-vision-instruct"
WATSON_VISION_MODEL_PROMPT="""Please analyze this receipt image and extract the following key information:
1. Total amount paid (final amount including any taxes and tips)
2. Currency used
3. Merchant/Store name
4. Date of transaction (if visible)

Important notes:
- If you see multiple amounts, focus on the final total amount
- Be precise with numerical values
"""
WATSON_ACCESS_TOKEN_POST_ENDPOINT = "https://iam.cloud.ibm.com/identity/token"