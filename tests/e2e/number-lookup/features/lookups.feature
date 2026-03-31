Feature: [Number Lookup]
  E2E test for Number Lookup API

  Background:
    Given the Number Lookup service is available

  Scenario: [Lookup] lookup for a phone number with no additional features
    When I send a request to lookup for a phone number with no additional features
    Then the response contains the details of the phone number lookup with line details only

  Scenario: [Lookup] lookup for a phone number with all the features
    When I send a request to lookup for a phone number with all the features
    Then the response contains the details of the phone number lookup with all the features
