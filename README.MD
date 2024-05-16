## Small Streamlit RAG-application 

### Running in docker


1. Build container

    ```
    docker build -t name . 
    ```
2. Run
    ```
    docker run -p 8501:8501 -e GIGA_KEY=your_gigachat_key name
    ```
