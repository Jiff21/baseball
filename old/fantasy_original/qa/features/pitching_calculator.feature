Feature: Single game calculation should work properly

  Scenario: The Pitcher gets a no decision
    Given Scoring Settings are set to default
    And the pitcher goes "8" innings
    And the pitcher allows "3" earned runs
    And the pitcher walks "5" batter
    And the pitcher allows "4" hits
    And the pitcher gives up "1" homeruns
    And the pitcher strikes out "8" batters
    When we calculate game
    Then we expect his score to be "17"

  Scenario: The Pitcher gets a win but only goes 6 innings
    Given Scoring Settings are set to default
    And the pitcher goes "6.0" innings
    And the pitcher allows "3" earned runs
    And the pitcher walks "5" batter
    And the pitcher allows "4" hits
    And the pitcher gives up "1" homeruns
    And the pitcher strikes out "8" batters
    And the pitcher gets a win
    When we calculate game
    Then we expect his score to be "16"

  Scenario: The Pitcher takes a loss and goes 7.2 innings
    Given Scoring Settings are set to default
    And the pitcher goes "7.66" innings
    And the pitcher allows "3" earned runs
    And the pitcher walks "2" batter
    And the pitcher allows "7" hits
    And the pitcher gives up "2" homeruns
    And the pitcher strikes out "8" batters
    And the pitcher takes a loss
    When we calculate game
    Then we expect his score to be "10"

  Scenario: The Pitcher takes gets a quality start
    Given Scoring Settings are set to default
    And the pitcher goes "7.67" innings
    And the pitcher allows "3" earned runs
    And the pitcher walks "5" batter
    And the pitcher allows "4" hits
    And the pitcher gives up "1" homeruns
    And the pitcher strikes out "8" batters
    And the pitcher gets a quality start
    When we calculate game
    Then we expect his score to be "16"

  Scenario: The Pitcher get 1.1 inning save
    Given Scoring Settings are set to default
    And the pitcher goes "1.33" innings
    And the pitcher allows "0" earned runs
    And the pitcher walks "1" batter
    And the pitcher allows "1" hits
    And the pitcher gives up "0" homeruns
    And the pitcher strikes out "2" batters
    And the pitcher gets a save
    When we calculate game
    Then we expect his score to be "9"

  Scenario: The Pitcher pitches a perfect game
    Given Scoring Settings are set to default
    And the pitcher goes "9" innings
    And the pitcher allows "0" earned runs
    And the pitcher walks "0" batter
    And the pitcher allows "0" hits
    And the pitcher gives up "0" homeruns
    And the pitcher strikes out "10" batters
    And the pitcher gets a win
    When we calculate game
    Then we expect his score to be "42"
