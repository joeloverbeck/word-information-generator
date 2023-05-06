from tqdm import tqdm

# Add a wrapper function to show progress during the execution of a function
def progress_wrapper(func):
    def wrapped_func(*args, **kwargs):
        with tqdm(total=1, desc=f"Executing {func.__name__}...") as progress_bar:
            result = func(*args, **kwargs)
            progress_bar.update(1)
        return result
    return wrapped_func
