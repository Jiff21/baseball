Feature: We can scrape standings data

  Scenario: Standings get wins works
    Given we load the test data for single team standings
      And we create a standings object
    When we get wins
    Then the current stat should be an int equal to "77"

  Scenario: Standings get losses works
    Given we load the test data for single team standings
      And we create a standings object
    When we get losses
    Then the current stat should be an int equal to "41"

  Scenario: Standings get righty standing splits works
    Given we load the test data for single team standings
      And we create a standings object
    When we get standings for a righty pitching splits
      And we set the win avg to the current stat
    Then the current stat should be a float equal to "0.6046511627906976"
    When we set the loss avg to the current stat
    Then the current stat should be a float equal to "0.3953488372093023"
    When we set the game avg to the current stat
    Then the current stat should be an int equal to "86"

  Scenario: Standings get lefty standing splits works
    Given we load the test data for single team standings
      And we create a standings object
    When we get standings for a lefty pitching splits
      And we set the win avg to the current stat
    Then the current stat should be a float equal to "0.7812500000000000"
    When we set the loss avg to the current stat
    Then the current stat should be a float equal to "0.2187500000000000"
    When we set the game avg to the current stat
    Then the current stat should be an int equal to "32"

  Scenario: Standings get home standing splits works
    Given we load the test data for single team standings
      And we create a standings object
    When we get standings for home pitching splits
      And we set the win avg to the current stat
    Then the current stat should be a float equal to "0.2586206896551724"
    When we set the loss avg to the current stat
    Then the current stat should be a float equal to "0.258620689655"
    When we set the game avg to the current stat
    Then the current stat should be an int equal to "58"

  Scenario: Standings get road standing splits works
    Given we load the test data for single team standings
      And we create a standings object
    When we get standings for road pitching splits
      And we set the win avg to the current stat
    Then the current stat should be a float equal to "0.5666666666666667"
    When we set the loss avg to the current stat
    Then the current stat should be a float equal to "0.4333333333333333"
    When we set the game avg to the current stat
    Then the current stat should be an int equal to "60"
