from __future__ import annotations

import json
import math
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from geo_visibility.metrics import (
    SentenceAttribution,
    paired_visibility_changes,
    score_impressions,
)
from geo_visibility.pilot import parse_attributions, run_pilot, select_pilot_queries
from geo_visibility.providers import (
    CachedProvider,
    LLMRequest,
    LLMResponse,
    OllamaConfig,
    OllamaProvider,
)
from geo_visibility.schema import DatasetColumns, QueryExample, SourceDocument, load_dataset
from geo_visibility.suggestions import (
    build_suggestion_prompt,
    generate_suggestion,
    replace_query_source,
)


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0
        self.requests: list[LLMRequest] = []

    def generate(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        self.requests.append(request)
        return LLMResponse(
            text='{"sentences":[{"text":"Example answer.","citations":["d1"]}]}',
            model=request.model,
            provider="fake",
        )


class DatasetTests(unittest.TestCase):
    def test_loads_jsonl_and_normalizes_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "query_id": "q1",
                        "query": "Question?",
                        "sources": [{"id": "d1", "text": "Source text", "title": "Title"}],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            loaded = load_dataset(path)
        self.assertEqual(loaded[0].sources[0].title, "Title")
        self.assertEqual(loaded[0].sources[0].text, "Source text")

    def test_normalizes_integer_query_and_source_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "query_id": 12,
                            "query": "Question?",
                            "sources": [{"id": 34, "text": "Source text"}],
                        }
                    ]
                ),
                encoding="utf-8",
            )
            loaded = load_dataset(path)
        self.assertEqual(loaded[0].id, "12")
        self.assertEqual(loaded[0].sources[0].id, "34")

    def test_rejects_missing_query_fields_and_duplicate_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.json"
            path.write_text(
                json.dumps(
                    [
                        {"query_id": "q1", "query": "Question?", "sources": []},
                        {"query_id": "q1", "query": "Again?", "sources": []},
                    ]
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate query id"):
                load_dataset(path)


class MetricTests(unittest.TestCase):
    def test_word_count_and_position_adjusted_word_count_share_citations(self) -> None:
        scores = score_impressions(
            [
                SentenceAttribution("Alpha beta", ("d1", "d2")),
                SentenceAttribution("Gamma", ("d2",)),
            ],
            ["d1", "d2", "d3"],
        )
        self.assertAlmostEqual(scores["d1"].word_count, 1 / 3)
        self.assertAlmostEqual(scores["d2"].word_count, 2 / 3)
        self.assertEqual(scores["d3"].word_count, 0)
        expected = (1 + math.exp(-0.5)) / 3
        self.assertAlmostEqual(scores["d2"].position_adjusted_word_count, expected)

    def test_rejects_unknown_citations(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown cited source"):
            score_impressions([SentenceAttribution("Text.", ("missing",))], ["d1"])

    def test_paired_visibility_changes_requires_matching_pairs(self) -> None:
        baseline = [
            {
                "query_id": "q",
                "doc_id": "d",
                "word_count": 0.5,
                "position_adjusted_word_count": 0.4,
            }
        ]
        revised = [
            {
                "query_id": "q",
                "doc_id": "d",
                "word_count": 0.75,
                "position_adjusted_word_count": 0.6,
            }
        ]
        result = paired_visibility_changes(baseline, revised)[0]
        self.assertAlmostEqual(result["word_count_delta"], 0.25)
        self.assertAlmostEqual(result["word_count_relative_change_pct"], 50.0)
        with self.assertRaisesRegex(ValueError, "identical query/source pairs"):
            paired_visibility_changes(baseline, [])


class PilotTests(unittest.TestCase):
    def test_pilot_selection_is_seeded_and_excludes_source_free_queries(self) -> None:
        queries = [
            QueryExample("q1", "Question 1", ()),
            QueryExample("q2", "Question 2", ()),
            QueryExample("q3", "Question 3", (SourceDocument("d3", "Document 3"),)),
            QueryExample("q4", "Question 4", (SourceDocument("d4", "Document 4"),)),
            QueryExample("q5", "Question 5", (SourceDocument("d5", "Document 5"),)),
        ]
        first = select_pilot_queries(queries, 2, 7)
        second = select_pilot_queries(queries, 2, 7)
        self.assertEqual([query.id for query in first], [query.id for query in second])
        self.assertEqual(len(first), 2)
        self.assertTrue(all(query.sources for query in first))
        with self.assertRaisesRegex(ValueError, "between 1 and 50"):
            select_pilot_queries(queries, 51, 7)

    def test_response_parser_rejects_unknown_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown source IDs"):
            parse_attributions(
                '{"sentences":[{"text":"Answer.","citations":["unknown"]}]}',
                {"d1"},
            )

    def test_response_parser_accepts_one_exact_citation_string(self) -> None:
        attributions = parse_attributions(
            '{"sentences":[{"text":"Answer.","citations":"d1"}]}',
            {"d1"},
        )
        self.assertEqual(attributions[0].source_ids, ("d1",))

    def test_response_parser_diagnoses_malformed_citations_with_excerpt(self) -> None:
        response = '{"sentences":[{"text":"Answer.","citations":"d1, d2"}]}'
        with self.assertRaisesRegex(
            ValueError, r"one exact source ID string.*response excerpt:.*d1, d2"
        ):
            parse_attributions(response, {"d1", "d2"})

    def test_cached_provider_reuses_identical_request(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = FakeProvider()
            cached = CachedProvider(provider, directory)
            request = LLMRequest("Prompt", "test-model", seed=3)
            self.assertEqual(cached.generate(request), cached.generate(request))
            self.assertEqual(provider.calls, 1)

    def test_ollama_adapter_uses_configured_tag_and_records_digest(self) -> None:
        responses = [
            BytesIO(
                b'{"models":[{"name":"chosen:tag","digest":"sha256:abc"}]}'
            ),
            BytesIO(
                b'{"model":"chosen:tag","response":"answer","created_at":"now"}'
            ),
        ]
        config = OllamaConfig("http://ollama.test", "chosen:tag")
        response_schema = {
            "type": "object",
            "properties": {"sentences": {"type": "array"}},
            "required": ["sentences"],
        }
        with patch(
            "geo_visibility.providers.urllib.request.urlopen", side_effect=responses
        ) as urlopen:
            response = OllamaProvider(config).generate(
                LLMRequest(
                    "Prompt",
                    "chosen:tag",
                    temperature=0.2,
                    top_p=0.8,
                    seed=4,
                    response_format=response_schema,
                )
            )
        self.assertEqual(response.provider_version, "sha256:abc")
        self.assertEqual(urlopen.call_count, 2)
        generation_request = urlopen.call_args_list[1].args[0]
        self.assertEqual(generation_request.full_url, "http://ollama.test/api/generate")
        payload = json.loads(generation_request.data)
        self.assertEqual(payload["model"], "chosen:tag")
        self.assertEqual(payload["format"], response_schema)
        self.assertEqual(payload["options"]["top_p"], 0.8)
        self.assertEqual(payload["options"]["seed"], 4)

    def test_pilot_requests_schema_constrained_known_citations(self) -> None:
        query = QueryExample(
            "q1",
            "Question?",
            (SourceDocument("d1", "Text."), SourceDocument("d2", "More text.")),
        )
        provider = FakeProvider()
        run_pilot([query], provider, "test-model", query_limit=1, seed=1)
        schema = provider.requests[0].response_format
        self.assertIsInstance(schema, dict)
        assert isinstance(schema, dict)
        item = schema["properties"]["sentences"]["items"]
        self.assertEqual(item["required"], ["text", "citations"])
        self.assertEqual(item["properties"]["citations"]["items"]["enum"], ["d1", "d2"])

    def test_bounded_pipeline_emits_visibility_records(self) -> None:
        queries = [
            QueryExample(
                "q1",
                "Question?",
                (SourceDocument("d1", "Text."),),
            )
        ]
        records, selected, answers = run_pilot(
            queries, FakeProvider(), model="test-model", query_limit=1, seed=3
        )
        self.assertEqual(selected, ["q1"])
        self.assertEqual(len(records), 1)
        self.assertTrue(records[0]["cited"])
        self.assertEqual(records[0]["rank"], 1)
        self.assertIn('"sentences"', answers[0]["answer"])
        self.assertIsNone(records[0]["doc_url"])

    def test_missing_citation_fields_are_explicitly_uncited(self) -> None:
        class MissingCitationProvider:
            def generate(self, request: LLMRequest) -> LLMResponse:
                return LLMResponse(
                    text='{"sentences":[{"text":"Unattributed claim."}]}',
                    model=request.model,
                    provider="fake",
                )

        query = QueryExample(
            "q1",
            "Question?",
            (SourceDocument("d1", "Text."), SourceDocument("d2", "More text.")),
        )
        records, _, answers = run_pilot(
            [query], MissingCitationProvider(), "test-model", query_limit=1, seed=1
        )
        self.assertEqual(answers[0]["citation_status"], "missing_fields_treated_as_uncited")
        self.assertEqual(answers[0]["cited_source_ids"], [])
        self.assertIn("sentence(s) 1", answers[0]["citation_warnings"][0])
        self.assertTrue(all(not record["cited"] for record in records))
        self.assertTrue(all(record["word_count"] == 0 for record in records))
        self.assertTrue(
            all(
                record["citation_status"] == "missing_fields_treated_as_uncited"
                for record in records
            )
        )

    def test_geo_bench_rows_can_be_bounded_and_get_generated_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.jsonl"
            rows = [
                {
                    "query": f"Question {index}?",
                    "sources": [
                        {
                            "cleaned_text": f"Text {index}",
                            "url": f"https://example.test/{index}",
                        }
                    ],
                }
                for index in range(3)
            ]
            path.write_text(
                "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8"
            )
            loaded = load_dataset(
                path,
                columns=DatasetColumns(
                    query_id=None,
                    source_id=None,
                    source_text="cleaned_text",
                    source_title=None,
                ),
                max_rows=1,
            )
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].id, "query-1")
        self.assertEqual(loaded[0].sources[0].id, "source-1")
        self.assertEqual(loaded[0].sources[0].url, "https://example.test/0")

    def test_prompt_truncation_is_recorded_and_applied(self) -> None:
        query = QueryExample(
            "q1", "Question?", (SourceDocument("d1", "x" * 10),)
        )
        records, _, _ = run_pilot(
            [query],
            FakeProvider(),
            model="test-model",
            query_limit=1,
            seed=3,
            source_char_limit=4,
        )
        self.assertEqual(records[0]["source_chars_provided"], 4)
        self.assertTrue(records[0]["source_truncated"])

    def test_suggestion_prompt_does_not_claim_a_visibility_prediction(self) -> None:
        prompt = build_suggestion_prompt("Query?", "Original text.")
        self.assertIn("hypothesis, not a prediction", prompt)
        self.assertIn("Original text.", prompt)

    def test_suggestion_generation_and_paired_source_replacement(self) -> None:
        class SuggestionProvider:
            def generate(self, request: LLMRequest) -> LLMResponse:
                return LLMResponse(
                    text='{"rationale":"Clearer phrasing","revised_document":"Revised text."}',
                    model=request.model,
                    provider="fake",
                )

        query = QueryExample("q1", "Question?", (SourceDocument("d1", "Original text."),))
        suggestion = generate_suggestion(
            SuggestionProvider(), "test-model", query.query, query.sources[0].text
        )
        revised_query = replace_query_source(query, "d1", suggestion.revised_document)
        self.assertEqual(revised_query.sources[0].text, "Revised text.")
        self.assertEqual(revised_query.query, query.query)


if __name__ == "__main__":
    unittest.main()
