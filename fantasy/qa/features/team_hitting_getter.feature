Feature: The stat retrieval is working properly

  Scenario: The team hitting data is where we think it should be
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
    Then we expect miami to be the third team in TEAM_HITTING_STATS

  Scenario: The short name should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get the short name for team 3
    Then we expect short name to be "Miami"

  Scenario: At bats should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get at bats for team 3
    Then we expect at bats to be "3785"

  Scenario: RBIs should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get RBIs for team 3
    Then we expect RBIs to be "494"

  Scenario: Walks should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get walks for team 3
    Then we expect walks to be "313"

  Scenario: Runs should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get runs for team 3
    Then we expect runs to be "516"

  Scenario: Strikeouts should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get strikeouts for team 3
    Then we expect strikeouts to be "860"

  Scenario: Runs should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get runs for team 3
    Then we expect runs to be "516"

  Scenario: Total Games should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get total games for team 3
    Then we expect total games to be "110"

  Scenario: Hits should be what we expect for all hitting
    Given we have stubbed hitting data
    When we get the relevant part of the hitting json
      And we get hits for team 3
    Then we expect hits to be "1001"
