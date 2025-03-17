# Roadmap
## Last update: 17.03.2025

<details>
  <summary><h2 id="10">1.0 - Released | 16.03.2025</h2></summary>
  
### Input
- [x] Webserver  
- [x] PDF file upload  
- [x] Website Frontend  
- [x] Username and real name input  
- [x] PDF Processing  
- [x] Extract text from PDF  
- [x] Summarize text  
- [x] Parse text to AI Agent  
- [x] Allow manual input too (with /manual route)  

### AI Agent
- [x] Thinking  
- [x] Coding  
- [x] Summary  

### Output
- [x] Downloadable .cs file  

</details>

<details>
  <summary><h2 id="11">1.1 - Released | 17.03.2025</h2></summary>

### AI Agent
- [x] Generate .drawio files based on code  

### Output
- [x] Downloadable .drawio file  

### Documentation
- [x] Guide on how to self host  

</details>

<details>
  <summary><h2 id="11">1.2 - In Development | March 2025</h2></summary>
  
### PAP 
- [ ] Enhanced and refined pap design

### AI 
- [ ] Request changes to existing code

### Frontend
- [ ] Display version number
- [ ] Add website icon

</details>


# Self-Host & Contribution

## Get started

To self-host `autocoder`, follow these steps:

### Prerequisites
- Docker installed ([Installation guide](https://docs.docker.com/get-docker/))
- Git installed ([Installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/ufz0/autocoder.git
   cd autocoder
2. Build the docker image:
    ```sh
    docker build -t autocoder .
3. Run the container:
   ```sh
    docker run -d -p 8088:8088 --name autocoder autocoder
4. Open the website in your browser:
    https://localhost:8088


## Contributing

Contributions are welcome! Follow these steps to contribute:

### Guidelines
- Follow the existing code style.
- Ensure your changes do not break existing functionality.
- Write clear and concise commit messages.
- Update documentation if needed.

### Steps to Contribute
1. **Fork the repository** on GitHub.
2. **Clone your fork**:
   ```sh
   git clone https://github.com/your-username/autocoder.git
   cd autocoder
3. Create a branch for your change:
    ```sh
    git checkout -b feature-name
4. Make your changes and commit them:
    ```sh
    git add .
    git commit -m "Add feature-name"
5. Push your changes to your fork
    ```sh
    git push origin feature-name
6. Make a pull request on this repository

