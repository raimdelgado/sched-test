# sched-test

sched-test (python) is a Python 3 project for dealing with the schedulability of real-time tasks based on rate monotonic schedulability analysis (response time test and utilization bound test)

## Installation 

This project is currently running only on Linux (Debian-based distribution) with apt manager. Run the install_me.sh script :

```bash
sudo -H ./install_me.sh
```

This would create a virtual Python 3 environment in the same directory and install the required Python modules such as pyqt5 and numpy. 

## Usage

```bash
./sched-test
```
or: 

```bash
source ./init_python_venv.sh
python main.py
```

To clear the environment: (Only the required and install scripts will remain)

```bash
sudo -H ./clean_env.sh

```






