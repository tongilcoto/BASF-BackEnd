Feature: As an api consumer I want to be informed of a person missing data
  Scenario Outline: As an api consumer I want to be informed of a person missing data
    Given I am an authorised api consumer
    When I create an invalid person by missing "<field>" data
    Then I get a "422" error

    Examples:
    | field     |
    | firstName |
    | lastName  |
    | all |
