from pathlib           import Path
from src.domain.models import ResearchReport

class MarkdownReportBuilder:

    def build(self, report: ResearchReport, output_file: Path) -> None:

        lines: list[str] = []

        self._build_header(report, lines)

        self._build_factor_rankings(report,lines)

        for factor in report.factors:
            self._build_factor_section(factor, lines)

        output_file.parent.mkdir(parents=True,exist_ok=True)

        output_file.write_text("\n".join(lines), encoding="utf-8")

    def _build_header(self, report: ResearchReport, lines: list[str]) -> None:

        lines.append(
            "# Market Factor Research Report"
        )

        lines.append("")

        lines.append(
            "## Dataset Summary"
        )

        lines.append("")

        lines.append(
            f"Analysis Timestamp: "
            f"{report.analysis_timestamp}"
        )

        lines.append(
            f"Observation Count: "
            f"{report.observation_count}"
        )

        lines.append(
            f"Date Range: "
            f"{report.start_date}"
            f" -> "
            f"{report.end_date}"
        )

        lines.append("")

        factor_rankings = sorted(
            report.factors,
            key=lambda factor: abs(
                factor.nifty_correlation.coefficient
            ),
            reverse=True,
        )

        strongest = factor_rankings[0]

        lines.append(
            "## Executive Summary"
        )

        lines.append("")

        lines.append(
            f"Strongest factor: "
            f"{strongest.factor_name}"
        )

        lines.append(
            f"Nifty correlation: "
            f"{strongest.nifty_correlation.coefficient:.3f}"
        )

        lines.append("")

    def _build_factor_rankings(
        self,
        report: ResearchReport,
        lines: list[str],
    ) -> None:

        rankings = sorted(
            report.factors,
            key=lambda factor: abs(
                factor.nifty_correlation.coefficient
            ),
            reverse=True,
        )

        lines.append(
            "## Factor Ranking (Nifty Gap)"
        )

        lines.append("")

        lines.append(
            "| Rank | Factor | Correlation | Accuracy |"
        )

        lines.append(
            "|------|--------|------------:|----------:|"
        )

        for rank, factor in enumerate(
            rankings,
            start=1,
        ):

            lines.append(
                f"| {rank} "
                f"| {factor.factor_name} "
                f"| {factor.nifty_correlation.coefficient:.3f} "
                f"| {factor.nifty_directional.accuracy:.2%} |"
            )

        lines.append("")

    def _build_factor_section(
        self,
        factor,
        lines: list[str],
    ) -> None:

        lines.append(
            f"# {factor.factor_name}"
        )

        lines.append("")

        lines.append(
            "## Correlation Analysis"
        )

        lines.append("")

        lines.append(
            f"Nifty Gap: "
            f"{factor.nifty_correlation.coefficient:.3f}"
        )

        lines.append(
            f"Sensex Gap: "
            f"{factor.sensex_correlation.coefficient:.3f}"
        )

        lines.append("")

        lines.append(
            "## Directional Analysis"
        )

        lines.append("")

        lines.append(
            f"Nifty Accuracy: "
            f"{factor.nifty_directional.accuracy:.2%}"
        )

        lines.append(
            f"Sensex Accuracy: "
            f"{factor.sensex_directional.accuracy:.2%}"
        )

        lines.append("")

        lines.append(
            "## Bucket Analysis (Nifty)"
        )

        lines.append("")

        lines.append(
            "| Bucket | Observations | Accuracy |"
        )

        lines.append(
            "|--------|-------------:|----------:|"
        )

        for bucket in factor.nifty_buckets:

            lines.append(
                f"| {bucket.bucket_name} "
                f"| {bucket.observations} "
                f"| {bucket.accuracy:.2%} |"
            )

        lines.append("")

        lines.append(
            "## Bucket Analysis (Sensex)"
        )

        lines.append("")

        lines.append(
            "| Bucket | Observations | Accuracy |"
        )

        lines.append(
            "|--------|-------------:|----------:|"
        )

        for bucket in factor.sensex_buckets:
            lines.append(
                f"| {bucket.bucket_name} "
                f"| {bucket.observations} "
                f"| {bucket.accuracy:.2%} |"
            )

        lines.append("")

        lines.append(
            "## Lag Analysis (Nifty)"
        )

        lines.append("")

        lines.append(
            "| Feature | Correlation |"
        )

        lines.append(
            "|---------|------------:|"
        )

        for lag in factor.nifty_lags:

            lines.append(
                f"| {lag.feature} "
                f"| {lag.coefficient:.3f} |"
            )

        lines.append("")

        lines.append(
            "## Lag Analysis (Sensex)"
        )

        lines.append("")

        lines.append(
            "| Feature | Correlation |"
        )

        lines.append(
            "|---------|------------:|"
        )

        for lag in factor.sensex_lags:
            lines.append(
                f"| {lag.feature} "
                f"| {lag.coefficient:.3f} |"
            )

        lines.append("")