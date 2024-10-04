class SimplePythonInterpreter:
    def execute(self, code):
        # Create a local dictionary to hold the function and variables
        local_scope = {}
        try:
            # Execute the validated code
            exec(code, {}, local_scope)
            return local_scope
        except Exception as e:
            print(f"Execution Error: {e}")
            return None