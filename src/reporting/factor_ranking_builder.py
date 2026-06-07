from src.domain.models import FactorSummary, FactorRanking


class FactorRankingBuilder:

    def build(self, factors: list[FactorSummary]) -> list[FactorRanking]:

        rankings: list[FactorRanking] = []

        for factor in factors:
            rankings.append(
                FactorRanking(
                    factor_name=factor.factor_name,
                    nifty_correlation=factor.nifty_correlation.coefficient,
                    sensex_correlation=factor.sensex_correlation.coefficient,
                    nifty_accuracy=factor.nifty_directional.accuracy,
                    sensex_accuracy=factor.sensex_directional.accuracy,
                )
            )

        return rankings