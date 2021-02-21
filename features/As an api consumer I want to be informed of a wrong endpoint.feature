Feature: As an api consumer I want to be informed of a wrong endpoint
  Scenario: As an api consumer I want to be informed of a wrong endpoint
    Given I am an authorised api consumer
    When I send a get request to a wrong endpoint
    Then I get a "404" error