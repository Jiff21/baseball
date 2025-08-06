Feature: Pitcher Expected Stats Calculations
  As a fantasy baseball user
  I want to calculate expected stats for a pitcher against specific teams
  So that I can make informed lineup decisions

  Background:
    Given I am on the fantasy expected start page
    And the team stats data is loaded

  Scenario: The front end correctly adds wins points expectations to the pitchers expected scores
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: CBS
    And we have selected Starter Expected Innings: 6
    And the San Francisco Giants have 38 losses against righties (0.45238095238 loss percentage)
    Then the expected score added for pitching wins is 2.2619047619

  Scenario: The front end correctly adds losses points expectations to the pitchers expected scores
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: CBS
    And we have selected Starter Expected Innings: 6
    And the San Francisco Giants have 46 wins against righties (0.54761904761 win percentage)
    Then the expected score added for pitching losses is -1.64285714283

  Scenario: The front end correctly adds runs allowed points expectations to the pitchers expected scores
    Given we have selected Pitcher Handedness: Lefty
    And we have selected League Type: CBS
    And we have selected Starter Expected Innings: 5
    And the San Francisco Giants have scored 0.2 runs per plate appearance against lefties
    And the San Francisco Giants have averaged 1.1 plate appearances per inning against lefties
    Then the expected score added for pitching runs allowed is -12

  Scenario: The front end correctly calculates strikeout expectations
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: ESPN
    And we have selected Starter Expected Innings: 7
    And the San Francisco Giants have averaged 4.5 plate appearances per inning against righties
    And the San Francisco Giants have 0.33 strikeouts per 9 plate appearance against righties
    Then the expected score added for pitching strikeouts is 5.1975

  Scenario: The front end correctly calculates walks allowed expectations
    Given we have selected Pitcher Handedness: Lefty
    And we have selected League Type: ESPN
    And we have selected Starter Expected Innings: 8
    And the San Francisco Giants have averaged 1.1 plate appearances per inning against lefties
    And the San Francisco Giants have 0.3 walks per 9 plate appearance against lefties
    Then the expected score added for pitching walks allowed is -10.8

  Scenario: The front end correctly calculates hits allowed expectations
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: Yahoo
    And we have selected Starter Expected Innings: 6.33
    And the San Francisco Giants have averaged 1.1 plate appearances per inning against righties
    And the San Francisco Giants have 1.034 hits per 9 plate appearance per inning against righties
    Then the expected score added for pitching hits allowed is -7.199742

  Scenario: The front end correctly calculates home runs allowed expectations
    Given we have selected Pitcher Handedness: Lefty
    And we have selected League Type: CBS
    And we have selected Starter Expected Innings: 2.66
    And the San Francisco Giants have averaged 2.0 plate appearances per inning against lefties
    And the San Francisco Giants have 0.006001 home runs per 9 plate appearance against lefties
    Then the expected score added for pitching home runs allowed is -0.03192532

  Scenario: The front end correctly calculates innings pitched expectations
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: CBS
    And we have selected Starter Expected Innings: 6
    Then the expected score added for pitching innings is 18.0

  Scenario: Pitcher handedness affects calculations differently
    Given we have selected League Type: CBS
    And we have selected Starter Expected Innings: 6
    When I select Pitcher Handedness: Righty
    And I calculate expected stats for San Francisco Giants
    And I store the results for "Righty" handedness
    When I select Pitcher Handedness: Lefty
    And I calculate expected stats for San Francisco Giants
    Then the results should be different from the "Righty" results
    Then the results should not contain NaN

  Scenario: Different league types have different scoring
    Given we have selected Pitcher Handedness: Righty
    And we have selected Starter Expected Innings: 6
    When I select League Type: CBS
    And I calculate expected stats for San Francisco Giants
    And I store the results for "CBS" league
    When I select League Type: ESPN
    And I calculate expected stats for San Francisco Giants
    Then the results should be different from the "CBS" results

  Scenario: Expected innings affects all rate stats proportionally
    Given we have selected Pitcher Handedness: Righty
    And we have selected League Type: CBS
    When I select Starter Expected Innings: 6
    And I calculate expected stats for San Francisco Giants
    And I store the results for "6 innings"
    When I select Starter Expected Innings: 9
    And I calculate expected stats for San Francisco Giants
    Then the strikeouts should be 1.5 times the "6 innings" strikeouts
    And the walks should be 1.5 times the "6 innings" walks
    And the hits should be 1.5 times the "6 innings" hits
