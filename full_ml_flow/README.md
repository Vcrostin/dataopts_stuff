```curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "age": -0.02,
       "sex": 0.03,
       "bmi": -0.05,
       "bp": 0.04,
       "s1": -0.01,
       "s2": 0.06,
       "s3": -0.03,
       "s4": 0.02,
       "s5": -0.04,
       "s6": 0.01
     }'
```

`{'predict': 99.18}`
