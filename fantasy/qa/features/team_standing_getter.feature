Feature: The standings retrieval is working properly

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

  Scenario: Verse Lefties standings data
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And get verse lefties team standings
    Then win percentage verse lefties should be "0.409091"
      And loss percentage verse lefties should be "0.590909"
      And team game verse lefties should be "22"

  Scenario: Get all standings data should work correctly
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
      And get all win/loss data from standings
    Then general win average should be "0.472700"
      And general loss average should be "0.527300"
      And team games at home should be "55"
      And road win average should be "0.454545"
      And road loss average should be "0.545455"
