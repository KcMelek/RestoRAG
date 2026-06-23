# cli.py — thin CLI entry point; delegates to app.services

import argparse
import json
import sys

from config import settings
from app.services.document_service import convert_to_markdown, list_supported_formats


def cmd_convert(args):
    result = convert_to_markdown(args.input, force_ocr=args.ocr)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result["markdown"])
        print(f"Wrote {result['char_count']} chars to {args.output}")
    else:
        print(result["markdown"])


def cmd_ingest(args):
    from app.services.indexing_service import ingest_directory

    report = ingest_directory(args.path, recreate=not args.no_recreate)
    print(f"Ingested {report['total_chunks']} chunks from {len(report['files'])} file(s):")
    for item in report["files"]:
        print(
            f"  - {item['filename']}: {item['chunks_indexed']} chunks "
            f"({item['char_count']:,} chars)"
        )


def cmd_sources(args):
    from app.services.indexing_service import get_index_stats

    stats = get_index_stats()
    print(f"Vector store: {stats['db_path']}")
    print(f"Total chunks: {stats['total_chunks']}")
    if not stats["sources"]:
        print("No indexed files yet. Run: python cli.py ingest")
        return
    print("Indexed files:")
    for src in stats["sources"]:
        print(f"  - {src['filename']}: {src['chunks']} chunks")


def cmd_query(args):
    from app.services.rag_service import query_knowledge_base

    response = query_knowledge_base(args.question)
    print(json.dumps(response, indent=2, ensure_ascii=False))


def cmd_eval(args):
    from app.tests.evaluation import run_evaluation

    report = run_evaluation()
    for r in report["results"]:
        print("=" * 80)
        print(f"[{r['id']}] {'PASS' if r['passed'] else 'FAIL'}")
        print(f"QUERY: {r['query']}")
        print(f"RESPONSE: {r['answer']}")
        print(f"ACTION: {r['action']} (expected: {r['expected_action']})")
        print(f"SCORE: {r['score']:.0%} | action_ok: {r['action_ok']}")
        missing = [
            kw
            for kw in r["expected_keywords"]
            if kw.lower() not in (r["answer"] or "").lower()
        ]
        if missing:
            print(f"MISSING KEYWORDS: {missing}")
    print("=" * 80)
    print(f"\nAccuracy: {report['passed']}/{report['total']} ({report['accuracy']:.0%})")


def cmd_formats(args):
    print("Supported formats:", ", ".join(list_supported_formats()))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="dialagent",
        description="DialAgent — document conversion, ingestion, and RAG queries",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_convert = sub.add_parser("convert", help="Convert a file to markdown")
    p_convert.add_argument("input", help="Path to PDF, Word, image, or markdown file")
    p_convert.add_argument("-o", "--output", help="Write markdown to file instead of stdout")
    p_convert.add_argument("--ocr", action="store_true", default=None, help="Force OCR on")
    p_convert.add_argument(
        "--no-ocr",
        action="store_false",
        dest="ocr",
        help="Force OCR off (PDF only; images always use OCR)",
    )
    p_convert.set_defaults(func=cmd_convert)

    p_ingest = sub.add_parser("ingest", help="Index documents into the vector store")
    p_ingest.add_argument(
        "--path",
        default=settings.DEFAULT_INGEST_PATH,
        help=f"Directory containing documents (default: {settings.DEFAULT_INGEST_PATH})",
    )
    p_ingest.add_argument(
        "--no-recreate",
        action="store_true",
        help="Append to existing index instead of rebuilding",
    )
    p_ingest.set_defaults(func=cmd_ingest)

    p_sources = sub.add_parser("sources", help="List files indexed in the vector store")
    p_sources.set_defaults(func=cmd_sources)

    p_query = sub.add_parser("query", help="Ask a question against the indexed knowledge base")
    p_query.add_argument("question", help="Question to ask")
    p_query.set_defaults(func=cmd_query)

    p_eval = sub.add_parser("eval", help="Run the RAG evaluation suite")
    p_eval.set_defaults(func=cmd_eval)

    p_formats = sub.add_parser("formats", help="List supported input formats")
    p_formats.set_defaults(func=cmd_formats)

    args = parser.parse_args()
    try:
        args.func(args)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
