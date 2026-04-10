def get_scenario_by_id(scenarios: list[dict], scenario_id: str) -> dict | None:
    for scenario in scenarios:
        if scenario["id"] == scenario_id:
            return scenario
    return None


def get_scenarios_by_category(scenarios: list[dict], category: str) -> list[dict]:
    return [scenario for scenario in scenarios if scenario["category"] == category]


def summarize_scenario(scenario: dict) -> dict:
    return {
        "title": scenario["title"],
        "category": scenario["category"],
        "environment": scenario["environment"],
        "cloud": scenario["cloud"],
        "severity": scenario["severity"],
    }
