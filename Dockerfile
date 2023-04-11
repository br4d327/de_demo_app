FROM python:3.10
EXPOSE 8501
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
COPY . .
CMD streamlit run app.py
