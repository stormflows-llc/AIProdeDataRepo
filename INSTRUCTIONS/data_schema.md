# **Standardized JSON Data Schema for Full World Cup Predictions**

To ingest your predictions into the benchmarking engine, you must output a single, flat array of JSON objects under the root key "predictions".

Every single match (72 Group Stage matches \+ 32 Knockout matches \= 104 matches total) must contain exactly the keys specified below.

## **JSON Schema Specification**

{  
  "predictions": \[  
    {  
      "stage": "group\_stage",  
      "group": "A",  
      "match\_id": 1,  
      "home\_team": "Mexico",  
      "away\_team": "South Africa",  
      "predicted\_home\_score": 2,  
      "predicted\_away\_score": 0,  
      "extra\_time\_or\_penalties\_winner": "none",  
      "home\_win\_probability": 0.64,  
      "draw\_probability": 0.22,  
      "away\_win\_probability": 0.14,  
      "model\_confidence": "high"   
    },  
    {  
      "stage": "round\_of\_32",  
      "group": "none",  
      "match\_id": 73,  
      "home\_team": "Argentina",  
      "away\_team": "Sweden",  
      "predicted\_home\_score": 1,  
      "predicted\_away\_score": 1,  
      "extra\_time\_or\_penalties\_winner": "Argentina",  
      "home\_win\_probability": 0.45,  
      "draw\_probability": 0.35,  
      "away\_win\_probability": 0.20,  
      "model\_confidence": "medium"  
    }  
  \]  
}

## **Validation Rules**

1. "stage": Must be a string strictly restricted to: \["group\_stage", "round\_of\_32", "round\_of\_16", "quarterfinals", "semifinals", "third\_place", "grand\_final"\].  
2. "group": Must be a single uppercase string letter from "A" to "L". For all knockout stages, this value MUST be "none".  
3. "match\_id": An integer from 1 to 104 tracking the sequential order of matches. (Matches 1-72 are Group Stage; 73-104 are Knockout Stage).  
4. "predicted\_home\_score" / "predicted\_away\_score": Must be integers ![][image1] reflecting the score at the end of active play (90 mins for group stage, 90 or 120 mins for knockout stage).  
5. "extra\_time\_or\_penalties\_winner": If a knockout match is a draw, specify the country name that advances via Extra Time or Penalties. If the match is settled in 90 minutes (or is a group stage match), this MUST be "none".  
6. "home\_win\_probability" \+ "draw\_probability" \+ "away\_win\_probability": Must sum up exactly to 1.00 (![][image2]). Note: In knockout stages, draw\_probability maps the likelihood of the game going to extra time/penalties.  
7. "model\_confidence": String enum restricted strictly to \["high", "medium", "low"\].  
8. Total Array Length: Must contain exactly 104 objects. No missing rows, no duplicate matches.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAZCAYAAABQDyyRAAABS0lEQVR4Xu2UvUrDUBiGKy66iIM4xPySiLjqoCC4OQmOgrOLCF6C4OTSW3Bx8RoEN8HFSUHq6CUoCqIu+hwJEt/ka9OWgkIe+Cjnfb+/E8pptRoaRkgURYfEM/FK7Kr/QxiGGyR8EvvqDQq9OsRF4XxHXBVzSrDIWr5IW71+yLJsyvVR3WlxHE+rXsL3/XmS34kz9epA3Y21AHGiuonneTMUPLL1pXrdyAdZC5T0nrDABIUPRIfjuPqKNcjSa5Gm6SzFT/xPztVTrEGW3pUkSRYo+uArnKpnYQ2y9EoYvO6SufGxer2wBln6L7jpTp448JtA7UvVoLzvverfcNMDlxAEwZZ6/UKvbWsBvGXV3a2PMJdUHwY3jL57hXO7aqmRwWM2mS9xze8t8YY8pnl/A7adY8PNOsGNVrV+aNyTS+OVOsESi1rf0PCv+QLpW2u3//Aa/QAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAZCAYAAACRiGY9AAAB90lEQVR4Xu2VzytEURTHzcJCoagpZcybMVMTIszWRnaysLHzB1iLlYWNhY0tf4BsrJSyY2VlR5SSJj9DaNhMQ+F7xn3jOHMud1JT6n7r23Q/59z7zvfNvDd1dV5eXrVSJB6PT0ioKQiCYfgYfofXZP0noX8JfoEfcL0hWedCzyrcJbmzYrFYAw6YkVwKPdPwW7hOJBJTFI732IS+J3iBrQvYvyh6dul8OpOM4N28XpWi0WgjDpmVXMpc7NvdIyaHk8JwIzI8bmSrZKHAB/8cKpPJNP0WCoOPa0OAFTXOFXz+5Cp6zOCTCq9NKNR3LIPlNM5FdfhV47hZBwqvWai8NjzYkca5TKhnCy8ovLpQ5iBnp1KpDr5POW9f41xm76OFV+wNvkL1yJqzHL+pa8sAhxrnMsPnLbz8NmW8FAovk15Zc5ZjKNszdapxLjN80cJPFF4KlUwm+2TNWY6h5rThaViNc5nhK3qI4Se2ovBSKLxE+mXNWS6hSHQh+n+RDN7kDIPO8zXqy0qoCLFsNlsveDkUPCBrzqoi1A2cC9e4k21yMATaIIbaeshIxPiDj/peoLwRSeCjpn9M1lSZO+BsfDPtYv89fAtvUR0X7uR1rFvAr9LpdDPneD4Cc+Y2es6ph9dJYHfm7Ev4wnwSO5O9Xl5eXl5e/0Efqanb1sVbeIIAAAAASUVORK5CYII=>