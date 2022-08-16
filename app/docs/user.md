# WolframAlphaEqual

This function uses the [WolframAlpha](https://www.wolframalpha.com/) engine to compare a student's response to the correct answer. Its power can be leveraged to realise physical-units-aware evaluation, symbolic expression comparison and much more. No validation is carried out on function inputs, values are simply sent to the API in the form `response == answer`. So for example if the student provided `10 kilograms`, and the answer was defined as `0.01 tonnes`, then [`10 kilograms == 0.01 tonnes`](https://www.wolframalpha.com/input?i=10+kilograms+%3D%3D+0.01+tonnes) is sent to the WolframAlpha API.

