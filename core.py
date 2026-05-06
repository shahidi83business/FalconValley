import importlib

class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, *args, **kwargs):
        if self.successor:
            return self.successor.handle(*args, **kwargs)
        return None

class ChainManager:
    def __init__(self, method_paths):
        """
        Initialize the ChainManager with a list of method paths.
        :param method_paths: List of tuples [(module_path, function_name), ...]
        """
        self.method_paths = method_paths

    def execute(self, *args, **kwargs):
        """
        Execute the chain of methods dynamically.
        :param args: Positional arguments for the first method.
        :param kwargs: Keyword arguments for the first method.
        :return: Output of the last method in the chain.
        """
        result = None
        for module_path, function_name in self.method_paths:
            try:
                # Dynamically import the module
                module = importlib.import_module(module_path)

                # Retrieve the function from the module
                func = getattr(module, function_name)

                # Ensure the retrieved attribute is callable
                if not callable(func):
                    raise TypeError(f"{function_name} is not callable in module {module_path}.")

                # Execute the function with the provided arguments
                result = func(*args, **kwargs)

                # Update args and kwargs for the next function in the chain
                args = (result,) if result is not None else ()
                kwargs = {}

            except ImportError as e:
                raise ImportError(f"Failed to import module {module_path}: {e}")

            except AttributeError as e:
                raise AttributeError(f"Module '{module_path}' does not have a function '{function_name}': {e}")

            except TypeError as e:
                raise TypeError(f"Error calling function '{function_name}' in module '{module_path}': {e}")

        return result

# Example usage
if __name__ == "__main__":
    # Define a chain of methods to execute
    method_chain = [
        ("core", "EcoMethod1Handler.handle"),
        ("core", "EcoMethod2Handler.handle")
    ]

    # Initialize the ChainManager with the method chain
    chain_manager = ChainManager(method_chain)

    # Execute the chain with initial arguments
    result = chain_manager.execute(method="eco1")
    print(result)  # Output: Eco Method 1 executed

    result = chain_manager.execute(method="eco2")
    print(result)  # Output: Eco Method 2 executed
