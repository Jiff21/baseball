Feature: We can scrape team hitting splits data

  Scenario Outline: Splits get runs works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get runs
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 306      |
      | Road   | 305      |
      | Lefty  | 212      |
      | Righty | 364      |


  Scenario Outline: Splits get Games works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get games
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 63       |
      | Road   | 64       |


  Scenario Outline: Splits get Hits works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get hits
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 543      |
      | Road   | 557      |
      | Lefty  | 347      |
      | Righty | 794      |


  Scenario Outline: Splits get Homeruns works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get homeruns
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 100      |
      | Road   | 97       |
      | Lefty  | 74       |
      | Righty | 95       |


  Scenario Outline: Splits get Walks works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get walks
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 249      |
      | Road   | 193      |
      | Lefty  | 107      |
      | Righty | 260      |


  Scenario Outline: Splits get Strikeouts works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get strikeouts
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 578      |
      | Road   | 649      |
      | Lefty  | 260      |
      | Righty | 1003     |


  Scenario Outline: Splits get Total Plate Appearances works for <split> Data
    Given we load the test data for single team "<split>" Splits
      And we create a SplitsScraper object
    When we get plate appearances
    Then the current stat should be an int equal to <expected>

    Examples:
      | split  | expected |
      | Home   | 2400     |
      | Road   | 2463     |
      | Lefty  | 1326     |
      | Righty | 3757     |


  Scenario Outline: When we calculate <runs> runs per <games> games
    Given we set runs to <runs> and games to <games>
      And we create a SplitsScraper object
    When we get runs per game
    Then the current stat should be a float equal to <expected>

    Examples:
      | runs   | games  | expected           |
      | 10     | 9      | 1.1111111111111112 |
      | 22     | 44     | 0.5                |
      | 400    | 80     | 5.0000000000000000 |
      | 306    | 63     | 4.8571428571428568 |
  #
  # Scenario: Splits get righty standing splits works
  #   Given we load the test data for single team Splits
  #     And we create a Splits object
  #   When we get Splits for a righty pitching splits
  #     And we set the win avg to the current stat
  #   Then the current stat should be a float equal to "0.6046511627906976"
  #   When we set the loss avg to the current stat
  #   Then the current stat should be a float equal to "0.3953488372093023"
  #   When we set the game avg to the current stat
  #   Then the current stat should be an int equal to "86"
