# How to use this experiment preprocessor engine?

## Persyaratan

- Redeploy `vertexes-stream` stacks in Portrainer
- Don't forget to attach your env

## Step by step

1. **Clone Repository**
   Clone the Vertexes Stream to your local machine Anda with this command:

   ```bash
   git clone https://github.com/Vertexes-CSL/vertexes-stream.git
   ```

2. **Fill the .env inside**: Benchmark to the `.env.example` file

3. **Install the requirements, Start the engine**
   ```bash
   cd [folder]
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   python3 main.py
   ```

4. **Kafka Verification**: Open your Offset Explorer, use ths details
   - On General section, fill `Bootstrap Server` section with `85.209.163.202:9092,85.209.163.202:19092`
   - On Zookeeper section, fill `Host` and `Port` section with `85.209.163.202` and `2181`
   - Then, connect

5. **MongoDB Verification**: Access MongoDB Atlas, create your account and use the uri to be hitted in the `store` service env