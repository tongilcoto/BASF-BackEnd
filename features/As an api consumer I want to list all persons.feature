Feature: As an authorised api consumer I want to list all persons
  Scenario: As an api consumer I want to list all persons
    Given I am an authorised api consumer
    When I ask for all persons
    Then I get a "list" OK response with matching schema
