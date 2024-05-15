# Install
First of all, clone the repository
```bash
git clone https://github.com/adrijmz/os_group_project.git
```

## Using Docker
To install the GROBID image, execute the following command
```bash
docker pull lfoppiano/grobid:0.7.2
```

To build the extractor image, execute the followint command from the root directory of the repository
```bash
cd /root/directory/of/os_group_project
docker build -t paper_kg .
```

## From Source
To install the GROBID image, execute the following command
```bash
docker pull lfoppiano/grobid:0.7.2
```

### Install Python Environment
This project requires Python 3.8

### Step 1
Create a virtual environment to isolate the project dependencies
```bash
conda create -n myenv python=3.8
```
Init the environment created if it is necessary
```bash
conda init myenv
```
Activate the new environment
```bash
conda activate myenv
```

### Step 2
Install dependencies
```bash
cd /path/to/root/directory/of/os_group_project
pip install -r requirements.txt
```