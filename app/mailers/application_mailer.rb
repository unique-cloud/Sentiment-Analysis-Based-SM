class ApplicationMailer < ActionMailer::Base
  default from: (Rails.env.production?? ENV['EMAIL_FROM_ADDRESS'] : "example@example.com")
  layout 'mailer'
end
