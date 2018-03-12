class Micropost < ApplicationRecord
  has_many :combinations, dependent: :destroy
  has_many :tags, through: :combinations
  belongs_to :user
  default_scope -> { order(created_at: :desc) }
  validates :user_id, presence: true
  validates :content, presence: true, length: { maximum: 140 }

  def combine_tag(tag)
    unless tags.include?(tag)
      tags << tag
    end
  end

  # Post the post content to the web service
  def analyze
    data = { micropost_id: id,
             content: content}
    send_to_ml_service(data)
  end

  private

  def send_to_ml_service(data = {})
    if Rails.env.production?
      url = ENV['ML_WEBSERVICE_URL']
    else
      url = ""
    end

    return if url.blank?
    uri = URI.parse(url)
    return unless uri.is_a?(URI::HTTP) || uri.is_a?(URI::HTTPS)

    header = {'Content-Type': 'application/json'}
    body = data
    http = Net::HTTP.new(uri.host, uri.port)
    request = Net::HTTP::Post.new(uri.request_uri, header)
    request.body = body.to_json
    http.request(request)
  end
end
