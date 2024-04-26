# Analysis and monitoring system using AWS

COMP4442 Project also...

<img width="454" alt="image" src="https://github.com/samchenghowing/COMP4442/assets/56993697/f8ce1790-f8a1-457a-a30d-32d850cfcc49">

## Project setup to run the backend application locally

### Create a virtual environment for the app

```
python3 -m venv .venv
source .venv/bin/activate

# in windows environment, use below
python3 -m venv .venv
source .venv/Scripts/activate
```

### Install the dependencies

```
pip3 install -r requirements.txt
```

### run the Spark app locally for testing


```
cd AWS_EMR_Spark


# Get driver_summary and save result csv to driver-summary folder
python3 driver_summary.py --data_source detail-records --output_uri result/driver-summary/

# Get driver_speed and save result csv to driver-speed folder
python3 driver_speed.py --data_source detail-records --output_uri result/driver-speed/ --start_time '2017-01-01 00:00:00' --end_time '2017-01-07 00:00:00'
```
