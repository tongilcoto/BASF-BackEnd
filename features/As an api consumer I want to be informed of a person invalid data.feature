Feature: As an api consumer I want to be informed of a person invalid  data
  Scenario Outline: As an api consumer I want to be informed of a person invalid data
    Given I am an authorised api consumer
    When I create an invalid person by "<error>" error
    Then I get a "422" error

    Examples:
    | error |
    | numbers at firstName |
    | numbers at lastName |
    | symbols at firstName |
    | symbols at secondName |