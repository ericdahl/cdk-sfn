# cdk-sfn

Example repo showing AWS Step Function which:

- executes Lambda to flip a coin
- waits 5 seconds
- checks result
    - if Heads, finishes
    - if tails, repeats cycle
  

## Deployment

```
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ cdk deploy
```

## Cleanup

```
(.venv) $ cdk destroy
```
