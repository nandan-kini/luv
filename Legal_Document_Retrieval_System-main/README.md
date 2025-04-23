
# Legal Sarathi

Our idea tackles a significant issue that attorneys in Indian courts deal with: the laborious and prone-to-error manual analysis of unstructured legal case documents. Insufficient contextual knowledge frequently causes delays and imprecise case comprehension. We suggest creating an automated event extraction tool as a solution to this. This program efficiently extracts important events, important players and timelines. We propose to optimize case analysis through an intuitive interface, guaranteeing precise insights.


![Logo](https://raw.githubusercontent.com/ishaanshetty2040/Legal_Document_Retrieval_System/main/LOGO-PROJECT.png)


## Installation

To get started with Legal Sarathi, follow these simple steps:

### Prerequisites
Docker installed on your system

### Step 1: Clone the Repository

```bash
git clone https://github.com/ishaanshetty2040/Legal_Document_Retrieval_System.git

cd Legal_Document_Retrieval_System
```
### Step 2: Build the Docker Image
We have provided a Dockerfile to streamline the setup process. Execute the following command to build the Docker image:
```bash
docker build -t mylegalsarathi .

```

### Step 3: Verify the Image Creation:
To ensure your image has been created and is listed among your local Docker images, run:
```bash
docker images

```
You should see **myLegalSarathi** in the list of available images

### Step 4: Run the Container
Once the Docker image is built successfully, run the container using the following command:
```bash
docker run -d --name project-container myLegalSarathi


```

### Step 5: Start the Backend (say on terminal 1)

To enable the backend, you will need to start the Uvicorn server. The server will host the ASGI application that powers the backend of Legal Sarathi. Run the following command inside the Docker container:
⁠ 
```bash
  uvicorn searchIndex:app --reload
```

### Step 6: Start the Frontend (say on another terminal, terminal 2)
To render the frontend, use the Streamlit application.

```bash
  streamlit run frontend.py
```


Now that you have both the backend and frontend running, Legal Sarathi should be fully operational. Enjoy using your Legal Sarathi application!

### Goals
* Develop an automated event extraction tool for legal case documents in Indian courts.
* Focus on capturing the context surrounding extracted events and participants to enhance comprehension of legal cases.
* Improve legal insights by providing meaningful and relevant insights from extracted events, aiding in trend identification.
* Develop a natural language processing (NLP) system capable of understanding user queries in natural language.
* Enable users to access the full PDF document directly from the search results.
* Providing full summary of the pdf and then user can also sort documents based on relevance most recent or oldest.

## Acknowledgements

We extend our heartfelt gratitude to Mr. Harsh Singhal and Mr. Shivananda S for their invaluable guidance and support throughout the duration of this project. Their expertise and encouragement have been instrumental in shaping our ideas and refining our approach. 
At the end, it wouldn’t have been possible without the dedication and collaborative spirit of the diligent team members(Ishaan, Joshitha, Kritika and Ninaad, students of Ramaiah Institute of Technology) which has significantly contributed towards the success of this endeavor.


## Demo

https://github.com/ishaanshetty2040/Legal_Document_Retrieval_System/assets/81769425/0b2e13dc-f8d8-41cb-9f8d-c3d3ae690bb7


