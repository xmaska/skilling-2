@CBD @smoke
Feature: Smoke test of the Computer Database

  Scenario Outline: Create Search and Delete Computer Model - Positive story
    Given I open the Computer Database Tool
    When I click on Add new Computer
    And I fill Name as "<computer_name>", Introduced as "<introduced>", Discontinued as "<discontinued>" and company as "<company>"
    And I make a screenshot of "form filled"
    Then I click on create this computer which is valid: "<valid_entry>"
    And I make a screenshot of "computer created"
    When I filter for "<computer_name>"
    And I make a screenshot of "computer filtered"
    Then I delete the selected computer
    And I make a screenshot of "computer deleted"
    Examples:
      | computer_name  | introduced | discontinued | company | valid_entry |
      | Test Computer  | 2000-01-12 | 2001-01-12   | Nokia   | True        |
      | Test Computer2 | 2001-01-12 | 2010-01-12   | IBM     | True        |

  Scenario Outline: Create Search and Delete Computer Model - Negative story
    Given I open the Computer Database Tool
    When I click on Add new Computer
    And I fill Name as "<computer_name>", Introduced as "<introduced>", Discontinued as "<discontinued>" and company as "<company>"
    And I make a screenshot of "form filled"
    Then I click on create this computer which is valid: "<valid_entry>"
    And I make a screenshot of "alert visible"
    Examples:
      | computer_name | introduced | discontinued | company | valid_entry |
      | Test Computer | sdgsdg     | dfhdfh       | IBM     | False       |
      | Test Computer | 2000-01-12 | 1001-01-12   | Nokia   | False       |