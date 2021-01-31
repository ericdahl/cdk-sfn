# cdk-sfn

Example repo showing AWS Step Function which:

- executes Lambda to flip a coin
- waits 5 seconds
- checks result
    - if Heads, finishes
    - if tails, repeats cycle
