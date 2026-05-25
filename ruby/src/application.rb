# frozen_string_literal: true
# rbs_inline: enabled

require 'date'

class Application
  class ValueError < StandardError; end
  class DigitLengthError < StandardError; end

  USERNAMES           = ['hayat01sh1da'].freeze
  BODY_TEMPLATE       = File.read(File.join(__dir__, 'body_template.md')).freeze
  FULL_UNITS          = { 'd' => 'daily', 'w' => 'weekly', 'm' => 'monthly' }.freeze
  MONTHS_WITH_30_DAYS = %w[April June September November].freeze

  # @rbs username: String
  # @rbs unit: String
  # @rbs year: String
  # @rbs return: void
  def self.run(username: 'hayat01sh1da', unit: 'd', year: Time.now.year.to_s)
    instance = new(username:, unit:, year:)
    instance.validate_username!
    instance.validate_unit!
    instance.validate_year!
    instance.run
  end

  # @rbs username: String
  # @rbs unit: String
  # @rbs year: String
  # @rbs return: void
  def initialize(username: 'hayat01sh1da', unit: 'd', year: Time.now.year.to_s)
    @username = username
    @unit     = unit
    @year     = year
  end

  # @rbs return: void
  def validate_username!
    raise ValueError, "#{username} is NOT a permitted username." unless USERNAMES.include?(username)
  end

  # @rbs return: String
  def validate_unit!
    case unit
    when 'd', 'w', 'm'
      unit
    else
      raise ValueError, 'Provide d, w or m as a valid unit.'
    end
  end

  # @rbs return: String
  def validate_year!
    Integer(year)
    if year.length > 4
      raise DigitLengthError, 'Year must be 4 digits.'
    elsif year.to_i < Time.now.year
      raise ValueError, 'Provide newer than or equal to the current year.'
    else
      year
    end
  end

  # @rbs return: void
  def run
    Date::MONTHNAMES.compact.each.with_index(1) do |month, i|
      index     = format('%02d', i)
      directory = File.join('..', '..', 'working-report', username, year, "#{index}_#{month}")
      process_month(month, i, index, directory)
    end
  end

  private

  attr_reader :username, :unit, :year

  # @rbs month: String
  # @rbs month_index: Integer
  # @rbs index: String
  # @rbs directory: String
  # @rbs return: void
  def process_month(month, month_index, index, directory)
    case unit
    when 'd', 'w' then process_days(month, month_index, index, directory)
    when 'm'      then export_template(directory:, index:, month:)
    end
  end

  # @rbs month: String
  # @rbs month_index: Integer
  # @rbs index: String
  # @rbs directory: String
  # @rbs return: void
  def process_days(month, month_index, index, directory)
    create_templates(month) do |d|
      next if skip_day?(month_index, d)

      day = format('%02d', d)
      export_template(directory:, index:, day:, month:)
    end
  end

  # @rbs month_index: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def skip_day?(month_index, day)
    unit == 'd' ? weekend?(month_index, day) : !monday?(month_index, day)
  end

  # @rbs return: String
  def full_unit
    FULL_UNITS.fetch(unit, '')
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def monday?(month, day)
    Time.new(year, month, day).monday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def saturday?(month, day)
    Time.new(year, month, day).saturday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def sunday?(month, day)
    Time.new(year, month, day).sunday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def weekend?(month, day)
    date = Time.new(year, month, day)
    date.saturday? || date.sunday?
  end

  # @rbs return: bool
  def leap_year?
    (year.to_i % 400).zero? || (!!(year.to_i % 100).nonzero? && (year.to_i % 4).zero?)
  end

  # @rbs date: String
  # @rbs return: String
  def body(date)
    format(BODY_TEMPLATE, date)
  end

  # @rbs directory: String
  # @rbs index: String
  # @rbs day: String
  # @rbs month: String
  # @rbs array: Array[untyped]
  # @rbs return: void
  def export_template(directory: '', index: '', day: '', month: '', array: [])
    date     =  array
    date     << "#{day} " unless day.empty?
    date     << "#{month} #{year}"
    filename = File.join(directory, "#{year}#{index}#{day}_#{full_unit}_working_report.md")
    FileUtils.mkdir_p(directory)
    File.write(filename, body(date.join)) unless File.exist?(filename)
  end

  # @rbs month: String
  # @rbs return: void
  def create_templates(month, &)
    1.upto(31).each do |d|
      next if skip_day_of_month?(month, d)

      yield(d)
    end
  end

  # @rbs month: String
  # @rbs day: Integer
  # @rbs return: bool
  def skip_day_of_month?(month, day)
    case month
    when 'February'           then day > (leap_year? ? 29 : 28)
    when *MONTHS_WITH_30_DAYS then day > 30
    else false
    end
  end
end
