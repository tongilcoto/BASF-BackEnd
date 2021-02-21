Feature: As an authorised api consumer I want to successfully create a new complete person with special characters
  Scenario: As an api consumer I want to successfully create a new complete person with special characters
    Given I am an authorised api consumer
    When I create a new complete person with special characters
    Then I get a "create" OK response with matching schema
    And I can retrieve created person