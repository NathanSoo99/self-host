# Self-Host
Self hosted cloud storage solution using a virtual file system.

Currently only consists of a very basic virtual command line interface to create and look at virtual directories.

## Running the Program
1. Clone the repo
2. Set up and activate virtual environment
```bash
cd self-host
python3 -m venv self-host
source self-host/bin/activate
```
3. Install dependencies and create data and storage folders
```bash
pip install -r requirement.txt
mkdir data
mkdir storage
```
4. Run program
```bash
cd src
python3 run.py
```

## Objective
The idea is for a personal cloud storage solution for hosting locally on a PC or using cloud computing. Originally I planned on making this a mobile project, however due to my lack of familiarity, I have decided on getting started with a desktop version at least for the time being.

This is a personal project which I have wanted to start for a while, however I am quite the procrastinator and I have not been able to do so for a while. As a result I am doing this development formost with maximising movitation and minimising mental load in mind. This means that I am working on whatever seems doable at the time and not doing detailed planning.

## Development Log
### 20/8/26
Current progress until start of logs include:
- Database design to support virtual file system.
- Functions which inspect the contents of, create, modify and delete directories.
- Functions which currently read, create, modify and delete file metadata.