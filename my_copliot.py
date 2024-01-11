# Import the Google Generative AI library
import google.generativeai as genai

# Initialize the GenerativeModel with 'gemini-pro' for chat and code
text_model = genai.GenerativeModel('gemini-pro')

# Initialize the GenerativeModel with 'gemini-pro-vision' for graphs
image_model = genai.GenerativeModel('gemini-pro-vision')

# Configure the library with your API key
genai.configure(api_key="Your-API-Key-Here")

# Regular expression for pattern matching
import re

# IPython for working with IPython environment
import IPython

# OS for interacting with the operating system
import os

# JSON for working with JSON data
import json

# Base64 for encoding and decoding base64 data
import base64

# Image class from IPython.display for displaying images
from IPython.display import Image

# register_line_magic for registering custom magic commands
from IPython.core.magic import register_line_magic

# Registering a Jupyter Notebook magic command named 'chat'
@register_line_magic
def chat(contents):
    # Generating a response using the 'generate_content' method of the 'text_model' object
    # The method takes a formatted string containing the provided 'contents'
    response = text_model.generate_content(f'''
                                    Answer the question in a short quick readable paragraph, dont provide answer in any format or code
                                    {contents}
                                    ''').text

    # Printing the generated response to the output
    print(response)


# Define a function named 'chatn' that takes 'contents' as a parameter
@register_line_magic
def chatn(contents):
    try:
        # Use regular expression to find all occurrences of '--in' followed by digits in 'contents'
        numbers = [int(match.group().replace('--in', '')) for match in re.finditer(r'--in\d+', contents)]

        # Remove the found pattern '--in\d+' from 'contents'
        contents_filter = re.sub(r'--in\d+', '', contents)

        # Check if there are any references (numbers) found
        if numbers:
            # Retrieve the current cell contents for all references using the IPython 'In' variable
            current_cell_contents = [In[number] for number in numbers]

            # Combine the contents into a single string with line breaks
            combined_content = '\n'.join(current_cell_contents)

            # Execute the text_model to generate response
            response = text_model.generate_content(f'''
                                            {combined_content}
                                            Answer the question in a short readable paragraph, don't provide the answer in any format or code
                                            {contents_filter}
                                            ''').text

            # Print the generated response
            print(response)

        else:
            # Print an error message if no references are found
            print('Please provide a correct codeblock reference.')

    except Exception as e:
        # Print an error message if an exception occurs
        print('Please provide a correct codeblock reference.')

# Register a custom line magic command
@register_line_magic
def code(contents):

    # Get the IPython shell instance
    from IPython.core.getipython import get_ipython
    shell = get_ipython()

    # Generate code content using a text model
    response = text_model.generate_content(f'''
                                    write a python code that and dont answer anything else
                                    {contents}
                                    ''').text

    # Remove ``` and python from the response
    response = response.replace('```', '')

    # Clean up the response
    response = response.replace('python', '').strip('\n').rstrip('\n').replace('```python', '')

    # Prepare payload for setting the next input
    payload = dict(
        source='set_next_input',
        text=response,
        replace=False,
    )

    # Write the payload to the IPython shell
    shell.payload_manager.write_payload(payload, single=False)

# Define a function named 'coden' that takes 'contents' as a parameter
@register_line_magic
def coden(contents):
    try:

        # Get the IPython shell instance
        from IPython.core.getipython import get_ipython
        shell = get_ipython()

        # Use regular expression to find all occurrences of '--in' followed by digits in 'contents'
        numbers = [int(match.group().replace('--in', '')) for match in re.finditer(r'--in\d+', contents)]

        # Remove the found pattern '--in\d+' from 'contents'
        contents_filter = re.sub(r'--in\d+', '', contents)

        # Check if there are any references (numbers) found
        if numbers:
            # Retrieve the current cell contents for all references using the IPython 'In' variable
            current_cell_contents = [In[number] for number in numbers]

            # Combine the contents into a single string with line breaks
            combined_content = '\n'.join(current_cell_contents)

            # Execute the text_model to generate code
            response = text_model.generate_content(f'''{combined_content}
                                                  {contents_filter}
                                                  please write Python code and don't answer anything else, dont provide output of the code
                                                  ''').text
            # Remove ``` and python from the response
            response = response.replace('```', '')

            # Clean up the response
            response = response.replace('python', '').strip('\n').rstrip('\n').replace('```python', '')

            # Prepare payload for setting the next input
            payload = dict(
                source='set_next_input',
                text=response,
                replace=False,
            )

            # Write the payload to the IPython shell
            shell.payload_manager.write_payload(payload, single=False)

        else:
            # Print an error message if no references are found
            print('Please provide a correct codeblock reference.')

    except Exception as e:
        # Print an error message if an exception occurs
        print('Please provide a correct codeblock reference.')


############################################################### file_name must be provide in the same folder as the notebook
# Chat with graph Feature
# Try to get the current notebook filename using IPython
# try:
#     file_name = IPython.extract_module_locals()[1]['__vsc_ipynb_file__']

#     # Extract the base name (file name) from the file path
#     file_name = os.path.basename(file_name)

# except:
#     # If an exception occurs, print a message indicating no file
#     file_name = None
        
############################################################### file_name must be provide in the same folder as the notebook

# Register a custom magic command for the Jupyter notebook
@register_line_magic
def graph(contents):
    # Search for the pattern --in<number>
    pattern = re.compile(r'--in\d+')

    # Find the first occurrence of the pattern in the contents
    match = pattern.search(contents)

    # Remove the pattern from the contents
    contents_filter = pattern.sub('', contents)

    # Define a new pattern for --filename=<word>
    pattern_f = re.compile(r'--filename=\w+')

    # Find the first occurrence of the new pattern in the contents
    match_f = pattern_f.search(contents)

    # Remove the new pattern from the filtered contents
    contents_filter = pattern_f.sub('', contents_filter)

    # If the --in<number> pattern is found
    if match:
        # Get the global variable file_name
        global file_name

        # Check if file_name is available from the IPython magic command
        if file_name:
            notebookName = file_name
            with open(notebookName, "r") as f:
                # Load the notebook JSON data
                notebook_json = json.load(f)
        elif match_f:
            # Extract the filename from the --filename=<word> pattern
            match_c = match_f.group().replace('--filename=', '')
            notebookName = match_c + '.ipynb'
            with open(notebookName, "r") as f:
                # Load the notebook JSON data
                notebook_json = json.load(f)
        else:
            # If neither file_name nor --filename=<word> is provided, print an error message
            return 'Please provide a correct file path using --filename=<filename>.ipynb, e.g., --filename=mycode.ipynb'

        # Extract the number from the --in<number> pattern
        number = int(match.group().replace('--in', ''))

        # Find the cell with the specified execution_count in the notebook JSON data
        element = next(cell for cell in notebook_json['cells'] if 'execution_count' in cell and cell['execution_count'] == number)

        # Extract image data from the cell's output
        image_data = element['outputs'][0]['data']['image/png']

        # Decode base64 image data
        image_base64 = base64.b64decode(image_data)

        # Save the image in the local directory as img_code.jpg
        with open('img_code.jpg', 'wb') as f:
            f.write(image_base64)

        # Load the image using the Image() function
        image = Image(filename='img_code.jpg')

        # extract information using image model
        response = image_model.generate_content([contents_filter, image])
        print(response.text)
    else:
        # If --in<number> pattern is not found, print an error message
        print('Please provide a correct code block reference.')


# Chat with Files Feature
# Register a custom magic command for IPython
@register_line_magic
def chatf(contents):
    try:
        # Parse the folder name from the provided argument
        folder_match = re.search(r'--folder_name=(\S+)', contents)
        if not folder_match:
            # Print an error message if folder name is not provided in the correct format
            print("Please provide a valid folder name using the format '--folder_name=<folder_name>'.")
            return

        # Extract the folder name from the regex match
        folder_name = folder_match.group(1)

        # Get a list of Python files in the specified folder
        python_files = [file for file in os.listdir(folder_name) if file.endswith('.py')]

        # Check if any Python files were found
        if not python_files:
            print(f"No Python files found in the folder '{folder_name}'.")
            return

        # Initialize an empty string to store combined content
        combined_content = ""

        # Iterate through each Python file in the folder
        for file_name in python_files:
            with open(os.path.join(folder_name, file_name), 'r') as file:
                # Read the content of the file
                file_content = file.read()

                # Format the combined content with file name and its code
                combined_content += f"\nfile: {file_name}\n{file_content}\n{'_'*15}\n"

        # Remove the pattern of folder from the input contents
        contents_filter = re.sub(r'--folder_name=\S+', '', contents)

        # Generate content using a model and display the response
        response = text_model.generate_content(f'''
                                        {combined_content}
                                        Answer the question in a short readable paragraph, don't provide the answer in any format or code
                                        {contents_filter}
                                        ''').text
        print(response)

    except Exception as e:
        # Print an error message if an exception occurs
        print(f'An error occurred: {str(e)}')