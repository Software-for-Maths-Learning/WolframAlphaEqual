# WolframAlphaEqual Grading Script

This simple grading script uses the WolframAlpha API to compare two strings. It performs two requests in parallel:

1. One to check how the user's `response` is interpreted by WolframAlpha
2. One to compare the `response` to the `answer`, by submitting the following input to the api: `res == ans`

**NOTE**: To work, this grading script requires a valid WolframAlpha AppID! This should be stored in the **`WOLFRAM_APPID`** env variable.

## Outputs

```json
{
  "is_correct": "<bool or null>",
  "interp_string": "<string>",
  "raw_comp": "<dict>",
  "raw_interp": "<dict>"
}
```

## `is_correct`

Extracted from the second WolframAlpha call. More specifically, the `"id": "Result"` pod's first `subpod.plaintext` value.

## `interp_string`

Human friendly string which indicates how WolframAlpha interpreted the user response. Extracted from the first WolframAlpha call. Corresponds also to the value of `plaintext` from the first `subpod` in the `"id" : "Input"` pod.

For example, if the user entered `10 kg`, this might look like `10 kg (kilograms)`

## `raw_comp`

**For debugging**, passes the raw json result obtained from the second WolframAlpha call (comparison).

## `raw_interp`

**For debugging**, passes the raw json result obtained from the first WolframAlpha call (interpretation).

_Will also return `error` detailing any issues that were encountered along the way_
