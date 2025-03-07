require 'date'
require 'fileutils'

class Application
  class ValueError < StandardError; end
  class DigitLengthError < StandardError; end

  USERNAMES = ['hayat01sh1da'].freeze

  def self.run(username: 'hayat01sh1da', unit: 'd', year: Time.now.year.to_s)
    instance = new(username, unit, year)
    instance.validate_username!(username)
    instance.validate_unit!(unit)
    instance.validate_year!(year)
    instance.run
  end

  def initialize(username, unit, year)
    @username = username
    @unit     = unit
    @year     = year
  end

  def validate_username!(username)
    raise ValueError, "#{username} is NOT a permitted username." unless USERNAMES.include?(username)
  end

  def validate_unit!(unit)
    case unit
    when 'd', 'w', 'm'
      unit
    else
      raise ValueError, 'Provide d, w or m as a valid unit.'
    end
  end

  def validate_year!(year)
    Integer(year)
    if year.length > 4
      raise DigitLengthError, 'Year must be 4 digits.'
    elsif year.to_i < Time.now.year
      raise ValueError, 'Provide newer than or equal to the current year.'
    else
      year
    end
  end

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
            export_template(directory, index, day, month)
          else
            next unless is_monday?(i, d)
            export_template(directory, index, day, month)
          end
        }
      when 'm'
        export_template(directory, index, month)
      end
    }
  end

  private

  attr_reader :username, :unit, :year

  def full_unit
    case unit
    when 'd'
      'daily'
    when 'w'
      'weekly'
    when 'm'
      'monthly'
    end
  end

  def is_monday?(month, day)
    Time.new(year, month, day).monday?
  end

  def is_saturday?(month, day)
    Time.new(year, month, day).saturday?
  end

  def is_sunday?(month, day)
    Time.new(year, month, day).sunday?
  end

  def is_weekend?(month, day)
    date = Time.new(year, month, day)
    date.saturday? || date.sunday?
  end

  def is_leap_year?
    (year.to_i % 400).zero? || (!!(year.to_i % 100).nonzero? && (year.to_i % 4).zero?)
  end

  def body(date)
    text  = []
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

  def export_template(directory, index, day = '', month)
    date     =  []
    date     << "#{day} " unless day.empty?
    date     << "#{month} #{year}"
    filename = File.join(directory, "#{year}#{index}#{day}_#{full_unit}_working_report.md")
    FileUtils.mkdir_p(directory) unless Dir.exist?(directory)
    IO.write(filename, body(date.join)) unless File.exist?(filename)
  end

  def create_templates(month)
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
