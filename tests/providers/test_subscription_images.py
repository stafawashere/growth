"""The subscription adapter's image path, against the fake claude CLI: a request carrying images
goes in as one stream-json user message with the image blocks before the text, the answer is read
from the final result event, and every flag that keeps tools, settings and MCP servers off is the
same as on the text path. A live run of the same path is tools/subscription_image_smoke.py."""
import base64
import json

from app.providers.base import ImageInput, Message, ProviderRequest
from app.providers.subscription import DISALLOWED_TOOLS
from tests.providers.test_subscription import cli, ledger, option_value, provider_for  # noqa: F401

PAGE_BYTES = b"\x89PNG not really a page"


def image_request():
   return ProviderRequest(
      role="transcriber",
      model="claude-sonnet-5",
      system="You transcribe handwritten mathematics.",
      messages=(Message(role="user", content="Question Q1, parts (a) and (b)."),),
      max_output_tokens=3000,
      output_schema={"type": "object"},
      images=(ImageInput(media_type="image/png", data=PAGE_BYTES, width=800, height=1000),),
   )


def test_an_image_rides_in_a_stream_json_user_message_with_every_tool_still_off(cli, ledger):
   cli.mode("stream_json")

   result = provider_for(cli, ledger).generate(image_request())
   record = cli.record()
   argv = record["argv"]
   message = json.loads(record["stdin"])
   blocks = message["message"]["content"]

   assert option_value(argv, "--input-format") == "stream-json"
   assert option_value(argv, "--output-format") == "stream-json"
   assert "--verbose" in argv
   assert option_value(argv, "--tools") == ""
   assert option_value(argv, "--disallowedTools") == ",".join(DISALLOWED_TOOLS)
   assert option_value(argv, "--setting-sources") == ""
   assert "--strict-mcp-config" in argv
   assert message["type"] == "user"
   assert [block["type"] for block in blocks] == ["image", "text"]
   assert base64.b64decode(blocks[0]["source"]["data"]) == PAGE_BYTES
   assert blocks[1]["text"] == "Question Q1, parts (a) and (b)."
   assert json.loads(result.text) == {"parts": [], "unreadable": []}


def test_a_request_without_images_keeps_the_plain_text_path(cli, ledger):
   cli.mode("success")
   request = image_request()
   text_only = ProviderRequest(**{**request.__dict__, "images": ()})

   provider_for(cli, ledger).generate(text_only)
   record = cli.record()

   assert option_value(record["argv"], "--output-format") == "json"
   assert "--input-format" not in record["argv"]
   assert record["stdin"] == "Question Q1, parts (a) and (b)."
