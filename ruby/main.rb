require_relative './src/application'

username, unit, year, *_ = ARGV

if username && unit && year
  ::TemplateCreator::Application.run(username:, unit:, year:)
elsif username
  ::TemplateCreator::Application.run(username:)
elsif unit
  ::TemplateCreator::Application.run(unit:)
elsif year
  ::TemplateCreator::Application.run(year:)
else
  ::TemplateCreator::Application.run
end
