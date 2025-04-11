class StructuredOutputModel:
    def __init__(self, base_model, output_schema):
        self.base_model = base_model
        self.output_schema = output_schema

    def invoke(self, input_data):
        # Call the base model with the input data
        response = self.base_model.invoke(input_data)
        # Parse the response into the structured output schema
        return self.output_schema.parse(response)