# My Energy App: API

## Prerequisites
1. The id and refresh token for your metering point. Those can be retrieved through the [Eloverblik portal](https://eloverblik.dk)
2. A config.ini file located at my-energy-app\api\ containing:
```
[DEFAULT]
meteringpointid = <meteringpointid>
refreshtoken = <refreshtoken>
```

## Install
`py -m pip install -r requirements.txt`

or

`conda install -n <env_name> requirements.txt`

## Run
`uvicorn main:app --reload`

## Explore
http://127.0.0.1:8000/docs
