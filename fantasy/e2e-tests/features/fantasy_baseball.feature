Feature: Fantasy Baseball Application
  As a fantasy baseball user
  I want to calculate expected points and manage custom scoring settings
  So that I can make informed decisions about my fantasy team

  Background:
    Given I navigate to the Fantasy Baseball application
    And the application loads successfully

  @smoke @typescript
  Scenario: Application loads without TypeScript compilation errors
    Given I am on the Fantasy Baseball page
    Then the application should load without TypeScript errors
    And the browser console should not contain any TypeScript errors
    And the page should render all main components
    And I should see the league type dropdown
    And I should see the handedness dropdown
    And I should see the "Calculate Expected Points" button

  @smoke
  Scenario: Calculate Expected Points without errors
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    And I click the "Calculate Expected Points" button
    Then I should not see any error messages
    And I should see the team matchup analysis results
    And the results should contain expected fantasy points for all teams
    And the scoring settings accordion should be collapsed
    And the page should scroll to the team matchup analysis section

  @scoring-settings
  Scenario: Scoring settings display with decimal points
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    Then I should see the "Scoring Settings" section
    And all scoring values should display with one decimal point
    And I should see the "Batting" subsection with all required fields
    And I should see the "Pitching" subsection with all required fields

  @custom-league
  Scenario: Save and load custom league settings
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    And I modify the batting "Singles" value to "1.5"
    And I modify the pitching "Wins" value to "3.0"
    And I enter "MBL" as the league name
    And I click the "Save" button
    Then I should see a success message
    When I select "ESPN" from the league type dropdown
    And I select "MBL" from the league type dropdown
    Then the batting "Singles" value should be "1.5"
    And the pitching "Wins" value should be "3.0"

  @validation
  Scenario: Verify all required batting fields are present
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    Then I should see the following batting fields:
      | Field Name          |
      | Singles             |
      | Doubles             |
      | Triples             |
      | Home Runs           |
      | Walks               |
      | Intentional Walks   |
      | Hit By Pitch        |
      | Runs                |
      | Runs Batted In      |
      | Stolen Base         |
      | Caught Stealing     |
      | Strike Outs         |

  @validation
  Scenario: Verify all required pitching fields are present
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    Then I should see the following pitching fields:
      | Field Name                  |
      | Walks Issued                |
      | IBB   |
      | Earned Runs                 |
      | Hits Allowed                |
      | Hit Batters                 |
      | HRA           |
      | Innings (3 outs)            |
      | Strikeouts                  |
      | Wins                        |
      | Losses                      |
      | Saves                       |
      | Blown Saves                 |
      | Quality Starts              |
      | Total Bases                 |

  @handedness
  Scenario: Left and right handedness produce different results
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    And I select "Righty" from the handedness dropdown
    And I click the "Calculate Expected Points" button
    Then I should see the team matchup analysis results
    And I store the results for "Righty" handedness
    When I select "Lefty" from the handedness dropdown
    And I click the "Calculate Expected Points" button
    Then I should see the team matchup analysis results
    And the results should be different from the "Righty" results
    And at least 50% of teams should have different fantasy point values

  @accordion
  Scenario: Scoring settings accordion functionality
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    Then the scoring settings accordion should be open
    When I click the scoring settings accordion header
    Then the scoring settings accordion should be collapsed
    When I click the scoring settings accordion header again
    Then the scoring settings accordion should be open

  @inline-fields
  Scenario: Scoring settings display inline with titles
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    And the scoring settings accordion is open
    Then each batting field should be displayed inline with its title
    And each pitching field should be displayed inline with its title
    And all input fields should allow up to 3 digits
    And the innings field should allow thirds (e.g., 6.1, 6.2)

  @team-rows
  Scenario: Team results display in row format
    Given I am on the Fantasy Baseball page
    When I select "Custom" from the league type dropdown
    And I click the "Calculate Expected Points" button
    Then I should see the team matchup analysis results
    And each team should be displayed in its own row
    And each team row should show fantasy points and key stats
    And team rows should be sortable by points and team name

  @error-handling
  Scenario: Handle API errors gracefully
    Given I am on the Fantasy Baseball page
    And the backend API is unavailable
    When I select "Custom" from the league type dropdown
    And I click the "Calculate Expected Points" button
    Then I should see an appropriate error message
    And the application should remain functional
