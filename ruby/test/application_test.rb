require 'minitest/autorun'
require_relative '../src/application'

class ApplicationTest < Minitest::Test
  def setup
    @year           = '2100'
    @base_dir       = File.join('..', 'summary_of_news_articles')
    @template_files = File.join(base_dir, year, '**', '*.md')
  end

  ########## Regular Cases ##########

  def test_run_by_daily_unit
    ::TemplateCreator::Application.run(unit: 'd', year: year)
    check_template_files('daily')
  end

  def test_run_by_weekly_unit
    ::TemplateCreator::Application.run(unit: 'w', year: year)
    check_template_files('weekly')
  end

  def test_run_by_monthly_unit
    ::TemplateCreator::Application.run(unit: 'm', year: year)
    check_template_files('monthly')
  end

  ########## Irregular Cases ##########

  def test_initialize_with_invalid_unit
    e = assert_raises RuntimeError do
      ::TemplateCreator::Application.run(unit: 'foobar', year: year)
    end
    assert_equal(e.message, 'Provide d, w or y as a valid unit')
  end

  def test_initialize_with_non_digit_argument
    e = assert_raises ArgumentError do
      ::TemplateCreator::Application.run(year: 'foobar')
    end
    assert_equal(e.message, 'invalid value for Integer(): "foobar"')
  end

  def test_initialize_with_invalid_value_as_year
    e = assert_raises RuntimeError do
      ::TemplateCreator::Application.run(year: '20233')
    end
    assert_equal(e.message, 'Year must be 4 digits')
  end

  def test_initialize_with_older_year
    e = assert_raises RuntimeError do
      ::TemplateCreator::Application.run(year: '2022')
    end
    assert_equal(e.message, 'Provide newer than or equal to the current year')
  end

  def teardown
    destination_dir = File.join(base_dir, year)
    FileUtils.rm_rf(destination_dir) if Dir.exist?(destination_dir)
    FileUtils.rm_rf(base_dir) if no_template?
  end

  private

  attr_reader :year, :base_dir, :template_files

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
