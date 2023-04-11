# Amy-cli - AI-powered Command-Line Assistant

Amy is a command-line interface for using AI-powered instructions. It is designed to generate appropriate commands for a given query using OpenAI's GPT-3.5-turbo model.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/amy.git
cd amy
```


2. Install the required dependencies:
```python
pip install -r requirements.txt
```


## Usage

1. Initialize Amy with your OpenAI API key:
```python
python amy.py init <your_api_key>
```


Replace `<your_api_key>` with your actual OpenAI API key.

2. Use Amy with various commands:

- Execute a given query and run the generated instruction:

  ```
  python amy.py execute "<your_query>"
  ```

- Display the current configuration:

  ```
  python amy.py show_config
  ```

- Display the command history:

  ```
  python amy.py history
  ```

- Enter interactive mode to continuously input queries and execute instructions:

  ```
  python amy.py interactive
  ```

## Maintenance

To maintain Amy, you can update the configuration file (`config.json`) with new settings as needed. For example, you can update the allowed commands, engine, temperature, and other parameters.

If you want to clear the command history, you can delete or empty the `command_history.json` file.

## Contributing

If you would like to contribute to the project, please fork the repository and submit your changes through a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

This README.md template provides a brief introduction, installation instructions, usage guidelines, maintenance tips, and information about contributing to the project. Feel free to modify the content as needed to fit your specific requirements.

