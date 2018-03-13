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
      url = "https://pmishra.pythonanywhere.com/"
    end

    return if url.blank?
    uri = URI.parse(url)
    return unless uri.is_a?(URI::HTTP) || uri.is_a?(URI::HTTPS)

    header = {'Content-Type': 'application/json'}
    body = data
    https = Net::HTTP.new(uri.host, uri.port, use_ssl: true)
    request = Net::HTTP::Post.new(uri.request_uri, header)
    request.body = body.to_json
    response = https.request(request)
    return unless response.code == '200'
    set_tags(JSON.parse(response.body))
  end

    def set_tags(result)
      names = result['response'].scan(/[a-z]+/)
      if names.any?
        names.each do |name|
          name.downcase!
          tag = Tag.new(name: name)
          tag = Tag.find_by(name: name) unless tag.save
          self.combine_tag(tag) if tag
        end
      end
    end
end

