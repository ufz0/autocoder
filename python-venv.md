# Guide for Developers: Creating and Using a Python Virtual Environment

1. **Create a Virtual Environment**:
    Run the following command in your terminal:
    ```
    python3 -m venv <venv_name>
    ```
    Replace `<venv_name>` with the desired name for your virtual environment.

2. **Activate the Virtual Environment**:
    - On macOS/Linux:
      ```
      source <venv_name>/bin/activate
      ```
    - On Windows:
      ```
      <venv_name>\Scripts\activate
      ```

3. **Install Dependencies**:
    Once the virtual environment is activated, you can install Python packages using `pip`:
    ```
    pip install <package_name>
    ```

4. **Deactivate the Virtual Environment**:
    To exit the virtual environment, simply run:
    ```
    deactivate
    ```

5. **Freeze Dependencies**:
    To save the installed packages to a `requirements.txt` file:
    ```
    pip freeze > requirements.txt
    ```

6. **Recreate Environment from Requirements**:
    To recreate the environment on another machine:
    ```
    python3 -m venv <venv_name>
    source <venv_name>/bin/activate  # Activate the environment
    pip install -r requirements.txt  # Install dependencies
    ```