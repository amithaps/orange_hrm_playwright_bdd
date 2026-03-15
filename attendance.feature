Feature: Attendance Management
  As an OrangeHRM user
  I want to manage my attendance records
  So that my work hours are accurately tracked

  Background:
    Given I am on the OrangeHRM login page

  @smoke @regression @attendance
  Scenario Outline: Full CRUD lifecycle of an attendance punch-in record
    When I login with credentials
    And I navigate to the Attendance section
    And I ensure a clean state by removing existing records
    And I create a Punch-in record with note <initial_note>
    And I update the record note to <updated_note>
    Then I delete the record with note <updated_note>
    And I log out of the application
    Examples:
    | initial_note           | updated_note                      |
    | Starting Shift 101 | Starting Shift 101 - Updated |