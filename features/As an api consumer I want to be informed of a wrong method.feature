Feature: As an api consumer I want to be informed of a wrong method
  Scenario Outline: As an api consumer I want to be informed of a wrong method
    Given I am an authorised api consumer
    When I send a "<method>" request to "<endpoint>" endpoint
    Then I get a "405" error

    Examples:
    | method | endpoint |
    | put    | list     |
    | get    | create   |
    | put    | details  |
    | post   | create   |