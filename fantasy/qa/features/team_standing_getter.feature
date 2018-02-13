Feature: The stat retrieval is working properly

  Scenario: The team standings data is where we expect it
    Given we have stubbed team standings data
    When we get the relevant part of the standings json
    Then TEAM_STANDING_DICT short code should be mia
