import json
import os
import httpx
import asyncio


def grading_function(body: dict) -> dict:
    """
    Function used to grade a student response.
    ---
    The handler function passes only one argument to grading_function(),
    which is a dictionary of the structure of the API request body
    deserialised from JSON.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. This is also subject to
    standard response specifications.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that grading_function() is the main function used
    to output the grading response.
    """

    return query_wolframalpha(body["response"], body["answer"])


def query_wolframalpha(res, ans):
    """
    Make a call to the WolframAlpha API, checking if res and ans are equal
    ----
    This will make two calls:
        - One which only include the `res` parameter, used to return to the user how their input was interpreted
        - One which actually performs the comparison

    """
    common_params = {"appid": os.getenv("WOLFRAM_APPID"), "output": "json"}

    interp_params = {
        "podtitle": "Input*",
        "input": res,
        **common_params,
    }

    comp_params = {
        "podtitle": "Result",
        "input": f"{res} == {ans}",
        **common_params,
    }

    [interp_res, comp_res] = asyncio.run(get_queries([interp_params, comp_params]))

    # Deal with the interpretation query response
    if not "error" in interp_res:
        try:
            interp_string = (
                list(
                    filter(
                        lambda x: x.get("id") == "Input",
                        interp_res.get("queryresult", {}).get("pods", []),
                    )
                )[0]
                .get("subpods", [{}])[0]
                .get("plaintext", None)
            )
        except:
            interp_string = "error"
    else:
        interp_string = "error"

    # Deal with comparison
    if not "error" in comp_res:
        try:
            is_correct = (
                list(
                    filter(
                        lambda x: x.get("id") == "Result",
                        comp_res.get("queryresult", {}).get("pods", []),
                    )
                )[0]
                .get("subpods", [{}])[0]
                .get("plaintext", None)
            )
        except:
            is_correct = None
    else:
        is_correct = None

    return {
        "is_correct": is_correct == "True",
        "interp_string": interp_string,
        "raw_comp": comp_res,
        "raw_interp": interp_res,
    }


async def get_queries(query_list):
    """Perform multiple get requests to the ROOT_URL at once"""

    ROOT_URL = "http://api.wolframalpha.com/v2/query"

    async with httpx.AsyncClient() as client:
        tasks = (client.get(ROOT_URL, params=params) for params in query_list)
        responses = await asyncio.gather(*tasks)

    data = [safe_get_json(res) for res in responses]

    return data


def safe_get_json(response):
    """
    Safely get data from API request
    (contains code specific to the WolframAlpha API)
    """

    try:
        response.raise_for_status()
    except httpx.RequestError as e:
        return {
            "error": {
                "type": "RequestError",
                "description": repr(e),
            }
        }
    except httpx.HTTPStatusError as e:
        return {
            "error": {
                "type": "HTTPStatusError",
                "description": repr(e),
            }
        }

    # Get the data
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        return {
            "error": {
                "description": "An Error occured when parsing JSON from response"
                + repr(e),
            }
        }

    # Check that the request was a success
    if not data.get("queryresult", {}).get("success"):
        return {
            "error": {
                "description": "Query to WolframAlpha was unsucesssful",
                "response": data,
            }
        }

    return data


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("dev.env")

    print(query_wolframalpha("10kg", "10000g"))
