Feature: MLB Team Statistics API
  As a fantasy baseball application
  I want to extract team statistics from MLB standings data
  So that I can calculate expected wins and losses for different scenarios

  Background:
    Given I load the json from the mock api call

  Scenario Outline: Extract wins against righties for teams
    When I am getting expected wins against Righties for "<team>"
    Then the expected wins against Righties will be <wins> for "<team>"

    Examples:
      | team | wins |
      | SF   | 61   |
      | NYY  | 73   |

  Scenario Outline: Extract losses against righties for teams
    When I am getting expected losses against Righties for "<team>"
    Then the expected losses against Righties will be <losses> for "<team>"

    Examples:
      | team | losses |
      | SF   | 57     |
      | NYY  | 45     |

  Scenario Outline: Extract wins against lefties for teams
    When I am getting expected wins against Lefties for "<team>"
    Then the expected wins against Lefties will be <wins> for "<team>"

    Examples:
      | team | wins |
      | SF   | 19   |
      | NYY  | 21   |

  Scenario Outline: Extract losses against lefties for teams
    When I am getting expected losses against Lefties for "<team>"
    Then the expected losses against Lefties will be <losses> for "<team>"

    Examples:
      | team | losses |
      | SF   | 25     |
      | NYY  | 23     |

  Scenario Outline: Extract total wins (no splits) for teams
    When I am getting expected wins with no splits for "<team>"
    Then the expected wins with no splits will be <wins> for "<team>"

    Examples:
      | team | wins |
      | SF   | 80   |
      | NYY  | 94   |

  Scenario Outline: Extract total losses (no splits) for teams
    When I am getting expected losses with no splits for "<team>"
    Then the expected losses with no splits will be <losses> for "<team>"

    Examples:
      | team | losses |
      | SF   | 82     |
      | NYY  | 68     |
