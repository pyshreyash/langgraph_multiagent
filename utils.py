from pydantic import ValidationError


# Function to validate LLM output with predefined schemas
async def validate_with_retry(llm_call, schema, retries=3):

    for _ in range(retries):

        result = await llm_call()

        try:
            return schema.model_validate(result)
        except ValidationError:
            continue

    raise ValueError("Failed structured output after retries")