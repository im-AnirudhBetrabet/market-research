from pathlib import Path

from src.domain.models import (
    ResearchReport,
)


class MarkdownReportBuilder:

    def build(self, report: ResearchReport, output_file: Path) -> None:

        lines: list[str] = []

        lines.append("# Gift Nifty Research Report\n")

        lines.append("## Correlation Analysis\n")
        lines.append(f"- Gift Return → Nifty Gap: {report.nifty_correlation.coefficient:.6f}")
        lines.append(f"- Gift Return → Sensex Gap: {report.sensex_correlation.coefficient:.6f}\n")

        lines.append("## Directional Analysis\n")

        lines.append(f"- Nifty Gap Accuracy: {report.nifty_directional.accuracy:.2%}")

        lines.append(f"- Sensex Gap Accuracy: {report.sensex_directional.accuracy:.2%}\n")

        lines.append(
            "## Nifty Bucket Analysis\n"
        )

        lines.append("| Bucket | Observations | Accuracy |")

        lines.append("|----------|----------:|----------:|")

        for result in report.nifty_buckets:

            lines.append(
                f"| {result.bucket_name} "
                f"| {result.observations} "
                f"| {result.accuracy:.2%} |"
            )

        lines.append("")

        lines.append(
            "## Sensex Bucket Analysis\n"
        )

        lines.append(
            "| Bucket | Observations | Accuracy |"
        )

        lines.append(
            "|----------|----------:|----------:|"
        )

        for result in report.sensex_buckets:

            lines.append(
                f"| {result.bucket_name} "
                f"| {result.observations} "
                f"| {result.accuracy:.2%} |"
            )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )