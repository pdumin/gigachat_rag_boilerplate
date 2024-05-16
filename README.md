## Small Streamlit RAG-application

### Installation and running

1. Create virtual enviroment

    ```
   python -m venv .venv
   source .venv/bin/activate
    ```

2. Install dependencies: `pip install -r requirements.txt`
3. Create `.secrets.toml` in `.streamlit` dir with `GIGA_KEY='you_gigachat_key'`
4. Run app: `streamlit run app.py`

Replace `source.txt` file with data you needed. 

**TO DO**
* source file uploading
* setting chunksize and overlap size from web-interface 