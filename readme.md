# WolframAlphaEqual Grading Script

This simple grading script uses the WolframAlpha API to compare two strings. It performs two requests in parallel:

- One to check how the user's `response` is interpreted by WolframAlpha
- One to compare the `response` to the `answer`, by submitting the following input to the api: `res == ans`

**NOTE**: To work, this grading script requires a valid WolframAlpha AppID! This should be stored in the **`WOLFRAM_APPID`** env variable.

## Outputs

```json
{
  "is_correct": <bool or null>,
  "interp_string": <explanatory string for how `response` was interpreted>,
  "raw_comp": <raw Wolfram API response for the comparison>,
  "raw_interp": <raw Wolfram API response for the interpretation>,
}
```

_Will also return `error` detailing any issues that were encountered along the way_
