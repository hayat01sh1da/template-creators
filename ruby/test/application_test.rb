require 'minitest/autorun'
require_relative '../src/application'

class ApplicationTest < Minitest::Test
  def setup
    @username       = 'hayat01sh1da'
    @year           = '2100'
    @base_dir       = File.join('..', '..', 'working-report', username)
    @template_files = File.join(base_dir, year, '**', '*.md')
  end

  def teardown
    destination_dir = File.join(base_dir, year)
    FileUtils.rm_rf(destination_dir) if Dir.exist?(destination_dir)
    FileUtils.rm_rf(base_dir) if no_template?
  end

  private

  attr_reader :username, :year, :base_dir, :template_files

  def check_template_files(unit)
    filepath           = File.join('..', 'testing_file_lists', "#{unit}_templates.txt")
    expected_templates = File.open(filepath).read.split("\n")
    actual_templates   = Dir[template_files]
    assert_equal(expected_templates, actual_templates)
  end

  def no_template?
    Dir[template_files].empty?
  end
end

class RegularCaseTest < ApplicationTest
  def test_run_by_daily_unit
    Application.run(username:, unit: 'd', year: year)
    check_template_files('daily')
  end

  def test_run_by_weekly_unit
    Application.run(username:, unit: 'w', year: year)
    check_template_files('weekly')
  end

  def test_run_by_monthly_unit
    Application.run(username:, unit: 'm', year: year)
    check_template_files('monthly')
  end
end

class IrregularCaseTest < ApplicationTest
  def test_initialize_with_invalid_username
    error = assert_raises Application::ValueError do
      Application.run(username: 'InvalidUsername', unit: 'm', year: year)
    end
    assert_equal('InvalidUsername is NOT a permitted username.', error.message)
  end

  def test_initialize_with_invalid_unit
    error = assert_raises Application::ValueError do
      Application.run(username:, unit: 'foobar', year: year)
    end
    assert_equal('Provide d, w or m as a valid unit.', error.message)
  end

  def test_initialize_with_non_digit_argument
    error = assert_raises ArgumentError do
      Application.run(username:, year: 'foobar')
    end
    assert_equal('invalid value for Integer(): "foobar"', error.message)
  end

  def test_initialize_with_invalid_value_as_year
    error = assert_raises Application::DigitLengthError do
      Application.run(username:, year: '20233')
    end
    assert_equal('Year must be 4 digits.', error.message)
  end

  def test_initialize_with_older_year
    error = assert_raises Application::ValueError do
      Application.run(username:, year: '2022')
    end
    assert_equal('Provide newer than or equal to the current year.', error.message)
  end
end
