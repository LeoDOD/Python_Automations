Feature: This is just an example of the Web Browsing capabilities of the Autoation.

  @example-1
  Scenario: Verify we can perform a google search
    Given I go to www.Google.com
    Then I type BoNY Mellon in the field with Title-Search
    And I click the Input with Name=btnK
    And i wait