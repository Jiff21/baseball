Feature: The stat retrieval is working properly

  Scenario: The team standings data is where we expect it
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
    Then TEAM_STANDING_DICT short code should be mia

  Scenario: Wins are what we expect in standings data
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And we get wins for team 1 from standings
    Then wins should be "52"

  Scenario: Losses are what we expect in standings data
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And we get losses for team 1 from standings
    Then losses should be "58"

  Scenario: Games are what we expect in standings data
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And we get games for team 1 from standings
    Then games should be "110"

  Scenario: Verse Righties standings data
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And get verse righty team standings
    Then win percentage verse righties should be "0.488636363636"
      And loss percentage verse righties should be "0.511364"
      And team game verse righties should be "88"
