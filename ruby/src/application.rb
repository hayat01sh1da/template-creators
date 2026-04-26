# rbs_inline: enabled

require 'date'

class Application
  class ValueError < StandardError; end
  class DigitLengthError < StandardError; end

  USERNAMES = ['hayat01sh1da'].freeze

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
    Date::MONTHNAMES.compact.each.with_index(1) { |month, i|
      index     = sprintf('%02d', i)
      directory = File.join('..', '..', 'working-report', username, year, "#{index}_#{month}")
      case unit
      when 'd', 'w'
        create_templates(month) { |d|
          day = sprintf('%02d', d)
          if unit == 'd'
            next if is_weekend?(i, d)
            export_template(directory:, index:, day:, month:)
          else
            next unless is_monday?(i, d)
            export_template(directory:, index:, day:, month:)
          end
        }
      when 'm'
        export_template(directory:, index:, month:)
      end
    }
  end

  private

  attr_reader :username, :unit, :year

  # @rbs return: String
  def full_unit
    case unit
    when 'd'
      'daily'
    when 'w'
      'weekly'
    when 'm'
      'monthly'
    else
      ''
    end
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def is_monday?(month, day)
    Time.new(year, month, day).monday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def is_saturday?(month, day)
    Time.new(year, month, day).saturday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def is_sunday?(month, day)
    Time.new(year, month, day).sunday?
  end

  # @rbs month: Integer
  # @rbs day: Integer
  # @rbs return: bool
  def is_weekend?(month, day)
    date = Time.new(year, month, day)
    date.saturday? || date.sunday?
  end

  # @rbs return: bool
  def is_leap_year?
    (year.to_i % 400).zero? || (!!(year.to_i % 100).nonzero? && (year.to_i % 4).zero?)
  end

  # @rbs array: Array[untyped]
  # @rbs date: String
  # @rbs return: String
  def body(date, array = [])
    text  = array
    text << "# TITLE on #{date}\n\n"
    text << "## 1. CATEGORY\n\n"
    text << "### 1-1. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "### 1-2. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "### 1-3. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "## 2. CATEGORY\n\n"
    text << "### 2-1. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "### 2-2. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "### 2-3. SUBCATEGORY\n\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text << "- ITEM\n"
    text.join
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
    FileUtils.mkdir_p(directory) unless Dir.exist?(directory)
    IO.write(filename, body(date.join)) unless File.exist?(filename)
  end

  # @rbs month: String
  # @rbs return: void
  def create_templates(month, &)
    1.upto(31).each { |d|
      case month
      when 'February'
        next if is_leap_year? && d > 29
        next if d > 28
        yield(d)
      when 'April', 'June', 'September', 'November'
        next if d > 30
        yield(d)
      else
        yield(d)
      end
    }
  end
end
